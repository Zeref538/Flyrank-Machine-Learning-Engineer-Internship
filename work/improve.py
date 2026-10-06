"""Can anything beat the five-line rule? One change per run, scored against the rule on the same folds.

The capstone judged everything on ONE split: 9 held-out clients. Clients range from 0% to 97%
declining, and one holds 35% of the pages, so a single split mostly measures which clients
landed in test. This harness tests every client instead: 5-fold GroupKFold on client_id,
repeated over 4 seeds = 20 folds, each client held out once per seed.

    python work/improve.py <run>        # e.g. rule, gb_paper, gb_client_rank
    python work/improve.py --list

Gate, label, rule and the 14 features are copied unchanged from capstone.ipynb.
Results append to work/outputs/improve_runs.json; the human log is experiments.md.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "outputs" / "improve_runs.json"
SEEDS = [0, 1, 2, 3]
K = 5

df = pd.read_csv(ROOT / "data" / "raw" / "content_refresh_anonymized.csv")
df["is_declining"] = df["trend_direction"].str.lower().eq("down").astype(int)
elig = df[(df.impressions_90d >= 250) & (df.avg_position > 0) & (df.avg_position <= 20)].copy()
elig = elig.reset_index(drop=True)

tier_med = elig.groupby("position_tier")["ctr"].transform("median")
elig["ctr_gap_ratio"] = ((tier_med - elig.ctr) / tier_med.replace(0, np.nan)).clip(lower=0).fillna(0)
elig["freshness_term"] = (elig.days_since_last_update / 365).clip(upper=1)
elig["rule_score"] = elig.ctr_gap_ratio + elig.freshness_term

BANNED = {"trend_direction", "trend_pct", "is_declining",
          "impressions_last_30d", "impressions_prev_30d", "clicks_last_30d",
          "clicks_prev_30d", "sessions_last_30d", "sessions_prev_30d"}
FEATURES = ["ctr_gap_ratio", "freshness_term", "ctr", "avg_position", "impressions_90d",
            "clicks_90d", "days_since_last_update", "content_age_days", "word_count",
            "engagement_rate", "scroll_rate", "days_with_impressions", "search_volume",
            "competition"]
assert not (set(FEATURES) & BANNED)

y = elig.is_declining.values
groups = elig.client_id.values
X = elig[FEATURES].replace([np.inf, -np.inf], np.nan).fillna(0)
# Percentile of each feature inside its own client. Uses only that client's feature values,
# never labels, and a client is wholly in train or wholly in test, so nothing crosses the split.
X_rank = X.groupby(groups).rank(pct=True)


def gb(Xm, **kw):
    def score(tr, te, seed):
        m = GradientBoostingClassifier(random_state=seed, **kw).fit(Xm.iloc[tr], y[tr])
        return m.predict_proba(Xm.iloc[te])[:, 1]
    return score


def rank_blend(a, b):
    "Average of two methods' within-fold ranks."
    def score(tr, te, seed):
        return (pd.Series(a(tr, te, seed)).rank(pct=True) + pd.Series(b(tr, te, seed)).rank(pct=True)).values
    return score


def rule(tr, te, seed):
    return elig.rule_score.values[te]


def blend_strict(tr, te, seed):
    "Leak check for blend_rule_gb: the tier-median CTR (used by the rule and by ctr_gap_ratio)"
    "is computed from the training clients only, so test pages never shape their own score."
    e = elig.copy()
    med = e.iloc[tr].groupby("position_tier")["ctr"].median()
    tm = e.position_tier.map(med)
    e["ctr_gap_ratio"] = ((tm - e.ctr) / tm.replace(0, np.nan)).clip(lower=0).fillna(0)
    r = (e.ctr_gap_ratio + e.freshness_term).values
    Xs = e[FEATURES].replace([np.inf, -np.inf], np.nan).fillna(0)
    m = GradientBoostingClassifier(random_state=seed).fit(Xs.iloc[tr], y[tr])
    return (pd.Series(r[te]).rank(pct=True)
            + pd.Series(m.predict_proba(Xs.iloc[te])[:, 1]).rank(pct=True)).values


RUNS = {
    "rule": rule,
    "gb_paper": gb(X),
    "gb_client_rank": gb(X_rank),
    "gb_raw_plus_rank": gb(pd.concat([X, X_rank.add_suffix("_r")], axis=1)),
    "gb_shallow_slow": gb(X, n_estimators=400, learning_rate=0.03, max_depth=2, subsample=0.8),
    "gb_min_leaf_50": gb(X, min_samples_leaf=50),
    "blend_rule_gb": rank_blend(rule, gb(X)),
    "blend_rule_gb_shallow": rank_blend(rule, gb(X, n_estimators=400, learning_rate=0.03,
                                                max_depth=2, subsample=0.8)),
    "blend_rule_gb_strict": blend_strict,
    "hgb": lambda tr, te, seed: HistGradientBoostingClassifier(random_state=seed)
        .fit(X.iloc[tr], y[tr]).predict_proba(X.iloc[te])[:, 1],
}


def p_at(scores, labels, k):
    order = np.lexsort((np.arange(len(scores)), -np.asarray(scores)))
    return float(np.asarray(labels)[order[:k]].mean())


assert p_at([3, 2, 1], [1, 0, 1], 2) == 0.5


def per_client_p10(scores, labels, cl):
    "Mean precision@10 inside each test client with 50+ pages: the queue one team would get."
    vals = [p_at(scores[cl == c], labels[cl == c], 10) for c in np.unique(cl) if (cl == c).sum() >= 50]
    return float(np.mean(vals))


def evaluate(fn):
    rows = []
    for seed in SEEDS:
        for f, (tr, te) in enumerate(GroupKFold(K, shuffle=True, random_state=seed).split(X, y, groups)):
            assert not set(groups[tr]) & set(groups[te])
            s, yt, ct = fn(tr, te, seed), y[te], groups[te]
            r = elig.rule_score.values[te]
            rows.append(dict(seed=seed, fold=f, n=len(te), clients=len(set(ct)),
                             p50=p_at(s, yt, 50), p50_rule=p_at(r, yt, 50),
                             auc=roc_auc_score(yt, s) if len(set(yt)) > 1 else np.nan,
                             pc10=per_client_p10(s, yt, ct), pc10_rule=per_client_p10(r, yt, ct)))
    return pd.DataFrame(rows)


def summarise(name, R):
    d = R.p50 - R.p50_rule
    dc = R.pc10 - R.pc10_rule
    by_seed = R.assign(d=d).groupby("seed").d.mean()
    return dict(
        run=name,
        commit=subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, cwd=ROOT).stdout.strip(),
        folds=len(R), pages=int(len(elig)), clients=int(elig.client_id.nunique()),
        p50=round(R.p50.mean(), 3), p50_seed_spread=round(R.groupby("seed").p50.mean().std(), 3),
        p50_minus_rule=round(d.mean(), 3), seed_means_minus_rule=[round(v, 3) for v in by_seed],
        folds_won=int((d > 0).sum()), folds_lost=int((d < 0).sum()),
        auc=round(R.auc.mean(), 3),
        pc10=round(R.pc10.mean(), 3), pc10_minus_rule=round(dc.mean(), 3),
        pc10_folds_won=int((dc > 0).sum()), pc10_folds_lost=int((dc < 0).sum()),
        seeds=SEEDS, fold_p50=R.p50.round(3).tolist(), fold_pc10=R.pc10.round(3).tolist(),
    )


def versus(a, b):
    "Fold-by-fold: does run a beat run b on the same folds?"
    log = {r["run"]: r for r in json.loads(OUT.read_text())}
    d = np.array(log[a]["fold_p50"]) - np.array(log[b]["fold_p50"])
    dc = np.array(log[a]["fold_pc10"]) - np.array(log[b]["fold_pc10"])
    seed_means = d.reshape(len(log[a]["seeds"]), K).mean(axis=1).round(3).tolist()
    print(f"{a} minus {b}: P@50 {d.mean():+.3f}, seed means {seed_means}, "
          f"folds won {(d > 0).sum()} lost {(d < 0).sum()} | "
          f"per-client P@10 {dc.mean():+.3f}, won {(dc > 0).sum()} lost {(dc < 0).sum()}")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[2] == "--vs":
        sys.exit(versus(sys.argv[1], sys.argv[3]))
    if "--confirm" in sys.argv:          # fresh seeds never used while choosing
        SEEDS = [4, 5, 6, 7, 8, 9]
        sys.argv.remove("--confirm")
        suffix = "@confirm"
    else:
        suffix = ""
    if len(sys.argv) != 2 or sys.argv[1] not in RUNS:
        sys.exit("runs: " + ", ".join(RUNS))
    name = sys.argv[1] + suffix
    s = summarise(name, evaluate(RUNS[sys.argv[1]]))
    print(json.dumps(s, indent=2))
    log = json.loads(OUT.read_text()) if OUT.exists() else []
    OUT.write_text(json.dumps([r for r in log if r["run"] != name] + [s], indent=2))
