# Run time report

## Target (ADR-011)

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
| 112 films | 3 | 6.14 | 6.23 | yes |
| 500 films | 3 | 7.49 | 7.55 | yes |

## Per stage, in memory (median seconds)

| Stage | 112 films | 500 films | 5000 films |
|---|---|---|---|
| classify | 0.0008 | 0.0008 | 0.0017 |
| kpi tables | 0.0094 | 0.0096 | 0.0149 |
| whole bundles | 0.0132 | 0.0301 | 0.2018 |
| bundle ranking | 0.0019 | 0.0018 | 0.0023 |
| standalones | 0.0037 | 0.0035 | 0.0047 |
| entry position | 0.0083 | 0.0084 | 0.0157 |
| talent | 0.0372 | 0.0394 | 0.0563 |
| bootstrap | 0.0671 | 0.3236 | 4.7046 |
| **all stages** | 0.145 | 0.416 | 5.031 |

## Before / after

| Stage | Before (row by row) | After (whole column) | Change |
|---|---|---|---|
| classify, 5000 films | 0.0385s | 0.0018s | 22x faster |

## Caveats

- Timings are from one laptop. Another machine will differ; the shape (how time grows with size) should hold.
- The very first run after a restart can be a few seconds slower while the system loads Python and the files from disk.
- Copied data repeats the same films, so it tests speed and memory, not new findings.
- The bootstrap draws resamples in batches of 1,000 so memory stays small at any list size.