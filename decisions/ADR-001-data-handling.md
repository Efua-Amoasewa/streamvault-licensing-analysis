# ADR-001: Account for every id, save every answer once, treat zero money as missing, and stop on impossible data

- **Status:** Accepted
- **Date:** 2026-11-18
- **Decision owner:** Esther Acquandoh

## Context

The candidate list has defects (F-05), the database is a shared service for polite use only, and it stores 0 when nobody entered a budget or revenue. Kwame needs a full account of the 127 lines, and Adjoa needs to repeat the run without calling the database again and without a bad record quietly changing the answer.

## Decision 1: Every line gets a status, and every answer is saved once

Read every line as text and give it one status: usable, repeat, blank, unmatched other-database id, or invalid. An id from another film database ("tt...") is looked up through the database's own matching service and replaced by the id it matches; if that film is already on the list it is a repeat (this is what happened: it is The Dark Knight). Ids written "0155" or "155.0" count as "155". The first copy of a repeated id is kept; which copy does not matter, because every answer for the same id is identical.

Request each usable id once, wait a tenth of a second between requests, retry only temporary errors (honouring the database's "wait" instruction), never retry "not found", and save each raw answer to disk with the time it was fetched. Every saved answer is listed in `data/raw/manifest.csv`.

**Alternatives rejected**

- **Let the standard file reader drop bad lines.** Fewer lines of code, but it silently turns 127 lines into 126 and hides the "N/A". Kwame would get a total that does not reconcile with the list he gave.
- **Fetch again on every run.** Always fresh, but slower, needs the internet in the meeting, and results can change between two runs of the same list.

## Decision 2: Zero money means "missing"; impossible data stops the run

A film with zero budget or revenue is still counted as a title but left out of every return calculation. A set of checks runs before any result is produced. Impossible problems stop the run with a message saying what to fix: a repeated film, the wrong film returned, an implausible date, negative money, a film lost between fetching and analysis, a franchise film on the list missing from its franchise, or a released franchise film with no figures saved. Softer problems (missing money, cast or director, an unreleased film) are reported as warnings.

**Alternatives rejected**

- **Drop films without money.** Simple, but the film's title, cast and franchise are still real, and dropping it hides it from the counts.
- **Replace zero with an estimate** such as the average budget. Keeps every film in the maths, but invents data that then looks real.

## Consequences

- **What this buys:** A full reconciliation (127 lines → 124 valid-looking → 117 unique → 112 films → 112 with usable figures), no infinite returns, a first run of 234 film requests plus 1 id lookup and 71 whole-franchise requests, a second run of 0, and an offline mode for meetings.
- **What this costs:** The saved data goes out of date; each answer carries its fetch date and the run report prints the range. The gate's thresholds are my judgement.
- **What it costs the client if I am wrong:** Amounts edited in the database after 17–18 November are not reflected. A film whose zero is a real zero would be wrongly excluded, which does not happen for released films.
- **What would make me revisit this:** A need for fresher figures (delete `data/raw` and fetch again), or several warnings in a row on a new list.

## What this survives

At about 500 titles Adjoa replaces the id file and runs the analysis. Only new ids are requested (about 1,000 requests, roughly two minutes at the polite pace). Every id still lands in a category, the run report lists new and removed films, and the gate still stops on impossible data. I tested a made-up zero-budget film (flagged, excluded, no crash), a made-up repeated film, and a copy with the franchise figures deleted (both stop the run with a clear message).
