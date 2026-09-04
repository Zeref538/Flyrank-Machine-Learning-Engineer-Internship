# Open It on Your Phone — fix log

**John Andrei Martinez · General AI Fluency · Week 6**

**Live URL:** https://johnandrei.vercel.app

I audited at 390×844 (iPhone 14), then re-checked 768 and 1440 to make sure the mobile
fixes didn't break the wider layouts. Everything below is measured, not eyeballed — I ran
the measurements in a real browser and put the numbers next to each fix.

---

## 1. The nav bar was sliced off at the screen edge

**Broken.** On a 390px screen the floating top bar sat in a container 348px wide, but the
row inside it needed **379px** — a logo plus six 38px icons plus gaps and padding. Flex
items don't shrink on their own, so the row just ran past the edge and the last icon (copy
phone number) was cut in half.

Measured: `.nav-bar` right edge at **396px**, its container at **364px**, screen at 390px.

**Fixed.** Below 560px I hide the phone-copy button and grow the rest to **44px**, which is
the smallest comfortable thumb target. Both copy buttons still exist in the Contact section,
where there's room. Padding and gaps tightened so five 44px icons plus the logo fit even a
360px Android screen.

Measured after: bar right edge **363px**, container **364px** — inside, with a pixel spare.

## 2. My first attempt at that fix silently did nothing

Worth writing down because it cost me a build.

I added the mobile rules right next to the other nav CSS. Rebuilt, measured, and the icons
were *still* 38px. The rule was in the stylesheet — I checked by listing the loaded rules
from the browser — and the button had the right class. It just wasn't winning.

**A media query adds no strength to a rule.** My override sat around line 343; the plain
`.nav-icon { width: 38px }` sat around line 360. When two rules are equally specific, the
one written last wins, and "inside a media query" doesn't count as more specific. Moving my
block to the end of the file fixed it instantly.

I left a comment there explaining why it lives at the bottom, so nobody tidies it back up.

## 3. The chat box was fiddly to use with a thumb

**Broken.** Measured on the phone width:

| control | was | now |
|---|---|---|
| text input height | **16px** | 43px |
| input font size | 12.8px | **16px** |
| send button | 28×26 | 43×43 |
| suggestion chips | 25px tall | 36px |
| window dots | 10×10 | 34px hit area (dot still looks 10px) |

The font size is the one that isn't about looks. **Safari on iOS zooms the whole page in
when you focus an input smaller than 16px, and it doesn't zoom back out.** That's the sudden
jump you get on badly built mobile forms. 16px is the threshold that stops it happening.

For the three window dots I didn't make them bigger — they're a deliberate mac-window nod.
I gave each an invisible 34px pad around it instead, so the dot looks the same and the
tappable area is three times wider.

## 4. One image was 39% of the whole page's image weight

**Broken.** `alfred-demo.gif` was **3,600 KB** at 620×316. The site has 95 images totalling
9.3 MB, and that single file was over a third of it. GIF stores motion as whole frames with
almost no compression, so a short clip balloons.

**Fixed.** Converted to animated WebP with ImageMagick:

```
magick alfred-demo.gif -coalesce -layers optimize -quality 55 -define webp:method=6 alfred-demo.webp
```

**3,600 KB → 931 KB**, a 74% cut, with all **230 frames** kept. I verified the frame count
after converting rather than assuming — a silently truncated animation would have looked
fine in a still.

It's still the largest asset on the site by some way. Halving the frame rate would cut it
again, but I'd rather keep the demo smooth than chase the number.

## 5. Every link works — but two demos pretend to be broken

I checked all **47** outbound links in `data.js` (every repo, demo, and certificate) with a
script that requests each one and reports anything that isn't a 200.

**46 of 47 passed. One timed out** — `callback-ai.onrender.com`, after 25 seconds.

The diagnosis is the interesting part. I re-ran it alone with a longer timeout and got
**200 in 0.38 seconds**. Nothing is broken: Render's free tier puts an app to sleep after 15
minutes idle, and my first request had woken it up. My timeout was too short for a cold start,
not the site being down.

That's still a real problem for a visitor, though. Someone clicking "live demo" and staring
at a blank tab for 40 seconds concludes the project is dead. So I labelled both Render-hosted
demos **"live demo (free host, ~30s to wake)"**. The wait is the same; the impression isn't.

## 6. Checked and already fine — so I changed nothing

- **No sideways scrolling** at 390, 768, or 1440. The page content measured 380px wide on a
  390px screen. This is the most common mobile break and it wasn't there.
- **Contrast passes.** Body text is `rgb(139,152,169)` on `rgb(7,9,13)` — a ratio of
  **6.8:1**, against the 4.5:1 the accessibility standard asks for. Checked across eight
  different text styles; all the same, all passing.
- **No blurry images.** I compared each image's displayed width against its real pixel width
  across all 97 on the page. Zero were stretched more than 1.35×, so nothing is upscaled into
  mush.
- **Tablet and desktop unaffected.** My changes are inside a `max-width: 560px` block, and I
  confirmed at 768 and 1440 that the nav still shows all six icons at 38px.

**One false alarm worth admitting.** A phone screenshot showed the hero line reading
"Aspiring **Data Analyst**" with the text apparently printed twice and overlapping. It looked
badly broken. Before touching it I measured the elements: the hidden placeholder is
`visibility: hidden` and both boxes sit exactly on top of each other by design. The
screenshot had simply caught the rotating title mid-animation, one word sliding out as the
next slid in. I nearly "fixed" something that was working correctly, on the evidence of a
still frame.

## What's left for me

- **Open it on my actual phone.** Everything above is a real browser at a phone's exact size,
  which finds layout and sizing problems reliably — but it isn't a thumb on glass. Things a
  simulator can't tell me: whether the tap targets feel right in the hand, how the animations
  perform on a mid-range Android, and whether the address bar hiding on scroll shifts
  anything. That check is mine to do, and this log gets a note when it's done.
- The `alfred-demo.webp` is still 931 KB.
- The chat's window dots are real buttons that look decorative. The hit area is fixed; the
  affordance still isn't obvious.
