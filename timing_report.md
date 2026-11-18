# Run time report

## Target

The whole offline run, from typing the command to a finished report, takes under 10 seconds on Adjoa's laptop at next year's list size (about 500 films), short enough to rerun live in a meeting (ADR-004).

## Method

- **Hardware / container spec:** Windows-11-10.0.26300-SP0, AMD64, Python 3.15.2, pandas 3.1.1, numpy 2.5.5; no container.
- **What was timed, from which event to which event:** from starting `python src/run_all.py --offline` in a fresh process to that process exiting with the report written: start-up, imports, reading every saved file from disk, flattening, the data checks, the analysis (including all 14 uncertainty comparisons) and the report. The run uses a throw-away copy of the project; larger sizes copy the real films and their franchises with new ids, so the data has a realistic shape. Network fetching is excluded: it happens only for new ids (about two minutes for 500 new films at the polite pace) and is done before the meeting. A second measurement times each analysis step on data already in memory, up to 5,000 films, to show which step grows with list size.
- **Runs, warm or cold, and which figure is reported:** per size, one cold run straight after the project copy is written (the system has not yet read or scanned the files), reported on its own, then 10 warm runs, each a fresh process; median, 95th percentile and worst are reported, and the target is judged on the warm worst. Per-step timings: 5 runs after a warm-up, median reported.
- **How to reproduce:** `python src/timing.py` (rewrites this report).

## Results

| Scenario | Runs | Median | p95 | Worst | Target met? |
|---|---|---|---|---|---|
| 112 films, first run on freshly copied files (cold) | 1 | 7.77 s | – | 7.77 s | yes |
| 112 films, repeat runs (warm) | 10 | 2.93 s | 3.04 s | 3.08 s | yes |
| 500 films, first run on freshly copied files (cold) | 1 | 27.3 s | – | 27.3 s | NO |
| 500 films, repeat runs (warm) | 10 | 5.77 s | 7.8 s | 8.14 s | yes |

Each analysis step on data already in memory (median seconds):

| Step | 112 films | 500 films | 5000 films |
|---|---|---|---|
| classify | 0.0008 | 0.0008 | 0.0015 |
| kpi tables | 0.0111 | 0.0103 | 0.0122 |
| whole bundles | 0.0166 | 0.0318 | 0.2197 |
| bundle ranking | 0.0022 | 0.002 | 0.0021 |
| standalones | 0.0049 | 0.0038 | 0.0042 |
| entry position | 0.0093 | 0.0091 | 0.0167 |
| talent | 0.0432 | 0.0396 | 0.0537 |
| uncertainty (all 14 comparisons) | 0.3238 | 1.2084 | 20.978 |
| **all steps** | 0.417 | 1.305 | 21.331 |

## Before / after

| Query / stage | Before | After | Change |
|---|---|---|---|
| Group films (5,000 films): one call per row → one whole-column rule | 0.0255 s | 0.0014 s | 19x faster |
| All 14 uncertainty comparisons (500 films): multinomial draw → counting random picks | 2.81 s | 1.18 s | 2.4x faster |

## Caveats

- Timings are from one laptop. Another machine will differ; the shape (how time grows with size) should hold.
- The cold run is dominated by reading about a thousand freshly written files, which Windows also scans for viruses. Adjoa meets it at most once, the first time she runs after fetching new data or restarting the laptop; a practice run before the meeting avoids it. The run reads each saved file once (later steps read the flattened tables).
- Copied data repeats the same films, so it tests speed and memory, not new findings.
- At 5,000 films the uncertainty step alone takes well over 10 seconds; the budget is for about 500 titles. Lowering `N_RESAMPLES` in `src/uncertainty.py` from 10,000 to 2,000 would cut it by about four-fifths.
- The two ways of drawing reshuffles give the same results to within one percentage point; they differ only in the random sequence.