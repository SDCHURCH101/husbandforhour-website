# Husband for an Hour — website

Fixed-price handyman service for the Fairbanks North Star Borough.
Static, no build step required to serve (plain HTML/CSS/JS).

## Structure
- `index.html`, `services.html`, `pricing.html`, `service-area.html`, `about.html`, `contact.html`
- `assets/styles.css`, `assets/app.js`, `assets/img/*`
- `robots.txt`, `sitemap.xml`
- `build.py` — generator that emits the HTML pages + sitemap from shared templates
- `pricebook.json` — full flat-rate price book (build input for the pricing page)

## Rebuild
```
python3 build.py
```
Regenerates all pages. `pricebook.json` is the data source for the pricing page; regenerate it from the source spreadsheet if prices change.

## Notes
- Quote/contact forms are demo mode (client-side). Wire to Formspree/Netlify Forms to receive submissions.
- `CNAME.ready` holds the intended custom domain. Do NOT rename to `CNAME` until cutting the domain over from the current host.
