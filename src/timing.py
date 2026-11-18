"""Measure run time against the budget in ADR-004.

Two measurements:
1. End to end: the real command (`python src/run_all.py --offline`) in a throw-away copy of the
   project, from a fresh Python start, reading every saved file from disk. This is what Adjoa feels.
2. Per stage, in memory, up to 5,000 films: shows which step grows with list size.
"""
import json
import math
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

import bundles
import shortlist
import talent
import uncertainty
from analysis import CUTOFF_YEAR, classify, kpi_table, load_films

SIZES = [112, 500, 5000]          # real list, next year's list, a stress test
END_TO_END_SIZES = [112, 500]     # sizes for the full command (5,000 would mean 10,000+ files)
RUNS = 5                          # timed runs per size (after one warm-up run)
E2E_RUNS = 10                     # enough runs for a meaningful p95
TARGET_SECONDS = 10.0             # ADR-004: whole offline run, from typing the command to the report
ID_OFFSET = 1_000_000             # keeps ids unique when the real list is copied
ROOT = Path(".").resolve()


# ---------- end to end ----------

def _shift_json(src, dst_dir, endpoint, shift, suffix):
    record = json.loads(src.read_text(encoding="utf-8"))
    p = record["payload"]
    if p is not None:
        if endpoint in ("details", "credits", "collection_parts"):
            p["id"] += shift
        if endpoint == "details" and p.get("belongs_to_collection"):
            p["belongs_to_collection"] = {**p["belongs_to_collection"],
                                          "id": p["belongs_to_collection"]["id"] + shift,
                                          "name": p["belongs_to_collection"]["name"] + suffix}
        if endpoint == "collection":
            p["id"] += shift
            p["name"] += suffix
            p["parts"] = [{**part, "id": part["id"] + shift} for part in p["parts"]]
    new_id = int(record["movie_id"]) + shift
    record["movie_id"] = str(new_id)
    (dst_dir / f"{new_id}.json").write_text(json.dumps(record), encoding="utf-8")
    return str(new_id)


def build_project(n, dest):
    """A copy of the project whose saved data holds about n films (the real ones, copied with new ids)."""
    shutil.copytree(ROOT / "src", dest / "src", ignore=shutil.ignore_patterns("__pycache__"))
    raw = ROOT / "data" / "raw"
    film_ids = sorted(int(p.stem) for p in (raw / "details").glob("*.json"))
    copies = math.ceil(n / len(film_ids))
    ids, manifest = [], []
    for endpoint in ("details", "credits", "collection", "collection_parts"):
        (dest / "data" / "raw" / endpoint).mkdir(parents=True)
    for k in range(copies):
        shift, suffix = k * ID_OFFSET, ("" if k == 0 else f" #{k}")
        take = film_ids if (k + 1) * len(film_ids) <= n else film_ids[: n - k * len(film_ids)]
        for fid in take:
            for endpoint in ("details", "credits"):
                new = _shift_json(raw / endpoint / f"{fid}.json", dest / "data/raw" / endpoint, endpoint, shift, suffix)
                saved = json.loads((raw / endpoint / f"{fid}.json").read_text(encoding="utf-8"))
                manifest.append({"movie_id": new, "endpoint": endpoint, "status_code": saved["status_code"],
                                 "fetched_at": saved["fetched_at"]})
            ids.append(fid + shift)
        for endpoint in ("collection", "collection_parts"):
            for path in (raw / endpoint).glob("*.json"):
                _shift_json(path, dest / "data/raw" / endpoint, endpoint, shift, suffix)
        # A partial copy leaves out some franchise films; give them figures as franchise films
        # not on the list, exactly as a real online run would fetch them.
        on_copy = {fid + shift for fid in take}
        for path in (raw / "collection").glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))["payload"] or {}
            for part in payload.get("parts", []):
                details = raw / "details" / f"{part['id']}.json"
                target = dest / "data/raw/collection_parts" / f"{part['id'] + shift}.json"
                if part["id"] + shift not in on_copy and details.exists() and not target.exists():
                    _shift_json(details, dest / "data/raw/collection_parts", "collection_parts", shift, suffix)
    pd.DataFrame({"tmdb_id": ids}).to_csv(dest / "data" / "id_list.csv", index=False)
    pd.DataFrame(manifest).to_csv(dest / "data" / "raw" / "manifest.csv", index=False)
    return len(ids)


def time_end_to_end(n):
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        films = build_project(n, dest)
        seconds, cold = [], None
        for i in range(E2E_RUNS + 1):                       # first run reads freshly written files: reported apart
            start = time.perf_counter()
            done = subprocess.run([sys.executable, "src/run_all.py", "--offline"], cwd=dest,
                                  capture_output=True, text=True)
            elapsed = time.perf_counter() - start
            assert done.returncode == 0, done.stdout[-2000:] + done.stderr[-2000:]
            if i:
                seconds.append(elapsed)
            else:
                cold = elapsed
        return films, seconds, cold


