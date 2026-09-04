# Survive the Crit — design review log

**John Andrei Martinez · General AI Fluency · Week 6**

**Site reviewed:** https://johnandrei.vercel.app
**Reviewed:** 2026-09-05, on a phone
**Reviewer:** a friend outside my course — deliberately not someone who already
knows what I work on, since the whole test is whether the site says it for me.

## What I gave them

The live URL plus my proof statement, so they were judging the site against the
job it is supposed to do rather than against their taste:

> I can ship machine-learning results that survive honest validation instead of
> quietly failing on it. The one person I'm speaking to is a hiring manager
> screening candidates for a junior AI/ML or data role. The one action I want
> from them: email me to talk about it.

## The two questions, asked before anything else

**Q1 — "In ten seconds, what do I do?"**

> "Like a full stack dev, or like ML DevOps, or AI engineering."

**Q2 — "Would you believe I'm good at it?"**

> "I don't have any project or portfolio myself, so compared to yours, you're
> good."

**Both of these are failures, and I'm recording them as failures.**

Q1 came back as three guesses instead of one answer. I went looking for why, and
found it in my own hero section: the headline rotates through three different job
titles — "Data Analyst", then "AI Engineer", then "Machine Learning Engineer". He
gave me a list because the page gave him a list. That one stung, because I built
that animation on purpose and thought it showed range. It reads as indecision.

Q2 never actually answered the question. "Compared to me, you're good" is a
comparison to the reviewer, not a judgement of the work — he had no evidence to
weigh, so he weighed me against himself. A hiring manager has no such fallback;
they compare me to other candidates. The cause is my tagline: it lists the
*fields* I work in (agents, RAG, forecasting, computer vision) and gives not one
concrete thing I did. Breadth is not proof.

## Everything else they said

> "The phone UI looks broken on the nav bar."
>
> "The projects — I can't scroll down."

I did not argue with either, which took some doing, because I had audited and
fixed the mobile navigation the day before and my first instinct was to say
"that's already fixed."

## Must-fix

Confusing, broken, blocks the one action, or stops the proof landing.

| # | Finding | Why it's a must-fix |
|---|---|---|
| 1 | Hero rotates three job titles, so nobody can name one | Kills Q1. If the first line doesn't say what I am, nothing after it matters |
| 2 | Tagline lists fields, gives no evidence | Kills Q2. Nothing concrete to judge, so the proof statement never lands |
| 3 | Projects section traps scrolling on a phone | Someone who can't scroll past the projects never reaches the contact form — it blocks the one action outright |
| 4 | Nav looks broken on a phone | First thing seen on the site |

## Nice-to-have

Nothing. Every piece of feedback he gave was a must-fix. That is itself a
finding — a review this short with a 100% must-fix rate means the problems are
near the surface, not in the details.

## Diagnosis of the two bugs

Worth writing up separately, because the second one has a cause I'd never have
guessed from the symptom.

**The nav.** Checked first, before assuming he was wrong. The fix I shipped
yesterday *is* live — I pulled the deployed stylesheet straight off the server
and searched it:

```
curl -s https://johnandrei.vercel.app/assets/index-ZL6YoIt3.css | grep -o "nav-icon-phone.\{0,200\}"
```

The mobile rules are in the deployed file, and re-measuring at 360px wide, the
bar ends at 351px inside a 359px container — it fits. So the geometry is fine
and the "looks broken" is something else. Which leads to the same cause as the
scroll bug:

**Sticky hover.** A phone has no mouse, so when you tap something, the browser
fakes a hover and *leaves it stuck there* until you tap somewhere else. Every
`:hover` rule on the site is therefore a rule that latches on touch.

For the nav, that means a tapped icon keeps its little text label open, sitting
over the bar like a stuck box.

For the projects it's worse. Each card has a detail panel, `position: absolute;
inset: 0`, which covers the entire card and is itself scrollable
(`overflow-y: auto`). Touch the card while scrolling, hover latches, the panel
appears, and now the thing under your finger is a small scroll box instead of
the page. The page stops moving. That is exactly "I can't scroll down", and it
means anyone browsing on a phone gets stopped dead at the projects grid — before
the contact form.

The site already had an `@media (hover: none)` block — a CSS rule that only
applies on devices where hovering isn't real — but it only switched off the zoom
animations, not the overlay or the nav labels.

## Status

The fixes for all four are written and verified in a local build (job title
locked to one, tagline rewritten around the honest-validation result, hover
overlay and nav labels disabled on touch). They are **not on the live site yet**
— I stopped short of deploying so I could decide on the hero copy myself rather
than have it rewritten for me. This log gets the before/after evidence and the
commit hash once they ship.
