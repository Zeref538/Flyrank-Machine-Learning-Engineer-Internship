# The Plan to Keep Building

**John Andrei Martinez · General AI Fluency · Week 8**

The point of this note is that adding case study number two should be a
twenty-minute job, not an afternoon of remembering how the site works. Written now,
while I still remember.

---

## Where the next case goes

One file: **`src/data.js`** in the [Portfolio repo](https://github.com/Zeref538).
Nothing else. The top of that file says so:

```js
// ============================================================
//  EDIT THIS FILE to change any content on the site.
//  Add / remove items in any array — the UI updates itself.
// ============================================================
```

A case study is one object pushed onto the `projects` array. The grid, the card, the
detail overlay and the tag filters all read from it, so adding an object is the
whole job — there is no component to touch and no layout to adjust.

## The steps, in order

1. **Put the screenshots in `public/projects/`** first, named `<slug>-1.png`,
   `-2.png` and so on. Do this before writing anything, because the object
   references them by path and a missing file shows an empty card.
   - If any of them is an animated GIF, **convert it first**:
     `magick in.gif -coalesce -layers optimize -quality 55 -define webp:method=6 out.webp`.
     A GIF stores motion as near-uncompressed whole frames; the last one I converted
     went from 3,600 KB to 931 KB with all 230 frames intact.
2. **Copy the nearest existing project object** in `data.js` and edit it in place.
   Copying beats writing from scratch because the field names have to match exactly
   and a typo in a key fails silently — the field just does not render.
3. **Write the three beats** (below).
4. **Run it locally:** `npm run dev`, then look at the card *and* open the detail
   overlay. The overlay is where the description and highlights actually show; the
   card only ever shows three clamped lines.
5. **Check the numbers before pushing.** Every metric in the new case gets run
   through `/claim-check` against the source it came from. This is the step I will
   be tempted to skip and the one that has already caught me.
6. **Ship it:** `npm run build`, commit, push. Vercel deploys from `main` on its
   own — about a minute. Then load the live URL and confirm the change is actually
   there, because editing a file is not deploying it.

## The three-beat shape (from Week 2)

Each case is three sentences before it is anything else. Write these first, in a
scratch file, and only then fill in the object.

| beat | what goes in it | the test |
|---|---|---|
| **Problem** | What was actually hard, in one sentence, without me in it | Would someone who does not know me understand why this needed doing? |
| **What I did** | The decision, not the tool list | Does it name a choice I could have made differently? |
| **What came of it** | A number, including the one that got worse | Is there a real figure, and did I say what it is measured against? |

The third beat is the one that decides whether the case is worth having. "Built an
X with Y" is a description. "Precision@50 fell from 0.72 to 0.52 when I tested on
clients the model had never seen, and I published that" is evidence.

**Fields that matter most, in order:** `metric` (shows on the card, so it is the
only number most people see), `highlights` (the detail overlay — four bullets, each
carrying a number), `description`, then `tags`, `link` and `demo`. If the project
has a live demo on a free host that sleeps, set
`demoLabel: "live demo (free host, ~30s to wake)"` so a visitor does not think it
is dead.

---

## The next real piece of work

**A holdout experiment on the FlyRank refresh queue.**

My capstone ends on an honest limitation: the whole thing is decision support, not
evidence, because nobody ever refreshed pages at random and watched what happened.
The paper names the fix in one sentence — refresh a random half of the queued pages,
hold the other half untouched, compare after 90 days.

That is the next case study, and it is the right one because it is the direct
answer to my own paper's biggest weakness. It also turns a ranking claim into a
causal one, which is the single thing my portfolio cannot currently show.

**Second in line, if the holdout is not possible without client access:** rebuild
the queue on the warehouse release rather than the 30,000-row snapshot, using real
per-page edit timestamps. That would settle the decay question I had to abandon —
the snapshot's staleness column turned out to be near-constant within a client, so
content decay was simply not measurable.

## The reminder

A recurring calendar event, first Saturday of every month, 10:00:

> **Portfolio: add or refresh one case study (30 min)**
> Open `src/data.js`. Three beats: problem, what I did, what came of it — with a
> number in the third. Run `/claim-check` before pushing.
> Plan: `flyrank-ml-internship/work/ai-fluency/plan-to-keep-building.md`
> Next up: FlyRank refresh-queue holdout experiment.

Monthly rather than weekly on purpose. A weekly nudge for something I will not do
weekly becomes a notification I learn to dismiss, and a dismissed reminder is worse
than none — it teaches me to ignore the thing.

## Keeping the build context

The Claude Project stays. It already holds the identity kit, the writing rules, the
stack, and — more useful than any of it — the specific mistakes: that a media query
adds no CSS specificity, that iOS zooms an input under 16px, that
`days_since_last_update` in this dataset is not what its name says.

Rebuilding that context costs more than writing the case study. Keeping it means
the next one starts with "here is the new project, use the usual shape" instead of
re-explaining who I am and how I write.

The working rules also live in `~/.claude/CLAUDE.md` outside any single project, and
the writing-style rules are re-injected on every prompt by a hook, so the voice
holds even in a fresh session with no history.
