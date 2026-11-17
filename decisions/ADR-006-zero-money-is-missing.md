# ADR-006: Treat a zero budget or revenue as "missing", and stop the run when data is impossible

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

The database stores 0 when nobody entered a figure. Dividing by a zero budget gives an infinite return that would swamp every total. This list has no such film today, but a list of about 500 probably will.

## Decision

A film with zero budget or revenue is still counted as a title but left out of every return calculation. A set of checks runs before any result is produced: impossible problems (repeated film, wrong film returned, bad date, negative money, film lost on the way) stop the run; softer ones (missing money, cast or director, unreleased) are reported as warnings.

## Alternatives considered

### Alternative A: Drop the film completely

- **How it would work:** Remove any film without money.
- **Why it is attractive:** Simple.
- **Why rejected:** The film's title, cast and collection are still real; dropping it hides it from the counts.

### Alternative B: Replace zero with an estimate

- **How it would work:** Fill with an average budget.
- **Why it is attractive:** Keeps every film in the maths.
- **Why rejected:** Invents data that would then look real.

## Consequences

- **What this buys:** No infinite values; every exclusion is counted in the run report.
- **What this costs:** The gate's thresholds are my judgement.
- **What it costs the client if I am wrong:** A film that should be excluded could be included only if its zero is a real zero, which does not happen for released films.
- **What would make me revisit this:** Several warnings in a row on a new list.

## What this survives

I tested a made-up zero-budget film (flagged, excluded, no crash) and a made-up repeated film (run stops with a clear message). At about 500 titles the gate runs in a fraction of a second.