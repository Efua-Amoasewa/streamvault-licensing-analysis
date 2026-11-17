from pathlib import Path

import numpy as np
import pandas as pd

from analysis import POLICIES, classify, load_films

OUT_DIR = Path("outputs")
N_RESAMPLES = 10_000
SEED = 42                 # fixed, so the answer is the same every run


def bootstrap_gap(franchise, standalone, rng):
    """How big is the median gap, and could it be luck? Resample both groups with replacement."""
    f = franchise.to_numpy()
    s = standalone.to_numpy()
    f_medians = np.median(f[rng.integers(0, len(f), (N_RESAMPLES, len(f)))], axis=1)
    s_medians = np.median(s[rng.integers(0, len(s), (N_RESAMPLES, len(s)))], axis=1)
    gap = f_medians - s_medians
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