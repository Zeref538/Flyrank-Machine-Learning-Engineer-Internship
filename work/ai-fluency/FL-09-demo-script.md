# FL-09 — demo video: recording plan and narration script

**John Andrei Martinez · General AI Fluency · Week 8**

The video for FL-09. Target **4 min 30 s** (the brief allows 3–5). Narration is
AI-generated and the script says so out loud, because the assignment rewards
naming where AI did the work.

The README this pairs with is
[`.claude/skills/claim-check/README.md`](../../.claude/skills/claim-check/README.md).

---

## Before hitting record

1. Open a terminal, maximise it, set the font to roughly **16–18pt**. Small text
   is the most common reason a demo video is unreadable.
2. `cd` into the repo so the prompt stays short:
   ```bash
   cd ~/OneDrive/Documents/Portfolio/Flyrank-internship/flyrank-ml-internship
   ```
3. Run `clear`. Start on an empty screen.
4. Open `.claude/skills/claim-check/evals/draft_01.md` in a second window — it
   gets shown briefly at 1:25.
5. **Close anything showing client data or a token.** The Hugging Face token is
   still live until it is rotated.
6. OBS: **Sources → + → Display Capture**, then **Start Recording**. 1080p.

### The trap

The real agent run takes about **2 min 25 s**. Do not stop the recording and
restart once the result appears — a replayed cached result is what makes a demo
look staged, and a reviewer comparing narration to timestamps will spot it. Let
it run and talk over the wait. The 1:45 section is written to fill exactly that
gap.

---

## Shot list

Bracketed lines are what I *do*. Quoted lines are what the *voice says*.

### 0:00 – 0:25 · What it is

*[Empty terminal.]*

> "This is claim-check, an agent I built during the FlyRank AI Fluency track. It
> reads a draft — a README, a paper section, a project card — pulls out every
> number in it, and tells you which ones it can actually find in the files those
> numbers came from. The narration you're hearing is AI-generated. The agent, the
> evals, and the failures I'm about to show you are mine.
>
> The problem it solves is specific. You write a number down on Tuesday from a
> notebook you re-run on Thursday. The number is now wrong and you cannot tell by
> looking at it."

### 0:25 – 1:00 · The tool runs standalone

*[Run:]*
```bash
python .claude/skills/claim-check/lookup.py 0.88
```

> "Underneath the agent is one plain Python file with no dependencies — it imports
> only `re`, `json`, `pathlib` and `sys`, on purpose, so it can't break because of
> a package update. Here it searches for 0.88 and finds forty sources, marking each
> one EXACT. That's the number from my capstone, and it traces to the committed
> metrics files and the notebook that produced them."

*[Run:]*
```bash
python .claude/skills/claim-check/lookup.py --self-check
```

> "It also carries its own self-tests. If those ever fail, the search layer is
> broken and nothing above it can be trusted."

### 1:00 – 1:25 · Architecture

*[Run `ls .claude/skills/claim-check/`]*

> "The architecture is deliberately two layers. `lookup.py` does the searching —
> cheap, deterministic, no model involved. `SKILL.md` is the agent's instructions:
> what counts as a claim, which verdicts exist, and the hard rules it must not
> break. The agent decides; the Python does the finding. Most claims never need the
> model at all, which is why this is fast and costs almost nothing."

### 1:25 – 1:45 · Show the draft

*[Switch to `evals/draft_01.md`, scroll slowly.]*

> "This is my eval fixture. Seven cases, with deliberate errors planted in it, and
> — this matters — I wrote the expected answers before the tool existed, back in the
> design assignment. So the evals test the tool. They aren't reverse-engineered from
> whatever it happens to do."

### 1:45 – 3:15 · The live run — **the design decision**

*[Launch `claude`, then type:]*
```
/claim-check .claude/skills/claim-check/evals/draft_01.md
```

*[Press enter. Do not cut. Keep talking.]*

