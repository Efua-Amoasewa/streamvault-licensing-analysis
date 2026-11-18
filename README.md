# StreamVault licensing analysis

Compares franchise bundles with standalone films for a $14M licensing budget, using film data from a public database.

## Setup

```bash
git clone <this repository>
cd streamvault-licensing-analysis
python -m venv .venv
source .venv/Scripts/activate        # Git Bash on Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

To fetch new data, copy `.env.example` to `.env` and put your TMDb key in it:

```
TMDB_API_KEY=your_key_here
```

## Run

```bash
python src/run_all.py --offline      # uses the saved data in data/raw; no key or internet
python src/run_all.py                # also fetches any film, id lookup or franchise list not yet saved
```

Read the result in `outputs/run_report.md`: where every id went, the data check, both time windows (per film and per whole franchise), how sure we are, incomplete franchises, the shortlist and the walk-away price ceilings. If the data check fails, the run stops and says why.

Separate checks:

```bash
python src/spot_check.py             # re-fetches 12 films live and compares (needs the key)
python src/timing.py                 # rebuilds 112- and 500-film copies, times cold and warm full runs, writes timing_report.md
```

## Using a new list

Replace `data/id_list.csv` (one column headed `tmdb_id`) and run `python src/run_all.py`. Only new films are fetched (about two minutes for 500 new films); do it before a meeting, then use `--offline` in the meeting. To fetch everything again, delete `data/raw` first. Settings such as the cut-off year (`CUTOFF_YEAR` in `src/analysis.py`) and the bundle and talent thresholds sit at the top of their files.

## Folders

- `data/` the id list, saved database answers (`raw`: film details, credits, id lookups, franchise lists, figures for franchise films not on the list) and flattened tables (`processed`)
- `src/` the code (`run_all.py` runs it in order); `src/explore/` holds the one-off profiling scripts used to find the data problems
- `outputs/` tables and the run report
- `decisions/` five decision notes (ADR-001 to ADR-005); related calls share a note
- `data_findings.md`, `client_memo.md`, `improvement.md`, `timing_report.md`

## Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.
