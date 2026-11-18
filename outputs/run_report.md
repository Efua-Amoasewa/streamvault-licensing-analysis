# Run report

Run at: 2026-11-18T13:05:34+00:00
Data as of: 2026-11-17 to 2026-11-17 (when each film was fetched)
Mode: offline, saved snapshot

## Where every id went

| Stage | Rows | Delta | Reason |
|---|---|---|---|
| ids in the file | 127 |  | every line, including blanks |
| valid-looking ids | 124 | -3 | blank lines, text placeholders, negatives, unmatched other-database ids (1 other-database id(s) looked up and kept) |
| unique ids to request | 117 | -7 | same film listed more than once (including via another database's id) |
| films found in the database | 112 | -5 | ids the database does not know |
| films with usable return figures | 112 | 0 | zero or missing budget or revenue |

## Data quality gate

| check | films_affected | result | meaning |
|---|---|---|---|
| film ids are unique | 0 | pass | the same film appears twice, so every total would be inflated |
| film returned is the film asked for | 0 | pass | the database answered with a different id than we requested |
| release dates are real and plausible | 0 | pass | a film cannot be placed in a time window |
| money is never negative | 0 | pass | impossible budget or revenue |
| films fetched match films analysed | 0 | pass | a film was lost between fetching and analysis |
| every franchise film is found in its whole bundle | 0 | pass | a bundle would be valued without a film we know is in it; fetch the bundle lists (online run) |
| budget and revenue both entered | 0 | pass | zero means 'nobody entered a figure'; excluded from return metrics, still counted as titles |
| every film has cast listed | 0 | pass | missing from the lead-actor read |
| every film has a director listed | 0 | pass | missing from the director read |
| every film is marked Released | 0 | pass | an unreleased film has no real revenue |

## Franchise vs standalone: median return per film (return = revenue / budget)

All years:

| group | titles | usable | median_return | mean_return | median_revenue_m | pre2000_share |
|---|---|---|---|---|---|---|
| franchise | 87 | 87 | 5.53 | 7.94 | 618.64 | 0.32 |
| standalone | 25 | 25 | 5.0 | 10.48 | 291.46 | 0.52 |

2000 onward:

| group | titles | usable | median_return | mean_return | median_revenue_m | pre2000_share |
|---|---|---|---|---|---|---|
| franchise | 59 | 59 | 5.05 | 5.45 | 795.92 | 0.0 |
| standalone | 12 | 12 | 4.49 | 4.89 | 450.09 | 0.0 |

## How sure are we (10,000 resamples; 'ahead' = share of resamples where franchise median is higher)

Per film, resampling whole bundles so a series' films move together; and per whole bundle (the unit actually bought).

| window | unit | franchise_units | standalone_films | franchise_median | standalone_median | gap_low_95 | gap_high_95 | share_franchise_ahead |
|---|---|---|---|---|---|---|---|---|
| all years | film | 87 | 25 | 5.53 | 5.0 | -6.24 | 3.16 | 0.78 |
| 2000 onward | film | 59 | 12 | 5.05 | 4.49 | -0.68 | 2.73 | 0.8 |
| all years | whole bundle | 23 | 25 | 4.49 | 5.0 | -6.77 | 2.38 | 0.4 |
| 2000 onward | whole bundle | 12 | 12 | 5.02 | 4.49 | -0.95 | 2.83 | 0.74 |

## Bundles on the list that are not complete (valued whole, including the films not on the list)

| collection_name | films_on_list | films_released | whole_bundle_return | not_on_list |
|---|---|---|---|---|
| Die Hard Collection | 4 | 5 | 3.68 | A Good Day to Die Hard |
| Ice Age Collection | 3 | 6 | 7.5 | Ice Age: Continental Drift; Ice Age: Collision Course; The Ice Age Adventures of Buck Wild |
| Indiana Jones Collection | 4 | 5 | 4.13 | Indiana Jones and the Dial of Destiny |
| Jurassic Park Collection | 3 | 7 | 4.97 | Jurassic World; Jurassic World: Fallen Kingdom; Jurassic World Dominion; Jurassic World Rebirth |
| Mission: Impossible Collection | 5 | 8 | 3.3 | Mission: Impossible - Fallout; Mission: Impossible - The Final Reckoning; Mission: Impossible - Dead Reckoning Part One |
| Star Wars Collection | 6 | 9 | 6.17 | Star Wars: The Force Awakens; Star Wars: The Rise of Skywalker; Star Wars: The Last Jedi |
| The Bourne Collection | 3 | 5 | 3.6 | The Bourne Legacy; Jason Bourne |
| The Matrix Collection | 3 | 4 | 3.23 | The Matrix Resurrections |
| The Terminator Collection | 4 | 6 | 2.48 | Terminator Genisys; Terminator: Dark Fate |
| Toy Story Collection | 4 | 5 | 5.62 | Toy Story 5 |

## Shortlist (every film from 2000 onward)

Franchise bundles: The Lord of the Rings Collection; The Avengers Collection; Harry Potter Collection

Standalone films: Inception; Interstellar; Spirited Away; The Incredibles; Monsters, Inc.

## Walk-away ceilings relative to the shortlist (1 unit = a typical standalone, 4.49x)

| title | kind | films | driving_return | value_units | per_film_vs_typical_standalone | share_of_budget | ceiling_m |
|---|---|---|---|---|---|---|---|
| The Lord of the Rings Collection | bundle | 3 | 9.37 | 6.26 | 2.09 | 0.24 | 3.33 |
| The Avengers Collection | bundle | 4 | 5.98 | 5.33 | 1.33 | 0.2 | 2.84 |
| Harry Potter Collection | bundle | 8 | 3.74 | 6.67 | 0.83 | 0.25 | 3.55 |
| Inception | standalone | 1 | 5.24 | 1.17 | 1.17 | 0.04 | 0.62 |
| Interstellar | standalone | 1 | 4.52 | 1.01 | 1.01 | 0.04 | 0.54 |
| Spirited Away | standalone | 1 | 14.47 | 3.22 | 3.22 | 0.12 | 1.72 |
| The Incredibles | standalone | 1 | 6.86 | 1.53 | 1.53 | 0.06 | 0.81 |
| Monsters, Inc. | standalone | 1 | 5.0 | 1.11 | 1.11 | 0.04 | 0.59 |

## Changes since the last run

0 new films, 0 films no longer on the list. New ids: []; gone: []

## Time taken (seconds)

| step | seconds |
|---|---|
| classify ids | 0.01 |
| flatten | 0.49 |
| whole bundles | 0.12 |
| shortlists | 0.15 |
| talent | 0.07 |
| uncertainty | 0.78 |
| price ceilings | 0.06 |
| whole run (wall clock) | 1.98 |