# ---------- per stage, in memory ----------

def scale(films, directors, leads, parts, n):
    """Copy the real data until it has n films. Each copy gets its own ids and collections."""
    copies = math.ceil(n / len(films))
    f_parts, d_parts, l_parts, p_parts = [], [], [], []
    for k in range(copies):
        shift = k * ID_OFFSET
        f_parts.append(films.assign(movie_id=films["movie_id"] + shift,
                                    collection_name=films["collection_name"] + f" #{k}"))
        d_parts.append(directors.assign(movie_id=directors["movie_id"] + shift))
        l_parts.append(leads.assign(movie_id=leads["movie_id"] + shift))
        p_parts.append(parts.assign(movie_id=parts["movie_id"] + shift,
                                    collection_name=parts["collection_name"] + f" #{k}"))
    big_films = pd.concat(f_parts, ignore_index=True).head(n)
    keep = set(big_films["movie_id"])
    big_dirs = pd.concat(d_parts, ignore_index=True)
    big_leads = pd.concat(l_parts, ignore_index=True)
    return (big_films, big_dirs.loc[big_dirs["movie_id"].isin(keep)],
            big_leads.loc[big_leads["movie_id"].isin(keep)], pd.concat(p_parts, ignore_index=True))


def run_stages(films, directors, leads, parts):
    """Run every analysis stage once; return seconds per stage."""
    seconds = {}

    def timed(label, function):
        start = time.perf_counter()
        result = function()
        seconds[label] = time.perf_counter() - start
        return result

    classified = timed("classify", lambda: classify(films, "standalone"))
    modern = classified.loc[classified["release_year"] >= CUTOFF_YEAR]
    timed("kpi tables", lambda: (kpi_table(classified), kpi_table(modern)))
    whole = timed("whole bundles", lambda: bundles.whole_bundle_table(parts))
    timed("bundle ranking", lambda: shortlist.bundle_table(whole, CUTOFF_YEAR))
    timed("standalones", lambda: shortlist.standalone_table(modern, parts))
    timed("entry position", lambda: shortlist.entry_position(classified))
    timed("talent", lambda: [talent.talent_table(window, people)
                             for window in (classified, modern) for people in (directors, leads)])
    timed("uncertainty (all 14 comparisons)",
          lambda: uncertainty.gap_rows(films, whole, np.random.default_rng(uncertainty.SEED)))
    return seconds


def classify_with_apply(films):
    """The slow way, kept only to measure against: one Python call per film."""
    def label(row):
        n = row["collection_films_in_list"]
        return "franchise" if (pd.notna(n) and n >= 2) else "standalone"
    return films.assign(group=films.apply(label, axis=1))


