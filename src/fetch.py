import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.themoviedb.org/3"
RAW_DIR = Path("data/raw")
TIMEOUT = (3.05, 10)        # connect timeout, read timeout (seconds)
PAUSE_SECONDS = 0.1         # be gentle: pause between live requests

# Which URL each kind of data comes from.
ENDPOINTS = {
    "details": "/movie/{id}",
    "credits": "/movie/{id}/credits",
}


def make_session():
    """A session that identifies itself and retries only temporary failures."""
    session = requests.Session()
    session.headers["User-Agent"] = "streamvault-licensing-analysis (educational project)"
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],   # temporary problems only
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch_one(session, api_key, movie_id, endpoint):
    """Get one response, from disk if we already have it.

    Returns (record, from_cache). The record holds status_code,
    fetched_at (UTC) and payload (the JSON, or None for a 404).
    """
    path = RAW_DIR / endpoint / f"{movie_id}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8")), True

    url = BASE_URL + ENDPOINTS[endpoint].format(id=movie_id)
    response = session.get(url, params={"api_key": api_key}, timeout=TIMEOUT)

    if response.status_code == 404:
        payload = None                 # the film doesn't exist: record it, don't crash
    else:
        response.raise_for_status()    # anything else unexpected stops the run loudly
        payload = response.json()

    record = {
        "movie_id": movie_id,
        "endpoint": endpoint,
        "status_code": response.status_code,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")
    time.sleep(PAUSE_SECONDS)
    return record, False


def main():
    load_dotenv()
    api_key = os.environ["TMDB_API_KEY"]

    ids = pd.read_csv("data/ids_classified.csv", dtype=str, keep_default_na=False)
    usable = ids.loc[ids["status"] == "usable", "tmdb_id"].tolist()
    assert len(usable) > 0, "no usable ids to fetch"
    session = make_session()
    manifest = []
    requests_made = 0

    for movie_id in usable:
        for endpoint in ENDPOINTS:
            record, from_cache = fetch_one(session, api_key, movie_id, endpoint)
            requests_made += 0 if from_cache else 1
            manifest.append({
                "movie_id": movie_id,
                "endpoint": endpoint,
                "status_code": record["status_code"],
                "fetched_at": record["fetched_at"],
            })

    manifest = pd.DataFrame(manifest)
    manifest.to_csv(RAW_DIR / "manifest.csv", index=False)

    print("live requests made this run:", requests_made)
    print(manifest.groupby("endpoint")["status_code"].value_counts())
    assert len(manifest) == 2 * len(usable), "a fetch went missing"


if __name__ == "__main__":
    main()