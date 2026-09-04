# Make It Do Something

**John Andrei Martinez · General AI Fluency · Week 6**

**The one feature:** zeref-bot — the chat box in the About section of
[johnandrei.vercel.app](https://johnandrei.vercel.app). Ask it about my work, it answers
from my actual portfolio content.

**Why this one and not the contact form.** My site has a working contact form too, and I
tested it for this assignment (evidence below). But the interesting part of that form —
receiving the mail — is done by FormSubmit, a free service I point at. I wrote the form,
not the machinery behind it. With the chat box, the backend is my own code. Since the point
of this week is understanding a real feature end to end, I picked the one where the parts I
have to explain are mine.

---

## What a backend is

Everything I'd built before this was **frontend** — files sent to your browser, which your
browser draws. HTML for the words, CSS for how they look, JavaScript for what moves. All of
it lands on your machine, and anyone can read every line with right-click → View Source.

A **backend** is code that runs somewhere else — on a computer I don't sit in front of — and
sends back only the answer. You never see the code. That's the whole distinction: frontend
is the shopfront, backend is the kitchen. You order at the counter and food comes out; you
don't get to walk in and read the recipes.

For me it stopped being an abstract idea the moment I needed an API key. To ask an AI model
anything, I have to send a password with the request. If that password sits in frontend code,
it is public — not "a hacker could get it", but *anyone who right-clicks*. And then they run
up my bill.

So the key has to live somewhere the visitor can't reach. That's the backend, and that's why
mine exists. Not for cleverness. For one secret.

## What my feature does

A visitor types a question about me. The bot answers using only my real portfolio content —
my projects, jobs, certifications, and a couple of notes files. If it doesn't know, it's told
to say so and point at my email instead of inventing something.

The model itself has never heard of me. It wasn't trained on my portfolio and it has no memory
between messages. So every single time someone asks a question, I hand it a fresh briefing
along with the question. That's the trick the whole thing rests on.

## How the data flows

```
you type a question
        │
        ▼
  browser sends it to  /api/chat        ← my code, running on Vercel's computer
        │
        ├─ turns your question into 1,536 numbers  (an "embedding")
        ├─ compares it against 252 pre-computed chunks of my portfolio
        ├─ keeps the closest 6
        │
        ▼
  sends [those 6 chunks + your question + my instructions] to Azure OpenAI
        │                                   ↑
        │                     the API key is attached HERE, on the server,
        │                     where your browser never sees it
        ▼
  the model writes a reply
        │
        ▼
  my code sends back one line of text: {"reply": "..."}
        │
        ▼
  the chat box shows it
```

Two things about that picture that took me a while to get.

**The numbers step.** Before the site goes live I chop my content into small pieces — each
project, each job, each FAQ answer — 252 of them right now. Each piece gets turned into a list
of 1,536 numbers by a model built for exactly that. The useful property is that pieces which
*mean* similar things get similar lists, even when they share no words. "What computer vision
work has he done?" and "trained YOLOv8 on a custom 5-class dataset" have almost nothing in
common as text, but their number-lists point nearly the same direction. So I compare
directions, keep the closest six, and send only those. It saves sending my whole portfolio
with every question.

**Nothing is remembered.** There's no database of conversations. The bot isn't learning about
me over time. It's handed a briefing, answers, and forgets. If I change `data.js` and rebuild
the index, its knowledge changes; otherwise it stays exactly as it was.

## Evidence it actually works

Not a screenshot of my own browser — a request from the command line, so nothing about my
logged-in session or cached page can be helping it.

```
$ curl -X POST https://johnandrei.vercel.app/api/chat \
    -H "Content-Type: application/json" \
    -d '{"messages":[{"role":"user","content":"What did John build during the FlyRank internship?"}]}'
```

```json
{"reply":"At FlyRank AI John built a content refresh-priority scorer for real client search
data: he started with a hand-written rule baseline, then developed models evaluated on the
same held-out clients; queried a 9.8M-row monthly partition in DuckDB and authored the data
contract (eligibility gate, feature list, banned leakage columns); found and fixed a label
leak that falsely inflated ROC-AUC (0.612 -> 0.737 when the leak was present) and reported
honest metrics; and highlighted evaluation noise (Precision@50 swung 0.76-0.92 on
tie-breaking) so wins were reported with their uncertainty."}
```

`[http 200, 6.18s]`

Those numbers are real and they're mine — 9.8M rows, 0.612 to 0.737, the 0.76–0.92 swing all
come from my own notebooks. The bot is reading my actual work, not making up something
plausible about a student.

**The contact form, also tested** (not my submitted feature, but I'm not going to claim it
works without checking):

```
$ curl -X POST https://formsubmit.co/ajax/<my email> \
    -H "Origin: https://johnandrei.vercel.app" -d '{...}'
{"success":"true","message":"The form was submitted successfully."}
```

That message reached my Gmail.

**One thing that broke while testing, worth writing down.** My first attempt at the form came
back with *"Make sure you open this page through a web server, FormSubmit will not work in
pages browsed as HTML files."* Which sounds like my site is broken. It isn't. `curl` doesn't
send an `Origin` header — the field a browser adds saying which page you were on — so
FormSubmit couldn't tell where the request came from and guessed I was opening a file off my
desktop. Adding `-H "Origin: https://johnandrei.vercel.app"` fixed it instantly. The lesson I
keep relearning: read what the error is actually testing, not what it sounds like.

## Free tier

- **Vercel hobby** — hosts the site and runs `/api/chat`. Free.
- **Azure OpenAI** — the model. Not free per token, which is why the limits below exist and
  why I'm naming it instead of claiming the whole thing costs nothing.
- **FormSubmit** — free, no account needed.

To stop one bored visitor emptying my credit, the backend caps each person at **5 questions a
minute and 15 a day**, counted by their network address. I know the weakness: the count lives
in the function's memory, and that memory is wiped whenever the function goes cold. It's a
speed bump, not a lock. Good enough for a portfolio, and I'd rather write that down than
pretend it's airtight.

## What it can't do

It only knows what was in the index the last time I built it. That build is a command I run by
hand (`npm run index`), so if I add a project and forget, the bot answers confidently from
old knowledge and nothing warns anyone. Right now it's current — the answer above includes my
FlyRank work — but "current" is a thing I have to maintain, not a property of the system. The
real fix is to run the index build as part of the deploy so it can't drift, and that's the
next thing I'd change.
