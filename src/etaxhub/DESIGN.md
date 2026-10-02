# eTax Hub — design system

## Grounded in her world
A London cloud accountancy practice run by one chartered accountant, built on Xero.
Her clients buy software all day: Xero, Stripe, Shopify, Notion. They are used to
interfaces that are clean, bright and get out of the way. So the page should feel like
a well-made piece of software, not a solicitor's letterhead — but the credibility of
"chartered, 17 years" has to carry too.

Three words: **precise, bright, trustworthy.**

## Direction chosen
Three were considered:
- *Quiet authority* — navy and serif, feels like an old high-street firm. Rejected: she
  is explicitly a modern digital practice, it would fight her positioning.
- *Bold and modern* — near-black with one bright blue. Rejected: too close to a SaaS
  startup, undersells the chartered credential.
- **Clean and clinical (CHOSEN)** — deep navy structure, her own bright blue reserved
  for action, generous white, a serif only for headings so the practice still reads as
  professional rather than as an app.

## Palette — sampled from her own logo, every pair computed
Her logo blue is **#24B4E4** (sampled from the archived mark, 30,038px dominant). That
is within a shade of Xero's blue, almost certainly on purpose, so the page leans into it
rather than away.

| Token | Hex | Use |
|---|---|---|
| paper | `#F8FAFB` | page ground |
| ink | `#0C2531` | body text |
| muted | `#4A6472` | secondary text |
| primary | `#0B3A52` | headings, the dark band |
| accent | `#5B8CA6` | rules, icons, small marks |
| wash | `#E7F2F8` | tinted section ground |
| **cta** | **`#24B4E4`** | **buttons only — nowhere else** |

Her brand blue is the action colour. Nothing else on the page uses it, so when it
appears the eye already knows it means "click".

**Contrast, computed not guessed:**
- ink on paper 15.14:1 · muted on paper 5.98:1 · ink on wash 13.93:1
- muted on wash 5.50:1 · white on primary 12.06:1 · primary on paper 11.52:1
- **CTA label is ink on blue at 6.59:1.** White on that blue is 2.41:1 and FAILS, so the
  buttons use dark text. That is a deliberate decision, not an oversight.

## Type
- **Headings: Fraunces** (400/600). A serif with real character — carries "chartered,
  13 years" without looking like a 1990s practice.
- **Body: IBM Plex Sans** (400/500/600). Drawn for technical documents and numbers, which
  is exactly what this is.
- Both inlined as base64 woff2. The site CSP is `font-src 'self' data:`, so a Google
  Fonts link would be silently blocked and everything would fall back to Georgia.
- Not Inter and not Newsreader: those are BEANZ's own faces, reserved for BEANZ-branded
  work. Not Outfit or Instrument Serif either, which are Chef House's — client sites
  must not look like rebrands of each other.
- No condensed display faces. Her old site used Bebas Neue at 62px, which read as a gym
  flyer rather than a chartered practice.
- h1 clamp 2.4rem → 4.1rem. Body 18px. Line height 1.1 headings, 1.65 body.
- No eyebrow labels. No tracked uppercase anywhere.

## The one bold move
**The problem list.** Six lines, set large, one per line, full width, each with a thin
accent rule. It is the section prospects react to and it is the only place on the page
that shouts. Everything else stays calm so it reads.

## Rhythm
- 8px scale. Sections 112px desktop / 64px mobile.
- Grounds cycle: paper → wash → paper → **primary band (packages)** → paper.
- Max width 1140px, text measure capped at 62ch.
- Radius 10px everywhere. One soft shadow level, used only on the package cards.

## Logo
Rebuilt as inline SVG. Hers was a 256×260px JPEG with no transparency, sitting over the
hero with a visible pale box around it. The SVG version scales, has a real transparent
ground, and sits at a sane 40px in the header.

## Motion
A hover and focus state. Nothing else. `prefers-reduced-motion` respected.

## Images
No stock photography. There is a clearly marked slot for a real headshot of Sadaf — her
old site used a phone photo taken against a bright window, so her face was in shadow.
A proper portrait is the single cheapest improvement available to her.
