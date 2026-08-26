#!/usr/bin/env python3
"""Build BEANZ static site: injects fonts/image into the templates and writes
the finished HTML (plus sitemap.xml, robots.txt, 404.html) to the repo root.
Everything is self-contained — no external asset requests, except the social
share image (og.jpg) which must be a real URL for link previews to work."""
import base64, pathlib, urllib.parse, datetime

HERE  = pathlib.Path(__file__).resolve().parent
ROOT  = HERE.parent
FONTS = HERE / "assets" / "fonts"
IMG   = HERE / "assets" / "img"

BASE_URL = "https://beanzdesigns.com"
TODAY    = datetime.date.today().isoformat()

# The homepage template links to the portfolio via this placeholder URL; we
# rewrite it to a relative link for the real site.
PORT_LINK_PLACEHOLDER = "https://claude.ai/code/artifact/319a5937-4cd7-49c8-908d-a7a24274bb3d"

FONT_TOKENS = {
    "__INTER400__": "inter-400.woff2", "__INTER500__": "inter-500.woff2",
    "__NEWS400__": "news-400.woff2", "__NEWS500__": "news-500.woff2",
    "__NEWS400I__": "news-400i.woff2", "__NEWS500I__": "news-500i.woff2",
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

OG_IMG = f"{BASE_URL}/og.jpg"

def document(title, description, fragment, slug="", extra_head=""):
    """slug is the page's path, e.g. '' for home or 'care.html'."""
    canonical = BASE_URL + ("/" + slug if slug else "/")
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{title}</title><meta name="description" content="{description}">'
        f'<link rel="canonical" href="{canonical}">'
        # Open Graph (Facebook, WhatsApp, iMessage, LinkedIn...)
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="BEANZ Designs">'
        '<meta property="og:locale" content="en_GB">'
        f'<meta property="og:title" content="{title}">'
        f'<meta property="og:description" content="{description}">'
        f'<meta property="og:url" content="{canonical}">'
        f'<meta property="og:image" content="{OG_IMG}">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="BEANZ Designs — websites that get small businesses more customers">'
        # Twitter / X
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{title}">'
        f'<meta name="twitter:description" content="{description}">'
        f'<meta name="twitter:image" content="{OG_IMG}">'
        '<meta name="theme-color" content="#2C5A48">'
        f'<link rel="icon" href="{FAVICON_URI}">'
        f'{extra_head}'
        '</head><body>'
    )
    return head + "\n" + fragment + "\n</body></html>"

# LocalBusiness structured data for the homepage (town-level only — no street
# address published). Helps Google understand this is a UK web-design business.
JSONLD_HOME = (
    '<script type="application/ld+json">'
    '{"@context":"https://schema.org","@type":"ProfessionalService",'
    '"name":"BEANZ Designs",'
    '"description":"Conversion-led websites for small businesses, with done-for-you StoryBrand copywriting, design and build.",'
    f'"url":"{BASE_URL}","image":"{OG_IMG}","email":"hello@beanzdesigns.com",'
    '"telephone":"+44 7415 325212",'
    '"areaServed":{"@type":"Country","name":"United Kingdom"},'
    '"knowsAbout":["Web design","Website copywriting","StoryBrand","Small business marketing","SEO"]}'
    '</script>'
)

PAGES_FOR_SITEMAP = ["", "care.html", "faq.html", "portfolio.html", "privacy.html", "terms.html"]

def write_sitemap():
    urls = "".join(
        f"<url><loc>{BASE_URL}/{p}</loc><lastmod>{TODAY}</lastmod>"
        f"<priority>{'1.0' if p=='' else '0.7'}</priority></url>"
        for p in PAGES_FOR_SITEMAP
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f'{urls}</urlset>')
    (ROOT / "sitemap.xml").write_text(xml)

def write_robots():
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )

