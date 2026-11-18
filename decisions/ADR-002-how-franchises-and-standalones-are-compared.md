# ADR-002: How franchises and standalones are compared: groups, time windows, the headline measure, and the unit of comparison

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame's question is "bundles or standalones". To answer it every film needs a group, the brief asks for two time windows, returns have a long tail, and a franchise is bought whole while the data comes per film. Each of these four choices moves the answer, so each is decided here, with what the recommendation looks like if it went the other way. All four are recomputed on every run and printed in the run report.

## Decision 1: A franchise needs two films on the list; a film alone on the list is a standalone

Nine films (such as Jaws and The Incredibles) belong to a franchise in the database, but are the only film from it on our list. They count as standalones.

**Alternatives rejected**

- **Count them as franchise films**, as the database labels them. Rejected because we can only judge a bundle from the films we can see; a "bundle" of one film is not a bundle.
- **Leave the nine out.** Keeps the groups clean but throws away nine real films and shrinks the standalone group from 25 to 16.

**What the recommendation looks like under them:** drawing whole franchises at a time, franchise films lead in 79–93% of reshuffles under all three options. The direction never changes, only the strength.

**Cost if wrong:** the standalone group is a little more mixed, which slightly favours standalones. Two shortlisted standalones (The Incredibles, Monsters, Inc.) have a released sequel and may only be sold as a pair; the shortlist shows each title's number of other franchise films so negotiators see it.

## Decision 2: Report both windows; build the shortlist from 2000 onward; never cut a bundle in half

41 of 112 films were released before 2000, including the biggest returns (Star Wars 70.5x, Jaws 67.2x). Over half the standalone films are pre-2000, against a third of the franchise films, so the all-years comparison is tilted, and Finance distrusts pre-2000 figures. Every comparison is shown for all years and for 2000 onward; the shortlist is chosen from 2000 onward because it is closer to what StreamVault would license today. A franchise is sold whole, so a bundle is in the 2000-onward ranking only if every one of its released films is from 2000 or later. (Before this rule, Mission: Impossible was ranked without its 1996 film and Indiana Jones on one film.)

**Alternatives rejected**

- **Shortlist from all years.** Uses all the data, but the bundle shortlist becomes The Lord of the Rings, Back to the Future (1985–1990) and The Avengers, dropping Harry Potter for a 35-year-old trilogy from a different market; Toy Story and The Godfather follow.
- **Cut bundles at 2000 like single films.** One rule for everything, but it values something that cannot be bought: a studio will not sell Mission: Impossible without its first film.

**The answer changes with the window, and the memo says so first.** Per film, franchises lead in both (5.5x vs 5.0x all years; 5.1x vs 4.5x from 2000). Per whole bundle, the all-years answer reverses (4.4x vs 5.0x), and from 2000 onward the two tie (4.5x each).

**Cost if wrong:** a great older film (Back to the Future, second-ranked bundle across all years) is not on the shortlist.

## Decision 3: The median film is the headline, with the average shown beside it

Return (revenue divided by budget) has a long tail: the average film returns 8.5x, the middle film 5.37x.

**Alternative rejected: the average.** Familiar, but a handful of old hits set the answer. Across all years the average gives standalones 10.5x against 7.9x for franchises, the opposite of the median, because of Jaws and The Good, the Bad and the Ugly.

**Cost if wrong:** if blockbusters are what pay for a library, the median understates high-variance films. The run report prints both.

## Decision 4: Compare per film and per whole bundle, and reshuffle whole franchises

Two comparisons in both windows: the typical **film** in each group, and the typical **whole bundle** (every released film in the franchise, on the list or not) against the typical standalone film. The per-bundle comparison uses the same bundles the shortlist ranks: three or more released films (ADR-005). To measure how sure we are, the list is reshuffled 10,000 times, drawing whole franchises with replacement so Harry Potter's 8 films move together.

**Alternatives rejected**

- **Per film only, every film independent** (the original approach). Simple and the figure the brief describes, but it counts the 8 Harry Potter films as 8 pieces of evidence and ignores that bundles are sold all-or-none. Under it, franchises lead in 81% (all years) and 82% (2000 onward) of reshuffles: the strongest-looking case for bundles, and too strong.
- **Per whole bundle only.** Matches how bundles are bought, but leaves 11 bundles from 2000 onward, too few to stand alone, and drops the per-film view the brief asks for.

**What this buys:** an honest strength of evidence. Per film with franchises drawn whole, franchises lead in 79% (all years) and 80% (2000 onward) of reshuffles. Per whole bundle, they lead in only 36% across all years and 65% from 2000 onward. Every range includes zero. "Bundles are the safer class of purchase" is not supported; "these specific bundles are strong" is.

**Cost if wrong:** if the per-film view is the right one, the recommendation is slightly too cautious; the shortlist does not change.

## What this survives

At about 500 titles Adjoa reruns unchanged. The grouping reads franchise counts from the data each time, so films that are singles today become bundles when more of their franchise is listed. The cut-off year is one setting (`CUTOFF_YEAR` in `src/analysis.py`) that every step reads. The median becomes more stable and the per-bundle comparison gains enough bundles to stand on its own; all 14 comparisons are timed in `timing_report.md` (ADR-004).
