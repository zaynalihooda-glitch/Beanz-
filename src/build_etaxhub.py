#!/usr/bin/env python3
"""Build the eTax Hub spec mock-up into /etaxhub/.

Spec work for a prospect, same pattern as build_chefhouse.py. The site-wide CSP in
_headers is `font-src 'self' data:` and `style-src 'self' 'unsafe-inline'`, so a Google
Fonts <link> is silently blocked and the page falls back to Georgia. The webfonts are
therefore inlined as base64 here.

noindex, nofollow, and deliberately not in PAGES_FOR_SITEMAP: this is unsolicited spec
work for a firm that has not signed anything, and it must never compete with eTax Hub
in search.

    python3 src/build_etaxhub.py
"""
import base64, pathlib

HERE  = pathlib.Path(__file__).resolve().parent
ROOT  = HERE.parent
SRC   = HERE / "etaxhub"
FONTS = HERE / "assets" / "fonts"
OUT   = ROOT / "etaxhub"

TOKENS = {
    "__FRAUNCES400__": "etax-fraunces-400.woff2",
    "__FRAUNCES600__": "etax-fraunces-600.woff2",
    "__PLEX400__":     "etax-plex-400.woff2",
    "__PLEX500__":     "etax-plex-500.woff2",
    "__PLEX600__":     "etax-plex-600.woff2",
}


def build():
    html = (SRC / "index.src.html").read_text()
    for token, fname in TOKENS.items():
        path = FONTS / fname
        if not path.exists():
            raise SystemExit(f"missing font: {path}")
        html = html.replace(token, base64.b64encode(path.read_bytes()).decode())

    left = [t for t in TOKENS if t in html]
    if left:
        raise SystemExit(f"unreplaced tokens: {left}")

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(html)

    # Sadaf's own photo, cropped square for the circular avatar.
    (OUT / "sadaf-avatar.jpg").write_bytes((SRC / "sadaf-avatar.jpg").read_bytes())
    kb = round((OUT / "index.html").stat().st_size / 1024)
    print(f"built etaxhub/index.html  ({kb} KB)")


if __name__ == "__main__":
    build()
