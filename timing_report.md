# Run time report

## Target (ADR-004)

The whole offline run, from typing the command to a finished report, takes under 10 seconds on Adjoa's laptop at next year's list size (about 500 films). That is short enough to rerun live in a meeting.

## Method

- Hardware: Windows-11-10.0.26300-SP0, AMD64, Python 3.15.2, pandas 3.1.1
- End to end: `python src/run_all.py --offline` in a throw-away copy of the project, a fresh Python process each time, reading every saved file from disk (start-up, imports, reading, flattening, checks, analysis, report). 3 timed runs after one discarded warm-up. Network fetching is excluded: it happens only for new ids (about two minutes for 500 new films at the polite pace), and can be done before the meeting.
- Per stage: each analysis step on data already in memory, 5 runs after a warm-up, up to 5,000 films.
- Larger sizes copy the real films (and their bundles) with new ids, so the shape of the data is realistic.
- Reproduce: `python src/timing.py`

## End to end

| Scenario | Runs | Median (s) | Worst (s) | Target met? |
|---|---|---|---|---|
| 112 films | 3 | 2.94 | 3.24 | yes |
| 500 films | 3 | 5.98 | 6.11 | yes |

## Per stage, in memory (median seconds)

| Stage | 112 films | 500 films | 5000 films |
|---|---|---|---|
| classify | 0.0007 | 0.0008 | 0.0032 |
| kpi tables | 0.0095 | 0.0101 | 0.0286 |
| whole bundles | 0.0132 | 0.0321 | 0.485 |
| bundle ranking | 0.0019 | 0.0021 | 0.0056 |
| standalones | 0.0038 | 0.0037 | 0.0104 |
| entry position | 0.0084 | 0.0089 | 0.0358 |
| talent | 0.0376 | 0.0383 | 0.1186 |
| uncertainty (all 14 comparisons) | 0.2655 | 1.1729 | 36.2377 |
| **all stages** | 0.344 | 1.268 | 36.961 |

## Before / after

| Stage | Before (row by row) | After (whole column) | Change |
|---|---|---|---|
| classify, 5000 films | 0.0257s | 0.0015s | 17x faster |

## Caveats

- Timings are from one laptop. Another machine will differ; the shape (how time grows with size) should hold.
- The very first run after a restart can be a few seconds slower while the system loads Python and the files from disk.
- Copied data repeats the same films, so it tests speed and memory, not new findings.
- The uncertainty stage runs all 14 comparisons the report prints, each with 10,000 resamples of both groups, drawn in batches of 1,000 so memory stays small at any list size.