# ADR-002: Compare the typical film and the typical whole franchise against the typical standalone, in both time windows

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame's question is "bundles or standalones". The data comes per film, but a franchise is bought whole. Nine films belong to a franchise but are the only film from it on the list. Returns have a long tail: the average film returns 8.5x, the middle film 5.37x. 41 of 112 films are from before 2000, including the biggest returns (Star Wars 70.5x, Jaws 67.2x), over half the standalone films are pre-2000 against a third of the franchise films, and Finance distrusts pre-2000 figures. Films in one franchise succeed or fail together, so Harry Potter's 8 films are one bet, not 8.

## Decision

I measure value as box-office return (worldwide revenue divided by production budget) and compare the middle film of each group, and the middle whole franchise (every released film, on the list or not; three or more films) against the middle standalone, for all years and for 2000 onward. A franchise needs two films on the list (a film alone on the list is a standalone), a window never cuts a franchise in half, and uncertainty comes from 10,000 reshuffles of the list that draw whole franchises at a time.

## Alternatives considered

### Alternative A: Per film only, every film independent

- **How it would work:** Compare the middle franchise film with the middle standalone film, and reshuffle single films.
- **Why it is attractive:** Simple, uses every film, and is the figure the brief describes.
- **Why rejected:** It counts Harry Potter as 8 pieces of evidence and ignores that bundles are sold all-or-none. Under it franchises lead in both windows, in 81% (all years) and 82% (2000 onward) of reshuffles: the strongest-looking case for bundles, and too strong. Per whole franchise the all-years answer reverses (4.4x against 5.0x) and the 2000-onward answer is a tie (4.5x each).

### Alternative B: Per whole franchise only

- **How it would work:** One number per franchise, compared with standalone films.
- **Why it is attractive:** Matches exactly how bundles are bought.
- **Why rejected:** Leaves 11 franchises from 2000 onward, too few to stand alone, and drops the per-film view the brief asks for.

### Alternative C: The average instead of the middle film

- **How it would work:** Add all returns and divide.
- **Why it is attractive:** Familiar, and uses every value fully.
- **Why rejected:** A handful of old hits set the answer. Across all years the average gives standalones 10.5x against 7.9x for franchises, the opposite of the middle film (5.0x against 5.5x), because of Jaws and The Good, the Bad and the Ugly. The run report prints both.

### Alternative D: Count the nine lone films as franchise, or leave them out

- **How it would work:** Follow the database's franchise label, or drop the nine from both groups.
- **Why it is attractive:** Matches the database, or keeps the groups clean.
- **Why rejected:** A "bundle" of one film is not a bundle, and dropping them shrinks the standalone group from 25 to 16. Under all three options franchise films lead in 79–93% of reshuffles, so the direction never changes, only the strength.

### Alternative E: Cut franchises at 2000 like single films, or shortlist from all years

- **How it would work:** Keep only a franchise's post-2000 films; or rank every title regardless of year.
- **Why it is attractive:** One rule for everything; or uses all the data.
- **Why rejected:** A studio will not sell Mission: Impossible without its 1996 film, so a cut franchise cannot be bought. Shortlisting from all years swaps Harry Potter for Back to the Future (1985–1990), a 35-year-old trilogy from a different market.

### Alternative F: Raw revenue as the measure of value

- **How it would work:** Rank by worldwide box office in dollars.
- **Why it is attractive:** Big numbers, easy to say.
- **Why rejected:** Favours the most expensive films, and old and new money mix badly; a return partly cancels inflation because cost and income are in the same year's money (F-07).

## Consequences

- **What this buys:** An honest strength of evidence, said loudly in the memo. Per film, franchises lead in both windows (5.5x against 5.0x all years; 5.1x against 4.5x from 2000), in 79% and 80% of reshuffles. Per whole franchise, they trail across all years (4.4x against 5.0x; ahead in 36% of reshuffles) and tie from 2000 onward (4.5x each; ahead in 65%). Every range includes zero, so "bundles are the safer class of purchase" is not supported; "these specific bundles are strong" is.
- **What this costs:** A less clean headline, and a shortlist that leaves out older films. Two shortlisted standalones (The Incredibles, Monsters, Inc.) have a released sequel; the shortlist shows each title's number of other franchise films so negotiators see it.
- **What it costs the client if I am wrong:** If the per-film view is the right one, the recommendation is slightly too cautious; the shortlist does not change. If blockbusters are what pay for a library, the middle film understates high-variance titles. A great older franchise (Back to the Future) is not on the shortlist.
- **What would make me revisit this:** Licence prices or streaming viewing figures, which would replace box-office return as the measure; or evidence that classic films perform as well on a streaming service.

## What this survives

At about 500 titles Adjoa reruns unchanged. The grouping reads franchise counts from the data each time, so today's lone films become franchises when more of their series is listed. The cut-off year is one setting (`CUTOFF_YEAR` in `src/analysis.py`) that every step reads. More franchises let the per-franchise comparison stand on its own, and all 14 comparisons are recomputed and printed in the run report on every run.
