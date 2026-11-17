import numpy as np
import pandas as pd


def classify_ids(path="data/id_list.csv"):
    """Read the candidate list as text and label every row: usable, duplicate or why it was rejected."""
    raw = pd.read_csv(
        path,
        dtype=str,
        keep_default_na=False,     # keep "N/A" as text instead of turning it into a missing value
        skip_blank_lines=False,    # keep blank lines as rows so we can count them
    )
    cleaned = raw.iloc[:, 0].str.strip()

    is_blank = cleaned == ""
    is_imdb_id = cleaned.str.fullmatch(r"tt\d+")
    is_digits = cleaned.str.fullmatch(r"\d+")
    is_repeat = is_digits & cleaned.duplicated(keep="first")

    status = np.select(
        [is_blank, is_imdb_id, ~is_digits, is_repeat],
        ["blank", "imdb_id", "invalid_other", "duplicate"],
        default="usable",
    )
    result = pd.DataFrame({"tmdb_id": cleaned, "status": status})
    assert result["status"].value_counts().sum() == len(raw), "statuses don't add up to the rows read"
    return result


def main():
    result = classify_ids()
    print("rows read:", len(result))
    print(result["status"].value_counts())
    result.to_csv("data/ids_classified.csv", index=False)


if __name__ == "__main__":
    main()