# ADR-011: The time budget is 10 seconds for the whole offline run at 500 titles

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

The brief says Adjoa will rerun this on her own laptop, "sometimes live in a meeting", but sets no time. A budget has to be chosen and then measured the way she will experience it.

## Decision

From typing `python src/run_all.py --offline` to a finished report, under 10 seconds at about 500 titles, measured end to end: a fresh Python start, reading every saved file from disk, flattening, the data check, the analysis and the report. Fetching new films is outside the budget: it is done once, before the meeting (about two minutes for 500 new films at the polite pace).

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

- **What this buys:** A claim that matches what Adjoa will see: about 7.5 seconds at 500 titles on this laptop (see `timing_report.md`).
- **What this costs:** 10 seconds feels slow in a meeting; it is about the limit.
- **What it costs the client if I am wrong:** On a slower laptop the run may take 15 seconds. It still works; it is just a pause.
- **What would make me revisit this:** Lists of 5,000 titles. In memory the analysis then takes about 5 seconds, almost all of it the uncertainty reshuffles; reducing them from 10,000 to 2,000 would cut that by about four-fifths.

## What this survives

`python src/timing.py` rebuilds a 500-film copy of the project and re-measures, so Adjoa can check the budget on her own laptop.
