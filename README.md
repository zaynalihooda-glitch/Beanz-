# BEANZ — beanzdesigns.com

Marketing website for **BEANZ**, a studio that builds conversion-led websites for small businesses.

- **Live:** https://beanzdesigns.com
- **Design:** "Stone & Pine" palette, Fraunces + Archivo type, structured on the StoryBrand framework.
- **Hosting:** Netlify (auto-deploys from this repo's `main` branch).

## What's in here

```
index.html            ← built homepage (served by Netlify)
portfolio.html        ← built portfolio page
src/
  home.template.html       ← editable source for the homepage
  portfolio.template.html  ← editable source for the portfolio
  build.py                 ← builds the two HTML files above
  assets/fonts/*.woff2     ← embedded webfonts
  assets/img/*.jpg         ← case-study images
```

## Making changes

Edit the templates in `src/`, then rebuild the site:

```bash
python3 src/build.py
```

Commit and push — Netlify redeploys automatically. To roll back, revert to an
earlier commit (or in Netlify → Deploys → publish an older deploy).
