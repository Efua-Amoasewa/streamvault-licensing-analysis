from datetime import date
import pandas as pd


def run_checks(films, directors, cast, manifest, parts):
    dates = pd.to_datetime(films["release_date"], errors="coerce")
    in_collection = films.loc[films["collection_id"].notna()]
    missing_from_bundle = int((~in_collection["movie_id"].isin(parts["movie_id"])).sum())
    no_record = int(parts["budget"].isna().sum())
    parts_no_money = int((~parts["on_list"] & ((parts["budget"] <= 0) | (parts["revenue"] <= 0))).sum())
    details_ok = int(((manifest["endpoint"] == "details") & (manifest["status_code"] == 200)).sum())
    rules = [
        ("film ids are unique", int(films["movie_id"].duplicated().sum()), "FAIL", "the same film appears twice, so every total would be inflated"),
        ("film returned is the film asked for", int((films["movie_id"] != films["requested_id"]).sum()), "FAIL", "the database answered with a different id than we requested"),
        ("release dates are real and plausible", int((dates.isna() | (dates.dt.year < 1900) | (dates.dt.year > date.today().year)).sum()), "FAIL", "a film cannot be placed in a time window"),
        ("money is never negative", int(((films["budget"] < 0) | (films["revenue"] < 0)).sum()), "FAIL", "impossible budget or revenue"),
        ("films fetched match films analysed", abs(details_ok - len(films)), "FAIL", "a film was lost between fetching and analysis"),
        ("every franchise film is found in its whole bundle", missing_from_bundle, "FAIL", "a bundle would be valued without a film we know is in it; fetch the bundle lists (online run)"),
        ("every released franchise film has a figures record", no_record, "FAIL", "a bundle would be valued only on the films that happen to be on the list; fetch the bundle figures (online run)"),
        ("budget and revenue both entered", int(((films["budget"] <= 0) | (films["revenue"] <= 0)).sum()), "WARN", "zero means 'nobody entered a figure'; excluded from return metrics, still counted as titles"),
        ("franchise films not on the list have budget and revenue", parts_no_money, "WARN", "left out of their bundle's value; the bundle is valued on its films with figures"),
        ("every film has cast listed", int((~films["movie_id"].isin(cast["movie_id"])).sum()), "WARN", "missing from the lead-actor read"),
        ("every film has a director listed", int((~films["movie_id"].isin(directors["movie_id"])).sum()), "WARN", "missing from the director read"),
        ("every film is marked Released", int((films["status"] != "Released").sum()), "WARN", "an unreleased film has no real revenue"),
    ]
    return pd.DataFrame([
        {"check": n, "films_affected": b, "result": "pass" if b == 0 else s, "meaning": m}
        for n, b, s, m in rules
    ])


def enforce(checks):
    failed = checks.loc[checks["result"] == "FAIL"]
    if len(failed):
        lines = [f"  - {r.check}: {r.films_affected} affected ({r.meaning})" for r in failed.itertuples()]
        raise SystemExit("DATA QUALITY GATE FAILED. Fix the data, then run again:\n" + "\n".join(lines))