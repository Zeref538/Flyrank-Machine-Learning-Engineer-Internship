# Identity Kit — John Andrei Martinez

This documents the identity system already live on my portfolio (johnandrei.vercel.app), pulled straight from `src/index.css` and `public/favicon.svg` — decided once, so it doesn't get reinvented per page.

## Type

- **Heading:** Sora (free, Google Fonts)
- **Body:** Inter (free, Google Fonts)
- Two fonts, not a pile. Sora is geometric and a little technical for headings; Inter stays out of the way for reading body text.

## Palette

| Role | Hex | Swatch |
|---|---|---|
| Background (near-black) | `#07090d` | 🟫 |
| Text (near-white) | `#e6edf3` | ⬜ |
| Accent (main) | `#8b5cf6` | 🟣 |
| Surface (card background, a step off pure black) | `#0d1117` | ⬛ |
| Second accent (cyan) | `#22d3ee` | 🔵 |

**Correction, found by re-reading `index.css` instead of my own notes.** I wrote
this kit claiming one accent. There are two: the card border-glow blends
`#8b5cf6 → #22d3ee → #a78bfa`, so cyan is live on every card edge on the site.
Two accents isn't wrong — violet leads, cyan only ever appears inside a gradient,
never on its own — but a kit that under-reports what's shipping isn't a kit, it's
a wish. Documented rather than quietly deleted, because the drift is the lesson:
this is exactly how a "system" stops matching the site it describes.

Four colors, one accent used sparingly — for links, the cursor glow, and selection highlight — so the project screenshots and numbers stay the loudest thing on the page, not the UI.

## Logo / favicon

A lowercase "z" monogram (from Zeref538, my handle) in a rounded dark square, ringed in a faint accent stroke, with a small accent dot — same shape language as the terminal/ML aesthetic of the site itself. Lives at `public/favicon.svg`.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0a0c12"/>
  <rect width="63" height="63" x="0.5" y="0.5" rx="13.5" fill="none" stroke="#8b5cf6" stroke-opacity="0.45"/>
  <text x="30" y="45" font-family="ui-monospace, Consolas, monospace" font-size="38" font-weight="700" text-anchor="middle" fill="#e6edf3">z</text>
  <circle cx="47" cy="42" r="4.5" fill="#8b5cf6"/>
</svg>
```

## Style note (for the Claude Project)

> **Fonts:** Sora for headings, Inter for body. **Colors:** background `#07090d`, text `#e6edf3`, one accent `#8b5cf6` used sparingly (links, highlights, small UI details only). **Mood:** quiet dark-mode engineering terminal — calm and technical, never flashy, so the work is what a visitor actually looks at.
