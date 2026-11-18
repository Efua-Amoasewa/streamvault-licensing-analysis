from pathlib import Path

import numpy as np
import pandas as pd

import bundles
from shortlist import MIN_BUNDLE_FILMS
from analysis import CUTOFF_YEAR, POLICIES, classify, load_films

OUT_DIR = Path("outputs")
N_RESAMPLES = 10_000
BATCH = 1_000             # resamples drawn at a time, so memory stays small however many films
SEED = 42                 # fixed, so the answer is the same every run


def weighted_medians(values, weights):
    """Exact median of each resample, where weights[b, i] = how many times value i was drawn.
    Whole-array arithmetic: no loop over films or resamples."""
    order = np.argsort(values)
    v, w = values[order], weights[:, order]
    cum = w.cumsum(axis=1)
    total = cum[:, -1:]
    k_low, k_high = (total + 1) // 2, total // 2 + 1               # the two middle positions (1-based)
    lo = (cum >= k_low).argmax(axis=1)
    hi = (cum >= k_high).argmax(axis=1)
    return (v[lo] + v[hi]) / 2


def bootstrap_medians(values, clusters, rng):
    """Median of many resamples. Whole clusters are drawn with replacement, so the 8 Harry Potter
    films move together instead of counting as 8 independent results (ADR-002).
    With every value its own cluster this is the ordinary bootstrap."""
    _, cluster_index = np.unique(clusters, return_inverse=True)
    n_clusters = cluster_index.max() + 1
    pieces = []
    offsets = np.arange(BATCH)[:, None] * n_clusters
    for _ in range(N_RESAMPLES // BATCH):
        # Draw n_clusters clusters with replacement in each of BATCH resamples, then count how often each
        # was drawn (one bincount over the whole batch; ~7x faster than rng.multinomial, same distribution).
        drawn = rng.integers(0, n_clusters, size=(BATCH, n_clusters)) + offsets
        counts = np.bincount(drawn.ravel(), minlength=BATCH * n_clusters).reshape(BATCH, n_clusters)
        pieces.append(weighted_medians(values, counts[:, cluster_index]))
    return np.concatenate(pieces)


def bootstrap_gap(franchise, standalone, rng, franchise_clusters=None):
    """How big is the median gap, and could it be luck?"""
    keep = franchise.notna().to_numpy()
    f = franchise.to_numpy()[keep]
    f_clusters = (np.arange(len(f)) if franchise_clusters is None
                  else np.asarray(franchise_clusters)[keep].astype(str))
    s = standalone.dropna().to_numpy()
    gap = bootstrap_medians(f, f_clusters, rng) - bootstrap_medians(s, np.arange(len(s)), rng)
    return {
        "franchise_units": len(f),
        "standalone_films": len(s),
        "franchise_median": round(float(np.median(f)), 2),
        "standalone_median": round(float(np.median(s)), 2),
        "gap_low_95": round(float(np.percentile(gap, 2.5)), 2),
        "gap_high_95": round(float(np.percentile(gap, 97.5)), 2),
        "share_franchise_ahead": round(float((gap > 0).mean()), 2),
    }


def gap_rows(base, whole, rng):
    """Every comparison in the run: 3 policies x 2 windows x 2 ways of resampling films,
    plus whole bundle against standalone in both windows (14 in all)."""
    whole = whole.loc[whole["films_released"] >= MIN_BUNDLE_FILMS]     # the same bundles the shortlist ranks
    rows = []
    for policy in POLICIES:
        classified = classify(base, policy)
        windows = {"all years": classified,
                   "2000 onward": classified.loc[classified["release_year"] >= CUTOFF_YEAR]}
        for window_name, window in windows.items():
            fr = window.loc[window["group"] == "franchise"]
            standalone = window.loc[window["group"] == "standalone", "return_multiple"]
            clusters = fr["collection_name"].fillna(fr["movie_id"].astype(str))
            rows.append({"singles_as": policy, "window": window_name, "unit": "film",
                         "resampling": "each film independent",
                         **bootstrap_gap(fr["return_multiple"], standalone, rng)})
            rows.append({"singles_as": policy, "window": window_name, "unit": "film",
                         "resampling": "whole bundles",
                         **bootstrap_gap(fr["return_multiple"], standalone, rng, clusters)})

    # The unit Kwame actually buys: one whole bundle against one standalone film.
    classified = classify(base, "standalone")
    for window_name, from_year in {"all years": None, "2000 onward": CUTOFF_YEAR}.items():
        b = whole if from_year is None else whole.loc[whole["first_year"] >= from_year]
        films = classified if from_year is None else classified.loc[classified["release_year"] >= from_year]
        standalone = films.loc[films["group"] == "standalone", "return_multiple"]
        rows.append({"singles_as": "standalone", "window": window_name, "unit": "whole bundle",
                     "resampling": "each bundle independent",
                     **bootstrap_gap(b["whole_bundle_return"], standalone, rng)})
    return pd.DataFrame(rows)


def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    OUT_DIR.mkdir(exist_ok=True)
    base = load_films()
    whole = bundles.whole_bundle_table(bundles.build_parts(base))
    result = gap_rows(base, whole, np.random.default_rng(SEED))
    print(result)
    result.to_csv(OUT_DIR / "uncertainty.csv", index=False)


if __name__ == "__main__":
    main()
