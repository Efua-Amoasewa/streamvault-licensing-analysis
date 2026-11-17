# Run report

Run at: 2026-11-17T12:08:41+00:00
Data as of: 2026-11-17 to 2026-11-17 (when each film was fetched)
Mode: offline, saved snapshot

## Where every id went

| Stage | Rows | Delta | Reason |
|---|---|---|---|
| ids in the file | 127 |  | every line, including blanks |
| valid-looking ids | 123 | -4 | blank lines, text placeholders, other-database ids, negatives |
| unique ids to request | 117 | -6 | same id listed more than once |
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

| window | franchise_films | standalone_films | franchise_median | standalone_median | gap_low_95 | gap_high_95 | share_franchise_ahead |
|---|---|---|---|---|---|---|---|
| all years | 87 | 25 | 5.53 | 5.0 | -6.29 | 3.08 | 0.81 |
| 2000 onward | 59 | 12 | 5.05 | 4.49 | -0.58 | 2.43 | 0.82 |

## Shortlist (2000 onward)

Franchise bundles: The Lord of the Rings Collection; The Avengers Collection; Harry Potter Collection

Standalone films: Inception; Interstellar; Spirited Away; The Incredibles; Monsters, Inc.

## Changes since the last run

First run: nothing to compare with.

## Time taken (seconds)

| step | seconds |
|---|---|
| classify ids | 0.02 |
| flatten | 4.16 |
| shortlists | 0.07 |
| talent | 0.07 |
| uncertainty | 0.12 |
