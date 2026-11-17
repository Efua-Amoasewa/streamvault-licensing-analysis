# Improvement beyond the brief: one-command run with a data-quality check

## The problem it solves

The analysis was several separate steps, run in a set order, with nothing to stop bad data from reaching the numbers. Kwame's team will rerun it on a list of about 500 titles. A bigger list will contain a film with a zero budget, a repeated film or an unknown id. Without a check, those produce a wrong number that looks like a right one. I found this while designing it: a single zero budget would have turned one film's return into an infinite value.

## What I built

- **One command** (`python src/run_all.py`) that runs every step in order. An offline option uses the saved data, so no key or internet is needed.
- **A data-quality check** with nine rules. Five stop the run (repeated film, wrong film returned, impossible date, negative money, film lost on the way). Four only warn (missing money, cast, director, not yet released). Every rule prints how many films it affects.
- **A run report** (`outputs/run_report.md`) with where every id went (127 → 123 → 117 → 112), the check results, both time windows, the uncertainty ranges, the shortlist, the time each step took and which films are new or removed since the last run.
- **Zero money treated as missing** (ADR-006).

I tested the stop and the warning on made-up data: a repeated film halted the run with a clear message, and a zero budget was flagged and excluded without a crash.

## What it is worth to Kwame

- Anyone can rerun the whole analysis safely, with a one-page record of what happened.
- A bad list cannot silently produce a confident wrong answer.
- Adjoa's rerun at about 500 titles needs no knowledge of the individual steps.

## What it cost

One working session to build and test, about 190 lines of code. A full offline run takes about 4 seconds, mostly reading and reshaping the saved files. The cost to maintain is that the rules reflect my judgement of what is impossible; a new kind of problem needs a new rule.