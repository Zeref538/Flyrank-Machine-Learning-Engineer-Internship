# Break Your Own Site — where it breaks, and what I fixed

**John Andrei Martinez · General AI Fluency · Week 7**

**Live URL:** https://johnandrei.vercel.app

I went looking for cracks three ways: hitting URLs a stranger or a crawler would
try, reading the contact form's code line by line for inputs it does not defend
against, and checking what a pasted link actually shows. Everything below is a real
result from a real request, not a guess.

---

## How I probed it

One small shell script rather than clicking around, because a script re-runs after
every fix and clicking does not. `curl` fetches a URL from the command line;
`-o /dev/null` throws the page body away because I only want the status code, and
`-w "%{http_code}"` prints that code:

```sh
for u in / /nonexistent-page-xyz /robots.txt /sitemap.xml /cv.pdf \
         "/projects/../../etc/passwd" "/?q=%3Cscript%3E"; do
  printf "%-34s %s\n" "$u" \
    "$(curl -s -o /dev/null -w '%{http_code}' --max-time 25 "https://johnandrei.vercel.app$u")"
done
```

Result of that first run:

| URL | code | verdict |
|---|---|---|
| `/` | 200 | fine |
| `/nonexistent-page-xyz` | 404 | known limitation |
| `/robots.txt` | **404** | fix-now |
| `/sitemap.xml` | **404** | fix-now |
| `/cv.pdf` | 200 | fine |
| `/favicon.svg` | 200 | fine |
| `/projects/../../etc/passwd` | 403 | fine — the host blocks it |
| `/?q=<script>` | 200 | fine — React escapes it, nothing runs |

The `../../etc/passwd` one looks alarming, so it is worth explaining. `..` means
"go up one folder", so that URL asks the server to walk out of the website's own
directory and read a system file. It is the oldest trick there is. Vercel answers
403 (forbidden) without my code being involved at all, which is exactly what you
want — the defence sits below anything I could get wrong.

---

## Fix-now #1 — a shared link showed nothing

**Broken.** Grepping the served HTML for share tags returned exactly one line, a
plain description. No `og:` tags at all.

Those are Open Graph tags: the block of metadata LinkedIn, Slack, Discord and
Messenger read to build the preview card when someone pastes your link. With none
present the link renders as a bare grey box with a URL in it, which on a portfolio
you are sending to a recruiter reads as *broken site*.

**Fixed.** Added the full set — `og:title`, `og:description`, `og:image` with its
width, height and alt text, `twitter:card`, a `canonical` link, and a JSON-LD
`Person` block that tells Google the page is about a person rather than a generic
document.

I also had to make the image. An `og:image` wants 1200×630 and the only photo on
the site is 400×400; a small image gets rendered as a tiny thumbnail instead of the
wide card. So I generated one at `public/og-image.png` using the site's own dark
background and violet accent — photo, name, one job title, and the
honest-validation result in three lines.

One rule that catches people: **the image URL must be absolute.** `/og-image.png`
is silently ignored by every scraper. It has to be the full
`https://johnandrei.vercel.app/og-image.png`.

## Fix-now #2 — nothing told search engines the site exists

**Broken.** `robots.txt` and `sitemap.xml` both 404.

`robots.txt` is the first file a crawler asks for. Its absence is not fatal, since
Google will crawl anyway — but a `sitemap.xml` is how you hand a crawler the list
of pages instead of hoping it finds them, and the sitemap is normally announced
inside `robots.txt`. Missing both leaves findability to luck.

**Fixed.** Added both to `public/`, which Vercel serves at the site root.

## Fix-now #3 — the form accepted a message made of spaces

Found by reading the code, not by clicking, which is why I would otherwise have
missed it.

**Broken.** All three fields had the HTML `required` attribute. That only checks
the field is not an *empty string* — a single space satisfies it completely. So a
visitor or a bot could submit a name of `" "` and a message of `" "` and the form
would send it happily. I get a blank enquiry with no idea who it was from.

