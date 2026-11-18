import json
from pathlib import Path

import numpy as np
import pandas as pd

FIND_DIR = Path("data/raw/find")      # cached answers for other-database (IMDb) ids


def resolved_other_ids():
    """{IMDb id: TMDb id} from cached lookups. An id the database can't match maps to ''."""
    mapping = {}
    for path in FIND_DIR.glob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        matches = (record["payload"] or {}).get("movie_results", [])
        mapping[record["movie_id"]] = str(matches[0]["id"]) if len(matches) == 1 else ""
    return mapping


def classify_ids(path="data/id_list.csv"):
    """Read the candidate list as text and label every row: usable, duplicate or why it was rejected."""
    raw = pd.read_csv(
        path,
        dtype=str,
        keep_default_na=False,     # keep "N/A" as text instead of turning it into a missing value
        skip_blank_lines=False,    # keep blank lines as rows so we can count them
    )
    raw_value = raw.iloc[:, 0].str.strip()

    # "0155" or "155.0" (what a spreadsheet edit leaves behind) is the same film as "155"
    number = raw_value.str.extract(r"^0*(\d+)(?:\.0+)?$")[0]
    is_imdb_id = raw_value.str.fullmatch(r"tt\d+")
    lookup = resolved_other_ids()
    resolved = raw_value.map(lookup).where(is_imdb_id)
    tmdb_id = number.fillna(resolved.replace("", np.nan))     # an IMDb id becomes its TMDb id once looked up

    is_blank = raw_value == ""
    unresolved_imdb = is_imdb_id & tmdb_id.isna()
    is_valid = tmdb_id.notna() & (tmdb_id != "0")
    is_repeat = is_valid & tmdb_id.duplicated(keep="first")

    status = np.select(
        [is_blank, unresolved_imdb, ~is_valid, is_repeat],
        ["blank", "imdb_id", "invalid_other", "duplicate"],
        default="usable",
    )
    note = np.select(
        [is_imdb_id & is_repeat, is_imdb_id & ~is_repeat & is_valid],
        ["other-database id; same film as an id already on the list",
         "other-database id; looked up and replaced by its id here"],
        default="",
    )
    result = pd.DataFrame({"raw_value": raw_value, "tmdb_id": tmdb_id.fillna(""),
                           "status": status, "note": note})
    assert result["status"].value_counts().sum() == len(raw), "statuses don't add up to the rows read"
    return result


def main():
    result = classify_ids()
    print("rows read:", len(result))
    print(result["status"].value_counts())
    result.to_csv("data/ids_classified.csv", index=False)


if __name__ == "__main__":
    main()
