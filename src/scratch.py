import pandas as pd

m = pd.read_csv("data/raw/manifest.csv", dtype={"movie_id": str})
print(m.loc[m["status_code"] == 404, ["movie_id", "endpoint"]])