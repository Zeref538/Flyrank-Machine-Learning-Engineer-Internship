# Retrospective — written to the version of me who started this

**John Andrei Martinez · FlyRank AI Internship · September 2026**

---

You are about to open a 30,000-row CSV and think the job is building a good model. It
is not, and finding that out is the internship.

## What you set out to do

Week 1 you wrote it down as: rank which content pages a team should fix first, and
beat the baseline. You pictured the finish line as a number.

You do build it — gradient boosting, Precision@50 of 0.88. And the paper you publish
concludes that **it did not beat the five-line rule you wrote in week four**. The rule
got 0.86, and the rule's own score wanders between 0.76 and 0.92 on nothing but how
tied pages get ordered. A two-point gap inside a sixteen-point noise band is not a
result. You will spend a while looking for a way to call it a win, and I am glad you
did not find one.

## What changed

**You stopped trusting numbers that had not been attacked.**

Week six. Same model, same data, same features — split the rows randomly and ROC-AUC
is 0.728; hold whole clients out and it is 0.618. Across eight draws the random split
won 8 out of 8. That gap is bigger than the difference between any two models you
tried: you could have tuned all internship and never made up what one line of
splitting code gave away.

Nothing clever happened there. You just asked whether the test measured what you
thought it did. That question is now the first one you ask.

**You started testing your own tests.**

You had a leak check. It passed. That meant nothing, and you knew it meant nothing,
so you deliberately broke it: put the banned label-derived column back in and re-ran.
ROC-AUC went to 1.000 with that one column taking 0.999 of the importance. *That* is
when the 0.618 became believable — not because the check passed, but because you had
proof the check could fail.

The habit spreads. By the end, every rule set carries a guard that each rule must
match at least one real row — which immediately caught two of mine that could never
fire, because the shortest eligible page is 692 words and I had written `< 600`.

**You got faster at being wrong.**

Week seven, a friend looked at your portfolio and you asked him what you do. He said
"full stack dev, or ML DevOps, or AI engineering" — three guesses. Your first instinct
was to explain. Your second, the right one, was to open the hero section and find it
rotates through three different job titles. He gave a list because the page gave him
one.

## What you would build next

The paper ends on a limitation you cannot argue away: one snapshot, nobody assigned
pages to be refreshed, so every claim is decision support and none of it causal. The
fix costs nothing but discipline — refresh a random half of the queue, leave the rest
alone, compare after ninety days. That is the next project, and the only thing that
turns "worth reviewing" into "we know what refreshing does".

Second: rebuild the queue on the warehouse release with real per-page edit dates. You
abandoned the decay question because the snapshot's staleness column is a per-client
crawl date wearing a per-page name — two values cover 70% of rows.

## Three things that transfer

**1. Decide how you will be judged before you build anything.**
The split was worth more than every modelling decision combined, and you make that
choice in the first hour, when it feels like admin. Measurement is not the boring part
around the work — it is the work, and everything downstream inherits what you got
wrong there.

**2. A check that has never failed is not a check.**
An untested smoke alarm and a broken one look identical from outside. Break your own
guard deliberately and watch it scream before you trust the silence. Same on the
website, where a CSS fix I was certain of did nothing at all — a media query adds no
specificity, so the plain rule further down the file kept winning.

**3. Report the number that makes you look worse, and say what it is next to.**
Precision without a base rate is decoration: 0.88 sounds excellent until you put
"against 0.551" beside it. And the finding you least want is reliably the one worth
most. Not as a moral position — because the alternative is defending a number you
cannot reproduce, in a room with someone who can check.

---

The thing I did not expect: this made me a worse forecaster of my results and a much
better one about my own work. I have no idea whether the next model will be good — but
a much clearer idea of whether I will be able to tell.

*Paper: https://zeref538.github.io/flyrank-ml-internship/ · Site: https://johnandrei.vercel.app*
