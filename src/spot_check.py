import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from analysis import CUTOFF_YEAR, classify, load_films
from fetch import BASE_URL, ENDPOINTS, TIMEOUT, make_session

OUT_DIR = Path("outputs")
SEED = 42
MONEY_TOLERANCE = 0.01     # decided BEFORE looking: money may differ by up to 1%
MONEY_FIELDS = ["budget", "revenue", "return_multiple"]
TEXT_FIELDS = ["title", "release_date", "collection_name", "directors"]   # must match exactly


def pick_sample(films):
    """About a dozen films, in four deliberate slices, so the check cannot be accused of being chosen to pass."""
    classified = classify(films, "standalone")
    random_slice = films.sample(4, random_state=SEED)
    by_return = films.dropna(subset=["return_multiple"]).sort_values("return_multiple")
    extremes = pd.concat([by_return.head(2), by_return.tail(2)])
    singles = classified.loc[classified["collection_films_in_list"] == 1].head(2)   # reclassified by ADR-002
    days_from_cutoff = (pd.to_datetime(films["release_date"]) - pd.Timestamp(f"{CUTOFF_YEAR}-01-01")).abs()
    boundary = films.loc[days_from_cutoff.nsmallest(2).index]                       # closest to the cut-off year
    sample = pd.concat([
        random_slice.assign(slice="random"),
        extremes.assign(slice="extreme return"),
        singles.assign(slice="reclassified single"),
        boundary.assign(slice=f"{CUTOFF_YEAR} boundary"),
    ])
    return sample.drop_duplicates("movie_id")


def our_values(sample, directors):
    names = directors.groupby("movie_id")["name"].agg(lambda s: "; ".join(sorted(s)))
    out = sample.assign(directors=sample["movie_id"].map(names),
                        collection_name=sample["collection_name"].fillna("(none)"))
    return out.set_index("movie_id")[["slice"] + TEXT_FIELDS + MONEY_FIELDS]


def fetch_live(session, api_key, movie_id, endpoint):
    url = BASE_URL + ENDPOINTS[endpoint][0].format(id=movie_id)
    response = session.get(url, params={"api_key": api_key}, timeout=TIMEOUT)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def live_values(session, api_key, movie_ids):
    rows = []
    for movie_id in movie_ids:
        details = fetch_live(session, api_key, movie_id, "details")
        credits = fetch_live(session, api_key, movie_id, "credits")
        crew = pd.DataFrame(credits["crew"]) if credits else pd.DataFrame(columns=["job", "name"])
        names = sorted(crew.loc[crew["job"] == "Director", "name"])
        collection = details.get("belongs_to_collection")
        rows.append({
            "movie_id": movie_id,
            "title": details["title"],
            "release_date": details["release_date"],
            "collection_name": collection["name"] if collection else "(none)",
            "directors": "; ".join(names),
            "budget": details["budget"],
            "revenue": details["revenue"],
            "return_multiple": details["revenue"] / details["budget"] if details["budget"] else float("nan"),
        })
    return pd.DataFrame(rows).set_index("movie_id")


def compare(ours, live):
    """One row per film per field. Text must match exactly; money within the stated tolerance."""
    parts = []
    for field in TEXT_FIELDS + MONEY_FIELDS:
        mine, theirs = ours[field], live.loc[ours.index, field]
        if field in MONEY_FIELDS:
            difference = (theirs - mine).astype(float)
            matches = (difference.abs() <= MONEY_TOLERANCE * mine.abs()) | (mine.isna() & theirs.isna())
        else:
            difference = pd.Series(np.nan, index=ours.index)
            matches = mine == theirs
        parts.append(pd.DataFrame({
            "movie_id": ours.index, "slice": ours["slice"].to_numpy(), "field": field,
            "ours": mine.to_numpy(), "live": theirs.to_numpy(),
            "difference": difference.to_numpy(), "match": matches.to_numpy(),
        }))
    return pd.concat(parts, ignore_index=True)


def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", 45)
    OUT_DIR.mkdir(exist_ok=True)
    load_dotenv()
    api_key = os.environ["TMDB_API_KEY"]

    films = load_films()
    directors = pd.read_csv("data/processed/directors.csv")
    sample = pick_sample(films)
    ours = our_values(sample, directors)

    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    live = live_values(make_session(), api_key, ours.index.tolist())
    report = compare(ours, live)

    checked_films = ours.index.nunique()
    mismatched = report.loc[~report["match"]]
    print(f"Checked {checked_films} films ({len(report)} field checks) live at {checked_at}.")
    print("Slices:", ", ".join(f"{k} {v}" for k, v in ours["slice"].value_counts().items()))
    print(f"{report['match'].sum()} of {len(report)} field checks matched; {len(mismatched)} differ.")
    if len(mismatched):
        print("\nDifferences found:")
        print(mismatched)
    else:
        print("No differences, so nothing here changes the recommendation.")
    report.assign(checked_at=checked_at).to_csv(OUT_DIR / "spot_check.csv", index=False)


if __name__ == "__main__":
    main()