# Memo to Kwame

**From:** Esther Acquandoh
**Date:** 17 November 2026
**Subject:** Franchise bundles or standalone hits for the $14M licensing budget

## What I found

Franchise bundles probably give a better return than standalone films, but the data does not prove it. The typical franchise film returned 5.5 times its budget at the box office, against 5.0 for standalone films. Looking only at films released since 2000 it is 5.1 against 4.5. When I reshuffled the data 10,000 times, franchises came out ahead about 8 times in 10, but the plausible gap includes zero.

Averages tell a different story when old films are included: standalone films average 10.5 times and franchises 7.9. Over half the standalone films date from before 2000, including Jaws (67 times) and Star Wars (70 times), so I used the middle film instead.

Directors and lead actors are not a reason to buy. None met my test of 3+ films, in at least 2 series, with 75% beating the typical film. Peter Jackson's films beat the typical film half the time; Christopher Nolan's 29%.

## What I built

| What you asked for | Status | Evidence |
|---|---|---|
| Check of the film list | Done | 127 lines became 112 films; every line accounted for in `data_findings.md` |
| Analysis for both time periods | Done | One command reruns it; results in `outputs/run_report.md` |
| Reasons for each decision | Done | Seven notes in `decisions/` |
| Speed target of 5 seconds | Met | Under 0.25 seconds at 500 films, 1.4 seconds at 5,000 |
| One improvement | Done | Automatic data check and run report (`improvement.md`) |

## What I recommend

Lead with franchise bundles from 2000 onward and keep a smaller standalone allocation as a hedge.

**Bundles:** *The Lord of the Rings* (three films, 11.0 times its cost, rated 8.5), *The Avengers* (four films, 7.1 times, rated 8.2) and *Harry Potter* (eight films, 6.1 times, the biggest library, with all eight films above 3.7 times).

**Standalones:** *Inception* (5.2 times, rated 8.4), *Interstellar* (4.5 times, rated 8.5), *Spirited Away* (14.5 times on a $19M budget), *The Incredibles* (6.9 times) and *Monsters, Inc.* (5.0 times). The last two have sequels you may be able to license with them.

**Deal note, *The Lord of the Rings*:** the three films cost $266M to make and earned $2.92 billion. The number that drove this choice is **9.37 times**, the return of the weakest film (*The Fellowship of the Ring*). It is higher than the typical film in either group, so the bundle does not depend on picking the right film.

## What I could not stand behind

- **Licence prices.** I have box-office figures, not what these rights cost. A bundle that returns 11 times at the cinema may cost far more to license; check prices before committing the $14M.
- **Availability.** I do not know whether any of these rights are for sale.
- **Best-case numbers.** Every film in the list earned more than it cost, so the list is made of hits.
- **Old money.** Amounts are not adjusted for inflation and show box-office, not profit.
- **Small groups.** Only 12 standalone films since 2000.
- **Missing films.** 5 ids are unknown to the database, 4 were invalid, 6 were repeats and one film is missing because its id used another database's format.
- **Check against the source.** A live check of 12 films (84 facts) found no differences. Data is as of 17 November 2026.