> "That's running now, for real, and it takes about two and a half minutes — so let
> me use the time.
>
> Here's the design decision I'm most glad I made. My original design had three
> verdicts: verified, wrong, and unverifiable. Then this fixture broke it. One line
> claims the base rate was 0.6. The real value is 0.551. Is that verified? 0.551
> does round to 0.6 — but so does 0.649. Calling it verified hides a real
> difference. Calling it wrong is a false alarm, and false alarms are how you teach
> yourself to stop reading the output.
>
> So I added a fourth verdict: LOOSE. It means the number matches to only one
> decimal place, which is not a lie and not usable. That verdict didn't come from
> planning. It came from an eval failing, and it's now locked in with assertions in
> the tool's self-check so the distinction can't quietly rot away."

*[When the table appears, scroll through it.]*

> "There's the output. One row per claim, with the verdict, the file it came from,
> and what that file actually says."

### 3:15 – 4:05 · **The guardrail and the limitation**

*[Open the README, scroll to Limitations.]*

> "Now the guardrail, because this one cost me something. An early version searched
> every file in the outputs folder — including the CSVs. Those hold row-level client
> data, and the tool printed client pseudonyms straight into my terminal. Twice,
> after I thought I'd fixed it.
>
> The fix has three parts, because one wasn't enough: the CSVs are dropped from the
> search path entirely, the number pattern got word boundaries so it stops matching
> inside longer strings, and there's an ID mask over anything about to be printed.
> This is real client data under confidentiality terms, so the right design is one
> that cannot leak, not one that remembers not to.
>
> And the honest limitation: this checks transcription, not methodology. If the
> calculation behind a number was wrong, claim-check will cheerfully confirm the
> wrong number matches its source. It catches stale and mistyped figures. It cannot
> catch a bad experiment. That ceiling is written into the README, because a tool
> that quietly oversells what it verifies is worse than no tool."

### 4:05 – 4:30 · Close

> "Seven of seven eval cases pass, and two of those cases only exist because
> version one failed them. I built this with Claude Code — it wrote most of the
> lines in `lookup.py` — and the README has a section naming exactly what I checked
> myself.
>
> It has already earned its keep. It caught two numbers sitting live on my own
> portfolio that appear in no version of my work. Re-reading the page never found
> them. Checking the page against the committed files did."

*[Stop recording.]*

---

## Uploading

1. **studio.youtube.com** → **Create** (camera icon, top right) → **Upload videos**.
2. Drag the file in. Title:
   `claim-check — a number-verification agent (FlyRank AI Fluency, FL-09)`
3. On the **Visibility** step choose **Unlisted**, not Private. Private means
   reviewers cannot open it, and that is the most common way this submission fails.
4. **Save**, then copy the link from the **Video link** field.
5. Open that URL in a private/incognito window. If it plays without a login, it is
   genuinely unlisted.

## What to submit

```
https://github.com/Zeref538/flyrank-ml-internship/blob/main/.claude/skills/claim-check/README.md
<the unlisted YouTube URL>
```

## Two things to watch

- **Length.** The script runs ~4:30 at a normal pace. A fast AI voice can land it
  under 3:00, which fails the length criterion. Check the duration before
  uploading and slow the voice or add pauses rather than padding with filler.
- **Coverage.** The brief wants one design decision *and* one limitation on
  camera. The LOOSE verdict is the decision, the CSV leak is the guardrail, and the
  methodology ceiling is the limitation — three covered, so there is margin if a
  section gets trimmed.

## Criteria this is built to meet

| Criterion | Where |
|---|---|
| Stranger could reproduce setup from the README | README "Setup, from nothing" — clone, two commands, no keys |
| Eval results and limitations included, not hidden | README "Eval results (v2)" 7/7, and "Limitations" |
| Live end-to-end run, not slides | 1:45–3:15, uncut, real 2m25s runtime |
| 3–5 minutes, clear narration | ~4:30 |
| One design decision on camera | LOOSE verdict, 1:45–3:15 |
| One limitation on camera | CSV leak guardrail + methodology ceiling, 3:15–4:05 |
| Honest about where AI did the work | Stated at 0:00 and 4:05; README "Where AI did the work" |
