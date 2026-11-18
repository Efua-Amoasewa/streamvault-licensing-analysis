# ADR-003: Shortlist by average percentile rank, judge talent across series, and price as walk-away ceilings relative to the shortlist

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame asked for three franchise targets and five standalones, a read on directors and lead actors, and what to pay for the strongest franchise relative to everything else. Candidates differ on measures with different units, a person's good run may just be their franchise, and the data holds box-office figures but no licence prices.

## Decision 1: Rank candidates by the average of their percentile ranks

Bundles are scored on the whole franchise (every released film, on the list or not): bundle return (total revenue over total cost), weakest-film return and median rating. Standalones are scored on return, revenue and rating. Each measure becomes a rank between 0 and 1, and the score is their average. Bundles need at least 3 released films (ADR-005).

**Alternatives rejected, and the shortlist under them**

- **Return only.** One number, easy to explain, but Spirited Away (14.5x on a $19M budget) crowds out films that earn far more overall. Bundles become The Lord of the Rings, Ice Age, The Avengers (Harry Potter drops out); standalones become Spirited Away, The Incredibles, Inception, The Smurfs (rated 5.8), Monsters, Inc. (Interstellar drops out).
- **A weighted score with chosen weights** (for example 50% return, 25% each other measure). Lets priorities show, but the weights would be my guess. Under that example the same eight titles are chosen; only the standalones' order changes.

**Cost if wrong:** near-ties below the top three: valued whole, Ice Age (7.5x, rated 6.6) and Shrek (5.6x) both score 0.58 against Harry Potter's 0.67, so a good fourth bundle may be skipped. Each run writes the shortlist under all three rules to `outputs/shortlist_under_alternatives.csv`.

## Decision 2: A director or lead actor is a reliable signal only with 3+ films across 2+ series and a 75% hit rate

A "hit" is a film whose return beats the window's middle film. Requiring two separate series separates the person from the franchise (Elijah Wood's three films are all The Lord of the Rings).

**Alternatives rejected**

- **Hit rate alone.** Simple, but it crowns Elijah Wood (3 of 3) and Ray Romano (3 of 3), who each appear in one series: that measures the franchise, not the person.
- **A lower bar of two in three.** More names for negotiators, but from 2000 onward it adds only Robert Downey Jr. (5 of 7 across 2 series, 71%), whose films are almost all one connected Marvel universe; one film either way changes his verdict.

**Result, which depends on the window:** across all years Steven Spielberg (8 films, 4 series, 88%), Robert Zemeckis (4 films, 2 series, 100%) and Tom Hanks (5 films, 2 series, 80%) pass, but on 1975–1997 films or, for Hanks, mostly Toy Story. From 2000 onward nobody passes: Christopher Nolan has 7 films across 5 series and only 29% beat the typical film; Peter Jackson 50%. Talent is not a reason to pay more for a recent title; the useful lever is the reverse, refusing a premium for a name.

**Cost if wrong:** a genuinely bankable person is overlooked, because very few people can pass the test in 112 films.

## Decision 3: Express "what to pay" as walk-away ceilings relative to the shortlist

Every shortlisted title is measured in one unit: a typical standalone film released since 2000 (median return 4.49x).

- A **bundle** is all-or-none, so it is valued conservatively: number of films with box-office figures × its **weakest** film's return, in standalone units. You pay for every film, including the worst; a film with no figures (such as a recent release) adds nothing rather than an invented value.
- A **standalone** is valued on its own return, in standalone units.

Each title's share of the total units is its share of the $14M if the whole shortlist were bought: its walk-away ceiling. For The Lord of the Rings: 3 films × 9.37x ÷ 4.49x = 6.3 units, 24% of the shortlist, a ceiling of about **$3.3M**, about 2.1 times the per-film price of a typical standalone. Across all eight: about $9.7M bundles and $4.3M standalones.

**Alternatives rejected**

- **Value bundles on their median or total return.** Credits the strong films, but a bundle cannot be cherry-picked; the price should hold if the weak film is what subscribers get. Under the median, Harry Potter would be worth 11 units instead of 6.7, and the bundles' share would rise from 69% to about 75%.
- **No price guidance, rank only.** Claims nothing the data cannot support, but the brief asks what to pay, and a rank does not tell a negotiator when to walk away.

**Cost if wrong:** the ceilings inherit every limit of box-office return (hits-only list, nominal money, cheap films look strong: Spirited Away's 14.5x on $19M gives it 3.2 units). If studios price bundles far above these shares, the ceilings say walk away from deals that might still be worth doing on viewing grounds the data cannot see. Real licence quotes would turn them into value-for-money ratios.

## What this survives

Shortlist, talent table and ceilings are recomputed on every run (run report, `outputs/price_ceilings.csv`). At about 500 titles percentile ranks scale automatically, more people will have films across several series, and the ceilings follow whatever shortlist the data produces. The thresholds (`MIN_BUNDLE_FILMS`, `MIN_TALENT_FILMS`, `MIN_SERIES`, `HIT_RATE_BAR`) are named settings at the top of their files.
