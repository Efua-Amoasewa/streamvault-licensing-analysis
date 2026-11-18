from pathlib import Path

import numpy as np
import pandas as pd

import bundles
from analysis import CUTOFF_YEAR, classify, load_films

OUT_DIR = Path("outputs")
MIN_BUNDLE_FILMS = 3      # a bundle must have at least this many released films to be ranked (ADR-003)


def add_score(table, columns):
    """Average of the percentile ranks on each column (0 = worst, 1 = best)."""
    ranks = table[columns].rank(pct=True)
    return table.assign(score=ranks.mean(axis=1).round(3))


def load_whole_bundles():
    return bundles.whole_bundle_table(bundles.load_parts())


def bundle_table(whole, from_year=None, min_films=MIN_BUNDLE_FILMS):
    """One row per franchise bundle, valued WHOLE (every released film, on the list or not).

    A window never cuts a bundle in half: with from_year set, only bundles whose every film
    was released in or after that year are ranked (ADR-002)."""
    table = whole.loc[whole["films_released"] >= min_films]
    if from_year is not None:
        table = table.loc[table["first_year"] >= from_year]
    table = add_score(table, ["whole_bundle_return", "whole_weakest_film_return", "median_rating"])
    return table.sort_values("score", ascending=False).round(2)


def standalone_table(films, parts=None):
    """One row per standalone film, scored on return, revenue and rating.
    Flags films whose franchise has other released films: they may only be sold as a bundle."""
    alone = films.loc[(films["group"] == "standalone") & films["return_multiple"].notna()].assign(
        budget_m=lambda d: d["budget"] / 1_000_000)
    table = alone[["movie_id", "title", "release_year", "budget_m", "revenue_m",
                   "return_multiple", "vote_average", "collection_id"]]
    released_in_series = (parts.groupby("collection_id")["movie_id"].size()
                          if parts is not None and len(parts) else pd.Series(dtype="int64"))
    table = table.assign(other_films_in_series=(table["collection_id"].map(released_in_series) - 1)
                         .fillna(0).astype(int)).drop(columns="collection_id")
    table = add_score(table, ["return_multiple", "revenue_m", "vote_average"])
    return table.sort_values("score", ascending=False).round(2)


def ranking_alternatives(whole, modern_standalones):
    """What the shortlist would be under the rejected ranking rules (ADR-003)."""
    b = bundle_table(whole, CUTOFF_YEAR)
    s = modern_standalones
    rows = {
        "chosen: average of percentile ranks": (list(b.index[:3]), list(s["title"][:5])),
        "rejected A: return only": (list(b.sort_values("whole_bundle_return", ascending=False).index[:3]),
                                    list(s.sort_values("return_multiple", ascending=False)["title"][:5])),
        "rejected B: 50% return, 25% each other": (
            list(b.assign(w=b[["whole_bundle_return", "whole_weakest_film_return", "median_rating"]]
                          .rank(pct=True).to_numpy() @ np.array([.5, .25, .25]))
                 .sort_values("w", ascending=False).index[:3]),
            list(s.assign(w=s[["return_multiple", "revenue_m", "vote_average"]]
                          .rank(pct=True).to_numpy() @ np.array([.5, .25, .25]))
                 .sort_values("w", ascending=False)["title"][:5])),
    }
    return pd.DataFrame([{"rule": k, "bundles": "; ".join(v[0]), "standalones": "; ".join(v[1])}
                         for k, v in rows.items()])


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
    films = classify(load_films(), "standalone")                  # decision: ADR-002
    modern = films.loc[films["release_year"] >= CUTOFF_YEAR]      # decision: ADR-002
    parts = bundles.load_parts()
    whole = bundles.whole_bundle_table(parts)

    bundles_modern = bundle_table(whole, CUTOFF_YEAR)
    bundles_all = bundle_table(whole)
    stand_modern = standalone_table(modern, parts)
    alternatives = ranking_alternatives(whole, stand_modern)

    print("=== whole franchise bundles, every film from 2000 onward (shortlist = top 3) ===")
    print(bundles_modern.drop(columns="not_on_list"))
    print("\n=== whole franchise bundles, all years ===")
    print(bundles_all.drop(columns="not_on_list"))
    print("\n=== standalone films, 2000 onward (shortlist = top 5) ===")
    print(stand_modern)
    print("\n=== shortlist under the rejected ranking rules ===")
    print(alternatives.to_string(index=False))
    print("\n=== are the middle films of a bundle weaker? (all years | 2000 onward) ===")
    print(entry_position(films))
    print(entry_position(modern))

    bundles_modern.to_csv(OUT_DIR / "bundles_2000_onward.csv")
    bundles_all.to_csv(OUT_DIR / "bundles_all_years.csv")
    stand_modern.to_csv(OUT_DIR / "standalones_2000_onward.csv", index=False)
    alternatives.to_csv(OUT_DIR / "shortlist_under_alternatives.csv", index=False)


if __name__ == "__main__":
    main()
