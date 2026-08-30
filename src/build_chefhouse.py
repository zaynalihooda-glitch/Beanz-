#!/usr/bin/env python3
"""Build the Chef House spec mock-up + proposal into /chefhouse/.

These two pages are written as Artifact bodies (no <html>/<head>/<body>, fonts
pulled from Google) so the same source can be published straight to an Artifact.
This script wraps them into standalone documents and inlines the webfonts as
base64, because the site-wide CSP in _headers is `font-src 'self' data:` and
`style-src 'self'` — a Google Fonts <link> would be silently blocked and the
pages would fall back to Georgia.

Both pages are noindex: this is unsolicited spec work for a business that has
not signed anything, and it must never compete with Chef House in search or
surface the pricing page publicly.

    python3 src/build_chefhouse.py
"""
import base64, pathlib, re, urllib.parse

HERE  = pathlib.Path(__file__).resolve().parent
ROOT  = HERE.parent
SRC   = HERE / "chefhouse"
FONTS = HERE / "assets" / "fonts"
OUT   = ROOT / "chefhouse"

BASE_URL = "https://beanzdesigns.com"

# The proposal links to the mock-up. In the Artifact build that is the Artifact
# URL; on the real site it is a sibling page.
ARTIFACT_MOCKUP_URL = "https://claude.ai/code/artifact/5b915a42-cad4-437d-addb-ab4b5e19cb05"


def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def face(family, fname, weight="400", style="normal"):
    return (
        f'@font-face{{font-family:"{family}";font-style:{style};'
        f'font-weight:{weight};font-display:swap;'
        f'src:url(data:font/woff2;base64,{b64(fname)}) format("woff2")}}'
    )


MOCKUP_FONTS = "".join([
    face("Instrument Serif", "instrument-400.woff2"),
    face("Instrument Serif", "instrument-400i.woff2", style="italic"),
    face("Outfit",           "outfit-var.woff2", weight="100 900"),
    face("Amiri",            "amiri-400ar.woff2"),
])

PROPOSAL_FONTS = "".join([
    face("Newsreader", "news-300.woff2",  weight="300"),
    face("Newsreader", "news-400.woff2",  weight="400"),
    face("Newsreader", "news-500.woff2",  weight="500"),
    face("Newsreader", "news-400i.woff2", weight="400", style="italic"),
    face("Newsreader", "news-500i.woff2", weight="500", style="italic"),
    face("Inter",      "inter-300.woff2", weight="300"),
    face("Inter",      "inter-400.woff2", weight="400"),
    face("Inter",      "inter-500.woff2", weight="500"),
    face("Inter",      "inter-600.woff2", weight="600"),
])

_CHEF_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44">'
    '<circle cx="22" cy="22" r="21" fill="#F7F1E4"/>'
    '<circle cx="22" cy="22" r="20" fill="none" stroke="#4F7038" stroke-width="1.4"/>'
    '<path d="M22 12.5c-3.4 2.1-5 5-5 8.2 0 3.1 2.2 5.4 5 5.4s5-2.3 5-5.4c0-3.2-1.6-6.1-5-8.2z" '
    'fill="none" stroke="#4F7038" stroke-width="1.6"/>'
    '<path d="M22 15.5v16" stroke="#4F7038" stroke-width="1.6" stroke-linecap="round"/>'
    "</svg>"
)
# Percent-encode the whole SVG: it contains double quotes, which would otherwise
# terminate the href attribute early.
CHEF_FAVICON = urllib.parse.quote(_CHEF_SVG, safe="")


def strip_google_fonts(html):
    """Remove the <title>, preconnects and Google Fonts <link> from the source.

    Returns (title_text, remaining_html). The title is lifted out so it can go
    in the real <head>.
    """
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = m.group(1).strip() if m else "BEANZ Designs"
    html = re.sub(r"<title>.*?</title>\s*", "", html, flags=re.S)
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)
    html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\s*', "", html)
    return title, html


def document(title, description, body, fonts, favicon, og_image, canonical):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="data:image/svg+xml,{favicon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<style>{fonts}</style>
</head>
<body>
{body}
</body>
</html>
"""


def build():
    OUT.mkdir(exist_ok=True)

    # ---- mock-up -> /chefhouse/index.html
    title, body = strip_google_fonts((SRC / "mockup.src.html").read_text())
    (OUT / "index.html").write_text(document(
        title=title,
        description=("Concept website for Chef House, the Indian, Chinese and Arabic "
                     "family restaurant on Al Jazeera Street, Doha."),
        body=body,
        fonts=MOCKUP_FONTS,
        favicon=CHEF_FAVICON,
        og_image=f"{BASE_URL}/chefhouse/og-mockup.jpg",
        canonical=f"{BASE_URL}/chefhouse/",
    ))

    # ---- proposal -> /chefhouse/proposal.html
    title, body = strip_google_fonts((SRC / "proposal.src.html").read_text())
    body = body.replace(ARTIFACT_MOCKUP_URL, "/chefhouse/")
    (OUT / "proposal.html").write_text(document(
        title=title,
        description=("What we found, the free mock-up, and what it would cost to "
                     "finish it. Prepared for Chef House, Doha."),
        body=body,
        fonts=PROPOSAL_FONTS,
        favicon=CHEF_FAVICON,
        og_image=f"{BASE_URL}/chefhouse/og-proposal.jpg",
        canonical=f"{BASE_URL}/chefhouse/proposal.html",
    ))

    for f in ("index.html", "proposal.html"):
        print(f"built chefhouse/{f}  {(OUT / f).stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
