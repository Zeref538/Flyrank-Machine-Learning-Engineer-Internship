# Submission index — every deliverable, in one place

**John Andrei Martinez · FlyRank AI Internship · June–September 2026**
Machine Learning track (main) · General AI Fluency track

| | |
|---|---|
| **Research paper (capstone)** | https://zeref538.github.io/flyrank-ml-internship/ |
| **Personal site** | https://johnandrei.vercel.app |
| **This repository** | https://github.com/Zeref538/flyrank-ml-internship |

---

## Start here

If you only open three things:

1. **[The paper](https://zeref538.github.io/flyrank-ml-internship/)** — the capstone,
   with the honest conclusion that the model did not beat a five-line rule.
2. **[w06_validation_audit.ipynb](notebooks/w06_validation_audit.ipynb)** — the
   finding I would defend hardest: a row split inflates ROC-AUC by 0.080 over a
   client-grouped split, in 8 of 8 draws.
3. **[FL-10-retrospective.md](ai-fluency/FL-10-retrospective.md)** — what changed in
   how I work.

---

## Machine Learning track

Every notebook runs top to bottom against the committed dataset. The later ones
carry self-checks that fail the run rather than printing a warning.

| Code | Deliverable | What it establishes |
|---|---|---|
| ML-01 | [w01_research_question.ipynb](notebooks/w01_research_question.ipynb) | The question, and who the answer is for |
| ML-02 | [w02_ml_task_framing.ipynb](notebooks/w02_ml_task_framing.ipynb) | Framed as ranking, not classification |
| ML-03 | [w03_data_contract.ipynb](notebooks/w03_data_contract.ipynb) | Eligibility gate, feature list, banned columns |
| ML-05 | [w03_feature_leakage_check.ipynb](notebooks/w03_feature_leakage_check.ipynb) | The label trap, checked rather than assumed |
| ML-06 | [w04_signal_audit.ipynb](notebooks/w04_signal_audit.ipynb) | Tie-breaking noise band: P@50 moves 0.76–0.92 |
| ML-07 | [w04_baseline_score.ipynb](notebooks/w04_baseline_score.ipynb) | The five-line rule, written before any model |
| ML-08 | [w05_model.ipynb](notebooks/w05_model.ipynb) | Four models vs the rule on the same grouped split |
| ML-09 | [w06_validation_audit.ipynb](notebooks/w06_validation_audit.ipynb) | Row vs client split; deliberate-leak test |
| ML-10 | [w07_action_playbook.ipynb](notebooks/w07_action_playbook.ipynb) | Ranked queue, archetypes, no-go list, cost/value |
| ML-11 | [docs/index.html](../docs/index.html) → [live](https://zeref538.github.io/flyrank-ml-internship/) | The deployed paper |
| ML-12 | [w07_action_playbook.ipynb](notebooks/w07_action_playbook.ipynb) (closing cells) | Demo outline + two shareable cuts |
| Capstone | [capstone.ipynb](notebooks/capstone.ipynb) | Mirrors the paper section for section; single source of truth |
| Extension | [w08_warehouse_did.ipynb](notebooks/w08_warehouse_did.ipynb) | Before/after study on 13,233 optimized pages from the 79M-row warehouse; placebo test fails and says why |

### Receipts the paper's numbers trace to

| File | Holds |
|---|---|
| [w04_baseline_metrics.json](outputs/w04_baseline_metrics.json) | Baseline rule scores, eligible page count |
| [w05_model_metrics.json](outputs/w05_model_metrics.json) | All five methods, tie noise band, 8-split margin |
| [w07_playbook_metrics.json](outputs/w07_playbook_metrics.json) | Queue metrics, archetype counts, decay negative result |
| [capstone_metrics.json](outputs/capstone_metrics.json) | Split, model-vs-rule, bootstrap interval, leak test |
| [capstone_gate_sensitivity.json](outputs/capstone_gate_sensitivity.json) | The gate sweep: 5 thresholds x 8 splits |
| [w08_did_metrics.json](outputs/w08_did_metrics.json) | DiD, placebo, and their client-clustered intervals |
| [figures/](figures/) | The charts the paper embeds |

The ranked queue CSV is deliberately **not** committed — it is derived client data,
and `work/**/*.csv` is in `.gitignore`. The notebook regenerates it.

---

## General AI Fluency track

### Build the agent

| Code | Deliverable |
|---|---|
| FL-06 | [FL-06-agent-design.md](ai-fluency/FL-06-agent-design.md) — design and eval cases, written before any code |
| FL-07 | [FL-07-build-log.md](ai-fluency/FL-07-build-log.md) — build log, including the two failures |
| FL-09 | [claim-check README](../.claude/skills/claim-check/README.md) — what it does, setup, architecture, v2 evals, limits |
| — | The agent itself: [SKILL.md](../.claude/skills/claim-check/SKILL.md), [lookup.py](../.claude/skills/claim-check/lookup.py), [evals/](../.claude/skills/claim-check/evals/) |

### Fluency and workflow

| Deliverable | |
|---|---|
| FL-01 | [Workflow audit](ai-fluency/FL-01-workflow-audit.md) |
| FL-02 | [Prompt iteration log](ai-fluency/FL-02-prompt-iteration-log.md) |
| FL-04 | [Automation workflow](ai-fluency/FL-04-automation-workflow.md) |
| FL-05 | [Agents and MCP](ai-fluency/FL-05-agents-and-mcp.md) |
| — | [Prompt ladder](ai-fluency/prompt-ladder.md) |
| — | [Three roads: stack choice](ai-fluency/three-roads-stack-choice.md) |

### Portfolio and identity

| Deliverable | |
|---|---|
| — | [What are you proving?](ai-fluency/what-are-you-proving.md) — the proof statement everything else is judged against |
| — | [Identity kit](ai-fluency/identity-kit.md) |
| — | [Through line](ai-fluency/through-line.md) |
| — | [Framed cases](ai-fluency/framed-cases.md) |
| — | [Curate your images](ai-fluency/curate-your-images.md) |
| — | [Empty but live](ai-fluency/empty-but-live.md) |
| — | [Ship the ugly one](ai-fluency/ship-the-ugly-one.md) |
| PF-04 | [Personal site + DNS walkthrough](ai-fluency/PF-04-dns-walkthrough.md) |

### Hardening and launch

| Deliverable | |
|---|---|
| — | [Explain it like you built it](ai-fluency/explain-it-like-you-built-it.md) |
| — | [Make it do something](ai-fluency/make-it-do-something.md) |
| — | [Open it on your phone](ai-fluency/open-it-on-your-phone.md) — mobile audit, measured before/after |
| — | [Survive the crit](ai-fluency/survive-the-crit.md) — real reviewer feedback, sorted, fixed |
| — | [Break your own site](ai-fluency/break-your-own-site.md) — five fix-nows, six named limitations |
| — | [Plant your flag](ai-fluency/plant-your-flag.md) — analytics, launch hygiene, badge |

### Closing out

| Deliverable | |
|---|---|
| FL-10 | [Retrospective](ai-fluency/FL-10-retrospective.md) |
| — | [The plan to keep building](ai-fluency/plan-to-keep-building.md) |
| — | Build-in-public post: draft in the closing cells of [w07_action_playbook.ipynb](notebooks/w07_action_playbook.ipynb) |

### Screenshots

[ai-fluency/screens/](ai-fluency/screens/) — before/after evidence for the mobile audit.

---

## The findings, if you are short on time

1. **Validation design outweighed every modelling choice.** Splitting by row instead
   of by client inflated ROC-AUC from 0.618 to 0.728, in 8 of 8 random draws — a
   larger gap than between any two models I tried.
2. **The model did not beat the rule.** Precision@50 of 0.88 vs 0.86, inside a
   0.76–0.92 band the rule alone moves through from tie-breaking, and a bootstrap over
   held-out clients puts the difference at −0.260 to +0.140 — an interval containing zero.
   It also survives moving the eligibility gate: sweeping it from 100 to 2,000 impressions
   nearly halves the eligible pages and the gap never clears 0.10. Reported as a
   non-result rather than a two-point win.
3. **The one causal test failed its own placebo, and that is the finding.** A
   difference-in-differences on 13,233 really-optimized warehouse pages gives +2.75 clicks
   per page (95% CI +1.76 to +3.50, clustered by client) — until the placebo, which should
   return zero, comes back at −0.71 with a CI of −1.21 to −0.11. Entirely below zero, so
   the parallel-trends violation is not noise. The treated pages were already falling before
   anyone touched them, and they recovered to 97% of their own baseline, not above it. Pages
   that were optimized recovered; the data cannot show optimization is why.
4. **Nearly half the top of the queue should not be acted on.** 24 of the top 50 are
   pages with impressions and zero clicks — they rank high because zero clicks
   maximises the CTR-gap term. The queue's first rule is a refusal.

---

## Public-safety statement

All work is built on real, pseudonymised FlyRank client data, treated as
confidential throughout. No client name, URL, query, or raw row appears in this
repository, in the deployed paper, or in any figure. Pseudonymous identifiers are
used only for grouping and splitting, never as features, and never printed into
committed notebook output — which is asserted in code, not assumed.

Built on the [FlyRank](https://flyrank.ai) ML Internship dataset.
