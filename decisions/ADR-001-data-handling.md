# ADR-001: Account for every id, save every answer once, and stop the run on impossible data

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

The candidate list has defects (F-05): a blank line, text placeholders, repeats, an id from another film database and ids the database does not know. The database is a shared service for polite use only, it stores 0 when nobody entered a budget or revenue, and its franchise lists include films not yet released. Kwame needs every one of the 127 lines accounted for, and Adjoa needs to repeat the run in a meeting without the internet and without a bad record quietly changing the answer.

## Decision

I give every line one status (usable, repeat, blank, unmatched other-database id or invalid), request each usable id once and save every answer with its fetch time, so later runs read from disk. Zero money counts as missing, a franchise film counts as released only if it was out on the day its franchise list was fetched, and a check before any result stops the run on impossible data (a repeated film, the wrong film returned, a bad date, negative money, a film lost on the way, a franchise film missing from its franchise, or a released franchise film with no figures saved).

## Alternatives considered

### Alternative A: Let the standard file reader drop bad lines

- **How it would work:** Read the file with the usual reader and drop empty values.
- **Why it is attractive:** Fewer lines of code.
- **Why rejected:** It silently turns 127 lines into 126 and hides the "N/A", so Kwame's total would not reconcile with the list he gave. The other-database id would be dropped instead of being recognised as a third copy of The Dark Knight.

### Alternative B: Fetch again on every run

- **How it would work:** Call the database every time the analysis runs.
- **Why it is attractive:** Always the freshest figures.
- **Why rejected:** Needs the internet in the meeting, takes about two minutes at 500 titles at the polite pace, and the answer can change between two runs of the same list.

### Alternative C: Drop films with zero money, or fill in an estimate

- **How it would work:** Remove any film without a budget or revenue, or replace the zero with an average.
- **Why it is attractive:** Keeps the maths simple, or keeps every film in it.
- **Why rejected:** Dropping hides a real title from the counts; an estimate invents data that then looks real. Today no film on the list is affected, so neither choice would change the recommendation, but a 500-title list probably will have some.

### Alternative D: Judge "released" against today's date

- **How it would work:** Count a franchise film if its release date is before the day the analysis runs.
- **Why it is attractive:** Picks up new releases automatically.
- **Why rejected:** The saved franchise lists include Avengers: Doomsday (16 December 2026). From that day an offline rerun would count it with no figures, and Avengers would quietly become "incomplete" with nothing in the data changed.

### Alternative E: Keep the last copy of a repeated id

- **How it would work:** Keep the final occurrence instead of the first.
- **Why it is attractive:** None in particular; it is the other obvious default.
- **Why rejected:** Copies are the same film with identical answers, so the result is identical. I keep the first because it is simpler to explain.

## Consequences

- **What this buys:** A full reconciliation (127 lines → 124 valid-looking → 117 unique → 112 films → 112 with usable figures), a first run of 234 film requests plus 1 id lookup and 71 franchise requests, a second run of 0, an offline mode for meetings, and results that do not change unless the saved data does.
- **What this costs:** The saved data goes out of date; each answer carries its fetch date and the run report prints the range. New releases enter only when the franchise lists are fetched again.
- **What it costs the client if I am wrong:** Figures edited in the database after 17–18 November are not reflected, and Toy Story 5 (2026), still in cinemas, will move Toy Story's figure when refetched.
- **What would make me revisit this:** A need for fresher figures (delete `data/raw` and run online), or several data warnings in a row on a new list.

## What this survives

At about 500 titles Adjoa replaces the id file and runs the analysis. Only new ids are requested (about 1,000 requests, roughly two minutes), every id still lands in a category, the run report lists new and removed films, and the checks still stop the run on impossible data. I tested a made-up zero-budget film (flagged, excluded, no crash), a made-up repeated film and a copy with the franchise figures deleted (both stop the run with a clear message).
