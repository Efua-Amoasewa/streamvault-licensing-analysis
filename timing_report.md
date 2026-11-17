# Run time report

## Target

The whole analysis, from cached data to finished tables, runs in under 5 seconds on Adjoa's laptop at next year's list size (about 500 films), with room to spare at 10 times that.

## Method

- Hardware: Windows-11-10.0.26300-SP0, AMD64, Python 3.15.2, pandas 3.1.1
- What was timed: every analysis stage (classify, KPI tables, bundles, standalones, entry position, talent, bootstrap), from data already loaded in memory to finished tables. Network fetching and reading cached files from disk are excluded; fetching is the slow part and happens only for new ids.
- Runs: 5 warm runs per size after one discarded warm-up. Reported: median, 95th percentile, worst.
- Larger sizes are made by copying the real films with new ids and collections, so the shape of the data is realistic.
- Reproduce: `python src/timing.py`

## Results

| Scenario | Runs | Median (s) | p95 (s) | Worst (s) | Target met? |
|---|---|---|---|---|---|
| 112 films | 5 | 0.099 | 0.14 | 0.148 | yes |
| 500 films | 5 | 0.209 | 0.234 | 0.239 | yes |
| 5000 films | 5 | 1.353 | 1.367 | 1.371 | yes |

Median seconds per stage:

| Stage | 112 films | 500 films | 5000 films |
|---|---|---|---|
| classify | 0.0007 | 0.0008 | 0.0012 |
| kpi tables | 0.0091 | 0.0081 | 0.0095 |
| bundles | 0.0075 | 0.0075 | 0.009 |
| standalones | 0.002 | 0.0018 | 0.002 |
| entry position | 0.0086 | 0.0076 | 0.0127 |
| talent | 0.0339 | 0.0344 | 0.0387 |
| bootstrap | 0.0344 | 0.1463 | 1.2798 |

## Before / after

| Stage | Before (row by row) | After (whole column) | Change |
|---|---|---|---|
| classify, 5000 films | 0.0288s | 0.0020s | 14x faster |

## Caveats

- Timings are from one laptop. Another machine will differ; the shape (how time grows with size) should hold.
- Copied data repeats the same films, so it tests speed and memory, not new findings.
- The bootstrap is drawn in batches so memory stays small; one big array would need about 280 MB at 3,500 films.