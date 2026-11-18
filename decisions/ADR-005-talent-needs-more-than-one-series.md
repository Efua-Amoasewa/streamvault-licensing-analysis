# ADR-005: Call a director or lead actor a reliable signal only with 3+ films across 2+ series and a 75% hit rate

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

Kwame asked which directors and lead actors reliably signal a title worth licensing, because his negotiators use talent as a lever. A person's films often share a franchise, so a good run may just be the franchise: Elijah Wood's three films are all The Lord of the Rings.

## Decision

I take the first-billed cast member as the lead and count a film as a hit when its return beats the window's middle film. A person is a reliable signal only with at least 3 films, in at least 2 separate series, and a hit rate of 75% or more.

## Alternatives considered

### Alternative A: Hit rate alone

- **How it would work:** Rank people by the share of their films that beat the typical film.
- **Why it is attractive:** Simple.
- **Why rejected:** It crowns Elijah Wood (3 of 3) and Ray Romano (3 of 3), who each appear in one series. That measures the franchise, not the person.

### Alternative B: A lower bar of two in three

- **How it would work:** A 67% hit rate instead of 75%.
- **Why it is attractive:** More names for negotiators.
- **Why rejected:** From 2000 onward it adds only Robert Downey Jr. (5 of 7 across 2 series, 71%), whose films are almost all one connected Marvel universe; one film either way changes his verdict.

### Alternative C: A fixed hit bar such as 3x

- **How it would work:** A hit is any film returning more than three times its budget.
- **Why it is attractive:** An absolute, easy-to-say bar.
- **Why rejected:** On this hits-only list (F-01) 95 of 112 films return more than 3x, so almost everyone would pass and the test would not separate anyone.

### Alternative D: The top three billed as leads

- **How it would work:** Credit each film to its first three cast members.
- **Why it is attractive:** Captures ensemble films.
- **Why rejected:** Blurs the person with the ensemble and multiplies franchise effects (every Lord of the Rings actor would inherit the trilogy's record).

## Consequences

- **What this buys:** A test that separates the person from the franchise. Across all years Steven Spielberg (8 films, 4 series, 88%), Robert Zemeckis (4 films, 2 series, 100%) and Tom Hanks (5 films, 2 series, 80%) pass, but on 1975–1997 films or, for Hanks, mostly Toy Story. From 2000 onward nobody passes: Christopher Nolan has 7 films across 5 series and only 29% beat the typical film; Peter Jackson 50%. Talent is not a reason to pay more for a recent title; the useful lever is refusing a premium for a name.
- **What this costs:** Very few people can pass in 112 films, and a person whose films are all solid but not above the middle is called unreliable.
- **What it costs the client if I am wrong:** A genuinely bankable name is overlooked, or a film led by an ensemble is credited to one name.
- **What would make me revisit this:** A larger list where more people have films across several series.

## What this survives

The talent tables for both windows are recomputed on every run. At about 500 titles more people will qualify and the same rule applies; the thresholds (`MIN_TALENT_FILMS`, `MIN_SERIES`, `HIT_RATE_BAR`) are named settings at the top of `src/talent.py`.
