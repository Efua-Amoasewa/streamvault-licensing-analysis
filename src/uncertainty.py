from pathlib import Path

import numpy as np
import pandas as pd

from analysis import POLICIES, classify, load_films

OUT_DIR = Path("outputs")
N_RESAMPLES = 10_000
BATCH = 1_000             # resamples drawn at a time, so memory stays small however many films
SEED = 42                 # fixed, so the answer is the same every run


def bootstrap_medians(values, rng):
    """Median of many resamples (with replacement), drawn in batches to limit memory."""
    pieces = []
    for _ in range(N_RESAMPLES // BATCH):
        picks = rng.integers(0, len(values), (BATCH, len(values)))
        pieces.append(np.median(values[picks], axis=1))
    return np.concatenate(pieces)


def bootstrap_gap(franchise, standalone, rng):
    """How big is the median gap, and could it be luck?"""
    f = franchise.dropna().to_numpy()       # films with no usable return figure are left out
    s = standalone.dropna().to_numpy()
    gap = bootstrap_medians(f, rng) - bootstrap_medians(s, rng)
    return {
        "franchise_films": len(f),
        "standalone_films": len(s),
        "franchise_median": round(float(np.median(f)), 2),
        "standalone_median": round(float(np.median(s)), 2),
        "gap_low_95": round(float(np.percentile(gap, 2.5)), 2),
        "gap_high_95": round(float(np.percentile(gap, 97.5)), 2),
        "share_franchise_ahead": round(float((gap > 0).mean()), 2),
    }


def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    OUT_DIR.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)
    base = load_films()

    rows = []
    for policy in POLICIES:
        classified = classify(base, policy)
        windows = {"all years": classified,
                   "2000 onward": classified.loc[classified["release_year"] >= 2000]}
        for window_name, window in windows.items():
            franchise = window.loc[window["group"] == "franchise", "return_multiple"]
            standalone = window.loc[window["group"] == "standalone", "return_multiple"]
            rows.append({"singles_as": policy, "window": window_name,
                         **bootstrap_gap(franchise, standalone, rng)})

    result = pd.DataFrame(rows)
    print(result)
    result.to_csv(OUT_DIR / "uncertainty.csv", index=False)


if __name__ == "__main__":
    main()