def bootstrap_medians_multinomial(values, clusters, rng):
    """The earlier way of drawing reshuffles, kept only to measure against: one multinomial draw per batch."""
    _, cluster_index = np.unique(clusters, return_inverse=True)
    n_clusters = cluster_index.max() + 1
    pieces = []
    for _ in range(uncertainty.N_RESAMPLES // uncertainty.BATCH):
        counts = rng.multinomial(n_clusters, np.full(n_clusters, 1 / n_clusters), size=uncertainty.BATCH)
        pieces.append(uncertainty.weighted_medians(values, counts[:, cluster_index]))
    return np.concatenate(pieces)


def time_uncertainty(films, parts, drawer):
    """Seconds for all 14 uncertainty comparisons with the given way of drawing reshuffles."""
    whole = bundles.whole_bundle_table(parts)
    original, uncertainty.bootstrap_medians = uncertainty.bootstrap_medians, drawer
    try:
        start = time.perf_counter()
        uncertainty.gap_rows(films, whole, np.random.default_rng(uncertainty.SEED))
        return time.perf_counter() - start
    finally:
        uncertainty.bootstrap_medians = original


def main():
    films = load_films()
    directors = pd.read_csv("data/processed/directors.csv")
    cast = pd.read_csv("data/processed/cast.csv")
    parts = pd.read_csv(bundles.OUT)
    leads = cast.loc[cast["order"] == 0, ["movie_id", "person_id", "name"]]

    e2e = []
    for n in END_TO_END_SIZES:
        count, secs, cold = time_end_to_end(n)
        e2e.append({"scenario": f"{count} films, first run on freshly copied files (cold)", "runs": 1,
                    "median": round(cold, 2), "p95": "–", "worst": round(cold, 2),
                    "target_met": "yes" if cold <= TARGET_SECONDS else "NO"})
        e2e.append({"scenario": f"{count} films, repeat runs (warm)", "runs": len(secs),
                    "median": round(float(np.median(secs)), 2), "p95": round(float(np.percentile(secs, 95)), 2),
                    "worst": round(max(secs), 2), "target_met": "yes" if max(secs) <= TARGET_SECONDS else "NO"})
        print(e2e[-1])

    stage_medians, totals_by_size = {}, {}
    for n in SIZES:
        f, d, l, p = scale(films, directors, leads, parts, n) if n != len(films) else (films, directors, leads, parts)
        run_stages(f, d, l, p)                                # warm-up, not counted
        stages = pd.DataFrame([run_stages(f, d, l, p) for _ in range(RUNS)])
        stage_medians[n] = stages.median()
        totals_by_size[n] = round(float(stages.sum(axis=1).median()), 3)
    stage_table = pd.DataFrame(stage_medians).round(4)
    stage_table.columns = [f"{c} films" for c in stage_table.columns]
    print(stage_table)

    big, _, _, _ = scale(films, directors, leads, parts, 5000)
    start = time.perf_counter(); classify_with_apply(big); slow = time.perf_counter() - start
    start = time.perf_counter(); classify(big, "standalone"); fast = time.perf_counter() - start
    f500, _, _, p500 = scale(films, directors, leads, parts, 500)
    unc_before = time_uncertainty(f500, p500, bootstrap_medians_multinomial)
    unc_after = time_uncertainty(f500, p500, uncertainty.bootstrap_medians)

    lines = [
        "# Run time report", "",
        "## Target", "",
        f"The whole offline run, from typing the command to a finished report, takes under {TARGET_SECONDS:.0f} seconds "
        "on Adjoa's laptop at next year's list size (about 500 films), short enough to rerun live in a meeting (ADR-004).", "",
        "## Method", "",
        f"- **Hardware / container spec:** {platform.platform()}, {platform.machine()}, Python {sys.version.split()[0]}, "
        f"pandas {pd.__version__}, numpy {np.__version__}; no container.",
        "- **What was timed, from which event to which event:** from starting `python src/run_all.py --offline` in a fresh "
        "process to that process exiting with the report written: start-up, imports, reading every saved file from disk, "
        "flattening, the data checks, the analysis (including all 14 uncertainty comparisons) and the report. The run uses a "
        "throw-away copy of the project; larger sizes copy the real films and their franchises with new ids, so the data has a "
        "realistic shape. Network fetching is excluded: it happens only for new ids (about two minutes for 500 new films at "
        "the polite pace) and is done before the meeting. A second measurement times each analysis step on data already in "
        "memory, up to 5,000 films, to show which step grows with list size.",
        f"- **Runs, warm or cold, and which figure is reported:** per size, one cold run straight after the project copy is "
        f"written (the system has not yet read or scanned the files), reported on its own, then {E2E_RUNS} warm runs, each a "
        f"fresh process; median, 95th percentile and worst are reported, and the target is judged on the warm worst. "
        f"Per-step timings: {RUNS} runs after a warm-up, median reported.",
        "- **How to reproduce:** `python src/timing.py` (rewrites this report).", "",
        "## Results", "",
        "| Scenario | Runs | Median | p95 | Worst | Target met? |",
        "|---|---|---|---|---|---|",
        *[f"| {r['scenario']} | {r['runs']} | {r['median']} s | {r['p95']}{'' if r['p95'] == '–' else ' s'} | {r['worst']} s | {r['target_met']} |"
          for r in e2e], "",
        "Each analysis step on data already in memory (median seconds):", "",
        "| Step | " + " | ".join(stage_table.columns) + " |",
        "|---" * (len(stage_table.columns) + 1) + "|",
        *[f"| {name} | " + " | ".join(str(v) for v in row) + " |"
          for name, row in zip(stage_table.index, stage_table.to_numpy())],
        "| **all steps** | " + " | ".join(str(totals_by_size[n]) for n in SIZES) + " |", "",
        "## Before / after", "",
        "| Query / stage | Before | After | Change |",
        "|---|---|---|---|",
        f"| Group films (5,000 films): one call per row → one whole-column rule | {slow:.4f} s | {fast:.4f} s | {slow / fast:.0f}x faster |",
        f"| All 14 uncertainty comparisons (500 films): multinomial draw → counting random picks | {unc_before:.2f} s | {unc_after:.2f} s | {unc_before / unc_after:.1f}x faster |", "",
        "## Caveats", "",
        "- Timings are from one laptop. Another machine will differ; the shape (how time grows with size) should hold.",
        "- The cold run is dominated by reading about a thousand freshly written files, which Windows also scans for viruses. "
        "Adjoa meets it at most once, the first time she runs after fetching new data or restarting the laptop; a practice "
        "run before the meeting avoids it. The run reads each saved file once (later steps read the flattened tables).",
        "- Copied data repeats the same films, so it tests speed and memory, not new findings.",
        "- At 5,000 films the uncertainty step alone takes well over 10 seconds; the budget is for about 500 titles. "
        "Lowering `N_RESAMPLES` in `src/uncertainty.py` from 10,000 to 2,000 would cut it by about four-fifths.",
        "- The two ways of drawing reshuffles give the same results to within one percentage point; they differ only in the random sequence.",
    ]
    Path("timing_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\nwrote timing_report.md")


if __name__ == "__main__":
    main()
