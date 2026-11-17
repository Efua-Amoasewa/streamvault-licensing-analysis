# ADR-004: Rank shortlist candidates by the average of their percentile ranks

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

The shortlist needs three bundles and five standalone films. Candidates differ on several measures that have different units (a multiple, dollars, a rating).

## Decision

Bundles are scored on bundle return (total revenue over total cost), weakest-film return and median rating. Standalones are scored on return, revenue and rating. Each measure becomes a rank between 0 and 1 and the score is their average. Bundles need at least 3 films in the window.

## Alternatives considered

### Alternative A: Rank on return only

- **How it would work:** Pick the highest return.
- **Why it is attractive:** One number, easy to explain.
- **Why rejected:** Spirited Away (14.5x on a $19M budget) would crowd out films that also earn much more money overall.

### Alternative B: Weighted score with chosen weights

- **How it would work:** Give each measure a weight (for example 50% return).
- **Why it is attractive:** Lets the client's priorities show.
- **Why rejected:** The weights would be my guess, and with 12 films the order would change with them.

## Consequences

- **What this buys:** No unit conversions, no invented weights; weakest-film return protects against a bundle that depends on one hit.
- **What this costs:** Ties and near-ties; Ice Age (8.4x, rating 6.8) scores 0.67 against Harry Potter's 0.69 because of a lower rating.
- **What it costs the client if I am wrong:** A good fourth-placed bundle is skipped.
- **What would make me revisit this:** Kwame telling us what matters most (for example rating over revenue).

## What this survives

At about 500 titles, percentile ranks scale automatically. The three-film minimum keeps tiny collections out.