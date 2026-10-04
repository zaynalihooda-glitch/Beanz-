# eTax Hub — archived content library

Source material for the full multi-page build, pulled from the Wayback Machine.

## What is here

| File | What it is |
|---|---|
| `gen2/index-HOMEPAGE.txt` | **The most valuable file.** The 2025 WordPress homepage: her most recent and best copy, 33 headings. |
| `gen2/packages-FULL.txt` | Packages page with the full per-tier feature lists. NOTE: carries the EARLIER prices, £70/£125/£160. |
| `gen2/contact-us.txt` | 2025 contact page. |
| `gen1/home.txt` | 2021 totalSOLUTION homepage. |
| `gen1/faqs.txt` | 2021 FAQs. |

## What is deliberately NOT here

The 272-page `/resources/` library and the 20 calculators from the 2021 site.
That is totalSOLUTION's shared template content, byte-identical across every
firm using it and licensed from the vendor rather than owned by eTax Hub.
Rebuilding it would recreate the duplicate-content problem rather than solve
anything, and it is not ours to copy.

## What could not be fetched

The Wayback Machine rate-limited the harvest hard (HTTP 429 on nearly every
request, backing off to two minutes and still failing). The run was stopped
after 3 of 49 pages.

Two things worth knowing before anyone retries:

1. **The 2025 WordPress site was barely archived at all.** A CDX query returns
   almost nothing beyond the homepage, so the sector pages, services and about
   page from that generation probably were never captured. They are likely
   unrecoverable from the archive.
2. **The 2021 pages mostly exist**, but they are template boilerplate rather
   than her writing, so the value is low.

To retry: `python3 harvest.py` once the rate limit resets, probably a day later.

## The structure worth rebuilding (from the 2025 homepage nav)

About us · About You (sector dropdown) · Services · Pricing · Xero · Contact

Ten sector pages: contractors, ecommerce, hospitality, manufacturing,
media and technology, medical profession, owner-managed business,
professional services, property and construction, retail.

The 2021 site also had **six medical sub-pages** that the 2025 rebuild dropped:
consultants, dentists, GP practices, hospital doctors, locums, salaried GPs.
That is the sharpest niching eTax Hub has ever had and it is the obvious
phase-two build.

## Ask Sadaf for

- The `7-mistakes` ebook. Wayback rarely stored PDF bodies; she is the likelier source.
- The testimonials. The 2025 homepage had an "Our Happy Customers" section
  including a named quote from **Martin Lalor**, plus a "Clients and Partners"
  row with a Starling Bank logo. She told us she has none; she has.
- Confirmation of the current prices.
