# Data findings — StreamVault licensing analysis

## Summary

The list had 127 lines and produced 112 usable films. Fifteen lines did not become a new film: 3 were not valid ids, 7 repeated a film already on the list (one of them written as another database's id) and 5 are not in the database. Every line is accounted for in the table below. No real film is missing: the one line in another database's format turned out to be The Dark Knight, which is already in the analysis.

The 112 films are internally consistent. No film appears twice, every film returned is the one requested, all dates and amounts are plausible, and a live re-check of 12 films (84 facts) found no differences. The risks are in what the data can answer, not in its accuracy. Ranked by how much they move Kwame's recommendation: the list holds only hits; most franchises on it are incomplete, which flatters them; old mega-hits distort averages; and the groups are small. Treat every number in the memo as a comparison between options, not a forecast.

Data as of 17–18 November 2026 (each answer is saved with the time it was fetched).

## Reconciliation

| Stage | Rows | Delta | Reason |
|---|---|---|---|
| ids in the file | 127 | | every line, including a blank line |
| valid-looking ids | 124 | -3 | 1 blank line, 1 text placeholder ("N/A"), 1 negative number ("-1") |
| unique ids to request | 117 | -7 | 6 ids listed more than once, plus "tt0468569": another database's id, looked up live and matched to The Dark Knight (id 155), already on the list (twice) |
| films found in the database | 112 | -5 | 5 very large ids the database does not know (it answers "not found"): 7733901, 8471293, 8471294, 9412887, 9412888 |
| films with usable return figures | 112 | 0 | no film has a zero or missing budget or revenue |

To value franchises as they are sold (all films or none), the run also fetches each franchise's full film list and the figures for the 21 released films that are in those franchises but not on the candidate list. These extra films are used only to value bundles; they are never counted as candidates.

## Findings, ranked by risk

### F-01: The list contains only winners — Severity: High

- **What it is:** Every film in the list earned back more than it cost. The list is a set of well-known successes, not a sample of everything a studio might license.
- **How I detected it:** The lowest return in the list is 1.13x (The Shawshank Redemption). Zero films earn less than their budget. The typical film returns 5.37x.
- **Scale:** All 112 films.
- **Effect on the client's number:** Every return figure is a best case. A random film from the market would do far worse, for franchises and standalones alike. The comparison between the two groups is fairer than the absolute levels.
- **What I did about it:** Reported returns only as a comparison between groups and as relative price ceilings, never as an expected profit. Said so in the memo.
- **Residual risk:** Cannot be removed with this list. A list that includes flops is needed to measure it.

### F-02: Most franchises on the list are incomplete, which flatters them — Severity: High

- **What it is:** Studios sell a franchise all-or-none, but 10 of the 23 franchises on the list are missing released films (21 films in total). The missing films are mostly later, weaker sequels: Star Wars is missing the three 2015–2019 films, Jurassic Park the four Jurassic World films, Mission: Impossible the last three.
- **How I detected it:** Fetched each franchise's full film list from the database and compared it with the candidate list. A check in the run stops it if a franchise film on the list is not found in its franchise.
- **Scale:** 10 of 23 franchises; 21 films.
- **Effect on the client's number:** Valued on the list alone, every incomplete franchise looks better than it is: Star Wars 10.8x → 6.2x whole, Jurassic Park 8.9x → 5.0x, Indiana Jones 7.1x → 4.1x, Ice Age 8.4x → 7.5x. Measured per whole bundle (what Kwame buys), the all-years comparison **reverses**: the typical bundle returns 4.5x against 5.0x for a standalone film. From 2000 onward bundles still lead, 5.0x against 4.5x.
- **What I did about it:** Ranked bundles on the whole franchise, not the films on the list. Reported the per-bundle comparison next to the per-film one in both windows, and in the memo.
- **Residual risk:** The top three bundles (The Lord of the Rings, The Avengers, Harry Potter) are complete, so the shortlist does not change. Toy Story 5 (2026) is still in cinemas, so Toy Story's whole figure will move. One Ice Age film has no budget recorded, so Ice Age is valued on 5 of its 6 films.

### F-03: Old mega-hits distort the all-years average — Severity: High

- **What it is:** Films from 1966 to 1981 earned up to 70x their budget (Star Wars 70.5x, Jaws 67.2x, The Godfather 40.8x, The Good, the Bad and the Ugly 32.4x). They are real, but they come from a different era of cinema and ticket prices.
- **How I detected it:** Average return 8.5x against a typical (middle) film of 5.37x; 11 films flagged as unusually high by a standard outlier rule; the top five returns are all from 1966–1981, and the top ten from 1966–1994.
- **Scale:** 41 of 112 films were released before 2000 (28 franchise, 13 standalone). Over half the standalone films (52%) are pre-2000, against 32% of franchise films.
- **Effect on the client's number:** In the all-years window the standalone average (10.5x) is higher than the franchise average (7.9x). The typical film points the other way (5.5x franchise vs 5.0x standalone). The conclusion would flip depending on which measure I chose.
- **What I did about it:** Used the middle film as the headline measure (ADR-003). Reported two windows, all years and 2000 onward, and built the shortlist from 2000 onward (ADR-002).
- **Residual risk:** Amounts are not adjusted for inflation (F-07).

### F-04: The groups are small and franchise films are not independent — Severity: Medium

- **What it is:** From 2000 onward there are only 12 standalone films and 12 whole bundles. Films in one franchise rise and fall together: Harry Potter's 8 films are one decision, not 8.
- **How I detected it:** Counted films per group and window, then re-ran the comparison 10,000 times on reshuffled versions of the list, drawing whole franchises at a time (ADR-008).
- **Scale:** 12 standalone films and 59 franchise films in 12 franchises from 2000 onward.
- **Effect on the client's number:** Drawing whole franchises widens the uncertainty: the franchise film comes out ahead in 80% of reshuffles from 2000 onward (83% if every film were treated as independent); the plausible gap runs from -0.7x to +2.7x. Per whole bundle, bundles lead in 74% of reshuffles from 2000 onward and only 40% across all years. Every range includes zero.
- **What I did about it:** Reported the ranges and the share of reshuffles in which franchises lead, for both the per-film and per-bundle comparison. Required at least 3 released films before ranking a bundle.
- **Residual risk:** A bigger list (about 500 films) would tighten these ranges. Rerun the analysis then.

### F-05: The id list had defects that standard tools hide — Severity: Medium

- **What it is:** One blank line, one "N/A", one "-1", one id in another database's format, six repeated ids and five ids the database does not know.
- **How I detected it:** The usual file reader reports 126 rows, not 127, because it silently skips blank lines and turns "N/A" into a missing value. Reading every line as text and counting by category caught it, and the counts add up to 127. The other-database id was looked up live through the database's own matching service rather than dropped.
- **Scale:** 15 of 127 lines (12%).
- **Effect on the client's number:** Without removing repeats, seven extra rows (including The Dark Knight three times, Fight Club, Pulp Fiction and The Empire Strikes Back) would be counted and bundles would be inflated. Nothing real is lost: the other-database id was a third copy of The Dark Knight.
- **What I did about it:** Classified every line instead of dropping lines (ADR-007). Removed repeats, kept the first. Ids written as "0155" or "155.0", which a spreadsheet edit can produce, are now treated as the same film as "155".
- **Residual risk:** None for this list. The five unknown ids may be typing errors for real films; nothing in the data says which.

### F-06: Nine films belong to a franchise but appear alone — Severity: Medium

- **What it is:** Nine films have sequels or siblings but only one film on our list: The Silence of the Lambs, The Smurfs, Jaws, Monsters, Inc., Ghostbusters, Mad Max: Fury Road, Blade Runner, The Lion King, The Incredibles.
- **How I detected it:** Compared each film's franchise with how many films of that franchise are on our list.
- **Scale:** 9 of 112 films (8%). They change the standalone group from 16 films to 25.
- **Effect on the client's number:** Putting them in standalone, franchise or neither moves the share of reshuffles where franchise wins between 78% and 93% (see ADR-001). The direction never changes; the strength does.
- **What I did about it:** Counted them as standalone, because a bundle needs at least two films on our list. Ran all three options and reported the range. The standalone shortlist now shows how many other films each title's franchise has.
- **Residual risk:** The Incredibles and Monsters, Inc. are on the standalone shortlist, but each has a released sequel, so a studio may only sell them as a pair.

### F-07: Amounts are in the money of their release year, and some are rounded estimates — Severity: Low

- **What it is:** Budget and revenue are not adjusted for inflation or ticket-price changes. Four films have both figures in whole millions (for example Monsters, Inc.: $130M budget, $650M revenue, exactly 5.0x), which suggests estimates; Monsters, Inc.'s revenue likely includes a later re-release.
- **How I detected it:** Checked how the amounts are defined; counted films whose figures are both round millions; re-fetched Monsters, Inc. live (the source agrees with our copy).
- **Scale:** All films for inflation, most affecting pre-2000 films; 4 films for rounding.
- **Effect on the client's number:** A return multiple partly cancels inflation (cost and income are in the same year's money), so the damage is smaller than for raw revenue. Monsters, Inc. is fifth on the standalone shortlist with a score of 0.61, against 0.50 for sixth place, so a moderate correction would not remove it.
- **What I did about it:** Used return (revenue divided by budget) rather than raw revenue for the main comparison and said so.
- **Residual risk:** Re-release revenue cannot be separated from the original run in this data.

