# claim-check

An agent that checks every number in a draft against the file it came from, and
tells you which ones it could not find.

**Built by:** John Andrei Martinez · FlyRank AI Fluency track (FL-06 design, FL-07
build, FL-09 documentation)

---

## What it does, and who it is for

You finish a README, a project card, a paper section or a slide. It is full of
numbers you wrote down days ago from a notebook you have since re-run. Some of
those numbers are now wrong, and you cannot tell which by looking.

`claim-check` reads the draft, pulls out every checkable number, and returns one
row per claim:

| claim | verdict | source | what the source says |
|---|---|---|---|

There are four verdicts:

| verdict | meaning |
|---|---|
| **VERIFIED** | exact match in a source, or matches to two or more decimal places |
| **WRONG** | a source exists and disagrees |
| **LOOSE** | matches to only one decimal place — `0.551` rounds to `0.6`, but so does `0.649` |
| **UNVERIFIABLE** | no source found. **A finding, not a failure.** |

**Who it is for:** me, and anyone else keeping a repo where the numbers in the
writing have to trace back to numbers in the code. It is built for this repository's
layout, and the "Reusing it elsewhere" section says what to change.

**What it is not.** It does not improve your writing, does not add claims, and never
edits your draft. It reports; you decide.

---

## Setup, from nothing

You need Python 3.9+ and Claude Code. No API keys, no accounts, no packages beyond
the standard library — the lookup tool imports only `re`, `json`, `pathlib` and
`sys` on purpose, so it cannot break because of a dependency.

```bash
git clone https://github.com/Zeref538/flyrank-ml-internship
cd flyrank-ml-internship

# 1. the search tool runs standalone -- check it works before involving an agent
python .claude/skills/claim-check/lookup.py 0.88

# 2. the tool's own self-tests, including the rounding cases that define LOOSE
python .claude/skills/claim-check/lookup.py --self-check

# 3. open Claude Code in this folder; the skill is picked up from .claude/skills/
claude
```

Then in Claude Code:

```
/claim-check docs/index.html
```

If step 1 prints sources and step 2 prints `lookup self-check ok`, the tooling works
and anything that goes wrong afterwards is the agent, not the setup. That split is
deliberate: a tool you can run without an agent is a tool you can debug.

---

## Usage

**Check a file:**

```
/claim-check work/ai-fluency/break-your-own-site.md
```

**Check with a hint about where to look:**

```
/claim-check docs/index.html -- verify against the committed metrics JSONs
```

**Look one number up by hand, no agent involved:**

```bash
$ python .claude/skills/claim-check/lookup.py 0.551
20 source(s) for 0.551:
  [EXACT] work/outputs/w05_model_metrics.json:3
      "test_base_rate": 0.551,
  [EXACT] work/outputs/w07_playbook_metrics.json:5
      "base_rate": 0.551,
```

**A real run.** Checking the capstone paper before publishing it — 37 numbers, all
verified, and three of those only had my own notebook comment as a source, so I
recomputed them from `data/raw/` before trusting them. That last part is the agent
following its own rule: *a draft citing another draft is not a source.*

---

## How it is put together

```
  your draft (.md / .html / .ipynb)
          |
          v
  +---------------------+
  |   SKILL.md          |  the agent's instructions:
  |                     |  - what counts as a checkable claim
  |                     |  - the 4 verdicts and when each applies
  |                     |  - source order, cheapest first
  |                     |  - hard rules (never edit, never print ids,
  |                     |    never echo a token, never commit)
  +----------+----------+
             |
             v  tries sources in order, stops at the first that settles it
  +----------+----------------------------------------+
  | 1. lookup.py   <- deterministic, no LLM involved   |
  |    searches: work/outputs/*.json                   |
  |              work/notebooks/*.ipynb (source AND    |
  |                                      outputs)      |
  |              work/**/*.md                          |
  |    NOT the CSVs -- see Limitations                 |
  +----------------------------------------------------+
  | 2. grep        <- filenames, column names, quotes  |
  +----------------------------------------------------+
  | 3. recompute from data/raw/  <- asks first, always |
  +----------------------------------------------------+
             |
             v
    table of verdicts + a count
```

The important design decision is that **step 1 is not an LLM.** `lookup.py`
normalizes the number (strips commas, handles trailing zeros), searches the
committed sources, and reports `EXACT`, `ROUNDS-TO`, `ROUNDS-TO LOOSE` or
`NOT FOUND`. Most claims are settled there, deterministically, before the model
gets a chance to be creative about it. The agent's judgement is reserved for the
things judgement is actually needed for: what counts as a claim, and which source
is the right one.

