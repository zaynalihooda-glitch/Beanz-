#!/usr/bin/env python3
"""Build BEANZ static site: injects fonts/image into the templates and writes
index.html + portfolio.html to the repo root (self-contained, no external assets)."""
import base64, pathlib, urllib.parse

HERE  = pathlib.Path(__file__).resolve().parent
ROOT  = HERE.parent
FONTS = HERE / "assets" / "fonts"
IMG   = HERE / "assets" / "img"

# The homepage template links to the portfolio via this placeholder URL; we
# rewrite it to a relative link for the real site.
PORT_LINK_PLACEHOLDER = "https://claude.ai/code/artifact/319a5937-4cd7-49c8-908d-a7a24274bb3d"

FONT_TOKENS = {
    "__FR400__": "fr400.woff2", "__FR600__": "fr600.woff2", "__FR400I__": "fr400i.woff2",
    "__AR400__": "ar400.woff2", "__AR500__": "ar500.woff2", "__AR600__": "ar600.woff2",
}

def b64(path):
    return base64.b64encode(path.read_bytes()).decode()

def inject_fonts(html):
    for token, fname in FONT_TOKENS.items():
        html = html.replace(token, b64(FONTS / fname))
    return html

def encode_entities(html):
    # base64 blobs are ASCII, so encoding only non-ASCII chars is safe.
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in html)

FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<rect x="9" y="9" width="50" height="50" rx="15" fill="#B07C3F"/>'
    '<rect x="4" y="4" width="50" height="50" rx="15" fill="#2C5A48"/>'
    '<g fill="#F4F4F1"><path d="M30 22 C 30 12 40 10 41 13 C 41 20 34 24 30 22 Z"/>'
    '<ellipse cx="27.5" cy="34.5" rx="10.5" ry="14" transform="rotate(-16 27.5 34.5)"/></g></svg>'
)
FAVICON_URI = "data:image/svg+xml," + urllib.parse.quote(FAVICON, safe="")

def document(title, description, fragment):
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{title}</title><meta name="description" content="{description}">'
        f'<link rel="icon" href="{FAVICON_URI}"></head><body>'
    )
    return head + "\n" + fragment + "\n</body></html>"

def build():
    # Homepage -> index.html
    home = inject_fonts((HERE / "home.template.html").read_text())
    home = home.replace(PORT_LINK_PLACEHOLDER, "portfolio.html")
    (ROOT / "index.html").write_text(encode_entities(document(
        "BEANZ — Websites that get small businesses more customers",
        "BEANZ designs conversion-led websites for small businesses — get found, get trusted, get booked. Packages from £499.",
        home)))

    # Portfolio -> portfolio.html
    port = inject_fonts((HERE / "portfolio.template.html").read_text())
    port = port.replace("__FWH_JPG__", b64(IMG / "fwh_hero.jpg"))
    port = port.replace("__HOME__", "index.html")
    (ROOT / "portfolio.html").write_text(encode_entities(document(
        "BEANZ — Portfolio",
        "Recent websites designed and built by BEANZ, including the FWH Fitness case study.",
        port)))

    # Care plans -> care.html
    care = inject_fonts((HERE / "care.template.html").read_text())
    (ROOT / "care.html").write_text(encode_entities(document(
        "BEANZ — Care plans",
        "Monthly care plans for your BEANZ website — hosting, security, updates, content and support. No lock-in.",
        care)))

    for f in ("index.html", "portfolio.html", "care.html"):
        kb = round((ROOT / f).stat().st_size / 1024)
        print(f"built {f}  ({kb} KB)")

if __name__ == "__main__":
    build()
