# ADR-007: Account for every id, and save every database answer once

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

The list has defects (F-03) and a database that is polite-use only. We need both a full account of the 127 lines and a way to repeat the analysis without calling the database again.

## Decision

Read every line as text and give it one status: usable, repeat, blank, other-database id or invalid. Request each usable id once, wait a tenth of a second between requests, retry only temporary errors, never retry "not found", and save each raw answer to disk with the time it was fetched.

## Alternatives considered

### Alternative A: Let the standard reader drop bad lines

- **How it would work:** Read the file and drop empty values.
- **Why it is attractive:** Fewer lines of code.
- **Why rejected:** It silently turns 127 lines into 126 and hides the "N/A".

### Alternative B: Fetch again on every run

- **How it would work:** Call the database each time.
- **Why it is attractive:** Always fresh.
- **Why rejected:** Slower, depends on the internet, and results can change between runs.

## Consequences

- **What this buys:** A full reconciliation, a first run of 234 requests and a second run of 0, and an offline option.
- **What this costs:** The saved data goes out of date; each film carries its fetch date.
- **What it costs the client if I am wrong:** Amounts edited in the database after 17 November are not reflected.
- **What would make me revisit this:** A need for fresher figures, in which case delete the saved folder and fetch again.

## What this survives

At about 500 titles Adjoa replaces the id file and runs the analysis. Only new ids are requested (about 1,000 requests, roughly two minutes at the polite pace). Every id still lands in a category, and the run report lists new and removed films.