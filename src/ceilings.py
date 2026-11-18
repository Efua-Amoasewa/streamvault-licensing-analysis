"""Walk-away price ceilings: how much of the budget each shortlisted title is worth
RELATIVE to everything else on the shortlist (ADR-003).

There are no licence prices in the data, so this cannot say what a title costs. It says
what share of the money each title's box-office evidence can justify, so a negotiator knows
when a quoted price is out of line with the rest of the shortlist.

Value unit = one typical standalone film (the median standalone return, 2000 onward).
- A bundle is all-or-none, so it is valued conservatively: number of films with figures x its
  WEAKEST film's return, in standalone units. A film with no figures adds no value. You pay for every film, including the worst.
- A standalone is bought on its own: its own return, in standalone units.
"""
from pathlib import Path

import pandas as pd

import bundles
import shortlist
from analysis import CUTOFF_YEAR, classify, load_films

OUT_DIR = Path("outputs")
BUDGET_M = 14.0            # the board's licensing budget, $M
N_BUNDLES, N_STANDALONES = 3, 5


def ceiling_table(budget_m=BUDGET_M):
    films = classify(load_films(), "standalone")
    modern = films.loc[films["release_year"] >= CUTOFF_YEAR]
    parts = bundles.load_parts()
    whole = bundles.whole_bundle_table(parts)
    unit = modern.loc[modern["group"] == "standalone", "return_multiple"].median()

    b = shortlist.bundle_table(whole, CUTOFF_YEAR).head(N_BUNDLES)
    s = shortlist.standalone_table(modern, parts).head(N_STANDALONES)
    rows = pd.concat([
        pd.DataFrame({"title": b.index, "kind": "bundle", "films": b["films_with_money"].to_numpy(),
                      "driving_return": b["whole_weakest_film_return"].to_numpy(),
                      "value_units": (b["films_with_money"] * b["whole_weakest_film_return"] / unit).to_numpy()}),
        pd.DataFrame({"title": s["title"].to_numpy(), "kind": "standalone", "films": 1,
                      "driving_return": s["return_multiple"].to_numpy(),
                      "value_units": (s["return_multiple"] / unit).to_numpy()}),
    ], ignore_index=True)
    rows = rows.assign(per_film_vs_typical_standalone=rows["driving_return"] / unit,
                       share_of_budget=rows["value_units"] / rows["value_units"].sum())
    rows = rows.assign(ceiling_m=rows["share_of_budget"] * budget_m)
    return rows.round(2), round(float(unit), 2)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    table, unit = ceiling_table()
    print(f"one value unit = a typical standalone film since {CUTOFF_YEAR}, returning {unit}x")
    print(table.to_string(index=False))
    print(table.groupby("kind")[["share_of_budget", "ceiling_m"]].sum())
    table.to_csv(OUT_DIR / "price_ceilings.csv", index=False)


if __name__ == "__main__":
    main()
