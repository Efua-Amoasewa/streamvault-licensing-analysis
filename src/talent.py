from pathlib import Path

import pandas as pd

from analysis import classify, load_films

OUT_DIR = Path("outputs")
MIN_TALENT_FILMS = 3      # a person needs at least this many films to be judged
MIN_SERIES = 2            # ...across at least this many separate series/titles
HIT_RATE_BAR = 0.75       # share of their films that must beat the list's median return


def talent_table(films, people):
    """One row per person: how often their films beat the window's median return."""
    people = people.loc[people["movie_id"].isin(films["movie_id"])]
    baseline = films["return_multiple"].median()
    films = films.assign(series=films["collection_name"].fillna(films["title"]))
    joined = people.merge(films[["movie_id", "return_multiple", "series"]],
                          on="movie_id", how="inner", validate="many_to_one")
    assert len(joined) == len(people), "a person-film row lost its film"
    joined = joined.assign(hit=joined["return_multiple"] > baseline)
    table = joined.groupby(["person_id", "name"]).agg(
        films=("movie_id", "nunique"),
        series=("series", "nunique"),
        hit_rate=("hit", "mean"),
        median_return=("return_multiple", "median"),
    )
    table = table.loc[table["films"] >= MIN_TALENT_FILMS]
    table = table.assign(
        reliable=(table["series"] >= MIN_SERIES) & (table["hit_rate"] >= HIT_RATE_BAR)
    ).round(2)
    return table.sort_values(["reliable", "hit_rate", "films"], ascending=False).reset_index().drop(columns="person_id")


def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    OUT_DIR.mkdir(exist_ok=True)

    films = classify(load_films(), "standalone")
    windows = {"all_years": films, "2000_onward": films.loc[films["release_year"] >= 2000]}

    directors = pd.read_csv("data/processed/directors.csv")
    cast = pd.read_csv("data/processed/cast.csv")
    leads = cast.loc[cast["order"] == 0, ["movie_id", "person_id", "name"]]
    assert leads["movie_id"].is_unique, "a film has two top-billed actors"
    roles = {"directors": directors, "lead_actors": leads}

    for window_name, window in windows.items():
        for role_name, people in roles.items():
            table = talent_table(window, people)
            print(f"\n=== {role_name} with {MIN_TALENT_FILMS}+ films | {window_name} ===")
            print(table.head(12))
            table.to_csv(OUT_DIR / f"talent_{role_name}_{window_name}.csv", index=False)


if __name__ == "__main__":
    main()