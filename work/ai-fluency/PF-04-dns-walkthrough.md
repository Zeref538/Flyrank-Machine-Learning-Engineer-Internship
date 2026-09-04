# PF-04 — DNS Walkthrough

**John Andrei Martinez · General AI Fluency · Week 5**

**Live site:** https://johnandrei.vercel.app — Vercel free hobby tier, HTTPS automatic.

I checked it rather than trusting that it works:

```
$ curl -o /dev/null -w "status=%{http_code} tls=%{ssl_verify_result}\n" https://johnandrei.vercel.app
status=200 tls=0
```

`tls=0` means the certificate verified with no errors. That's the padlock, from
the command line instead of from squinting at the browser.

---

## What DNS actually does

Every computer on the internet is found by a number, not a name. My site lives on
machines at `216.198.79.67` and `64.29.17.67`. Nobody is going to type that.

DNS is the system that turns the name you type into that number. It is the
internet's directory service: you hand it `johnandrei.vercel.app`, it hands back
an address, and only then can your browser go knock on the door.

The part that surprised me is that your computer doesn't hold this directory.
Almost nothing does. The information is spread across thousands of machines and
gets assembled on demand, in about a tenth of a second, every single time.

## What a CNAME record is

A **record** is one line in that directory. Several kinds exist; two matter here.

An **A record** holds a real address — a number, the final answer.

A **CNAME record** holds a *name* instead. It is a signpost: this name is really
that other name, go ask about that one. Whoever reads it has to do a second
lookup before they have anything useful.

That sounds like a pointless extra hop until you own a name but not the machines.
If I ever connect a custom domain, I still won't run the servers my site sits on —
Vercel does, and their addresses can change whenever they like. They replace
hardware, add capacity, send people to a nearer data centre. Had I written
`216.198.79.67` into an A record and Vercel retired that machine, my site would go
dark and nothing would tell me why. A CNAME hands that problem back to the people
who can actually fix it. They change the number behind the name; my record never
moves.

One limit worth knowing: a CNAME can't sit on a bare domain like `example.com`
itself. The rules won't let a CNAME share a name with the other records a root
domain needs, such as its mail records. On a subdomain it's fine —
`www.example.com`, `me.example.com` — which is where it's normally used anyway.

## What happens between typing an address and the page loading

Someone types `johnandrei.vercel.app`. Nobody has visited it from that machine
before, so nothing is remembered anywhere. Here is the whole chain.

**1. The browser checks its own memory,** then the operating system's. Both empty.

**2. It asks a resolver.** A **resolver** is the service that does the legwork of
finding an answer for you. Mine is my own router:

```
Server:  globebroadband.net
Address: 192.168.254.254
```

which passes the question on to my internet provider. My browser asks one question
and then waits. Everything below happens on the resolver's side, not mine.

**3. The resolver starts at the top.** It doesn't know `vercel.app`, so it asks
the **root servers**, the machines sitting at the top of the whole system. They
don't know either — but they know who handles anything ending in `.app`.

**4. It asks the `.app` servers.** They don't know my site either. They do know
which machines are in charge of `vercel.app`, and they say so.

**5. It asks those machines.** A **nameserver** is a machine holding the real
records for a domain. Vercel's are:

```
$ nslookup -type=NS vercel.app
vercel.app  nameserver = ns1.vercel-dns-3.com
vercel.app  nameserver = ns2.vercel-dns-3.com
vercel.app  nameserver = ns3.vercel-dns-3.com
vercel.app  nameserver = ns4.vercel-dns-3.com
```

Four of them, so three can fail and the site still answers.

**6. The record comes back.** For my site that's the two addresses:

```
$ nslookup johnandrei.vercel.app
Addresses:  216.198.79.67
            64.29.17.67
```

Had it been a CNAME instead, the answer would have been another *name*, and the
resolver would quietly repeat steps 3 to 6 for that name before it had any number
at all. The browser never sees the difference. It just waits a little longer.

**7. The browser connects, and asks for me by name.** It opens an encrypted
connection to that address and, while setting it up, states which site it wants.
That matters more than it looks: thousands of sites share those addresses, and the
name is how Vercel knows which certificate to present and which site to serve.

**8. Certificate, then page.** Vercel shows the certificate it issued for my
domain. The browser checks that it covers the name asked for and hasn't expired,
shows the padlock, and only then requests the actual page.

**9. Everyone writes the answer down.** Each response is kept for a set time,
called its TTL. The next visitor in the next few minutes skips steps 3 to 6
entirely.

That last step is also the honest answer to "why isn't my new domain working
yet?" Usually nothing is broken. Some resolver between you and the site is still
holding an older answer until its timer runs out. There's nothing to fix. You wait.

## Where I'd start if it broke

One command tells you whether the problem is DNS at all:

```
nslookup yourdomain.com
```

No address back means nothing else matters yet — the browser never got far enough
to reach any host, so there's no point poking at hosting settings. An address
back means DNS did its job and the fault is further along: the host, the
certificate, or the site itself. That single check saves you from debugging the
wrong half.

---

## Every file in the deployed site

The brief asks that I can explain what I deployed. It's a React site built by
Vite and hosted on Vercel. Pushing to `main` on `Zeref538/portfolio` rebuilds and
republishes it in about a minute.

- **`index.html`** — the shell. One empty `<div id="root">` and one script tag.
  Vite fills in the built filenames during the build.
- **`src/main.jsx`** — puts the app inside that empty div.
- **`src/App.jsx`** — the whole page. It loops over the lists in `data.js`, so
  every section is generated from data instead of typed out by hand.
- **`src/data.js`** — all the content, as plain lists: `profile`, `experience`,
  `projects`, `skills`, `certifications`, `education`. Adding a project means
  adding one object here and nothing else.
- **`src/index.css`** — the colours and fonts from my identity kit
  (`--bg: #07090d`, `--accent: #8b5cf6`, Sora for headings, Inter for body) plus
  every layout rule.
- **`src/components/`** — one file each: `Reveal` (fades sections in as you
  scroll), `BorderGlow` (the glow that follows your cursor along a card edge),
  `RotatingText` and `ScrollFloat` (animation), `ParticleField`, `Noise` (a grain
  overlay), `Cursor`, `ChatWidget`, `ContactForm`, `StatusBar`.
- **`src/skillIcons.jsx`** — matches a skill or issuer name to its icon.
- **`api/chat.js`** — a small program that runs on Vercel's machines rather than
  in your browser, which is the only reason my API key isn't public. It takes a
  visitor's question, finds the most relevant pieces of my portfolio in
  `api/_index.json`, and sends just those to the model.
- **`scripts/build-index.mjs`** — builds that index from `data.js`, my knowledge
  notes, and project READMEs. I run it by hand, which is a known weakness: a stale
  index makes the chatbot answer confidently from old content.
- **`public/`** — `cv.pdf`, the favicon, my photo, project screenshots, certificate
  badges. Served exactly as they are.
- **`vite.config.js`** — the React plugin, plus a setting that splits React and the
  animation libraries into their own files so editing my own code doesn't force
  visitors to re-download everything.
- **`dist/`** — the built output Vercel actually serves. Generated by the build; I
  never edit it.

Space for the FlyRank completion badge is already there — it goes in the hero,
next to the "training — ML Engineering Intern @ FlyRank AI" status line that's
live on the site now.
