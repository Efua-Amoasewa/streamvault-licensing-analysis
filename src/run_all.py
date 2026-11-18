import argparse
import contextlib
import io
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

import analysis
import bundles
import ceilings
import fetch
import flatten
import load_ids
import shortlist
import talent
import uncertainty
from analysis import CUTOFF_YEAR
from quality_gate import enforce, run_checks

OUT_DIR = Path("outputs")


def quiet(function):
    """Run a stage without printing its details; the report carries the results."""
    with contextlib.redirect_stdout(io.StringIO()):
        function()


def markdown_table(table):
    table = table.reset_index()
    header = "| " + " | ".join(str(c) for c in table.columns) + " |"
    divider = "|" + "---|" * len(table.columns)
    rows = ["| " + " | ".join(str(v) for v in row) + " |" for row in table.to_numpy()]
    return "\n".join([header, divider, *rows])


def reconciliation(ids, manifest, films):
    counts = ids["status"].value_counts()
    invalid = int(counts.get("blank", 0) + counts.get("imdb_id", 0) + counts.get("invalid_other", 0))
    repeats = int(counts.get("duplicate", 0))
    usable = int(counts.get("usable", 0))
    via_other = int(ids["note"].str.startswith("other-database id").sum())
    not_found = int(((manifest["endpoint"] == "details") & (manifest["status_code"] == 404)).sum())
    money_missing = int(((films["budget"] <= 0) | (films["revenue"] <= 0)).sum())
    rows = [
        ("ids in the file", len(ids), "", "every line, including blanks"),
        ("valid-looking ids", len(ids) - invalid, -invalid,
         f"blank lines, text placeholders, negatives, unmatched other-database ids ({via_other} other-database id(s) looked up and kept)"),
        ("unique ids to request", usable, -repeats, "same film listed more than once (including via another database's id)"),
        ("films found in the database", len(films), -not_found, "ids the database does not know"),
        ("films with usable return figures", len(films) - money_missing, -money_missing, "zero or missing budget or revenue"),
    ]
    return pd.DataFrame(rows, columns=["Stage", "Rows", "Delta", "Reason"]).set_index("Stage")


def changes_since_last_run(films):
    path = OUT_DIR / "film_ids_last_run.csv"
    current = set(films["movie_id"])
    note = "First run: nothing to compare with."
    if path.exists():
        previous = set(pd.read_csv(path)["movie_id"])
        new, gone = sorted(current - previous), sorted(previous - current)
        note = f"{len(new)} new films, {len(gone)} films no longer on the list. New ids: {new[:20]}; gone: {gone[:20]}"
    films[["movie_id"]].to_csv(path, index=False)
    return note


def fetch_bundles():
    load_dotenv(".env")
    fetch.fetch_whole_bundles(fetch.make_session(), os.environ["TMDB_API_KEY"])


def main():
    parser = argparse.ArgumentParser(description="Run the whole StreamVault analysis, top to bottom.")
    parser.add_argument("--offline", action="store_true",
                        help="use the saved snapshot only: no API key and no internet needed")
    args = parser.parse_args()
    OUT_DIR.mkdir(exist_ok=True)
    wall_start = time.perf_counter()

    stages = [("classify ids", load_ids.main)]
    if not args.offline:
        stages.append(("fetch new films", fetch.main))
    stages.append(("flatten", flatten.main))
    if not args.offline:
        stages.append(("fetch whole bundles", fetch_bundles))
    stages.append(("whole bundles", bundles.main))
    timings = {}

    def run(label, function):
        start = time.perf_counter()
        quiet(function)
        timings[label] = round(time.perf_counter() - start, 2)
        print(f"  done: {label} ({timings[label]}s)")

    print("Running the analysis...")
    for label, function in stages:
        run(label, function)

    films = analysis.load_films()
    directors = pd.read_csv("data/processed/directors.csv")
    cast = pd.read_csv("data/processed/cast.csv")
    parts = pd.read_csv(bundles.OUT)
    manifest = pd.read_csv(Path("data/raw/manifest.csv"), dtype={"movie_id": str})
    ids = pd.read_csv("data/ids_classified.csv", dtype=str, keep_default_na=False)

    checks = run_checks(films, directors, cast, manifest, parts)
    print("\nData quality gate:")
    print(checks.to_string(index=False))
    enforce(checks)

    for label, function in [("shortlists", shortlist.main), ("talent", talent.main),
                            ("uncertainty", uncertainty.main), ("price ceilings", ceilings.main)]:
        run(label, function)

    classified = analysis.classify(films, "standalone")
    modern = classified.loc[classified["release_year"] >= CUTOFF_YEAR]
    gap = pd.read_csv(OUT_DIR / "uncertainty.csv")
    gap = gap.loc[(gap["singles_as"] == "standalone") & (gap["resampling"] != "each film independent"),
                  ["window", "unit", "franchise_units", "standalone_films", "franchise_median",
                   "standalone_median", "gap_low_95", "gap_high_95", "share_franchise_ahead"]]
    whole = bundles.whole_bundle_table(parts.assign(release_year=parts["release_year"].astype("Int64")))
    incomplete = whole.loc[~whole["complete"], ["films_on_list", "films_released", "whole_bundle_return", "not_on_list"]]
    top_bundles = shortlist.bundle_table(whole, CUTOFF_YEAR).head(3)
    top_standalones = shortlist.standalone_table(modern, parts).head(5)
    price, unit = ceilings.ceiling_table()
    fetched = pd.to_datetime(films["fetched_at"], format="ISO8601")

    report = "\n".join([
        "# Run report", "",
        f"Run at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Data as of: {fetched.min().date()} to {fetched.max().date()} (when each film was fetched)",
        f"Mode: {'offline, saved snapshot' if args.offline else 'online, new ids fetched'}", "",
        "## Where every id went", "", markdown_table(reconciliation(ids, manifest, films)), "",
        "## Data quality gate", "", markdown_table(checks.set_index("check")), "",
        "## Franchise vs standalone: median return per film (return = revenue / budget)", "",
        "All years:", "", markdown_table(analysis.kpi_table(classified)), "",
        f"{CUTOFF_YEAR} onward:", "", markdown_table(analysis.kpi_table(modern)), "",
        "## How sure are we (10,000 resamples; 'ahead' = share of resamples where franchise median is higher)", "",
        "Per film, resampling whole bundles so a series' films move together; and per whole bundle (the unit actually bought).", "",
        markdown_table(gap.set_index("window")), "",
        "## Bundles on the list that are not complete (valued whole, including the films not on the list)", "",
        markdown_table(incomplete), "",
        f"## Shortlist (every film from {CUTOFF_YEAR} onward)", "",
        "Franchise bundles: " + "; ".join(top_bundles.index), "",
        "Standalone films: " + "; ".join(top_standalones["title"]), "",
        f"## Walk-away ceilings relative to the shortlist (1 unit = a typical standalone, {unit}x)", "",
        markdown_table(price.set_index("title")), "",
        "## Changes since the last run", "", changes_since_last_run(films), "",
        "## Time taken (seconds)", "",
        markdown_table(pd.Series({**timings, "whole run (wall clock)": round(time.perf_counter() - wall_start, 2)},
                                 name="seconds").rename_axis("step").to_frame()), "",
    ])
    (OUT_DIR / "run_report.md").write_text(report, encoding="utf-8")
    print("\nWrote outputs/run_report.md")


if __name__ == "__main__":
    main()
