# ADR-004: Rank shortlist candidates by the average of their percentile ranks

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

The shortlist needs three bundles and five standalone films. Candidates differ on several measures that have different units (a multiple, dollars, a rating).

## Decision

Bundles are scored on the whole franchise (every released film, on the list or not): bundle return (total revenue over total cost), weakest-film return and median rating. Standalones are scored on return, revenue and rating. Each measure becomes a rank between 0 and 1 and the score is their average. Bundles need at least 3 released films (ADR-009).

## Alternatives considered

### Alternative A: Rank on return only

- **How it would work:** Pick the highest return.
- **Why it is attractive:** One number, easy to explain.
- **Why rejected:** Spirited Away (14.5x on a $19M budget) would crowd out films that also earn much more money overall.
- **What the shortlist looks like under it:** Bundles: The Lord of the Rings, Ice Age, The Avengers (Harry Potter drops out). Standalones: Spirited Away, The Incredibles, Inception, The Smurfs, Monsters, Inc. (Interstellar drops out; The Smurfs, rated 5.8, comes in).

### Alternative B: Weighted score with chosen weights

- **How it would work:** Give each measure a weight (for example 50% return).
- **Why it is attractive:** Lets the client's priorities show.
- **Why rejected:** The weights would be my guess, and with 12 films the order could change with them.
- **What the shortlist looks like under it:** With 50% on return and 25% on each other measure, the same three bundles and the same five standalones are chosen; only the order of the standalones changes.

## Consequences

- **What this buys:** No unit conversions, no invented weights; weakest-film return protects against a bundle that depends on one hit.
- **What this costs:** Near-ties below the top three: valued whole, Ice Age (7.5x, rating 6.6) and Shrek (5.6x) both score 0.58 against Harry Potter's 0.67.
- **What it costs the client if I am wrong:** A good fourth-placed bundle is skipped.
- **What would make me revisit this:** Kwame telling us what matters most (for example rating over revenue).

## What this survives

The top three bundles survive both rejected rules except return-only, which swaps Harry Potter for Ice Age. Each run writes the shortlist under all three rules to `outputs/shortlist_under_alternatives.csv`. At about 500 titles, percentile ranks scale automatically.