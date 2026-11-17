# Data findings — StreamVault licensing analysis

## Summary

The list had 127 lines and produced 112 usable films. Fifteen lines did not become a film: 4 were not valid ids, 6 repeated an earlier id and 5 are not in the database. Every line is accounted for in the table below.

The 112 films are internally consistent. No film appears twice, every film returned is the one requested, all dates and amounts are plausible, and a live re-check of 12 films (84 facts) found no differences. The risk is not in the data's accuracy but in what the data can answer. The list is full of proven hits, amounts are in the money of their release year, and we have box-office figures but no licence prices. Treat every number in the memo as a best case, not a forecast.

Data as of 17 November 2026 (each film was fetched that day).

## Reconciliation

| Stage | Rows | Delta | Reason |
|---|---|---|---|
| ids in the file | 127 | | every line, including a blank line |
| valid-looking ids | 123 | -4 | 1 blank line, 1 text placeholder ("N/A"), 1 negative number, 1 id from a different film database (starts "tt") |
| unique ids to request | 117 | -6 | 6 ids listed more than once (6 extra lines) |
| films found in the database | 112 | -5 | 5 very large ids the database does not know (it answers "not found") |
| films with usable return figures | 112 | 0 | no film has a zero or missing budget or revenue |

## Findings, ranked by risk

### F-01: The list contains only winners — Severity: High

- **What it is:** Every film in the list earned back more than it cost. The list looks like a set of well-known successes, not a sample of everything a studio might license.
- **How I detected it:** Checked the lowest return in the list: 1.13x (The Shawshank Redemption). Zero films earn less than their budget. The typical film returns 5.37x.
- **Scale:** All 112 films.
- **Effect on the client's number:** Every return figure is a best case. A random film from the market would do far worse, for franchises and standalones alike. The comparison between the two groups is fairer than the absolute levels.
- **What I did about it:** Reported returns only as a comparison between groups, never as an expected profit. Said so in the memo.
- **Residual risk:** Cannot be removed with this list. A list that includes flops is needed to measure it.

### F-02: Old mega-hits distort the all-years average — Severity: High

- **What it is:** Films from 1966 to 1981 earned up to 70x their budget (Star Wars 70.5x, Jaws 67.2x, The Godfather 40.8x). They are real, but they come from a different era of cinema and ticket prices.
- **How I detected it:** Average return 8.5x against a typical (middle) film of 5.37x; 11 films flagged as unusually high by a standard outlier rule; the top eight returns are all 1972–1994.
- **Scale:** 41 of 112 films were released before 2000 (28 franchise, 13 standalone). Over half the standalone films (52%) are pre-2000, against 32% of franchise films.
- **Effect on the client's number:** In the all-years window the standalone average (10.5x) is higher than the franchise average (7.9x). The typical film points the other way (5.5x franchise vs 5.0x standalone). The conclusion would flip depending on which measure I chose.
- **What I did about it:** Used the middle film as the headline measure (ADR-003). Reported two windows, all years and 2000 onward, and built the shortlist from 2000 onward (ADR-002).
- **Residual risk:** Amounts are not adjusted for inflation, so old and new films are still not exactly comparable.

### F-03: The id list had defects that standard tools hide — Severity: Medium

- **What it is:** One blank line, one "N/A", one negative id, one id in another database's format, six repeated ids and five ids the database does not know.
- **How I detected it:** The usual file reader reports 126 rows, not 127, because it silently skips blank lines and turns "N/A" into a missing value. Reading every line as text and counting by category caught it, and the counts add up to 127.
- **Scale:** 15 of 127 lines (12%).
- **Effect on the client's number:** Without the repeated-id removal, six films (including Fight Club, Pulp Fiction and The Empire Strikes Back) would be counted twice and bundles would be inflated. One real film (the id in the other database's format) is missing from the analysis.
- **What I did about it:** Classified every line instead of dropping lines (ADR-007). Removed repeats, kept the first. Left the other-format id out rather than guess its match.
- **Residual risk:** The missing film is not in the analysis. If it is a hit it would help the side of the comparison it belongs to.

### F-04: Nine films belong to a collection but appear alone — Severity: Medium

