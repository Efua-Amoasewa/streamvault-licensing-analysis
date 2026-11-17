import numpy as np
import pandas as pd

# Read everything as text and don't let pandas hide anything.
raw = pd.read_csv(
    "data/id_list.csv",
    dtype=str,
    keep_default_na=False,
    skip_blank_lines=False,
)
assert len(raw) == 127, f"expected 127 rows, got {len(raw)}"

# Step 1: remove stray spaces around each value.
cleaned = raw["tmdb_id"].str.strip()

# Step 2: build named True/False columns, one per rule.
is_blank = cleaned == ""
is_imdb_id = cleaned.str.fullmatch(r"tt\d+")
is_digits = cleaned.str.fullmatch(r"\d+")
is_repeat = is_digits & cleaned.duplicated(keep="first")

# Step 3: give each row one status. The first matching rule wins.
raw["status"] = np.select(
    [is_blank, is_imdb_id, ~is_digits, is_repeat],
    ["blank", "imdb_id", "invalid_other", "duplicate"],
    default="usable",
)

# Step 4: count and reconcile.
counts = raw["status"].value_counts()
print(counts)
assert counts.sum() == 127, "statuses don't add up to the rows read"

# Step 5: save the result so the next stage can use it.
raw["tmdb_id"] = cleaned
raw.to_csv("data/ids_classified.csv", index=False)