---

## Eval results (v2)

Seven cases in `evals/draft_01.md`, with expectations written in FL-06 **before**
the tool existed, so they are not reverse-engineered from what it happens to do.
Expected verdicts are in `evals/expected.md`; a full run is in
`evals/run_01_output.md`.

| # | Case | Expected | v2 result |
|---|---|---|---|
| 1 | "~17x a 50-page review capacity" | WRONG | pass — and for the right reason: 17 is a page count, not a multiplier |
| 2 | "P@50 of 0.88 against the rule's 0.86" | VERIFIED ×2 | pass, naming `w05_model_metrics.json` |
| 3a | "base rate was 0.55" | VERIFIED | pass |
| 3b | "base rate was 0.6" | LOOSE | pass |
| 4 | "13,562 pages across 29 clients" | VERIFIED ×2 | pass, nothing falsely flagged |
| 5b | "the April partition holds 4,102,887 rows" | UNVERIFIABLE | pass |
| 6 | "work/notebooks/w06_final.ipynb" | WRONG | pass — checks the path rather than assuming it |

**7 of 7.** Two of those cases only exist because v1 failed:

- **The LOOSE verdict did not exist in my FL-06 design.** I had three verdicts.
  Then case 3b — "0.6" against a real value of 0.551 — was neither verified nor
  wrong, because 0.551 genuinely does round to 0.6, and so does 0.649. Calling that
  VERIFIED hides a real difference; calling it WRONG is a false alarm that makes me
  stop reading the output. So the fourth verdict was added, with
  `assert round(0.551, 2) == 0.55` and `assert round(0.551, 1) == 0.6` in the
  tool's self-check so the distinction cannot rot.
- **Case 5 was a bad test and the agent was right.** I wrote it expecting
  UNVERIFIABLE, having forgotten that the ML-04 notebook already ran that query and
  its output is committed. A notebook output *is* a source. I replaced it with an
  April-partition figure nothing in the repo ever computed — which is the test I
  meant to write: if that ever returns VERIFIED, the agent has agreed with a number
  it never looked at, and the build stops.

---

## Limitations

- **It checks transcription, not methodology.** If the computation that produced a
  number was wrong, this will happily confirm the wrong number matches its source.
  It catches stale and mistyped figures. It cannot catch a bad experiment.
- **`lookup.py` deliberately does not search the CSVs in `work/outputs/`.** Those
  hold row-level client data. Searching them once caused the tool to print client
  pseudonyms into my terminal — twice, after I thought I had fixed it. The fix was
  three-part: drop the CSVs from the search path, add word boundaries to the number
  pattern, and add an ID mask over anything about to be printed.
- **Numbers with no source are common and that is the point.** A long
  UNVERIFIABLE list usually means the draft is quoting a number that was never
  written down anywhere, which is exactly the situation this was built for.
- **Built for this repo's layout.** The search paths are hardcoded to
  `work/outputs/`, `work/notebooks/` and `work/**/*.md`.
- **It cannot check a claim only a human can settle** — "the reviewer could not say
  what I do", "this is the best result" — and does not try.
- **Bare integers are noisy.** Searching `9` returns 48 sources. Small round
  numbers need the agent to pick the right one, and that is the step most likely to
  be wrong.

## Reusing it elsewhere

Two files matter. Change the search roots at the top of `lookup.py`, and delete the
"Claims about the Flewd hackathon data" section from `SKILL.md` — those three rules
encode gotchas specific to one dataset and would be nonsense anywhere else.

---

## Where AI did the work

I built this with Claude Code, and it wrote most of the lines in `lookup.py`.

What I did myself, and what makes it mine:

- **The design came first, in FL-06, before any code** — including the eval cases
  and their expected answers. That is why the evals are a real test rather than a
  description of the finished tool.
- **I found the failures.** The ID leak was caught by reading the tool's own
  output, not by a test — and it took two attempts to fix, because the first fix
  only closed one of the two paths pseudonyms travelled down.
- **I overruled it, and I overruled myself.** One assertion the model wrote was
  wrong about my own regex (`P@50` contains a legitimate standalone `50`). One eval
  case I wrote was wrong and the agent's answer was right, which is how case 5
  became case 5b.
- **The fourth verdict is mine.** LOOSE came from watching the three-verdict
  version give an answer that was technically defensible and practically useless.

The honest summary: Claude wrote the code faster than I would have, and every
decision about what the thing should refuse to do came from running it and not
liking what I saw.
