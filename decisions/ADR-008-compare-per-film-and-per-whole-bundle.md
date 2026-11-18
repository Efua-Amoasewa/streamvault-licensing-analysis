# ADR-008: Compare franchises and standalones both per film and per whole bundle, and treat a franchise's films as one draw

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame's question is "bundles or standalones". The data comes per film, but he buys a franchise whole and a standalone alone. The films of one franchise also succeed or fail together: Harry Potter's 8 films are one purchase, not 8 independent bets. A comparison that ignores either point overstates how sure we are.

## Decision

1. Report two comparisons in both windows: the typical **film** in each group (as before), and the typical **whole bundle** (every released film in the franchise, on the list or not) against the typical standalone film.
2. When measuring uncertainty, reshuffle whole franchises, not single films: a reshuffled list draws franchises with replacement and takes all their films together.

## Alternatives considered

### Alternative A: Per film only, every film independent (the original approach)

- **How it would work:** Compare the middle franchise film with the middle standalone film; reshuffle single films.
- **Why it is attractive:** Simple, uses every film, and the per-film figure is the one the brief describes.
- **Why rejected as the only view:** It counts the 8 Harry Potter films as 8 pieces of evidence and ignores that bundles are sold all-or-none.
- **What the recommendation looks like under it:** Franchises ahead in both windows, in 81% (all years) and 83% (2000 onward) of reshuffles. That is the strongest-looking case for bundles, and it is too strong.

### Alternative B: Per whole bundle only

- **How it would work:** One number per franchise.
- **Why it is attractive:** Matches how bundles are bought.
- **Why rejected as the only view:** Leaves 12 bundles from 2000 onward, too few to stand alone, and drops the per-film view the brief asks for.

## Consequences

- **What this buys:** An honest strength of evidence. Per film, with franchises drawn whole, franchises lead in 78% (all years) and 80% (2000 onward) of reshuffles. Per whole bundle, they lead in 74% from 2000 onward but only 40% across all years: **the all-years answer reverses** (typical bundle 4.5x against a typical standalone 5.0x).
- **What this costs:** A less clean headline. "Bundles are the safer class of purchase" is not supported; "these specific bundles are strong" is.
- **What it costs the client if I am wrong:** If the per-film view is the right one, the recommendation was slightly too cautious; the shortlist does not change.
- **What would make me revisit this:** A list of about 500 titles with more complete franchises, which would let the per-bundle comparison stand on its own.

## What this survives

Both comparisons and both reshuffling methods are recomputed on every run and printed in the run report. At about 500 titles the reshuffling takes about a third of a second.