FOUR04 = (
    '<style>'
    'html{color-scheme:light}'
    'body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;'
    'text-align:center;background:#F4F4F1;color:#1C231F;'
    'font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:40px}'
    '.b{max-width:460px}'
    '.mk{width:56px;height:56px;margin:0 auto 22px}'
    'h1{font-family:Georgia,"Times New Roman",serif;font-size:64px;margin:0 0 6px;color:#2C5A48;letter-spacing:-.02em}'
    'h2{font-family:Georgia,serif;font-weight:500;font-size:24px;margin:0 0 12px}'
    'p{color:#5E6B64;font-size:16px;line-height:1.6;margin:0 0 26px}'
    '.btn{display:inline-block;background:#2C5A48;color:#fff;text-decoration:none;'
    'font-weight:500;font-size:15px;padding:13px 24px;border-radius:9px}'
    '</style>'
    '<div class="b">'
    '<div class="mk"><svg viewBox="0 0 64 64"><rect x="9" y="9" width="50" height="50" rx="15" fill="#B07C3F"/>'
    '<rect x="4" y="4" width="50" height="50" rx="15" fill="#2C5A48"/><g fill="#F4F4F1">'
    '<path d="M30 22 C 30 12 40 10 41 13 C 41 20 34 24 30 22 Z"/>'
    '<ellipse cx="27.5" cy="34.5" rx="10.5" ry="14" transform="rotate(-16 27.5 34.5)"/></g></svg></div>'
    '<h1>404</h1><h2>Page not found</h2>'
    "<p>Sorry &mdash; the page you're looking for doesn't exist or has moved. "
    'Let\'s get you back on track.</p>'
    '<a class="btn" href="/">Back to home</a>'
    '</div>'
)

def build():
    # Homepage -> index.html
    home = inject_fonts((HERE / "home.template.html").read_text())
    home = home.replace(PORT_LINK_PLACEHOLDER, "portfolio.html")
    (ROOT / "index.html").write_text(encode_entities(document(
        "BEANZ — Websites that get small businesses more customers",
        "BEANZ designs conversion-led websites for small businesses — get found, get trusted, get booked. Packages from £495.",
        home, slug="", extra_head=JSONLD_HOME)))

    # Portfolio -> portfolio.html
    port = inject_fonts((HERE / "portfolio.template.html").read_text())
    port = port.replace("__FWH_JPG__", b64(IMG / "fwh_hero.jpg"))
    port = port.replace("__HOME__", "index.html")
    (ROOT / "portfolio.html").write_text(encode_entities(document(
        "BEANZ — Portfolio",
        "Recent websites designed and built by BEANZ, including the FWH Fitness case study.",
        port, slug="portfolio.html")))

    # Care plans -> care.html
    care = inject_fonts((HERE / "care.template.html").read_text())
    (ROOT / "care.html").write_text(encode_entities(document(
        "BEANZ — Care plans",
        "Monthly care plans for your BEANZ website — hosting, security, updates, content and support. No lock-in.",
        care, slug="care.html")))

    # FAQ -> faq.html
    faq = inject_fonts((HERE / "faq.template.html").read_text())
    (ROOT / "faq.html").write_text(encode_entities(document(
        "BEANZ — Frequently asked questions",
        "Common questions about working with BEANZ: our packages, done-for-you StoryBrand copy, timelines, ownership, care plans and more.",
        faq, slug="faq.html")))

    # Privacy Policy -> privacy.html
    privacy = inject_fonts((HERE / "privacy.template.html").read_text())
    (ROOT / "privacy.html").write_text(encode_entities(document(
        "BEANZ — Privacy Policy",
        "How BEANZ Designs collects, uses and protects your personal information, and the rights you have under UK GDPR.",
        privacy, slug="privacy.html")))

    # Terms of Service -> terms.html
    terms = inject_fonts((HERE / "terms.template.html").read_text())
    (ROOT / "terms.html").write_text(encode_entities(document(
        "BEANZ — Terms of Service",
        "The terms that apply when you buy a website or care plan from BEANZ Designs.",
        terms, slug="terms.html")))

    # Social share image (copied to root so /og.jpg resolves)
    (ROOT / "og.jpg").write_bytes((IMG / "og.jpg").read_bytes())

    # 404 page (Netlify serves /404.html automatically)
    (ROOT / "404.html").write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>BEANZ — Page not found</title><meta name="robots" content="noindex">'
        f'<link rel="icon" href="{FAVICON_URI}"></head><body>' + FOUR04 + '</body></html>')

    write_sitemap()
    write_robots()

    outputs = ("index.html", "portfolio.html", "care.html", "faq.html",
               "privacy.html", "terms.html", "404.html")
    for f in outputs:
        kb = round((ROOT / f).stat().st_size / 1024)
        print(f"built {f}  ({kb} KB)")
    print("built sitemap.xml, robots.txt, og.jpg")

if __name__ == "__main__":
    build()