## Looked wrong, is not wrong

| Apparent problem | Why it looks wrong | Why it is actually fine |
|---|---|---|
| "tt0468569" in the list | Looks like a lost film | It is The Dark Knight's id in another film database; matched live to id 155, which is already on the list. |
| Star Wars returns 70.5x | Looks like a data entry error | Budget $11M, revenue $775M, both confirmed in the live re-check. It is real, just from 1977; it is why I use the middle film, not the average. |
| The Shawshank Redemption returns only 1.13x, Blade Runner 1.49x | Looks like missing revenue | Both are known for modest box-office; both agree with the live database. |
| Two non-English films (Spirited Away, The Good, the Bad and the Ugly) | Might be dubbed or duplicate records | They are the original-language records, each present once. |
| Six repeated ids | Looks like 6 films counted twice | Removed before fetching; the final film table has no repeats (checked in code). |
| No film returns less than 1.0x | Looks like a filter removed losers | No filter was applied; it is a feature of the list (F-01). |
| 126 rows instead of 127 | The number the usual reader reports | The reader skips a blank line; 127 is correct (F-05). |

## How the tables are joined, and proof nothing is lost or doubled

- Each saved answer keeps the id we asked for. The run stops if the database returned a different film, if a film appears twice, or if the number of films flattened differs from the number fetched.
- Cast and directors are joined to films many-to-one with a check that every person-film row finds exactly one film; the row count before and after the join must match.
- Whole-bundle figures are joined to films one-to-one; the run stops if any film has two money records or if a franchise film on the list is missing from its franchise.

## Could not verify

- **Licence prices.** Nothing in the data says what any film or bundle costs to license. This is the biggest gap between the analysis and Kwame's real decision; the price ceilings are relative, not market prices.
- **Whether the rights are available,** and whether studios will sell a franchise without its newest films.
- **Whether budgets and revenues are complete.** The database is maintained by the public, so amounts may omit marketing costs or later income (home video, streaming, television), and some are rounded estimates (F-07).
- **How often each film is watched on a streaming service.** Box office is only a stand-in for appeal to subscribers.
- **Spot-check.** On 17 November 2026, 12 films were re-fetched live in four groups (4 random, the 2 highest and 2 lowest returns, 2 films moved to standalone, 2 closest to the year 2000). All 84 checked facts matched within the 1% tolerance set beforehand (exact match required for titles, dates, franchises and directors). On 18 November Monsters, Inc. was also re-checked. This shows the data was stored correctly, not that the database itself is correct.
