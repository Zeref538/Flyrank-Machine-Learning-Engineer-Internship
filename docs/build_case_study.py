"""Build docs/index.html (the case study, the site's front page) from docs/case-study.src.html and the committed results.

    python docs/build_case_study.py

The charts and tables are drawn from the numbers injected here, and every number
the prose quotes is checked against the result files. A re-run with new results
that disagree with the copy fails the build instead of publishing a stale claim.

Prose lives in case-study.src.html. Measurements live in work/outputs/*.json.
Edit the source, never index.html. The paper is docs/paper.html.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
RES = ROOT / "work" / "outputs"


def load(name: str):
    return json.loads((RES / name).read_text(encoding="utf-8"))


def signed(x: float, nd: int) -> str:
    """How the page writes a signed number: +0.14, &minus;0.26."""
    return ("+" if x >= 0 else "&minus;") + f"{abs(x):.{nd}f}"


def main():
    cap = load("capstone_metrics.json")
    sweep = load("capstone_leak_sweep.json")
    gates = load("capstone_gate_sensitivity.json")
    play = load("w07_playbook_metrics.json")
    w05 = load("w05_model_metrics.json")
    did = load("w08_did_metrics.json")

    res = {r["method"]: r for r in cap["results"]}
    data = {
        "baseRate": cap["base_rate"],
        "cleanAuc": cap["roc_auc_clean"],
        "results": cap["results"],
        "model": {"p50": res["gradient_boosting"]["P_at_50"]},
        "rule": {"p50": res["hand-written rule"]["P_at_50"]},
        "boot": cap["bootstrap"],
        "arch": cap["archetype_counts"],
        # column names and scores only: the schema is public, the rows are not
        "sweep": [{k: r[k] for k in ("column", "auc", "lift", "control")} for r in sweep],
        "did": {"treated": did["three_window_treated"], "control": did["three_window_control"]},
    }

    html = (DOCS / "case-study.src.html").read_text(encoding="utf-8")
    assert html.count("/*%%DATA%%*/") == 1, "data placeholder missing or duplicated"
    html = html.replace("/*%%DATA%%*/", json.dumps(data, separators=(",", ":")))

    check_privacy(html)
    check(html, cap, sweep, gates, play, w05, did)

    out = DOCS / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")


def check_privacy(html: str):
    """No pseudonymised ID from the data may reach the public page (DATA_USE.md rule 3)."""
    ids = set()
    with open(ROOT / "data" / "raw" / "content_refresh_anonymized.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ids.add(row["client_id"])
            ids.add(row["content_id"])
    hits = sum(1 for i in ids if i in html)  # count only: never print an ID
    assert hits == 0, f"{hits} client/content IDs appear on the page"
    assert not re.search(r"\b(client|content)_[0-9a-z]{8,}\b", html), "an ID-shaped string is on the page"
    print(f"  privacy: none of {len(ids):,} IDs on the page")


def check(html, cap, sweep, gates, play, w05, did):
    """Fail loudly rather than publish a number the results do not support."""
    b = cap["bootstrap"]
    res = {r["method"]: r for r in cap["results"]}
    model, rule = res["gradient_boosting"]["P_at_50"], res["hand-written rule"]["P_at_50"]

    # The headline is a non-result. If a re-run separates the two, the page is wrong.
    assert b["difference_ci_includes_zero"], "model now beats the rule: rewrite the headline"
    assert did["placebo_did_ci95"][1] < 0, "placebo interval no longer entirely below zero"
    assert did["treated_recovery_pct_of_baseline"] < 100, "treated pages now end above baseline"

    rows = 0
    clients = set()
    with open(ROOT / "data" / "raw" / "content_refresh_anonymized.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows += 1
            clients.add(row["client_id"])

    controls = [r["lift"] for r in sweep if r["control"]]
    by_col = {r["column"]: r for r in sweep}
    diffs = [g["diff"] for g in gates]
    decay = int(re.search(r"median (\d+) distinct", play["decay_insight"]).group(1))

    claims = [
        (f"{rows:,} pseudonymised pages from {len(clients)} clients", "dataset size"),
        (f"{cap['eligible_pages']:,} pages", "eligible pages"),
        (f"{cap['eligible_clients']} clients", "eligible clients"),
        (f"{cap['held_out_pages']:,} held-out pages", "held-out pages"),
        (f"{cap['base_rate']:.3f}", "base rate"),
        (f"<dd>{model:.2f}</dd>", "model P@50"),
        (f"<dd>{rule:.2f}</dd>", "rule P@50"),
        (signed(round(model - rule, 2), 2), "model minus rule"),
        (f"{signed(b['model_minus_rule_ci95'][0], 2)} to {signed(b['model_minus_rule_ci95'][1], 2)}", "gap CI"),
        (f"from {b['model_p50_ci95'][0]:.2f} to {b['model_p50_ci95'][1]:.2f}", "model CI"),
        (f"{b['resamples_model_ahead']:.0%}", "resamples model ahead"),
        # the paper's band: w05's tie-break sweep (capstone.ipynb re-measured 0.76-0.90, also inside)
        (f"between {w05['baseline_p50_tie_range'][0]:.2f} and {w05['baseline_p50_tie_range'][1]:.2f}", "tie band"),
        (f"led in {w05['splits_gb_beats_rule']}", "splits model led"),
        (f"{w05['mean_margin_over_8_splits']:.3f}", "mean margin"),
        (f">{cap['roc_auc_random_split']:.3f}<", "random-split AUC"),
        (f">{cap['roc_auc_clean']:.3f}<", "clean AUC"),
        (f"<b>{cap['roc_auc_with_hidden_leak']:.3f}</b>", "hidden-leak AUC"),
        (signed(cap["hidden_leak_cost"], 3), "hidden-leak cost"),
        (signed(min(controls), 3), "control lift"),
        (f"clicks_last_30d</code> ({signed(by_col['clicks_last_30d']['lift'], 3)})", "missed column"),
        (f"<b>{cap['archetype_counts']['zero_click_ghost']}</b> of", "zero-click pages"),
        (f"<b>{cap['top50_blocked_zero_click']}</b> of the top 50", "zero-click in top 50"),
        (f"<b>{play['review_status_counts']['ready for writer']:,}</b>", "ready for writer"),
        (f"<b>{play['review_status_counts']['needs an analyst look first']:,}</b>", "analyst first"),
        (f"{play['precision_at_k']['200']:.3f} at K = 200", "P@200"),
        (f"{play['precision_at_k']['200']:.1%}", "P@200 as percent"),
        (f"from {gates[0]['eligible']:,} pages to {gates[-1]['eligible']:,}", "gate pool"),
        (f"between {signed(min(diffs), 3)} and {signed(max(diffs), 3)}", "gate gap range"),
        (f"median of {decay} distinct", "decay column"),
        (f"{did['pages_treated']:,} eligible pages", "treated pages"),
        (f">{signed(did['naive_did_clicks'], 2)}<", "naive DiD"),
        (f">{signed(did['matched_did_clicks'], 2)}<", "matched DiD"),
        (f"{signed(did['matched_did_ci95'][0], 2)} to {signed(did['matched_did_ci95'][1], 2)}", "matched CI"),
        (f"<b>{signed(did['placebo_did_clicks'], 2)}</b>", "placebo DiD"),
        (f"{signed(did['placebo_did_ci95'][0], 2)} to {signed(did['placebo_did_ci95'][1], 2)}", "placebo CI"),
        (f"p = {did['placebo_p_value']:.3f}", "placebo p"),
        (f"<b>{did['treated_recovery_pct_of_baseline']:.0f}%</b>", "recovery"),
    ]
    missing = [f"{label} = {text!r}" for text, label in claims if text not in html]
    assert not missing, "page does not state:\n  " + "\n  ".join(missing)
    print(f"  checked {len(claims)} claims against work/outputs and the data")


if __name__ == "__main__":
    main()
