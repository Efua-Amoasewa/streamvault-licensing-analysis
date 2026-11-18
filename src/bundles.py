"""Whole bundles: a franchise is sold all-or-none, so value it with every released film in it,
not only the films that happen to be on the candidate list."""
import json
from pathlib import Path

import pandas as pd

from analysis import load_films

RAW_DIR = Path("data/raw")
OUT = Path("data/processed/bundle_parts.csv")


def _records(endpoint):
    for path in sorted((RAW_DIR / endpoint).glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["payload"] is not None:
            yield record


def _payloads(endpoint):
    for record in _records(endpoint):
        yield record["payload"]


def build_parts(films):
    """One row per released film per collection, with money from the list or from the extra fetch.

    "Released" means released by the day the franchise list was fetched, not by today: the saved
    answers then give the same result on every rerun, and a film that comes out later is picked up
    only when the list is fetched again (with its figures). Judged against today, a saved list would
    start counting a new film with no figures the day it opens."""
    rows = [{"collection_id": c["payload"]["id"], "collection_name": c["payload"]["name"], "movie_id": p["id"],
             "title": p["title"], "release_date": p.get("release_date") or "",
             "list_fetched_on": c["fetched_at"][:10]}
            for c in _records("collection") for p in c["payload"].get("parts", [])]
    if not rows:
        return pd.DataFrame(columns=["collection_id", "collection_name", "movie_id", "title", "release_date",
                                     "list_fetched_on", "on_list", "budget", "revenue", "vote_average",
                                     "release_year"])
    parts = pd.DataFrame(rows)
    parts = parts.loc[(parts["release_date"] != "") & (parts["release_date"] <= parts["list_fetched_on"])]

    fields = ["movie_id", "budget", "revenue", "vote_average"]
    extra = pd.DataFrame([{"movie_id": d["id"], "budget": d["budget"], "revenue": d["revenue"],
                           "vote_average": d["vote_average"]} for d in _payloads("collection_parts")], columns=fields)
    money = pd.concat([films[fields], extra], ignore_index=True)
    assert money["movie_id"].is_unique, "a film has two money records"
    parts = parts.merge(money, on="movie_id", how="left", validate="many_to_one")
    return parts.assign(on_list=parts["movie_id"].isin(films["movie_id"]),
                        release_year=pd.to_datetime(parts["release_date"]).dt.year)


def load_parts():
    """The table build_parts wrote, read once from one file instead of re-reading every saved answer."""
    return pd.read_csv(OUT)


def whole_bundle_table(parts, min_on_list=2):
    """One row per collection with 2+ films on the list: what you'd actually be buying."""
    has_money = (parts["budget"] > 0) & (parts["revenue"] > 0)
    p = parts.assign(budget_ok=parts["budget"].where(has_money), revenue_ok=parts["revenue"].where(has_money),
                     film_return=(parts["revenue"] / parts["budget"]).where(has_money),
                     missing_title=parts["title"].where(~parts["on_list"]))
    table = p.groupby("collection_name").agg(
        films_released=("movie_id", "nunique"),
        films_on_list=("on_list", "sum"),
        films_with_money=("film_return", "count"),
        first_year=("release_year", "min"),
        last_year=("release_year", "max"),
        whole_budget_m=("budget_ok", "sum"),
        whole_revenue_m=("revenue_ok", "sum"),
        whole_median_film_return=("film_return", "median"),
        whole_weakest_film_return=("film_return", "min"),
        median_rating=("vote_average", "median"),
        not_on_list=("missing_title", lambda s: "; ".join(s.dropna())),
    )
    table = table.loc[table["films_on_list"] >= min_on_list]
    table = table.assign(whole_budget_m=table["whole_budget_m"] / 1e6,
                         whole_revenue_m=table["whole_revenue_m"] / 1e6,
                         whole_bundle_return=table["whole_revenue_m"] / table["whole_budget_m"],
                         complete=table["films_on_list"] == table["films_released"])
    return table.round(2)


def main():
    films = load_films()
    parts = build_parts(films)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    parts.to_csv(OUT, index=False)
    table = whole_bundle_table(parts)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    print(table.drop(columns="not_on_list"))
    print(table["not_on_list"])


if __name__ == "__main__":
    main()
