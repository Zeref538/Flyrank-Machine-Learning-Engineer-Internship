# Task: add a case-study page - Which Page Do You Fix First? (FlyRank ML capstone)

Paste this file's path into a fresh Claude Code session opened in this folder,
or say "follow docs/CASE_STUDY_TASK.md". It adds a case-study page in John's
shared design, then cleans up the project.

## Where the page goes

**Add the page at `docs/case-study.html`.** GitHub Pages serves `docs/` on
`main` (https://zeref538.github.io/flyrank-ml-internship/), and the
`docs/index.html` there is the capstone paper, the submitted deliverable
(`submission/paper_url.txt`). Do not change the paper beyond adding a link.
Link the two pages to each other.

## The story this page tells

**The model did not beat a five-line rule, and the page leads with that.**
Precision@50 of 0.88 against the rule's 0.86, and the bootstrap interval on
the difference contains zero. Then the two leakage findings (splitting by row
instead of by client, and a label rebuildable from two unbanned columns),
which are the strongest parts. Then the causal test that failed its own
placebo.

## Where the facts are

`docs/index.html` (the paper), `work/outputs/*.json`, `work/notebooks/capstone.ipynb`, `work/notebooks/w06_validation_audit.ipynb`, `README.md`, `DATA_USE.md`.

## Traps specific to this project

- **This is real client data under the internship's terms.** Read
  `DATA_USE.md`. Aggregates only: no client or content IDs, URLs, queries or
  row-level values on the page, in figures, or in the build script's output.
- **Decision-support language only**: observed, measured, directional. The
  page must never say refreshing or optimizing a page causes a traffic change.
  The one causal test failed, and that failure is part of the story.
- The 0.992 and 1.000 ROC-AUCs are leak demonstrations. Never show them as
  results, and never in the hero.
- **Starter-repo files** (`notebooks/01-03`, `scripts/`, `outputs/`,
  `SETUP.md`, `GUIDE.md`, `skills/`, `.github/workflows/`) came from FlyRank's
  starter template, and CI runs some of them. List them in the cleanup; do not
  delete them without John's say.
- `data/raw/content_refresh_anonymized.csv` is the committed starter slice
  every notebook runs on. Never delete it.
- There is no model to download. The pill button links to the paper.
- `docs/` is the public site. Anything committed there is published.

## Read these first, fully, before changing anything

1. `../../BRAND.md` - the spec, including
   the "Tried and rejected" list.
2. `../../LiitLLM/docs/template.html` -
   the reference build.
3. Live reference: https://zeref538.github.io/liitllm/
4. This project's README and every file named under "Where the facts are" above.

## Part 1: the page

- Copy LiitLLM's `template.html` structure, CSS and scripts, then fill it with
  THIS project's content. Do not redesign from scratch and do not bring back
  anything on the rejected list.
- Copy the `fonts` folder (Schibsted Grotesk, Newsreader, Sora and the OFL
  licence files) and `docs/img/john.jpg` from LiitLLM, into the folder the
  page is served from.
- **Every number, chart and claim must come from this project's own files.**
  Do not invent results. If a LiitLLM section has no match here, drop it. If
  this project has something LiitLLM lacks, fit it into the same card style.
- **Charts are generated, not typed.** Build each figure with a committed script
  that reads committed result files, so re-running the script rebuilds it.
- Pick ONE project colour (not clay, and not a colour another project's page
  already uses - check BRAND.md). Use it wherever LiitLLM uses `--clay`, and run
  the dataviz palette validator on light and dark before using it. Add it to
  BRAND.md's colour table.
- The hero card fits one laptop screen (1366x768). The contents rail numbers
  match the number of sections.
- Keep the Simple / Technical toggle, and write both versions of every text.
- No em dashes anywhere in the copy.
- Link the page from the README (near the top) and from the live app if the app
  has a footer or about area.

## Part 2: clean up what is no longer used

- **Tracked files:** find scripts, configs, notes, old results and assets that
  nothing references any more. Grep for every file name before calling it
  unused. Remove them with `git rm` in their own commit, so they stay
  recoverable from history. Keep anything the README, tests, notebooks or
  pipeline still point to.
- **Page code:** remove CSS rules and JS for classes and ids that no longer
  appear in the HTML. Check `git diff` afterwards to confirm only dead rules went.
- **Junk:** `__pycache__`, `.pytest_cache`, old logs, your own screenshots and
  preview pages.
- **Big untracked files** (checkpoints, datasets, staging or upload folders): do
  NOT delete them yourself. List each one with its size, say whether it is safe
  to delete and why (rebuildable? a backup copy? the only copy?), and give John
  the exact PowerShell commands to delete the safe ones. He runs them.
- After cleanup, run the tests and rebuild the app and the page to prove
  nothing broke.

## Before saying it is done

- Screenshots at 1440x900, 1366x768, 768px and 390px, in light and dark.
- No sideways scroll (`scrollWidth` equals window width) and no console errors.
- **The live app still works** - load it locally and use its main feature once.
- Give John a localhost link to preview.
- Commit locally. Do NOT push until John says "push".
- Then run the `audit-site` skill; its model case-study list (items 75-86)
  applies to this page even though no language model is involved.
