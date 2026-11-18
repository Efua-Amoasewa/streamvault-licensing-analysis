# ADR-010: Express "what to pay" as walk-away ceilings relative to the shortlist

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame asked what to pay for the strongest franchise relative to everything else. The data holds box-office figures but no licence prices, so no absolute price can be defended. A negotiator still needs a number to walk away at.

## Decision

Measure every shortlisted title in one unit: a typical standalone film released since 2000 (median return 4.49x).

- A **bundle** is all-or-none, so it is valued conservatively: number of films × its **weakest** film's return, in standalone units. You pay for every film, including the worst.
- A **standalone** is bought on its own: its own return, in standalone units.

Each title's share of the total units is its share of the $14M if the whole shortlist were bought: its walk-away ceiling. For The Lord of the Rings: 3 films × 9.37x ÷ 4.49x = 6.3 units, 24% of the shortlist, a ceiling of about **$3.3M**, or about 2.1 times the per-film price of a typical standalone.

## Alternatives considered

### Alternative A: Value bundles on their median or total return

- **How it would work:** Films × median film return, or total revenue ÷ total budget.
- **Why it is attractive:** Credits the bundle's strong films.
- **Why rejected:** A bundle cannot be cherry-picked; the price should hold up if the weak film is what subscribers get. Under the median, Harry Potter would be worth 11 units instead of 6.7 and the bundles' share would rise from 69% to about 75%.

### Alternative B: Give no price guidance

- **How it would work:** Rank only.
- **Why it is attractive:** Nothing is claimed that the data cannot support.
- **Why rejected:** The brief asks what to pay, and a rank does not tell a negotiator when to walk away.

## Consequences

- **What this buys:** A ceiling for every shortlisted title, consistent with every other, and a suggested split: about $9.7M bundles and $4.3M standalones if all eight were bought.
- **What this costs:** The ceilings inherit every limit of box-office return: hits-only list, nominal money, cheap films look strong (Spirited Away's 14.5x on $19M gives it 3.2 units, more than its revenue alone would justify).
- **What it costs the client if I am wrong:** If studios price bundles far above these shares, the ceilings say walk away from deals that might still be worth doing on viewing grounds the data cannot see.
- **What would make me revisit this:** Real licence quotes, which turn the ceilings into a value-for-money ratio per title.

## What this survives

Recomputed on every run (`outputs/price_ceilings.csv` and the run report). At about 500 titles the shortlist may change, and the ceilings follow it automatically.
