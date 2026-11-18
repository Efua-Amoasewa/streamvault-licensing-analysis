# Improvement beyond the brief: value bundles as they are sold, and give negotiators a walk-away ceiling

## The problem it solves

Two gaps sat between the analysis and the room Kwame's negotiators walk into.

1. **Bundles were valued on the films that happened to be on the list.** Studios sell a franchise all-or-none, but 10 of the 23 franchises on the list are missing released films, usually the later, weaker sequels. Valued on the list alone, Star Wars looked like 10.8x; as a studio would actually sell it, it is 6.2x. A negotiator quoting the list figure would overpay, and would be told so by the studio's own numbers.
2. **The brief asks what to pay, and the data has no prices.** A ranking says which title is better, not when to walk away.

## What I built

- **Whole-bundle check** (`src/bundles.py`). For every franchise on the list, the run fetches the franchise's full film list and the figures for released films not on the list (71 extra requests, made once and saved). Every bundle is ranked on the whole franchise, and the run report lists each incomplete franchise and the films it is missing. A rule in the data check stops the run if a franchise film on the list is not found in its franchise.
- **Walk-away ceiling sheet** (`src/ceilings.py`). Every shortlisted title is valued in one unit, a typical recent standalone film. Bundles are valued conservatively on their weakest film, because you pay for all of them. Each title's share of the $14M becomes its ceiling (ADR-010). It is printed in the run report and saved as a table negotiators can take into the room.

Both run inside the one-command run (`python src/run_all.py`). Like everything else they are recomputed from the data, so next quarter's list gets new ceilings with no extra work.

## What it is worth to Kwame and Adjoa

- **Kwame gets a number to negotiate against**: for example "walk away from The Lord of the Rings above about $3.3M, roughly twice the per-film price of a typical standalone". He also gets a budget split ($9.7M franchises, $4.3M standalones) that the board can see follows from the evidence.
- **It changed the advice.** Valued whole, the typical franchise does *worse* than a standalone across all years and only slightly better since 2000. The recommendation moved from "franchises as a category" to "these three franchises". That is exactly the kind of overreach the board remembers from the trilogy two years ago.
- **Adjoa can answer "is that the whole series?"** live in a meeting from the run report, instead of looking it up.
- **Last quarter's passed five-film bundle can now be judged.** Add its ids to the list and the report will show whether it was complete and what it would have been worth relative to the shortlist.

## What it cost

About half a day and 140 lines of code. A first online run makes 71 extra requests (about 15 seconds at the polite pace); after that, none. The ceilings inherit every limit of box-office return (hits-only list, nominal money, no viewing data). They are relative limits, not market prices, and the memo says so.
