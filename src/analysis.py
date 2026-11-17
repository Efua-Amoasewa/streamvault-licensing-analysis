import numpy as np
import pandas as pd

POLICIES = ["standalone", "franchise", "exclude"]   # what to call collections alone in our list


def load_films():
    films = pd.read_csv(
        "data/processed/films.csv",
        dtype={"movie_id": "int64", "requested_id": "int64", "collection_id": "Int64"},
    )
    return films.assign(
        release_year=pd.to_datetime(films["release_date"]).dt.year,
        return_multiple=(films["revenue"] / films["budget"]).where((films["budget"] > 0) & (films["revenue"] > 0)),        revenue_m=films["revenue"] / 1_000_000,
        collection_films_in_list=films.groupby("collection_name")["movie_id"].transform("size"),
    )


def classify(films, singles_as):
    """Add a 'group' column. A collection with 2+ films in our list is a bundle.
    One alone in our list is treated according to singles_as."""
    in_list = films["collection_films_in_list"].fillna(0)      # 0 = no collection at all
    group = np.select(
        [in_list >= 2, in_list == 1],
        ["franchise", {"standalone": "standalone", "franchise": "franchise", "exclude": "excluded"}[singles_as]],
        default="standalone",
    )
    return films.assign(group=group, is_pre2000=films["release_year"] < 2000)


def kpi_table(films):
    """One row per group. Every statistic sits next to the number of films behind it."""
    films = films.loc[films["group"] != "excluded"]
    return films.groupby("group").agg(
        titles=("movie_id", "nunique"),
        usable=("return_multiple", "count"),
        median_return=("return_multiple", "median"),
        mean_return=("return_multiple", "mean"),
        median_revenue_m=("revenue_m", "median"),
        pre2000_share=("is_pre2000", "mean"),
    ).round(2)


def main():
    films = load_films()
    
    for policy in POLICIES:
        classified = classify(films, policy)
        windows = {"all years": classified,
                   "2000 onward": classified.loc[classified["release_year"] >= 2000]}
        for window_name, window in windows.items():
            print(f"\n--- singles as {policy!r} | {window_name} ---")
            print(kpi_table(window))


if __name__ == "__main__":
    main()