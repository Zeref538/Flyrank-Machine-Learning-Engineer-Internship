# Experiments: trying to beat the five-line rule

The capstone reported a tie: gradient boosting P@50 0.88 vs the rule's 0.86 on one split of 9 held-out clients, difference CI [-0.26, +0.14]. This log is the follow-up: can a genuine change beat the rule, measured so that a win means something?

## Protocol v2 (fixed before the first run)

- **Data:** `data/raw/content_refresh_anonymized.csv`, same gate as the capstone (impressions_90d >= 250, avg_position in (0, 20]): 13,562 pages, 29 clients. Same label, same rule, same 14 features, same banned columns (label plus the six 30-day window columns).
- **Split:** 5-fold GroupKFold on client_id, shuffled, seeds 0, 1, 2, 3. 20 folds; every client is held out once per seed. Old single-split scores do not compare with these.
- **Why the change:** client declining rates run from 0% to 97%, and one client holds 4,760 of the 13,562 pages. One 9-client split mostly measures which clients landed in test.
- **Primary metric:** P@50 per fold, minus the rule's P@50 on the same fold.
- **Secondary metric:** per-client P@10 (mean over test clients with 50+ pages), the queue one content team would actually get.
- **Beats the rule only if:** the mean P@50 difference is above 0 for all 4 seeds AND the model wins at least 15 of 20 folds. Anything less is a tie or a loss.
- **Code:** `python work/improve.py <run>`; raw results in `work/outputs/improve_runs.json`.

| # | date | change from best | settings | P@50 (seed spread) | minus rule | folds won/lost | per-client P@10 minus rule | AUC | n | code | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
