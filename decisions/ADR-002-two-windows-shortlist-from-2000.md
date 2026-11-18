# ADR-002: Report two time windows and build the shortlist from films released in 2000 or later

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

41 of 112 films were released before 2000, including the biggest returns (Star Wars 70.5x, Jaws 67.2x). The brief asks for both windows. Over half of the standalone films are pre-2000, against a third of the franchise films, so the all-years comparison is tilted.

## Decision

Show every comparison for all years and for 2000 onward. Choose the shortlist from 2000 onward, because it is closer to what StreamVault would license today.

A window never cuts a bundle in half. A franchise is sold whole, so a bundle is in the 2000-onward ranking only if every one of its released films is from 2000 or later; otherwise it appears in the all-years ranking only. (Before this rule, Mission: Impossible was ranked without its 1996 film and Indiana Jones on one film.)

## Alternatives considered

### Alternative A: Use all years for the shortlist

- **How it would work:** Rank every film and bundle regardless of year.
- **Why it is attractive:** Uses all data.
- **Why rejected:** The bundle shortlist would become The Lord of the Rings, Back to the Future (1985–1990) and The Avengers, dropping Harry Potter for a 35-year-old trilogy whose box-office was in a different market; Toy Story and The Godfather would follow.
- **What the recommendation looks like under it:** Per whole bundle, the all-years comparison reverses (typical bundle 4.5x against a typical standalone 5.0x), so "lead with bundles" would not hold as a general rule; only the specific strong bundles would.

### Alternative B: Cut bundles at 2000 like single films

- **How it would work:** Keep only the post-2000 films of each franchise.
- **Why it is attractive:** One rule for everything.
- **Why rejected:** Values something that cannot be bought. A studio will not sell Mission: Impossible without its first film.

## Consequences

- **What this buys:** A shortlist of films audiences can still relate to, and a fair comparison between groups in one era.
- **What this costs:** Standalone films shrink to 12.
- **What it costs the client if I am wrong:** A great older film (for example Back to the Future, the second-ranked bundle across all years) is not on the shortlist.
- **What would make me revisit this:** Evidence that classic films perform as well on a streaming service.

## What this survives

Per film, both windows point the same way (franchise 5.5x vs 5.0x all years; 5.1x vs 4.5x from 2000), and only the average flips in the all-years window. Per whole bundle the all-years window flips (4.5x vs 5.0x) while 2000 onward does not (5.0x vs 4.5x). The memo says both plainly. With about 500 titles the cut-off year is one setting (`CUTOFF_YEAR` in `src/analysis.py`) that every step reads.