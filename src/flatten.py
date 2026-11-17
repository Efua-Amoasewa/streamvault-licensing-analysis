import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")


def load_payloads(endpoint):
    """Read every cached file for one endpoint; keep only real films (not 404s).

    Each payload gets two extra fields: the id we REQUESTED, and when we fetched it.
    """
    payloads = []
    for path in sorted((RAW_DIR / endpoint).glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["payload"] is None:          # a 404: no film, nothing to flatten
            continue
        payloads.append({
            **record["payload"],
            "requested_id": int(record["movie_id"]),
            "fetched_at": record["fetched_at"],
        })
    return payloads


def build_films(details):
    """One row per film."""
    films = pd.json_normalize(details, sep="_", max_level=1)
    films = films.rename(columns={
        "id": "movie_id",
        "belongs_to_collection_id": "collection_id",
        "belongs_to_collection_name": "collection_name",
    })
    keep = ["movie_id", "requested_id", "title", "release_date", "budget", "revenue",
            "runtime", "vote_average", "vote_count", "original_language", "status",
            "collection_id", "collection_name", "fetched_at"]
    return films[keep]


def build_cast(credits):
    """One row per film per cast member."""
    cast = pd.json_normalize(credits, record_path="cast", meta=["id"], meta_prefix="film_")
    cast = cast.rename(columns={"id": "person_id", "film_id": "movie_id"})
    return cast[["movie_id", "person_id", "name", "order", "character"]]


def build_directors(credits):
    """One row per film per director."""
    crew = pd.json_normalize(credits, record_path="crew", meta=["id"], meta_prefix="film_")
    crew = crew.rename(columns={"id": "person_id", "film_id": "movie_id"})
    is_director = crew["job"] == "Director"
    return crew.loc[is_director, ["movie_id", "person_id", "name"]]


def main():
    details = load_payloads("details")
    credits = load_payloads("credits")

    films = build_films(details)
    cast = build_cast(credits)
    directors = build_directors(credits)

    # Checks: every claim about the data is a line of code.
    assert len(films) == 112, f"expected 112 films, got {len(films)}"
    assert films["movie_id"].is_unique, "duplicate film in films table"
    assert (films["movie_id"] == films["requested_id"]).all(), "TMDb returned a different id than we asked for"
    assert set(cast["movie_id"]) <= set(films["movie_id"]), "cast for an unknown film"

    print("films     :", len(films), "rows,", films["movie_id"].nunique(), "films")
    print("cast      :", len(cast), "rows,", cast["movie_id"].nunique(), "films")
    print("directors :", len(directors), "rows,", directors["movie_id"].nunique(), "films")
    print("films with no cast rows     :", len(films) - cast["movie_id"].nunique())
    print("films with no director rows :", len(films) - directors["movie_id"].nunique())
    print("films in a collection       :", films["collection_id"].notna().sum())
    print("films with no collection    :", films["collection_id"].isna().sum())

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    films.to_csv(OUT_DIR / "films.csv", index=False)
    cast.to_csv(OUT_DIR / "cast.csv", index=False)
    directors.to_csv(OUT_DIR / "directors.csv", index=False)


if __name__ == "__main__":
    main()