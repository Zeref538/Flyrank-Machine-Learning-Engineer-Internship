# Ship the Ugly One

**John Andrei Martinez · General AI Fluency · Week 5**

**Live URL:** https://johnandrei.vercel.app

---

## Every sitemap page is reachable

My Week-1 sitemap had four stops: Home, Work, About, Contact. I built it as one
scrolling page with anchors instead of four separate URLs, because there are four
sections, not four topics — splitting them would just add clicks between the
claim and the proof.

| Sitemap stop | Where it lives now | How you get there |
|---|---|---|
| HOME (the claim + one action) | `#home` — hero | lands here |
| WORK / case studies | `#projects` — 12 cards | nav "Projects", or the right-side rail |
| ABOUT | `#about` | nav "About" |
| CONTACT (the one action) | `#contact` — form, email, phone, GitHub, LinkedIn | nav "Contact", or the hero button |

Four sections I added past the sitemap: Experience, Certifications, Skills,
Education. Those aren't scope creep — the sitemap folded certs into About and I
found the About block got too long to read, so they became their own sections.

Nothing on the page is a placeholder anymore. That was the actual work this week.

## What I fixed to make it real

Two things were fake and I knew it.

**The FlyRank job had placeholder bullets.** There was literally a
`// TODO: replace these placeholder bullets` sitting in my data file with three
lines of generic intern-speak. Replaced with what I actually did: the 9.8M-row
DuckDB partition, the data contract, the leak I caught in my own work
(ROC-AUC 0.612 → 0.737 when I added a label-derived feature), and the
tie-breaking finding.

**The FlyRank capstone wasn't on the site at all.** It was case study #1 in my
own sitemap and the biggest thing I built all internship, and it was missing.
Added it as a project card with the honest numbers — P@50 0.88 for the model vs
0.86 for my hand-written rule, and the caveat that the model only wins in 6 of 8
client splits. The card links to the write-up and the repo.

I put the caveat on the card on purpose. "0.88 beats 0.86" without "and that gap
is inside the tie-breaking noise" would be the exact thing this internship keeps
teaching me not to do.

## How the site is built (no mystery code)

- **React 18 + Vite**, deployed on **Vercel** from the `main` branch of
  `Zeref538/portfolio`. Push to main → Vercel builds → live in about a minute.
- **All content lives in one file**, `src/data.js`. It exports plain arrays:
  `profile`, `experience`, `projects`, `skills`, `certifications`, `education`.
  `App.jsx` maps over them. To add a project I add an object; nothing else
  changes. That's why the two fixes above were data edits, not code edits.
- **The animations are components I can name**: `Reveal` (fade in on scroll,
  IntersectionObserver), `BorderGlow` (the glow that follows your cursor along a
  card edge), `RotatingText` and `ScrollFloat` (both GSAP), `ParticleField`,
  `Noise` (a grain overlay), `Cursor`. Each is one file in `src/components/`.
- **The chat widget (zeref-bot) is RAG, not a chatbot wrapper.**
  `scripts/build-index.mjs` reads `data.js`, `knowledge/*.md`, and project
  READMEs, chunks them, embeds each chunk with Azure OpenAI, and writes
  `api/_index.json`. At question time the Vercel serverless function in `api/`
  embeds your question, scores every chunk by cosine similarity, and hands the
  top matches to the model as context. No vector database — the index is a
  static JSON file I commit.
- **`CyclingCover`** cross-fades a project's screenshots, but only while the card
  is on screen, so twelve cards aren't each running a timer in the background.
- **`CopyButton`** copies my email or phone, and falls back to a hidden textarea
  when the clipboard API is blocked.

The one piece I'd have called mystery code a month ago is the RAG retrieval, so I
had AI walk me through cosine similarity before I shipped it. Short version: each
chunk becomes a list of numbers, your question becomes a list of numbers, and
similarity is the angle between them — closer angle, closer meaning.

## One real person opened it

> **TODO — John, fill this in after you send the link.**
> Send `https://johnandrei.vercel.app` to one real person, ideally someone in
> AI/ML or hiring. Ask them just to look, don't coach them. Then write down here:
> who they are (role, not necessarily name), what they said they saw first, what
> confused them, and whether the work landed. Their words, not a summary.

## Still ugly — the list I already know about

1. ~~**There is no photo of me anywhere on the site.**~~ **Fixed.** Real 400×400
   photo, top of the About section, next to my name and role. Real, not
   generated — the rule my curation doc set for anything that is me.
2. **The zeref-bot index is stale right now.** `npm run index` is a manual step
   and I just changed `data.js`, so the bot doesn't know about the FlyRank
   project yet. Worse, it fails silently — the bot answers confidently from the
   old index. This should run inside the build.
3. ~~**The FlyRank card has no screenshot.**~~ **Fixed.** There's no UI to
   screenshot, so I rendered two charts straight from `w05_model_metrics.json`
   instead: Precision@50 by method with the hand rule hatched, and the
   tie-breaking band showing why 0.88-over-0.86 isn't a win. Real numbers, no
   mockup. The script asserts the model's score is actually inside the band
   before it saves the image, so the chart can't outlive the claim it makes.
4. **Twelve project cards is too many for one screen.** The filter chips help,
   but "All" dumps everything and a visitor doesn't know which three to read.
   The sitemap said three cases. I shipped twelve.
5. **The hero says "Aspiring Machine Learning Engineer" on a rotating loop.**
   Three job titles cycling reads as undecided, which is the opposite of a claim.
6. **Mobile is workable, not good.** The project card hover overlay only opens on
   tap-to-focus, the section rail is hidden, and the cursor effect does nothing —
   so phone visitors get a plainer site than the one I designed.
7. **`img/Alfred/`, `img/LeanLLm/`, `img/callback-ai/` are untracked in git.**
   Local-only screenshot folders that never got committed. Ugly in the repo, not
   on the page.
8. **The Experience section has two entries and one of them is a VA job.** Honest,
   but thin.

Numbers 1 and 2 are the ones I'd fix first — one is a real gap a visitor notices,
the other is a silent wrong answer, which is worse than a missing one.
