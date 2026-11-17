# ADR-001: Treat a film whose collection has no other film in our list as a standalone

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decision owner:** Esther Acquandoh

## Context

Nine films (such as Jaws and The Incredibles) belong to a collection in the database, but only one film from that collection is in our list. Kwame must choose between bundles and standalone films, so every film needs a group. These nine could go either way.

## Decision

A franchise bundle needs at least two films from the same collection in our list. A film that is alone in our list counts as a standalone.

## Alternatives considered

### Alternative A: Count them as franchise

- **How it would work:** Any film that belongs to a collection is franchise.
- **Why it is attractive:** Matches how the database labels films.
- **Why rejected:** We can only judge a bundle from the films we can see. A "bundle" of one film is not a bundle.

### Alternative B: Leave the nine out

- **How it would work:** Drop them from both groups.
- **Why it is attractive:** Keeps the groups clean.
- **Why rejected:** Throws away nine real films and shrinks the standalone group to 16.

## Consequences

- **What this buys:** A simple rule that can be explained in one sentence, and a standalone group of 25.
- **What this costs:** Two shortlisted standalones (The Incredibles, Monsters Inc.) have sequels in the market.
- **What it costs the client if I am wrong:** The standalone group is a little more mixed, which makes the comparison slightly more favourable to standalone films.
- **What would make me revisit this:** If a bigger list contains more films from these collections, they become real bundles automatically.

## What this survives

I ran all three options. Franchise films are ahead in 81–95% of resamples in every case, so the direction does not depend on this choice, only the strength. At about 500 titles Adjoa can rerun the analysis unchanged; the rule reads the collection counts from the data each time.