- **What it is:** Nine films have sequels or siblings in the database but only one film in our list: The Silence of the Lambs, The Smurfs, Jaws, Monsters Inc., Ghostbusters, Mad Max: Fury Road, Blade Runner, The Lion King, The Incredibles.
- **How I detected it:** Compared each film's collection with how many films of that collection are in our list.
- **Scale:** 9 of 112 films (8%). They change the standalone group from 16 films to 25.
- **Effect on the client's number:** Putting them in standalone, franchise or neither moves the share of resamples where franchise wins between 81% and 95% (see ADR-001). The direction never changes; the strength does.
- **What I did about it:** Counted them as standalone, because a bundle needs at least two films in our list. Ran all three options and reported the range.
- **Residual risk:** The Incredibles and Monsters Inc. are on the standalone shortlist, but sequels exist, so they may also be licensable as a bundle.

### F-05: Some groups are very small — Severity: Medium

- **What it is:** From 2000 onward there are only 12 standalone films. The top bundle (The Lord of the Rings) has exactly 3 films.
- **How I detected it:** Counted films per group and window.
- **Scale:** 12 standalone and 59 franchise films in the 2000-onward window.
- **Effect on the client's number:** One film changes a small group's middle value noticeably. Reshuffling the data 10,000 times shows the plausible gap between groups runs from -0.6x to +2.4x from 2000 onward and from -6.3x to +3.1x for all years. Both ranges include zero, so a real advantage is likely but not proven.
- **What I did about it:** Reported the ranges. Required at least 3 films before ranking a bundle.
- **Residual risk:** A bigger list (about 500 films) would tighten these ranges. Rerun the analysis then.

### F-06: Amounts are in the money of their release year — Severity: Low

- **What it is:** Budget and revenue are not adjusted for inflation or ticket-price changes.
- **How I detected it:** Checked how the amounts are defined; the database stores one nominal figure per film.
- **Scale:** All films, most affecting pre-2000 films.
- **Effect on the client's number:** A return multiple partly cancels inflation (both cost and income are in the same year's money), so the damage is smaller than for raw revenue. Revenue totals across years are not comparable.
- **What I did about it:** Used return (revenue divided by budget) rather than raw revenue for the main comparison and said so.
- **Residual risk:** Re-releases that add to old revenue are not visible (the same-title check found none, but a re-release can add revenue under the same record).

## Looked wrong, is not wrong

| Apparent problem | Why it looks wrong | Why it is actually fine |
|---|---|---|
| Star Wars returns 70.5x | Looks like a data entry error | Budget $11M, revenue $775M, both confirmed in the live re-check. It is real, just from 1977; it is why I use the middle film, not the average. |
| The Shawshank Redemption returns only 1.13x, Blade Runner 1.49x | Looks like missing revenue | Both are known for modest box-office; both agree with the live database. |
| Two non-English films (Spirited Away, The Good, the Bad and the Ugly) | Might be dubbed or duplicate records | They are the original-language records, each present once. Spirited Away is on the shortlist as a real 14.5x. |
| Six repeated ids | Looks like 6 films counted twice | Removed before fetching; the final film table has no repeats (checked). |
| No film returns less than 1.0x | Looks like a filter removed losers | No filter was applied; it is a feature of the list (F-01). |
| Same title in two years | Could be a remake or re-release | Checked: no title appears twice in the list. |
| 126 rows instead of 127 | The number the usual reader reports | The reader skips a blank line; 127 is correct (F-03). |

## Could not verify

- **Licence prices.** Nothing in the data says what any film or bundle costs to license. This is the biggest gap between the analysis and Kwame's real decision.
- **Whether the rights are available.** The data says nothing about who owns or has already sold the rights.
- **Whether budgets and revenues are complete.** The database is maintained by the public, so amounts may omit marketing costs or later income (home video, streaming, television).
- **The film behind the other-format id.** It was not matched, so it is absent.
- **How often each film is watched on a streaming service.** Box office is only a stand-in for appeal to subscribers.
- **Spot-check.** On 17 November 2026, 12 films were re-fetched live in four groups (4 random, the 2 highest and 2 lowest returns, 2 films moved to standalone, 2 closest to the year 2000). All 84 checked facts matched within the 1% tolerance set beforehand (exact match required for titles, dates, collections and directors). This shows the data was stored correctly, not that the database itself is correct.