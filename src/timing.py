import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

import shortlist
import talent
import uncertainty
from analysis import classify, kpi_table, load_films

SIZES = [112, 500, 5000]          # real list, next year's list, a stress test
RUNS = 5                          # timed runs per size (after one warm-up run)
TARGET_SECONDS = 5.0              # decision ADR-006: fine for Adjoa to run live in a meeting
ID_OFFSET = 1_000_000             # keeps ids unique when the real list is copied


def scale(films, directors, leads, n):
    """Copy the real data until it has n films. Each copy gets its own ids and collections."""
    copies = math.ceil(n / len(films))
    film_parts, dir_parts, lead_parts = [], [], []
    for k in range(copies):
        shift = k * ID_OFFSET
        film_parts.append(films.assign(movie_id=films["movie_id"] + shift,
                                       collection_name=films["collection_name"] + f" #{k}"))
        dir_parts.append(directors.assign(movie_id=directors["movie_id"] + shift))
        lead_parts.append(leads.assign(movie_id=leads["movie_id"] + shift))
    big_films = pd.concat(film_parts, ignore_index=True).head(n)
    keep = set(big_films["movie_id"])
    big_dirs = pd.concat(dir_parts, ignore_index=True)
    big_leads = pd.concat(lead_parts, ignore_index=True)
    return (big_films,
            big_dirs.loc[big_dirs["movie_id"].isin(keep)],
            big_leads.loc[big_leads["movie_id"].isin(keep)])


def run_stages(films, directors, leads):
    """Run every analysis stage once; return seconds per stage."""
    seconds = {}

    def timed(label, function):
        start = time.perf_counter()
        result = function()
        seconds[label] = time.perf_counter() - start
        return result

    classified = timed("classify", lambda: classify(films, "standalone"))
    modern = classified.loc[classified["release_year"] >= 2000]
    timed("kpi tables", lambda: (kpi_table(classified), kpi_table(modern)))
    timed("bundles", lambda: shortlist.bundle_table(modern))
    timed("standalones", lambda: shortlist.standalone_table(modern))
    timed("entry position", lambda: shortlist.entry_position(classified))
    timed("talent", lambda: [talent.talent_table(window, people)
                             for window in (classified, modern) for people in (directors, leads)])
    rng = np.random.default_rng(uncertainty.SEED)
    timed("bootstrap", lambda: [
        uncertainty.bootstrap_gap(w.loc[w["group"] == "franchise", "return_multiple"],
                                  w.loc[w["group"] == "standalone", "return_multiple"], rng)
        for w in (classified, modern)])
    return seconds


def classify_with_apply(films):
    """The slow way, kept only to measure against: one Python call per film."""
    def label(row):
        n = row["collection_films_in_list"]
        return "franchise" if (pd.notna(n) and n >= 2) else "standalone"
    return films.assign(group=films.apply(label, axis=1))


def main():
    films = load_films()
    directors = pd.read_csv("data/processed/directors.csv")
    cast = pd.read_csv("data/processed/cast.csv")
    leads = cast.loc[cast["order"] == 0, ["movie_id", "person_id", "name"]]

    results, stage_medians = [], {}
    for n in SIZES:
        f, d, l = scale(films, directors, leads, n) if n != len(films) else (films, directors, leads)
        run_stages(f, d, l)                                   # warm-up, not counted
        runs = [run_stages(f, d, l) for _ in range(RUNS)]
        stages = pd.DataFrame(runs)
        totals = stages.sum(axis=1)
        stage_medians[n] = stages.median()
        results.append({"scenario": f"{n} films", "runs": RUNS,
                        "median": round(totals.median(), 3),
                        "p95": round(float(np.percentile(totals, 95)), 3),
                        "worst": round(totals.max(), 3),
                        "target_met": "yes" if totals.max() <= TARGET_SECONDS else "NO"})
    results = pd.DataFrame(results)
    stage_table = pd.DataFrame(stage_medians).round(4)
    stage_table.columns = [f"{c} films" for c in stage_table.columns]
    print(results.to_string(index=False))
    print("\nmedian seconds per stage:")
    print(stage_table)

    # before / after: the row-by-row way against the whole-column way, at 5,000 films
    big, _, _ = scale(films, directors, leads, 5000)
    start = time.perf_counter(); classify_with_apply(big); slow = time.perf_counter() - start
    start = time.perf_counter(); classify(big, "standalone"); fast = time.perf_counter() - start
    print(f"\nclassify at 5000 films: row-by-row {slow:.4f}s | whole-column {fast:.4f}s | {slow / fast:.0f}x faster")

    lines = [
        "# Run time report", "",
        "## Target", "",
        f"The whole analysis, from cached data to finished tables, runs in under {TARGET_SECONDS:.0f} seconds "
        "on Adjoa's laptop at next year's list size (about 500 films), with room to spare at 10 times that.", "",
        "## Method", "",
        f"- Hardware: {platform.platform()}, {platform.machine()}, Python {sys.version.split()[0]}, pandas {pd.__version__}",
        "- What was timed: every analysis stage (classify, KPI tables, bundles, standalones, entry position, talent, bootstrap), "
        "from data already loaded in memory to finished tables. Network fetching and reading cached files from disk are excluded; "
        "fetching is the slow part and happens only for new ids.",
        f"- Runs: {RUNS} warm runs per size after one discarded warm-up. Reported: median, 95th percentile, worst.",
        "- Larger sizes are made by copying the real films with new ids and collections, so the shape of the data is realistic.",
        "- Reproduce: `python src/timing.py`", "",
        "## Results", "",
        "| Scenario | Runs | Median (s) | p95 (s) | Worst (s) | Target met? |",
        "|---|---|---|---|---|---|",
    ]
    lines += [f"| {r.scenario} | {r.runs} | {r.median} | {r.p95} | {r.worst} | {r.target_met} |"
              for r in results.itertuples()]
    header = "| Stage | " + " | ".join(stage_table.columns) + " |"
    divider = "|---" * (len(stage_table.columns) + 1) + "|"
    stage_rows = [f"| {name} | " + " | ".join(str(v) for v in row) + " |"
                  for name, row in zip(stage_table.index, stage_table.to_numpy())]
    lines += ["", "Median seconds per stage:", "", header, divider, *stage_rows, "",
              "## Before / after", "",
              "| Stage | Before (row by row) | After (whole column) | Change |",
              "|---|---|---|---|",
              f"| classify, 5000 films | {slow:.4f}s | {fast:.4f}s | {slow / fast:.0f}x faster |", "",
              "## Caveats", "",
              "- Timings are from one laptop. Another machine will differ; the shape (how time grows with size) should hold.",
              "- Copied data repeats the same films, so it tests speed and memory, not new findings.",
              "- The bootstrap is drawn in batches so memory stays small; one big array would need about 280 MB at 3,500 films."]
    Path("timing_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\nwrote timing_report.md")


if __name__ == "__main__":
    main()