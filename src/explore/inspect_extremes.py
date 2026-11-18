import pandas as pd

films = pd.read_csv(
    "data/processed/films.csv",
    dtype={"movie_id": "int64", "requested_id": "int64", "collection_id": "Int64"},
)
films = films.assign(
    release_year=pd.to_datetime(films["release_date"]).dt.year,
    return_multiple=films["revenue"] / films["budget"],
    collection_films_in_list=films.groupby("collection_name")["movie_id"].transform("size"),
)

cols = ["movie_id", "title", "release_year", "budget", "revenue", "return_multiple"]

print("=== lowest return multiples ===")
print(films.nsmallest(8, "return_multiple")[cols])

print("\n=== highest return multiples ===")
print(films.nlargest(8, "return_multiple")[cols])

q1, q3 = films["return_multiple"].quantile([0.25, 0.75])
spread = q3 - q1
outside = (films["return_multiple"] > q3 + 1.5 * spread) | (films["return_multiple"] < q1 - 1.5 * spread)
print("\nreturn multiple: median", round(films["return_multiple"].median(), 2),
      "| mean", round(films["return_multiple"].mean(), 2),
      "| flagged by the IQR rule:", outside.sum())
print("films earning less than their budget:", (films["revenue"] < films["budget"]).sum())

print("\n=== same title, any year (possible re-release or remake) ===")
same_title = films["title"].str.strip().str.casefold().duplicated(keep=False)
print(films.loc[same_title, ["movie_id", "title", "release_year"]].sort_values("title"))

print("\n=== non-English films ===")
print(films.loc[films["original_language"] != "en", ["movie_id", "title", "release_year", "original_language"]])

print("\n=== five oldest films ===")
print(films.sort_values("release_date").head(5)[["movie_id", "title", "release_date"]])

print("\n=== in a collection, but alone in our list ===")
alone = films["collection_films_in_list"] == 1
print(films.loc[alone, ["movie_id", "title", "release_year", "collection_name"]])