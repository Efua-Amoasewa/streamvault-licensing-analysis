# ADR-009: Smaller judgement calls, in one place

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

Each of these is a choice the brief left open. None changes the recommendation on its own; each is listed with what it would cost if wrong.

| Call | What I decided | Why | Rejected alternative, and what it would change | Cost to Kwame if wrong |
|---|---|---|---|---|
| Measure of value | Box-office return: worldwide revenue divided by production budget | The only money figures in the data; a ratio partly cancels inflation (F-07) | Raw revenue: favours the most expensive films, and old and new money mix badly | Streaming viewing may not follow box office; a cheap cult film may be worth more to subscribers than its return suggests |
| Smallest bundle to rank | 3 released films | Two films is a pair, not a library; a 2-film "bundle" is decided by one film | 2 films: Kill Bill (2003–2004, 5.6x, weakest film 5.1x) enters and ranks third, pushing Harry Potter out | A strong pair is left off the shortlist: Kill Bill is worth a look if Tarantino rights come up, at a ceiling set the same way as the others |
| Lead actor | The first-billed cast member | The database's billing order is the closest available stand-in for the lead | Top three billed: blurs the person with the ensemble and multiplies franchise effects | A film led by an ensemble is credited to one name |
| What counts as a talent "hit" | Return above the window's typical (middle) film | Relative to the list, so it works in both windows | A fixed bar such as 3x: every film on this hits-only list would pass (F-01) | A person whose films are all solid but not above the middle is called unreliable |
| Talent bar | 3+ films, 2+ series, 75% hits (ADR-005) | Separates the person from the franchise | 67%: adds only Robert Downey Jr. from 2000 onward | A bankable name is missed |
| Repeated ids | Keep the first copy | Copies are the same film with identical answers, so the choice cannot change a number | Keep the last: identical result | None |
| Standalones with sequels | Shortlisted, but flagged with their number of other franchise films | They are the strongest standalone evidence; sale terms are unknown | Remove them: Inception, Interstellar, Spirited Away, WALL·E and The Departed would make the five | Two of five shortlisted standalones may only be sold as a pair (The Incredibles, Monsters, Inc.) |
| Rating as a ranking input | Included in the shortlist score | Audience rating is the only measure of how well a film is liked, which matters for a library | Leave it out: Ice Age (rated 6.6) would displace Harry Potter from the top three bundles | A well-rated, modest earner is ranked above a crowd-pleaser |
| Unreleased franchise films | Left out of whole-bundle values | No real revenue yet | Include them as zero: punishes franchises for a film still to come | Toy Story 5 (2026) is in cinemas; Toy Story's figure will move |

## What this survives

Every value above is a named setting at the top of its file (`MIN_BUNDLE_FILMS`, `MIN_TALENT_FILMS`, `MIN_SERIES`, `HIT_RATE_BAR`, `CUTOFF_YEAR`), so Adjoa can change one and rerun without editing logic.
