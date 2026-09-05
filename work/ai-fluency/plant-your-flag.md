# Plant Your Flag — domain, analytics, launch hygiene, badge

**John Andrei Martinez · General AI Fluency · Week 7**

**Live address:** https://johnandrei.vercel.app

---

## The address

I am on the free `vercel.app` subdomain, not a bought domain. The brief allows this
("a clean free subdomain is an acceptable fallback"), and the portal Q&A confirms a
host's own free subdomain qualifies. Budget is the honest reason — a `.com` is a
recurring cost I am not carrying while I am still a student.

**HTTPS is not optional and not something I configured.** Vercel issues and renews
the certificate itself and redirects plain HTTP to HTTPS, so there is no way to
reach the site over an unencrypted connection. Verified from the command line:

```sh
curl -sI http://johnandrei.vercel.app | head -1     # -> 308 redirect
curl -s -o /dev/null -w "%{http_code}\n" https://johnandrei.vercel.app   # -> 200
```

The one thing a real domain would buy me is that the address stops naming my host.
`johnandrei.com` says nothing about where it lives, so I could move off Vercel
tomorrow and nobody's bookmark breaks. That is the actual argument for a custom
domain, and it is the reason I will buy one — not because it looks more serious.

## Analytics

Installed Vercel Web Analytics and Speed Insights — two small packages, one line
each in `src/main.jsx`:

```jsx
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/react";
```

Why these two rather than Google Analytics: they count visits without setting a
cookie and without building a profile that follows someone across other sites,
which means no consent banner and nothing to explain to a visitor. The trade-off is
real — I get page views, referrers and countries, not the deep funnel analysis GA
would give me. For a one-page portfolio, "did anyone actually open this, and where
did they come from" is the entire question.

Speed Insights is the one I care more about. It reports the load speed *real
visitors* get on their own phones and connections. My own machine on my own wifi is
not a measurement of anything — it is the best case, measured by the person least
able to be objective about it.

**Both stay silent until the toggles are switched on in the Vercel dashboard**
(Project → Analytics → Enable, and the same for Speed Insights). That is a
deliberate design on Vercel's side: the code ships, the collection does not start
until the project owner opts in.

## Launch hygiene — checked on the real address, not locally

Everything below was verified with a request to the live server, because a build
that is correct on my laptop and never reached the host is the exact mistake worth
guarding against.

| item | status | evidence |
|---|---|---|
| page title | correct | `John Andrei Martinez — Machine Learning Engineer` in the served HTML |
| description | correct | rewritten around the honest-validation result |
| favicon | correct | `/favicon.svg` returns 200 |
| share preview image | correct | `/og-image.png` returns 200, 75,652 bytes, 1200×630 |
| Open Graph tags | correct | `og:title`, `og:description`, `og:image` + width/height/alt |
| Twitter card | correct | `summary_large_image` |
| canonical URL | correct | points at the https address |
| `robots.txt` | correct | 200, allows everything, announces the sitemap |
| `sitemap.xml` | correct | 200 |
| HTTPS | correct | http redirects, https serves 200 |

The share preview is the one worth dwelling on. Before this week the site had no
`og:` tags at all, so pasting the link into LinkedIn produced a grey box with a URL
— which reads as a broken site to the exact person you most wanted to impress. The
full write-up of that fix, including the trap where a relative image path is
silently ignored, is in
[break-your-own-site.md](break-your-own-site.md).

## The FlyRank badge

Installed in the footer as a self-contained inline SVG inside an `<a>`, linking to
https://internship.flyrank.ai/verify. Inline rather than a hotlinked image on
purpose: an image hosted on someone else's server becomes a broken box in my footer
the day they move the file, and I would not notice for months.

**Honest note on this one.** The badge's proper link carries a credential ID on the
end of the verify URL, and I do not have one yet — FlyRank issue the completion
certificate around mid-September, and the portal Q&A tells interns to submit without
it and update afterwards. So the badge currently links to the plain verification
page. It claims the internship, which is true; it does not claim a certificate I do
not hold. The ID slot is marked with a comment in `FooterTerminal.jsx` so it is a
one-line change when the certificate lands.

## Still mine to do

- Open the final address on a real phone once more. The mobile work so far is a
  real browser at a phone's exact size, which is not the same as a thumb on glass.
- Flip the Analytics and Speed Insights toggles in the Vercel dashboard, then
  screenshot the dashboard once it has data in it.
- Add the credential ID to the badge link when the certificate is issued.
- Buy the domain when the budget is there, for the portability reason above rather
  than the appearance one.
