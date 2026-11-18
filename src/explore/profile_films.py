import pandas as pd

# Read with explicit types. collection_id has gaps (standalones), so a plain
# integer type would turn it into decimals; "Int64" is the integer that allows gaps.
films = pd.read_csv(
    "data/processed/films.csv",
    dtype={"movie_id": "int64", "requested_id": "int64", "collection_id": "Int64"},
)
directors = pd.read_csv("data/processed/directors.csv")

dates = pd.to_datetime(films["release_date"], errors="coerce")
films = films.assign(release_year=dates.dt.year)

print("=== shape and types ===")
print(films.shape)
print(films.dtypes)

print("\n=== missing values per column ===")
nulls = films.isna().sum()
print(pd.DataFrame({"missing": nulls, "percent": (nulls / len(films) * 100).round(1)}))

print("\n=== zeros that probably mean 'nobody entered a number' ===")
money_cols = ["budget", "revenue", "runtime", "vote_count"]
print((films[money_cols] == 0).sum())

print("\n=== suspiciously tiny money values (1 to 9,999) ===")
tiny = films["budget"].between(1, 9_999) | films["revenue"].between(1, 9_999)
print(films.loc[tiny, ["movie_id", "title", "release_year", "budget", "revenue"]])

print("\n=== numeric summary ===")
print(films[["budget", "revenue", "runtime", "vote_average", "vote_count"]].describe().round(1))

print("\n=== dates ===")
print("missing or unparseable:", dates.isna().sum())
print("earliest:", dates.min().date(), " latest:", dates.max().date())
print("before 2000:", (films["release_year"] < 2000).sum(),
      "| 2000 onward:", (films["release_year"] >= 2000).sum())

print("\n=== categories (including blanks) ===")
print(films["status"].value_counts(dropna=False))
print(films["original_language"].value_counts(dropna=False))

print("\n=== possible duplicate films (same title and year) ===")
key = films["title"].str.strip().str.casefold() + "|" + films["release_year"].astype(str)
suspects = films.loc[key.duplicated(keep=False), ["movie_id", "title", "release_date"]]
print(suspects.sort_values("title"))

print("\n=== collection sizes (how many films from each collection are in our list) ===")
sizes = films.groupby("collection_name").size()    # standalones are excluded on purpose here
print(sizes.value_counts().sort_index().rename("collections"))
print(sizes.sort_values(ascending=False).head(15))

print("\n=== directors per film ===")
per_film = directors.groupby("movie_id").size()
print((per_film > 1).sum(), "films have more than one director")