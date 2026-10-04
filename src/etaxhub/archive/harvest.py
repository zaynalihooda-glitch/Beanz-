#!/usr/bin/env python3
"""Pull eTax Hub's own written content out of the Wayback Machine.

Deliberately does NOT take the 272-page /resources/ library or the calculators.
Those are the totalSOLUTION template's shared content, identical across every
firm on it, licensed from the vendor rather than owned by eTax Hub. Rebuilding
them would recreate the duplicate-content problem and would not be ours to copy.
"""
import urllib.request, urllib.error, re, html, time, pathlib, json

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
HERE = pathlib.Path(__file__).resolve().parent

GEN1 = ["/home", "/about-us", "/contact-us", "/packages", "/faqs", "/free-tax-advice", "/xero",
        "/sectors", "/sectors/contractors", "/sectors/ecommerce-business", "/sectors/hospitality",
        "/sectors/manufacturing", "/sectors/media-and-technology", "/sectors/medical-profession",
        "/sectors/medical-profession/consultants", "/sectors/medical-profession/dentists",
        "/sectors/medical-profession/gp-practices", "/sectors/medical-profession/hospital-doctors",
        "/sectors/medical-profession/locums", "/sectors/medical-profession/salaried-gps",
        "/sectors/owner-managed-business", "/sectors/professional-services",
        "/sectors/property-and-construction", "/sectors/retail",
        "/services", "/services/bookkeeping", "/services/business-start-ups",
        "/services/company-secretarial", "/services/corporation-tax",
        "/services/final-accounts-preparation", "/services/payroll",
        "/services/personal-tax", "/services/vat-returns"]

GEN2 = ["/", "/about-us/", "/packages/", "/contact-us/", "/services/", "/xero-page-info/",
        "/contractors/", "/ecommerce-business/", "/hospitality/", "/manufacturing/",
        "/media-and-technology/", "/medical-profession/", "/owner-managed-business/",
        "/professional-services/", "/property-construction/", "/retail/"]


def get(url, timeout=60, tries=6):
    """The Wayback Machine rate limits hard. Back off and keep going."""
    delay = 8
    for attempt in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get('Retry-After') or delay)
                print(f"      429, waiting {wait}s", flush=True)
                time.sleep(wait); delay = min(delay * 2, 120); continue
            if e.code == 404:
                return None
            time.sleep(delay); delay = min(delay * 2, 120)
        except Exception:
            time.sleep(delay); delay = min(delay * 2, 120)
    return None


def clean(raw):
    s = raw.decode('utf-8', 'replace')
    s = re.sub(r'<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->', '', s, flags=re.S | re.I)
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S | re.I)
    title = re.search(r'<title>(.*?)</title>', s, re.S)
    title = html.unescape(title.group(1).strip()) if title else ''
    heads = [(m.group(1).upper(), html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip())
             for m in re.finditer(r'<(h[1-4])[^>]*>(.*?)</\1>', s, re.S | re.I)]
    heads = [(t, h) for t, h in heads if h]
    body = html.unescape(re.sub(r'<[^>]+>', '\n', s))
    body = re.sub(r'\n[ \t]*\n+', '\n', body)
    lines = [l.strip() for l in body.split('\n') if l.strip() and len(l.strip()) > 2]
    return title, heads, lines


def harvest(paths, host, ts, outdir, label):
    out = HERE / outdir
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for i, p in enumerate(paths, 1):
        url = f"https://web.archive.org/web/{ts}/https://{host}{p}"
        raw = get(url)
        name = (p.strip('/').replace('/', '__') or 'index') + '.txt'
        if not raw or len(raw) < 3000:
            print(f"  [{i:>2}/{len(paths)}] MISS {p}")
            index.append({'path': p, 'ok': False})
            time.sleep(6); continue
        title, heads, lines = clean(raw)
        txt = [f"SOURCE: {url}", f"PATH:   {p}", f"TITLE:  {title}", "", "--- HEADINGS ---"]
        txt += [f"  {t}: {h}" for t, h in heads]
        txt += ["", "--- TEXT ---"] + lines
        (out / name).write_text('\n'.join(txt))
        print(f"  [{i:>2}/{len(paths)}] ok   {p}  ({len(lines)} lines)")
        index.append({'path': p, 'ok': True, 'title': title, 'file': name, 'headings': len(heads)})
        time.sleep(6)
    (out / '_index.json').write_text(json.dumps({'label': label, 'host': host, 'pages': index}, indent=2))
    got = sum(1 for x in index if x['ok'])
    print(f"  -> {got}/{len(paths)} saved into {outdir}/\n")
    return got


if __name__ == "__main__":
    print("GENERATION 1 (totalSOLUTION, 2021) — her own pages only, not the shared library")
    harvest(GEN1, "www.etaxhub.co.uk", "20210511", "gen1", "totalSOLUTION 2021")
    print("GENERATION 2 (WordPress/Salient, 2025)")
    harvest(GEN2, "etaxhub.co.uk", "20250330", "gen2", "WordPress 2025")
