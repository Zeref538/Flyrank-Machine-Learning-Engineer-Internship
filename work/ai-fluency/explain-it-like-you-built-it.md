# Explain It Like You Built It

**John Andrei Martinez · General AI Fluency · Week 5**

**The piece I picked:** the little chat box on my About section — zeref-bot. You
type a question about me, it answers. I picked it because for a while I couldn't
have told you what actually happens after you press enter, and because it's the
part of my site an interviewer is most likely to poke at: *"did you just glue
ChatGPT onto a page?"* I wanted to be able to say no, and mean it.

The file is `api/chat.js`, 187 lines.

---

## First thing that confused me: where does the answer come from?

My site is just files. HTML, CSS, JavaScript — sent to your browser, and your
browser draws them. There's no computer of mine sitting there thinking.

So if the bot's answer has to come from an AI model, and that model lives on
someone else's servers, something has to go *ask* it. And whatever asks it needs
a password — an API key. That's the whole problem in one sentence:

**If I put the key in my website's code, anyone can read it.**

Not "a hacker could." Anyone. Right-click, View Source, it's there. And then they
run up my bill.

## The fix: a tiny program that runs somewhere else

Vercel — where my site is hosted — lets you drop a file in a folder called `api/`
and it treats it differently. Instead of sending that file to your browser, it
keeps it and runs it on their machine, only when someone asks for it.

That's called a **serverless function**. The name is confusing. There *is* a
server; I just don't own it, don't set it up, and don't pay for it to sit idle.
It wakes up when a request comes in, runs, answers, and goes back to sleep.

So the shape is:

```
your browser  →  my function on Vercel  →  Azure OpenAI  →  back again
```

The key lives in that middle box, as an environment variable — a setting I typed
into Vercel's dashboard, not into any file. My browser code never sees it. That's
the entire reason this file exists.

## Second thing that confused me: how does it know about *me*?

The model was trained on the internet. It has never heard of me. So how does it
answer "what did he do at FlyRank?"

Short version: **I tell it, every single time, in the same message as your
question.** There's no memory and no training. Every request carries a briefing
document along with it.

The plain version of that would be: paste my entire portfolio into every message.
That works, and it's what I did first. But it's wasteful — you asked one question
and I'm sending my whole life story to answer it.

So the better version is what's in the file now, and it's the part I actually had
to be taught.

## The interesting bit: finding the right paragraphs by *meaning*

Before anything goes live, I run a script that chops my content into small chunks
— each project, each job, each FAQ answer. Right now that's **190 chunks**.

Then each chunk gets sent to a model that turns text into **numbers**. Not one
number — a list of **1,536** of them. That list is called an *embedding*, and the
useful property is this:

> Two pieces of text that *mean* similar things get similar lists of numbers,
> even if they share no words at all.

That's the whole trick, and it took me a while to believe it. "What computer
vision work has he done?" and "trained YOLOv8 on a custom 5-class dataset" don't
share a single important word. A keyword search finds nothing. But their number
lists come out pointing in nearly the same direction.

All 190 lists get saved into one file, `api/_index.json`. It's 5.6 MB of almost
nothing but numbers.

Then when you ask a question, the function does this (`api/chat.js`, lines 43–52):

1. Turn *your question* into a list of 1,536 numbers, the same way.
2. Compare it against all 190 saved lists.
3. Keep the closest 6.
4. Send only those 6 chunks to the model, with your question.

## How "closest" is measured, in plain terms

The comparison is a function called `cosine`, and it's 8 lines of ordinary
arithmetic — no library, no database:

```js
function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na  += a[i] * a[i];
    nb  += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1);
}
```

Here's the picture that finally made it click for me.

Think of two arrows starting from the same point. What we care about is **the
angle between them**, not how long they are. Same direction = same meaning.
Pointing apart = unrelated.

Length has to be ignored on purpose, because a long README and a one-line job
bullet can say the same thing — one is just wordier. The dividing at the end
(`/ Math.sqrt(na) * Math.sqrt(nb)`) is exactly that: it cancels out the lengths so
only direction is left. The answer comes out between -1 and 1, and bigger means
closer.

The `|| 1` on the end is a guard: if a list were somehow all zeros, we'd be
dividing by zero, which gives garbage. So use 1 instead. Small line, and I'd have
skipped it before this internship taught me what a divide-by-zero does to a
number you then sort by.

That's it. That's the "vector search." I expected a database. It's a loop, a
sort, and take the first 6.

## The part I got wrong, and how I found out

When I first wired up the model, it returned **nothing**. No error, no crash —
a successful response with an empty message. Which is the worst kind of broken,
because everything looks fine.

The model I use is `gpt-5-mini`, and it's a *reasoning* model — it thinks
privately before it writes, and that private thinking spends from the same token
budget as the visible answer. My budget was 1,200 tokens. It was using all 1,200
to think and had nothing left to say out loud.

One line fixed it:

```js
reasoning_effort: "minimal",
```

The comment above it in my file is there so future-me doesn't spend another
evening on it. I didn't guess this — I had to go read what the setting did. But
I understand it now, and it's a good lesson: "it returned successfully" is not
"it returned something."

## Two more things I put in on purpose

**A fallback.** If the index file is missing, or the embedding call fails, the
whole retrieval step is skipped and it sends the full portfolio instead
(lines 148–156). Slower and clumsier, but it answers. A broken clever path
shouldn't beat a working plain one.

**A rate limit.** 5 questions a minute, 15 a day, per visitor (lines 102–120).
Not for security — it's to stop one bored person refreshing my bill into the
ground. I know it's imperfect: it lives in memory, so it resets whenever the
function goes cold. It's a speed bump, not a lock, and I'd rather say that than
pretend otherwise.

## The one thing about it that's currently broken

`api/_index.json` says it was built on **2026-08-11**. Today is **2026-08-17**,
and I've added a whole project since — my FlyRank refresh-ranking work.

That project isn't in the index. So if you ask the bot about it, it will confidently
answer using only what it knew a week ago, and it won't tell you it's out of date.
The rebuild is a command I have to remember to run (`npm run index`).

That's the failure mode I hate most, and it's the same one this whole internship
keeps teaching me: not a crash, not an error message — a confident answer built
on stale input. It's on my "still ugly" list, and the real fix is to make the
rebuild part of the build so I can't forget it.

---

**What I'd tell a friend in one paragraph:** my site can't think, so it sends your
question to a small program on Vercel that holds the secret key. That program has
190 pieces of my portfolio pre-converted into lists of numbers, where similar
*meanings* produce similar numbers. It converts your question the same way, finds
the 6 closest pieces with about eight lines of arithmetic, and sends only those to
the AI along with your question. The AI isn't remembering me — it's reading a
short briefing I hand it every single time.