**Fixed.** Trim the whitespace off all three values first, refuse if anything is
then empty, and say so instead of failing silently. The trimmed values are what get
sent, too.

## Fix-now #4 — no spam defence at all

**Broken.** The form posts to FormSubmit.co with `_captcha: "false"` and had no
other filter. A public form with a visible email endpoint gets found by scrapers.

**Fixed.** Added a honeypot — an extra text field positioned off-screen, hidden
from screen readers with `aria-hidden` and skipped by the keyboard with
`tabIndex={-1}`. A person never sees it, so it stays empty. A bot fills in every
field it finds. Anything in that field and the submission is dropped, while the page
still shows "sent", because telling a bot it was caught only teaches whoever wrote
it.

Also capped the message at 5,000 characters and added `maxLength` to the name and
email inputs, so nobody can paste a novel into it.

## Fix-now #5 — the email placeholder was my own address

**Broken.** The name field said `John Andrei Martinez` and the email field said
`martinezjandrei8425@gmail.com`. Placeholders are meant to be examples, but greyed
text inside a form reads as *already filled in*. Someone could reasonably think the
form was prefilled and submit it without ever typing their own address — and I would
receive an enquiry from myself.

**Fixed.** Now `your name` and `you@company.com`.

## Double submit — already safe, checked anyway

The submit button is `disabled={status === "sending"}`, so the second click of a
fast double-click lands on a dead button. Nothing to fix. Worth checking rather than
assuming, since this is exactly where most forms send two emails.

---

## Speed

| measure | value |
|---|---|
| time to first byte | **0.12 s** |
| HTML document | 1.2 KB |
| largest script | 250 KB raw / **94 KB gzipped** |
| all JavaScript | 559 KB raw / ~200 KB gzipped |
| CSS | 54 KB raw / 10.6 KB gzipped |

Nothing here needs an emergency. It is a single page served from a CDN, and 0.12 s
to first byte means the network is not the problem. The JavaScript is the heaviest
part and most of it is the animation libraries — GSAP and Motion, about 167 KB raw
between them. That is a real cost for the visual style and I am choosing to keep it,
but I would rather write it down as a known trade-off than pretend the number is not
there.

---

## Known limitations — real, and not hidden

- **A wrong URL gets Vercel's plain 404, not a page of mine.** It is a one-page site
  so there are no sub-pages to mistype. The fix is a custom 404 that bounces back to
  the homepage. Low value, so it is on the list rather than done.
- **The animation libraries are ~167 KB of the payload.** Deliberate. If the site
  ever needs to load fast on a bad connection, that is the first thing to cut.
- **`alfred-demo.webp` is still 931 KB**, down from 3.6 MB but still the largest
  single asset on the site.
- **The two Render-hosted demos sleep** after 15 minutes idle and take about 30
  seconds to wake. Both are labelled so a visitor knows to wait; I cannot fix the
  free tier itself.
- **Rate limiting on the form is FormSubmit's, not mine.** The honeypot stops dumb
  bots. A determined person could still submit repeatedly and I would find out from
  my inbox.
- **I have not opened it in Safari on a real iPhone.** Everything mobile so far is a
  real browser at a phone's exact size, which finds layout problems reliably but is
  not the same as iOS Safari on real hardware.

---

## Hardening review

Submitted alongside the Week-6 design review, and that reviewer found two things
this probe did not — both on a real phone. The nav bar looked broken, and the
projects section would not scroll.

The scroll one turned out to be the most serious bug on the site. A phone has no
mouse, so tapping something makes the browser fake a hover and leave it stuck there.
Each project card has a detail panel covering the whole card, and that panel is
itself scrollable. Tap while scrolling, the hover latches, the panel appears, and now
your finger is dragging that little panel instead of the page. The page stops. Nobody
on a phone could scroll past the projects to reach the contact form — the one action
the whole site is for.

Both are fixed in the same commit as the work above, inside an `@media (hover: none)`
block, which is the CSS rule for "only apply this where hovering is not a real thing".

That is the argument for letting someone else try it. My script tested what I thought
to test. A thumb on glass found the one that actually blocked the goal.
