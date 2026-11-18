# ADR-004: The time budget is 10 seconds for the whole offline run at 500 titles

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

The brief says Adjoa will rerun this on her own laptop, "sometimes live in a meeting", but sets no time. A budget has to be chosen and then measured the way she will experience it.

## Decision

I set the budget at under 10 seconds for the whole offline run at about 500 titles, timed from typing `python src/run_all.py --offline` to a finished report in a fresh process. Fetching new films is outside the budget, because it is done once before the meeting (about two minutes for 500 new films at the polite pace).

## Alternatives considered

### Alternative A: 5 seconds for the analysis steps only (the original target)

- **How it would work:** Time each step on data already in memory.
- **Why it is attractive:** Easy to meet (under half a second at 500 films).
- **Why rejected:** It left out start-up and reading the saved files, which are most of what Adjoa waits for. The original report claimed the target was met while the real command took 4–7 seconds at 112 films.

### Alternative B: Include live fetching

- **How it would work:** Time a full online run.
- **Why it is attractive:** The worst case.
- **Why rejected:** Fetching speed is set by the shared database's polite-use limits, not by the analysis, and it can always be done ahead of the meeting.

## Consequences

- **What this buys:** A claim that matches what Adjoa will see. At 500 titles a repeat run takes about 6 seconds (worst of ten about 8); at 112 titles about 3 (see `timing_report.md` for median, p95 and worst). The measurement covers everything the run does, including all 14 uncertainty comparisons with 10,000 reshuffles each. Timing all 14, rather than 2 as an earlier version did, showed the reshuffling was the slow step; counting random picks instead of a multinomial draw made it 2.4 times faster with the same results to within a percentage point.
- **What this costs:** The first run after new data is fetched, or after a restart, is much slower (27 seconds at 500 titles, 8 at 112), because the laptop reads and virus-scans about a thousand freshly written files. The budget is judged on repeat runs, so Adjoa should do one practice run before the meeting.
- **What it costs the client if I am wrong:** If the meeting run is the cold one, or the laptop is slower, Kwame waits up to half a minute. The run still finishes and the answer is the same.
- **What would make me revisit this:** Lists of 5,000 titles, where the reshuffles alone take about 21 seconds in memory. Lowering `N_RESAMPLES` in `src/uncertainty.py` from 10,000 to 2,000 would cut that by about four-fifths, at the cost of shares that wobble by a couple of percentage points. A slow cold run would justify saving the flattened tables as one file per fetch so later runs skip the thousand small files.

## What this survives

`python src/timing.py` rebuilds 112- and 500-film copies of the project and re-measures cold and warm runs, so Adjoa can check the budget on her own laptop.
