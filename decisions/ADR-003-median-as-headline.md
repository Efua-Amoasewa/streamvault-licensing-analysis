# ADR-003: Use the median film, not the average, as the headline measure

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

Return multiple (revenue divided by budget) has a long tail. The average is 8.5x while the middle film is 5.37x; 11 films are flagged as unusually high.

## Decision

Report the median (the middle film) as the headline and show the average beside it as a warning.

## Alternatives considered

### Alternative A: Average return

- **How it would work:** Add all returns and divide.
- **Why it is attractive:** Familiar; uses every value fully.
- **Why rejected:** A handful of 1970s hits set the answer. In the all-years window the average gives standalone films 10.5x against 7.9x for franchises, the opposite of the median.

## Consequences

- **What this buys:** A number that one film cannot move much.
- **What this costs:** Ignores how large the best hits are, which matters to a buyer who wants a blockbuster.
- **What it costs the client if I am wrong:** If hits are what pay for the library, the median understates the value of high-variance films.
- **What would make me revisit this:** A list with licence prices, where the question becomes profit across the whole portfolio.

## What this survives

At about 500 titles the median becomes more stable and the gap between median and average should narrow. Adjoa can compare the two in the run report, which prints both.