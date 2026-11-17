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

Create a file named `.env` in the main folder with one line (needed only for fetching new data):

```
TMDB_API_KEY=your_key_here
```

## Run

```bash
python src/run_all.py --offline      # uses the saved data in data/raw; no key or internet
python src/run_all.py                # also fetches any film not yet saved
```

Read the result in `outputs/run_report.md`. If the data-quality check fails, the run stops and says why.

Separate checks:

```bash
python src/spot_check.py             # re-fetches 12 films live and compares (needs the key)
python src/timing.py                 # writes timing_report.md
```

## Using a new list

Replace `data/id_list.csv` (one column headed `tmdb_id`) and run `python src/run_all.py`. Only new films are fetched. To fetch everything again, delete `data/raw` first.

## Folders

- `data/` the id list, saved database answers (`raw`) and flattened tables (`processed`)
- `src/` the code (`run_all.py` runs it in order)
- `outputs/` tables and the run report
- `decisions/` one note per decision (ADR-001 to ADR-007)
- `data_findings.md`, `client_memo.md`, `improvement.md`, `timing_report.md`

## Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.