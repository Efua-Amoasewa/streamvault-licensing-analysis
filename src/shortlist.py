from pathlib import Path

import numpy as np
import pandas as pd

from analysis import classify, load_films

OUT_DIR = Path("outputs")
MIN_BUNDLE_FILMS = 3      # a "bundle" must have at least this many films in the window


def add_score(table, columns):
    """Average of the percentile ranks on each column (0 = worst, 1 = best)."""
    ranks = table[columns].rank(pct=True)
    return table.assign(score=ranks.mean(axis=1).round(3))


def bundle_table(films, min_films=MIN_BUNDLE_FILMS):
    """One row per franchise bundle (collection)."""
    bundles = films.loc[films["group"] == "franchise"].assign(budget_m=lambda d: d["budget"] / 1_000_000)
    bundles = bundles.sort_values("return_multiple")           # so 'first' below = weakest film
    table = bundles.groupby("collection_name").agg(
        films=("movie_id", "nunique"),
        first_year=("release_year", "min"),
        last_year=("release_year", "max"),
        total_revenue_m=("revenue_m", "sum"),
        total_budget_m=("budget_m", "sum"),
        median_film_return=("return_multiple", "median"),
        weakest_film_return=("return_multiple", "min"),
        weakest_film=("title", "first"),
        median_rating=("vote_average", "median"),
    )
    table = table.loc[table["films"] >= min_films]
    table = table.assign(bundle_return=table["total_revenue_m"] / table["total_budget_m"])
    table = add_score(table, ["bundle_return", "weakest_film_return", "median_rating"])
    return table.sort_values("score", ascending=False).round(2)


def standalone_table(films):
    """One row per standalone film, scored on return, revenue and rating."""
    alone = films.loc[films["group"] == "standalone"].assign(budget_m=lambda d: d["budget"] / 1_000_000)
    table = alone[["movie_id", "title", "release_year", "budget_m", "revenue_m",
                   "return_multiple", "vote_average"]]
    table = add_score(table, ["return_multiple", "revenue_m", "vote_average"])
    return table.sort_values("score", ascending=False).round(2)


def entry_position(films):
    """Do the middle films of a bundle return less than the first and last?"""
    f = films.loc[films["group"] == "franchise"].sort_values(["collection_name", "release_date"])
    f = f.assign(
        n=f.groupby("collection_name")["movie_id"].transform("size"),
        pos=f.groupby("collection_name").cumcount(),
    )
    f = f.loc[f["n"] >= 3]
    f = f.assign(
        entry=np.select([f["pos"] == 0, f["pos"] == f["n"] - 1], ["first", "last"], default="middle"),
        vs_bundle_median=f["return_multiple"] / f.groupby("collection_name")["return_multiple"].transform("median"),
    )
    return f.groupby("entry").agg(
        films=("movie_id", "count"),
        median_return=("return_multiple", "median"),
        median_vs_own_bundle=("vs_bundle_median", "median"),
    ).round(2)


def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    OUT_DIR.mkdir(exist_ok=True)
    films = classify(load_films(), "standalone")          # decision: ADR-001
    modern = films.loc[films["release_year"] >= 2000]     # decision: ADR-002

    print("=== franchise bundles, 2000 onward (shortlist = top 3) ===")
    bundles_modern = bundle_table(modern)
    print(bundles_modern)
    print("\n=== franchise bundles, all years (for comparison) ===")
    bundles_all = bundle_table(films)
    print(bundles_all.head(8))

    print("\n=== standalone films, 2000 onward (shortlist = top 5) ===")
    stand_modern = standalone_table(modern)
    print(stand_modern)
    print("\n=== standalone films, all years (top 8, for comparison) ===")
    print(standalone_table(films).head(8))

    print("\n=== are the middle films of a bundle weaker? (all years, then 2000 onward) ===")
    print(entry_position(films))
    print(entry_position(modern))

    bundles_modern.to_csv(OUT_DIR / "bundles_2000_onward.csv")
    bundles_all.to_csv(OUT_DIR / "bundles_all_years.csv")
    stand_modern.to_csv(OUT_DIR / "standalones_2000_onward.csv", index=False)


if __name__ == "__main__":
    main()