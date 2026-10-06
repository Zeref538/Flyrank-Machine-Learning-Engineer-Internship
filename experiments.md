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
| 1 | 2026-10-06 | baseline: the five-line rule | ctr_gap_ratio + freshness_term | 0.798 (0.015) | 0 | - | 0 | 0.594 | 13,562 pages, 29 clients, 20 folds | 6697923 | reference |
| 2 | 2026-10-06 | the capstone's gradient boosting, unchanged | sklearn defaults, 14 features | 0.848 (0.025) | +0.050, all 4 seeds above 0 | 15/4 | +0.101 | 0.642 | same | 6697923 | **best**, just meets the bar |
| 3 | 2026-10-06 | features ranked within their own client, replacing raw | defaults | 0.845 (0.016) | +0.047 | 11/6 | +0.084 | 0.602 | same | 6697923 | worse than #2 (-0.003, lost 10 of 18 decided folds); the absolute level matters |
| 4 | 2026-10-06 | within-client ranks added next to raw features | defaults, 28 features | 0.868 (0.023) | +0.070 | 15/3 | +0.098 | 0.617 | same | 6697923 | tie with #2 (+0.020, inside the spread; AUC fell) |
| 5 | 2026-10-06 | shallower, slower boosting | 400 trees, lr 0.03, depth 2, subsample 0.8 | 0.875 (0.015) | +0.077 | 16/4 | +0.102 | 0.647 | same | 6697923 | tie with #2 (+0.027, won 11 lost 6) |
| 6 | 2026-10-06 | min_samples_leaf 50 | otherwise defaults | 0.862 (0.012) | +0.064 | 15/4 | +0.104 | 0.645 | same | 6697923 | tie with #2 (+0.014) |
| 7 | 2026-10-06 | HistGradientBoosting instead of GradientBoosting | defaults | 0.834 (0.026) | +0.036 | 13/6 | +0.098 | 0.641 | same | 6697923 | worse than #2 (-0.014, below on all 4 seeds) |
| 8 | 2026-10-06 | average of the rule's rank and #2's rank | rank blend, equal weight | 0.879 (0.008) | +0.081, all 4 seeds above 0 | 18/1 | +0.107 | 0.640 | same | 6697923 | **promoted**: beats #2 by +0.031 on all 4 seeds, won 11 lost 3 |
| 9 | 2026-10-06 | #8 with #5's boosting settings | rank blend | 0.885 (0.011) | +0.087 | 18/2 | +0.111 | 0.642 | same | 6697923 | tie with #8 (+0.006); kept the simpler #8 |
| 10 | 2026-10-06 | leak check on #8: tier-median CTR from training clients only | rank blend | 0.881 (0.012) | +0.083 | 18/1 | +0.096 | 0.638 | same | 6697923 | same as #8 (+0.002): the shared median was not leaking |
| 11 | 2026-10-06 | confirmation of #8 on fresh seeds 4-9, never used while choosing | rank blend | 0.853 (0.037) | +0.089, all 6 seeds above 0 | 25/4 | +0.102 (won 26/3) | 0.634 | 30 folds | 6697923 | **beats the rule** (bar scaled to 30 folds: 23) |
| 12 | 2026-10-06 | confirmation of #2 on the same fresh seeds | defaults | 0.830 (0.028) | +0.066, all 6 seeds above 0 | 19/9 | +0.081 | 0.635 | 30 folds | 6697923 | misses the bar (19 < 23); blend minus #2 here: +0.023, won 16 lost 8, two seeds at 0 |

## Result

```
Best: run 8 (rank blend of the rule and gradient boosting), P@50 0.879 +/- 0.008 (4 seeds, 20 folds, 13,562 pages, 29 clients), commit 6697923
Confirmed on 6 fresh seeds: P@50 0.853 vs the rule's 0.764, +0.089, model ahead on every seed and in 25 of 30 folds
Tried: 11 runs after the baseline: the capstone model, 1 promoted, 4 ties, 2 worse, 1 leak check, 2 confirmations
```

**What changed from the capstone's "tie":** the capstone judged one split with 9 test clients. Tested on all 29 clients, the plain model already leads the rule, but not reliably enough (19 of 30 fresh folds). Blending it with the rule makes the lead hold on every seed. The blend's edge over the plain model is real but small (+0.023 on fresh seeds) and not something to oversell.

**Inside one client** (the queue a single content team gets), the blend's top 10 is right 81% of the time against the rule's 71% on fresh seeds (per-client P@10 0.811 vs 0.709, won 26 of 30 folds).

**Still true from the capstone:** splitting by client matters more than model choice; AUC stays modest (0.63-0.64), so this is a better ordering of the top of the queue, not a page-level predictor; the 90-day totals overlap the label's windows, as in the capstone.

**Next:** none planned. Any further gain needs a new signal, not more tuning: the three tuning runs (#5, #6, #9) all tied.
