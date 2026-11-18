# ADR-003: Rank candidates by the average of their percentile ranks, and price them as walk-away ceilings relative to the shortlist

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame asked for three franchise targets, five standalones, and what to pay for the strongest franchise relative to everything else. Candidates differ on measures with different units (a multiple, dollars, a rating), and the data holds box-office figures but no licence prices.

## Decision

I score each franchise of three or more released films on its whole-franchise return, its weakest film's return and its median rating, and each standalone on return, revenue and rating, turning each measure into a 0–1 rank and averaging them. Each shortlisted title's ceiling is its share of the $14M, measured in "typical recent standalone films" (median return 4.49x since 2000), with a franchise valued as its number of films with figures × its weakest film's return.

## Alternatives considered

### Alternative A: Rank on return only

- **How it would work:** Pick the highest returns.
- **Why it is attractive:** One number, easy to explain.
- **Why rejected:** Spirited Away (14.5x on a $19M budget) crowds out films that earn far more. Franchises would become The Lord of the Rings, Ice Age and The Avengers (Harry Potter drops out); standalones would add The Smurfs (rated 5.8) and drop Interstellar.

### Alternative B: A weighted score with chosen weights

- **How it would work:** For example 50% return and 25% on each other measure.
- **Why it is attractive:** Lets the client's priorities show.
- **Why rejected:** The weights would be my guess. Under that example the same eight titles are chosen; only the standalones' order changes.

### Alternative C: Leave rating out

- **How it would work:** Rank on money measures only.
- **Why it is attractive:** Box office is harder evidence than a public rating.
- **Why rejected:** Rating is the only measure of how well a film is liked, which matters for a library. Without it Ice Age (rated 6.6) displaces Harry Potter from the top three franchises.

### Alternative D: Rank two-film franchises too

- **How it would work:** Lower the minimum from 3 released films to 2.
- **Why it is attractive:** More candidates.
- **Why rejected:** Two films is a pair, decided by one film. Kill Bill (2003–2004, 5.6x, weakest film 5.1x) would enter third and push Harry Potter out. The same minimum applies to the per-franchise comparison in ADR-002.

### Alternative E: Remove standalones that have a sequel

- **How it would work:** Drop The Incredibles and Monsters, Inc. and re-score the rest.
- **Why it is attractive:** Every shortlisted standalone could then surely be bought alone.
- **Why rejected:** They are among the strongest standalone evidence and sale terms are unknown, so I flag them instead. Re-scored without them the five would be Inception, Spirited Away, Interstellar, The Departed and Memento.

### Alternative F: Value franchises on their median or total return

- **How it would work:** Films × middle film's return, or total revenue ÷ total budget.
- **Why it is attractive:** Credits the franchise's strong films.
- **Why rejected:** A franchise cannot be cherry-picked; the price should hold if the weak film is what subscribers get. Under the median, Harry Potter would be worth 11 units instead of 6.7, and franchises' share of the budget would rise from 69% to about 75%.

### Alternative G: Give no price guidance

- **How it would work:** Rank only.
- **Why it is attractive:** Claims nothing the data cannot support.
- **Why rejected:** The brief asks what to pay, and a rank does not tell a negotiator when to walk away.

## Consequences

- **What this buys:** The Lord of the Rings, The Avengers and Harry Potter; Inception, Interstellar, Spirited Away, The Incredibles and Monsters, Inc. A ceiling for each: The Lord of the Rings is 3 films × 9.37x ÷ 4.49x = 6.3 units, 24% of the shortlist, about **$3.3M**, roughly twice the per-film price of a typical standalone. Across all eight, about $9.7M franchises and $4.3M standalones.
- **What this costs:** Near-ties below the top three: Ice Age (7.5x, rated 6.6) and Shrek (5.6x) score 0.58 against Harry Potter's 0.67. The ceilings inherit every limit of box-office return: hits-only list, nominal money, and cheap films look strong (Spirited Away's 14.5x on $19M gives it 3.2 units).
- **What it costs the client if I am wrong:** A good fourth franchise is skipped; or, if studios price franchises far above these shares, the ceilings say walk away from deals that might still be worth doing on viewing grounds the data cannot see.
- **What would make me revisit this:** Kwame saying what matters most (for example rating over revenue), or real licence quotes, which would turn the ceilings into value-for-money ratios.

## What this survives

Every run writes the shortlist under all three ranking rules (`outputs/shortlist_under_alternatives.csv`) and the ceilings (`outputs/price_ceilings.csv`, also in the run report). At about 500 titles percentile ranks scale automatically and the ceilings follow whatever shortlist the data produces. `MIN_BUNDLE_FILMS` is a named setting.
