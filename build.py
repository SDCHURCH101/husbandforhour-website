#!/usr/bin/env python3
# Static site generator for Husband for an Hour (Fairbanks handyman).
# Emits 6 pages + robots.txt + sitemap.xml with shared header/footer/SEO.
import json, os, re

OUT="/tmp/husbandforhour"
BASE="https://www.husbandforhour.com"
NAME="Husband for an Hour"
PHONE="(907) 759-8080"
TEL="+19077598080"
EMAIL="hman@husbandforhour.com"
ADDR_CITY="Fairbanks"; ADDR_REGION="AK"; ADDR_ZIP="99707"; PO="PO Box 70200"
GEO=(64.8378,-147.7164)
YEAR="2026"
VER="11"  # asset cache-bust

# ---------------- inline icons ----------------
IC={
 "phone":'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "mail":'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield":'<path d="M12 2 4 5v6c0 5 3.4 8.5 8 10 4.6-1.5 8-5 8-10V5z"/><path d="m9 12 2 2 4-4"/>',
 "check":'<path d="M20 6 9 17l-5-5"/>',
 "wrench":'<path d="M14.7 6.3a4 4 0 0 0 5 5l-9 9a2.8 2.8 0 0 1-4-4z"/>',
 "drop":'<path d="M12 2.7C12 2.7 6 9 6 13.5a6 6 0 0 0 12 0C18 9 12 2.7 12 2.7z"/>',
 "zap":'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "paint":'<rect x="3" y="3" width="14" height="6" rx="1.5"/><path d="M17 6h2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-7v3"/><rect x="9" y="15" width="6" height="6" rx="1.5"/>',
 "door":'<path d="M5 21h14"/><path d="M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17"/><circle cx="14.5" cy="12" r="1"/>',
 "hammer":'<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 6.4 12 12l-2-2 5.6-5.6a2 2 0 0 1 2.8 0l1.2 1.2a2 2 0 0 1 0 2.8z"/>',
 "snow":'<path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="m9 4 3 3 3-3M9 20l3-3 3 3"/>',
 "home":'<path d="m3 10 9-7 9 7"/><path d="M5 9v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9"/><path d="M9 21v-7h6v7"/>',
 "building":'<rect x="4" y="2" width="16" height="20" rx="1.5"/><path d="M9 7h.01M15 7h.01M9 11h.01M15 11h.01M9 15h6v7"/>',
 "key":'<circle cx="7.5" cy="15.5" r="4.5"/><path d="m11 12 8-8 2 2-2 2 2 2-2 2-2-2-2 2"/>',
 "ruler":'<path d="M3 17 17 3l4 4L7 21z"/><path d="M7 11l2 2M11 7l2 2M9 15l1 1"/>',
 "sparkle":'<path d="M12 3 13.6 9 19 10.6 13.6 12.2 12 18 10.4 12.2 5 10.6 10.4 9z"/><path d="M19 15l.8 2.5L22 18l-2.2.5L19 21l-.8-2.5L16 18l2.2-.5z"/>',
 "pin":'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "star":'<path d="m12 2 3 6.5 7 .8-5.2 4.8L18.5 22 12 18.3 5.5 22l1.7-7.9L2 9.3l7-.8z"/>',
 "truck":'<path d="M3 6h11v9H3z"/><path d="M14 9h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
 "tag":'<path d="M3 7v5l9 9 7-7-9-9H4z" /><circle cx="7.5" cy="10.5" r="1.3"/>',
 "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
 "users":'<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.5a3 3 0 0 1 0 5.5M21 20a6 6 0 0 0-5-5.9"/>',
 "grid":'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 "lock":'<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
 "thermo":'<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/>',
 "calendar":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18z"/>',
 "menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',
 "chat":'<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/>',
 "leaf":'<path d="M11 20A7 7 0 0 1 4 13c0-6 7-9 16-9 0 9-3 16-9 16z"/><path d="M4 21c4-7 9-9 13-10"/>',
 "list":'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
}
def ic(n,cls=""):
    c=f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[n]}</svg>'

# ---------------- nav ----------------
NAV=[("index.html","Home"),("services.html","Services"),("pricing.html","Fixed Pricing"),
     ("service-area.html","Service Area"),("about.html","About"),("contact.html","Contact")]

def header(active):
    lis="".join(
      f'<li><a href="{u}" class="{"active" if u==active else ""}">{t}</a></li>' for u,t in NAV)
    lang=('<div class="lang"><button class="lang-btn" aria-label="Choose language">'
          +ic("globe")+'<span class="lang-label">English</span>'
          '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg></button>'
          '<div class="lang-panel"><input class="lang-search" type="text" placeholder="Search 80+ languages..." translate="no">'
          '<ul class="lang-list"></ul>'
          '<div class="lang-credit">Translation by Google</div></div></div>')
    return f'''<div class="util"><div class="wrap">
  <span class="u-item"><a href="tel:{TEL}">{ic("phone")}{PHONE}</a></span>
  <span class="u-item hide-sm"><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></span>
  <span class="u-spacer"></span>
  <span class="u-item hide-sm u-badge">{ic("shield")}Licensed &middot; Bonded &middot; Insured</span>
  <span class="u-item notranslate" translate="no">{lang}</span>
</div></div>
<header class="nav"><div class="wrap nav-inner">
  <a class="brand notranslate" href="index.html" translate="no" aria-label="{NAME} home">
    <img src="assets/img/logo.png" alt="{NAME} handyman logo" width="180" height="111"></a>
  <nav><ul class="nav-links">{lis}</ul></nav>
  <a class="nav-phone" href="tel:{TEL}">{PHONE}</a>
  <div class="nav-cta"><a class="btn btn-gold" href="contact.html">Get a Flat Quote</a></div>
  <button class="hamburger" aria-label="Menu">{ic("menu")}</button>
</div></header>'''

def footer():
    cols="".join(f'<a href="{u}">{t}</a>' for u,t in NAV)
    svc=["Kitchen &amp; Bath Repairs","Doors &amp; Windows","Drywall &amp; Paint",
         "Plumbing &amp; Drains","Electrical &amp; Fixtures","Arctic &amp; Winter Prep",
         "Hanging &amp; Assembly","Flooring &amp; Trim"]
    svccol="".join(f'<a href="services.html">{s}</a>' for s in svc)
    return f'''<footer class="ft"><div class="wrap">
  <div class="ft-grid">
    <div>
      <img class="flogo" src="assets/img/logo.png" alt="{NAME}">
      <p>Fixed-price handyman service for the Fairbanks North Star Borough. Know the price before we start, no time-and-materials surprises.</p>
      {seal(txt="")}
      <div class="ft-badges"><span>Licensed</span><span>Bonded</span><span>Insured</span><span>W-9 &amp; COI on request</span></div>
    </div>
    <div><h4>Pages</h4>{cols}</div>
    <div><h4>Services</h4>{svccol}</div>
    <div class="ft-contact"><h4>Contact</h4>
      <div>{ic("phone")}<a href="tel:{TEL}">{PHONE}</a></div>
      <div>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div>{ic("pin")}<span>{PO}, {ADDR_CITY}, {ADDR_REGION} {ADDR_ZIP}</span></div>
      <div>{ic("clock")}<span>Mon&ndash;Sat, 8am&ndash;6pm</span></div>
      <a class="btn btn-gold" style="margin-top:14px" href="contact.html">Request a Quote</a>
    </div>
  </div>
  <div class="ft-bottom">
    <span>&copy; {YEAR} {NAME}. Serving Fairbanks, North Pole &amp; the North Star Borough.</span>
    <span>Get the work done. Get your day back.</span>
  </div>
</div></footer>
<div class="mobile-bar">
  <a class="mb-call" href="tel:{TEL}">{ic("phone")}Call Now</a>
  <a class="mb-quote" href="contact.html">{ic("chat")}Free Quote</a>
</div>
<div id="google_translate_element"></div>
<script src="assets/app.js?v={VER}"></script>'''

# ---------------- SEO head ----------------
def biz_jsonld():
    services=["Kitchen and bath repairs","Plumbing and drain service","Minor electrical and fixtures",
      "Drywall patch and paint","Doors, windows and weatherization","Flooring and trim repair",
      "Hanging and furniture assembly","Arctic and winter weatherization","Safety and accessibility installs",
      "Exterior, gutters and curb appeal","Realtor punch lists","Rental turnovers and property maintenance"]
    return {
      "@context":"https://schema.org","@type":["HomeAndConstructionBusiness","HandymanService","LocalBusiness"],
      "@id":BASE+"/#business","name":NAME,
      "description":"Fixed-price handyman service in Fairbanks, Alaska. Flat-rate pricing from a published price book gives homeowners, realtors and property managers certainty on cost before work begins.",
      "url":BASE+"/","telephone":TEL,"email":EMAIL,
      "image":BASE+"/assets/img/og-image.jpg","logo":BASE+"/assets/img/logo.png",
      "priceRange":"$$","currenciesAccepted":"USD","paymentAccepted":"Cash, Check, Credit Card",
      "address":{"@type":"PostalAddress","postOfficeBoxNumber":"70200","addressLocality":ADDR_CITY,
        "addressRegion":ADDR_REGION,"postalCode":ADDR_ZIP,"addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":GEO[0],"longitude":GEO[1]},
      "areaServed":[{"@type":"AdministrativeArea","name":"Fairbanks North Star Borough"}]+
        [{"@type":"City","name":c} for c in ["Fairbanks","North Pole","Fox","Ester","Two Rivers","Salcha","Eielson AFB","Fort Wainwright","Pleasant Valley","Moose Creek"]],
      "serviceArea":{"@type":"GeoCircle","geoMidpoint":{"@type":"GeoCoordinates","latitude":GEO[0],"longitude":GEO[1]},"geoRadius":48000},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification",
        "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"08:00","closes":"18:00"}],
      "knowsLanguage":["en","es","ru","ko","tl","zh-CN","vi","de","fr","ja","ar","hi"],
      "slogan":"Get the work done. Get your day back.",
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Flat-Rate Handyman Price Book",
        "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s}} for s in services]},
      "sameAs":["https://www.facebook.com/husbandforhour"]
    }

def head(title,desc,slug,extra=None):
    canon=f"{BASE}/{slug}" if slug!="index.html" else BASE+"/"
    ld=[biz_jsonld()]
    if slug=="index.html":
        ld.append({"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":BASE+"/"})
    if slug!="index.html":
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
          {"@type":"ListItem","position":2,"name":dict(NAV)[slug],"item":canon}]})
    if extra: ld.extend(extra if isinstance(extra,list) else [extra])
    ldtags="".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#075c46">
<meta name="geo.region" content="US-AK"><meta name="geo.placename" content="Fairbanks, Alaska">
<meta name="geo.position" content="{GEO[0]};{GEO[1]}"><meta name="ICBM" content="{GEO[0]}, {GEO[1]}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/img/og-image.jpg">
<link rel="icon" href="assets/img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css?v={VER}">
{ldtags}
</head><body>'''

# ---------------- reusable blocks ----------------
def seal(txt="Proudly serving the<br>Fairbanks North Star Borough",cls=""):
    t=f'<span class="seal-txt">{txt}</span>' if txt else ""
    return f'<div class="seal {cls}"><img src="assets/img/badge.png" alt="{NAME} Alaska handyman badge" width="104" height="103">{t}</div>'

def page_hero(crumb,title,desc,extra=""):
    return f'''<section class="phero"><div class="wrap">
      <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
      <h1>{title}</h1><p class="lead">{desc}</p>{extra}</div></section>'''

def cta_band():
    return f'''<section class="sec cta"><div class="wrap reveal">
      <h2>Tell us the job. Get a flat-rate price.</h2>
      <p>No hourly meter running. No open-ended invoices. You approve the number before we lift a tool.</p>
      <div class="hero-cta"><a class="btn btn-gold btn-lg" href="contact.html">Get Your Flat Quote</a>
      <a class="btn btn-outline-light btn-lg" href="tel:{TEL}">{ic("phone")}{PHONE}</a></div>
    </div></section>'''

# FNSB service-area map (stylized, on-brand)
def area_map():
    # name, x, y, core (0 community / 1 town / 2 hub), label side
    places=[("Fairbanks",300,215,2,"top"),("Fort Wainwright",352,246,0,"right"),
            ("College",232,186,0,"left"),("Ester",168,250,0,"left"),("Fox",296,104,0,"top"),
            ("Pleasant Valley",470,178,0,"top"),("Two Rivers",566,150,0,"right"),
            ("North Pole",440,298,1,"left"),("Moose Creek",506,330,0,"top"),
            ("Eielson AFB",548,360,0,"right"),("Salcha",604,396,0,"right"),
            ("Harding Lake",656,424,0,"bottom")]
    def lab(side,x,y):
        if side=="top": return x,y-13,"middle"
        if side=="bottom": return x,y+25,"middle"
        if side=="left": return x-12,y+5,"end"
        return x+12,y+5,"start"
    dots=""
    for n,x,y,core,side in places:
        r=9 if core==2 else (7 if core==1 else 5)
        fill="var(--gold)" if core else "#ffffff"
        tx,ty,anc=lab(side,x,y)
        wt=700 if core else 600
        dots+=(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="var(--gold-d)" stroke-width="2"/>'
               f'<text x="{tx}" y="{ty}" text-anchor="{anc}" font-size="15.5" font-weight="{wt}" '
               f'fill="#eef3ee" font-family="Archivo,sans-serif" '
               f'style="paint-order:stroke;stroke:#053a2c;stroke-width:3.5px;stroke-linejoin:round">{n}</text>')
    return f'''<div class="map-card">
    <svg viewBox="0 0 760 520" role="img" aria-label="Service area map of the Fairbanks North Star Borough showing Fairbanks, North Pole, Fort Wainwright, Eielson AFB and surrounding communities">
      <defs><radialGradient id="rg" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="rgba(233,177,58,.28)"/><stop offset="100%" stop-color="rgba(233,177,58,0)"/></radialGradient></defs>
      <rect x="0" y="0" width="760" height="520" rx="22" fill="#053a2c"/>
      <path d="M44 64 H716 a20 20 0 0 1 20 20 V454 a20 20 0 0 1 -20 20 H44 a20 20 0 0 1 -20 -20 V84 a20 20 0 0 1 20 -20 Z"
        fill="#075c46" stroke="rgba(233,177,58,.4)" stroke-width="2" stroke-dasharray="3 8"/>
      <!-- rivers: Tanana (south) + Chena (through Fairbanks) -->
      <path d="M70 300 C 230 338, 360 350, 470 380 C 560 405, 650 420, 740 424" fill="none" stroke="#0e7d63" stroke-width="11" stroke-linecap="round" opacity=".55"/>
      <path d="M610 198 C 470 214, 380 205, 300 215" fill="none" stroke="#0e7d63" stroke-width="6" stroke-linecap="round" opacity=".5"/>
      <!-- highway corridors out of the Fairbanks hub -->
      <g fill="none" stroke="var(--gold)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity=".22">
        <polyline points="300,215 296,104"/>
        <polyline points="300,215 470,178 566,150"/>
        <polyline points="300,215 352,246 440,298 506,330 548,360 604,396 656,424"/>
        <polyline points="300,215 232,186"/>
        <polyline points="300,215 168,250"/>
      </g>
      <!-- core service radius around Fairbanks -->
      <circle cx="300" cy="215" r="132" fill="url(#rg)"/>
      <circle cx="300" cy="215" r="132" fill="none" stroke="var(--gold)" stroke-width="1.6" stroke-dasharray="5 9" opacity=".6"/>
      {dots}
      <!-- compass -->
      <g opacity=".65"><text x="690" y="84" text-anchor="middle" font-size="13" font-weight="700" fill="#cfe0d6" font-family="Archivo,sans-serif">N</text>
        <path d="M690 90 L690 108 M686 96 L690 90 L694 96" stroke="#cfe0d6" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <text x="44" y="502" font-size="14" fill="#9fc0b0" font-family="Inter,sans-serif">Fairbanks North Star Borough &middot; we cover the whole Borough</text>
    </svg></div>'''

# ---------------- pricing data ----------------
PRICE_GROUPS=[
 ("Plumbing &amp; Drains","drop",[
   ("Replace kitchen faucet (customer-supplied)","each",485,945),
   ("Replace bathroom faucet","each",430,870),
   ("Clear kitchen sink drain","each",240),
   ("Clear tub or shower drain","each",230),
   ("Replace P-trap under sink","each",215,280),
   ("Toilet flapper / fill-valve tune-up","toilet",210,295),
   ("Replace accessible shutoff valve","each",245,320),
 ]),
 ("Electrical &amp; Fixtures","zap",[
   ("Replace standard light fixture","each",235,295),
   ("Replace ceiling fan (existing box)","each",315,375),
   ("Replace switch or dimmer","each",150,205),
   ("Replace hardwired smoke / CO alarm","each",190,335),
 ]),
 ("Drywall, Patch &amp; Paint","paint",[
   ("Patch drywall hole up to 2 in","each",170,185),
   ("Patch nail holes up to 20 spots","room",175,200),
 ]),
 ("Hanging &amp; Assembly","hammer",[
   ("Hang single picture or artwork","each",110,120),
   ("Hang medium mirror (26&ndash;60 lb)","each",235,265),
   ("Install single floating shelf","each",195,220),
   ("Install blinds, standard window","opening",145,155),
   ("Install curtain rod, single opening","opening",155,170),
   ("Assemble nightstand / small table","each",180),
 ]),
 ("Caulking, Kitchen &amp; Bath","drop",[
   ("Re-caulk bathtub or shower perimeter","fixture",250,295),
   ("Re-caulk sink perimeter","fixture",145,170),
 ]),
 ("Doors &amp; Windows","door",[
   ("Replace interior door knob or lever","door",210,350),
   ("Install deadbolt (existing prep)","door",250,440),
   ("Adjust sticking exterior door","each",180),
   ("Replace door sweep","each",185,250),
 ]),
 ("Finish Carpentry &amp; Safety","ruler",[
   ("Install grab bar into framing","each",240,345),
   ("Install handrail up to 8 ft","run",500,860),
   ("Install baseboard up to 10 lin ft","run",265,355),
 ]),
 ("Arctic &amp; Winter Prep","snow",[
   ("Heat tape on accessible pipe (to 12 ft)","run",350,575),
   ("Pipe insulation on exposed line (to 20 ft)","run",280,400),
   ("Seasonal hose-bib shutdown (to 3 bibs)","home",195),
   ("Shovel sidewalk / entry (to 500 sq ft)","visit",210),
 ]),
 ("Exterior &amp; Curb Appeal","home",[
   ("Gutter cleaning, single story (to 100 lf)","run",280),
 ]),
]

def price_table(group):
    name,icon,rows=group
    trs=""
    for row in rows:
        svc,unit=row[0],row[1]
        flat = len(row)==3 or (len(row)==4 and row[2]==row[3])
        if flat:
            trs+=(f'<tr><td>{svc}</td><td class="muted">per {unit}</td>'
                  f'<td class="num eco">${row[2]}</td><td class="num"><span class="flat-tag">flat rate</span></td></tr>')
        else:
            trs+=(f'<tr><td>{svc}</td><td class="muted">per {unit}</td>'
                  f'<td class="num eco">${row[2]}</td><td class="num">${row[3]}</td></tr>')
    return f'''<div class="reveal"><div class="cat-head">{name}</div>
      <table class="price-table"><thead><tr><th>Service</th><th>Unit</th><th>Economy</th><th>Premium</th></tr></thead>
      <tbody>{trs}</tbody></table></div>'''

# ============================================================ PAGES
def home():
    services=[
     ("drop","Plumbing &amp; Drains","Running toilets, leaky and worn faucets, clogged drains, P-traps and shutoff valves."),
     ("zap","Electrical &amp; Fixtures","Light fixtures, ceiling fans, switches and dimmers, smoke and CO alarms."),
     ("paint","Drywall &amp; Paint","Holes, cracks, nail-pops and touch-up patching done clean and flush."),
     ("door","Doors &amp; Windows","Sticking doors, hardware, deadbolts, weatherstripping and draft sealing."),
     ("hammer","Hanging &amp; Assembly","TVs, mirrors, shelves, blinds, curtain rods and flat-pack furniture."),
     ("ruler","Carpentry &amp; Trim","Baseboard, casing, fence pickets, cabinet doors and finish repairs."),
     ("snow","Arctic &amp; Winter Prep","Heat tape, pipe insulation, hose-bib shutdowns and ice-dam mitigation."),
     ("shield","Safety &amp; Access","Grab bars, handrails, hardwired detectors and aging-in-place installs."),
    ]
    scards="".join(f'<div class="card reveal"><div class="icon">{ic(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i,t,d in services)
    auds=[
     ("home","Homeowners","The odd jobs you do not have time for, handled in one visit with a price you approved up front."),
     ("key","Realtors","Pre-listing punch lists and inspection repairs turned around fast so closings stay on schedule."),
     ("building","Property Managers","Make-readies, turnovers and recurring maintenance with clean documentation and one invoice."),
     ("users","Businesses","Storefront and office fixes handled on a flat rate, with W-9, EIN and COI provided on request."),
    ]
    acards="".join(f'<div class="aud reveal"><div class="icon gold">{ic(i)}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i,t,d in auds)
    steps=[("Tell us the job","Call, text, or send the request form with a couple of photos."),
           ("Get your flat price","We quote from our published price book, Economy or Premium, before any work starts."),
           ("We do the work","A skilled, insured technician shows up on schedule and gets it done right."),
           ("Get your day back","You approve, we clean up, and you move on with your life.")]
    stepcards="".join(f'<div class="step reveal"><h3>{t}</h3><p>{d}</p></div>' for t,d in steps)
    faqs=[
     ("Why &ldquo;Husband for an Hour&rdquo;?","Because somebody has to fix the honey-do list, and it does not have to be you. The name is a wink. The work is the real deal: licensed, insured technicians who show up and get it done."),
     ("What does fixed pricing actually mean?","Every common job has a set flat rate in our price book. We quote that number before we start, so you are never surprised by an hourly meter or an open-ended time-and-materials invoice."),
     ("Is there a fee for the estimate?","A standard onsite diagnosis is $200, and it is discounted when you have more than one price-book service done on the same visit. Many quotes can also be given remotely from a few photos at no charge."),
     ("What is the difference between Economy and Premium?","Same skilled labor either way. Economy uses solid standard-grade materials; Premium uses higher-end parts and finishes. You choose the tier that fits your budget."),
     ("Where do you work?","Across the Fairbanks North Star Borough: Fairbanks, North Pole, Fox, Ester, Two Rivers, Salcha, Eielson AFB, Fort Wainwright and the surrounding communities."),
     ("Are you licensed and insured?","Yes. We are licensed, bonded and insured, and we provide a W-9, EIN and Certificate of Insurance on request."),
     ("Do you speak my language?","Our site translates into more than 80 languages. Use the globe menu at the top of the page to read everything in the language you are most comfortable with."),
    ]
    faqhtml="".join(f'<details class="q reveal"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q,a in faqs)
    return head(
      "Husband for an Hour | Fairbanks Handyman Service, Flat-Rate Pricing",
      "Your wife&#39;s favorite backup husband. Husband for an Hour is a licensed, insured Fairbanks handyman service that knocks out your honey-do list with flat-rate pricing from a published price book. Call (907) 759-8080.",
      "index.html",
      extra=[
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
          {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
        {"@context":"https://schema.org","@type":"LocalBusiness","@id":BASE+"/#business",
         "aggregateRating":{"@type":"AggregateRating","ratingValue":"5","reviewCount":"3","bestRating":"5"},
         "review":[
           {"@type":"Review","author":{"@type":"Person","name":"Maria Babii"},
            "reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},
            "reviewBody":"Great team, very professional. Communication was clear which I really appreciate. The guys were tidy, did not leave a mess behind and double checked with me if I was happy with the results before leaving. Highly recommend."},
           {"@type":"Review","author":{"@type":"Person","name":"Danny Manilla"},
            "reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},
            "reviewBody":"Great customer service, flexible scheduling, fair pricing."},
           {"@type":"Review","author":{"@type":"Person","name":"J. C."},
            "reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},
            "reviewBody":"People you can trust, hands down."}]}
      ]
    )+header("index.html")+f'''
<section class="hero"><div class="wrap hero-grid">
  <div class="reveal">
    <p class="eyebrow" style="color:var(--gold)">Fairbanks &amp; North Pole Handyman</p>
    <h1>Your wife&rsquo;s favorite <span class="hl">backup husband</span>.</h1>
    <p class="lead">Husband for an Hour is the Fairbanks handyman crew that actually shows up, knocks out the honey-do list, and hands you a flat price before we start. No ring required. Just results.</p>
    <div class="hero-cta">
      <a class="btn btn-gold btn-lg" href="tel:{TEL}">{ic("phone")}Call or Text {PHONE}</a>
      <a class="btn btn-light btn-lg" href="contact.html">Get My Free Quote</a>
    </div>
    <div class="hero-trust">
      <span>{ic("check")}We actually answer the phone</span>
      <span>{ic("check")}Free quotes within 24 hours</span>
      <span>{ic("check")}Same-week scheduling</span>
    </div>
    <div class="hero-chips">
      <span class="chip">{ic("shield")}Licensed, bonded, insured</span>
      <span class="chip">{ic("tag")}Flat price, no surprises</span>
      <span class="chip">{ic("star")}5-star Google reviews</span>
    </div>
  </div>
  <div class="hero-visual reveal">
    <div class="hero-figure">
      <img src="assets/img/mascot.jpg" alt="Husband for an Hour mascot, a polar bear hugging a friendly Fairbanks handyman by the van">
      <div class="speech">&ldquo;Honey, it&rsquo;s already handled.&rdquo;</div>
      <div class="price-tag">Flat price<b>no surprises</b></div>
    </div>
  </div>
</div></section>

<section class="stats"><div class="wrap">
  <div class="stat reveal"><div class="num" data-count="5" data-suffix="+">0</div><div class="lbl">Years on the honey-do beat</div></div>
  <div class="stat reveal"><div class="num" data-count="400" data-suffix="+">0</div><div class="lbl">Jobs with a set price</div></div>
  <div class="stat reveal"><div class="num" data-count="25">0</div><div class="lbl">Kinds of fixes we tackle</div></div>
  <div class="stat reveal"><div class="num" data-count="109" data-suffix="K">0</div><div class="lbl">Reach on our viral van post</div></div>
</div></section>

<section class="vanband"><div class="wrap">
  <div class="vanband-head reveal">
    <span class="fbstat">{ic("star")}109,000+ reach on one Facebook post</span>
    <h2>The van Fairbanks can&rsquo;t stop talking about.</h2>
    <p class="lead" style="margin-left:auto;margin-right:auto">You have seen us on Airport Way. One photo of our wrapped van became one of the most shared local posts the Interior has ever seen. The name makes people grin. The work is what makes them call.</p>
  </div>
  <div class="vanband-photo reveal"><img src="assets/img/van-fairbanks.jpg" alt="Husband for an Hour wrapped service van on Airport Way in Fairbanks, Alaska, near the Fairbanks Airport Way and Steese Highway signs"></div>
  <div class="vanband-foot reveal">
    <p class="tagline-lg">&ldquo;Get the work done. Get your day back.&rdquo;</p>
    <a class="btn btn-gold btn-lg" href="#team">Meet the crew {ic("arrow")}</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">Hire with confidence</p>
    <h2>No mystery bills. No strangers. No stress.</h2>
    <p class="lead center">The two scariest parts of hiring a handyman, what it will cost and who walks into your home, are the two things we lock down before we start.</p></div>
  <div class="grid g-4" style="margin-top:42px">
    <div class="promise-card reveal"><div class="icon">{ic("tag")}</div><h3>The price is the price</h3><p>Quoted from our published price book and approved by you before any work begins. The number never moves.</p></div>
    <div class="promise-card reveal"><div class="icon">{ic("shield")}</div><h3>Licensed &amp; insured</h3><p>Real, vetted, insured professionals. We carry the coverage that protects your home and our crew.</p></div>
    <div class="promise-card reveal"><div class="icon">{ic("users")}</div><h3>Professional staff</h3><p>Friendly technicians who show up on time, respect your home, and clean up before they leave.</p></div>
    <div class="promise-card reveal"><div class="icon">{ic("check")}</div><h3>Done right, period</h3><p>We are not finished until you are happy with the work. Quality you can count on, every visit.</p></div>
  </div>
  <div class="center" style="margin-top:34px"><a class="btn btn-gold btn-lg" href="tel:{TEL}">{ic("phone")}Call or text {PHONE}</a></div>
</div></section>

<section class="sec value"><div class="wrap">
  <div class="center reveal" id="services-top"><p class="eyebrow">What we fix</p><h2>The whole honey-do list, in one visit.</h2>
  <p class="lead center">Leaky faucets to full punch lists. Hundreds of common repairs and installs, each with a set price in our book.</p></div>
  <div class="grid g-4" style="margin-top:42px">{scards}</div>
  <div class="center" style="margin-top:34px"><a class="btn btn-ghost btn-lg" href="services.html">Browse all services {ic("arrow")}</a></div>
</div></section>

<section class="sec value"><div class="wrap">
  <div class="split">
    <div class="reveal"><p class="eyebrow">The serious part</p><h2>A fun name. A price you can trust.</h2>
    <p class="lead">Most handymen run an hourly meter and surprise you at the end. We quote a flat rate from our published price book first, so you decide with the real number in hand.</p>
    <ul class="area-list" style="columns:1;margin:18px 0 6px;max-width:none">
      <li><b style="color:var(--ink)">Know the price first.</b>&nbsp; The number you approve is the number you pay.</li>
      <li><b style="color:var(--ink)">No surprise invoices.</b>&nbsp; No stopwatch, no padded materials, no &ldquo;it ran long.&rdquo;</li>
      <li><b style="color:var(--ink)">Economy or Premium.</b>&nbsp; Pick the material tier that fits your budget.</li>
    </ul>
    <a class="btn btn-green btn-lg" style="margin-top:16px" href="pricing.html">See how fixed pricing works {ic("arrow")}</a></div>
    <div class="quote-wrap reveal" style="margin:0 auto">
      <div class="quote-card">
        <div class="qc-top"><span class="qc-tag">Your Flat-Rate Quote</span><span class="qc-badge">Approved before work</span></div>
        <div class="qc-row"><span>Replace kitchen faucet</span><span class="price">$485</span></div>
        <div class="qc-row"><span>Re-caulk shower perimeter</span><span class="price">$250</span></div>
        <div class="qc-row"><span>Hang TV + mirror (add-on)</span><span class="price">$165</span></div>
        <div class="qc-total"><span>Total</span><span class="price">$900</span></div>
        <p class="qc-note">No hourly meter. No time-and-materials surprises. Economy or Premium, your choice.</p>
      </div>
      <div class="qc-stamp">FLAT<br>RATE</div>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">How it works</p><h2>Four steps to a finished list.</h2></div>
  <div class="steps" style="margin-top:48px">{stepcards}</div>
</div></section>

<section class="sec value" id="team"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">The crew</p><h2>Meet your backup husbands.</h2>
  <p class="lead center">The whole team, field and office. Skilled, insured technicians backed by a highly organized back office, treating your home like their own and cleaning up before they leave.</p></div>
  <div class="team-grid" style="margin-top:42px">
    <div class="team-card reveal"><div class="team-photo"><img src="assets/img/team-1.jpg" alt="Husband for an Hour field technician in Fairbanks" loading="lazy"></div>
      <div class="team-body"><div class="role">Field Technician</div><h3>Repairs &amp; Remodels</h3><p>Takes on the bigger jobs and the tricky fixes. If it can be repaired, he has repaired it.</p></div></div>
    <div class="team-card reveal"><div class="team-photo"><img src="assets/img/team-2.jpg" alt="Husband for an Hour field technician in Fairbanks" loading="lazy"></div>
      <div class="team-body"><div class="role">Field Technician</div><h3>On the Tools</h3><p>Your day-to-day backup husband. Shows up on time, fixes it right, and tidies up after the job.</p></div></div>
    <div class="team-card reveal"><div class="team-photo"><img src="assets/img/team-3.jpg" alt="Husband for an Hour project coordinator" loading="lazy"></div>
      <div class="team-body"><div class="role">Project Coordinator</div><h3>Quotes &amp; Scheduling</h3><p>Turns your photos and notes into a clear flat-rate quote and gets you on the schedule fast.</p></div></div>
    <div class="team-card reveal"><div class="team-photo"><img src="assets/img/team-4.jpg" alt="Husband for an Hour estimator" loading="lazy"></div>
      <div class="team-body"><div class="role">Estimating &amp; Support</div><h3>The Price Book</h3><p>Keeps the price book sharp and accurate, so your flat quote is fair and there are no surprises.</p></div></div>
    <div class="team-card reveal"><div class="team-photo"><img src="assets/img/team-5.jpg" alt="Husband for an Hour office manager" loading="lazy"></div>
      <div class="team-body"><div class="role">Office Manager</div><h3>The Back Office</h3><p>Runs the highly organized back office. Quotes, invoices and questions, all handled with a smile.</p></div></div>
  </div>
  <p class="muted center reveal" style="margin-top:22px;font-size:.92rem">Licensed, bonded and insured. W-9, EIN and Certificate of Insurance provided on request.</p>
</div></section>

<section class="sec reviews"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">Reviews</p>
    <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
    <h2>What your Fairbanks neighbors say.</h2>
    <p class="lead center">Real reviews from real customers on Google.</p></div>
  <div class="grid g-3" style="margin-top:40px">
    <div class="review-card reveal"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p>&ldquo;Great team, very professional. Communication was clear which I really appreciate. The guys were tidy, did not leave a mess behind and double checked with me if I was happy with the results before leaving. Highly recommend.&rdquo;</p>
      <div class="rev-by"><span class="rev-name">Maria Babii</span><span class="rev-src">{ic("star")}Google review</span></div></div>
    <div class="review-card reveal"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p>&ldquo;Great customer service, flexible scheduling, fair pricing. Used for septic pumping.&rdquo;</p>
      <div class="rev-by"><span class="rev-name">Danny Manilla</span><span class="rev-src">{ic("star")}Google review</span></div></div>
    <div class="review-card reveal"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
      <p>&ldquo;People you can trust, hands down.&rdquo;</p>
      <div class="rev-by"><span class="rev-name">J. C.</span><span class="rev-src">{ic("star")}Google review</span></div></div>
  </div>
  <div class="center" style="margin-top:32px"><a class="btn btn-gold btn-lg" href="https://www.google.com/search?q=Husband+for+an+Hour+Fairbanks+reviews" target="_blank" rel="noopener">Read more reviews on Google {ic("arrow")}</a></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="split">
    <div class="reveal"><p class="eyebrow">Who we help</p><h2>Homeowners, realtors, property managers and businesses.</h2>
    <p>Whether it is the one job that has nagged you for months or a 30-item make-ready before a tenant moves in, you get the same thing: a clear flat price and skilled field technicians backed by an organized back office.</p>
    <div class="grid" style="gap:14px;margin-top:18px">{acards}</div></div>
    <div class="split-media reveal"><img src="assets/img/home-kitchen.jpg" alt="Updated kitchen kept in good repair by Husband for an Hour in Fairbanks"></div>
  </div>
</div></section>

<section class="sec value"><div class="wrap">
  <div class="area-grid">
    <div class="reveal">{area_map()}</div>
    <div class="reveal">{seal()}<p class="eyebrow">Service area</p><h2>The whole Fairbanks North Star Borough.</h2>
    <p class="lead">If you are inside the Borough, we cover you. From downtown Fairbanks out to North Pole, Salcha, Two Rivers, Fox and the bases.</p>
    <ul class="area-list" style="margin-top:18px">
      <li class="core">Fairbanks</li><li class="core">North Pole</li><li>Fort Wainwright</li><li>Eielson AFB</li>
      <li>Fox</li><li>Ester</li><li>Two Rivers</li><li>Salcha</li><li>Pleasant Valley</li>
      <li>Moose Creek</li><li>Harding-Birch Lakes</li><li>College</li>
    </ul>
    <a class="btn btn-green" style="margin-top:22px" href="service-area.html">Check your area {ic("arrow")}</a></div>
  </div>
</div></section>

<section class="sec value"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">Questions</p><h2>Good to know before you call.</h2></div>
  <div class="faq" style="margin-top:36px">{faqhtml}</div>
</div></section>

<section class="sec qform" id="quote"><div class="wrap">
  <div class="qform-grid">
    <div class="reveal">
      <p class="eyebrow">Free, no-obligation quote</p>
      <h2>Ready to cross it off the list?</h2>
      <p class="lead">Tell us the job and snap a couple of photos. We reply fast, usually the same business day, with a flat price straight from our book. No hourly meter, no surprises.</p>
      <ul class="area-list" style="columns:1;margin:18px 0 6px;max-width:none">
        <li><b>Flat price up front</b> &mdash; you approve it before we start.</li>
        <li><b>Licensed, bonded, insured</b> professionals at your door.</li>
        <li><b>Same-week scheduling</b> across the Borough.</li>
      </ul>
      <p style="margin-top:18px;font-size:1.08rem">Prefer to talk? <a href="tel:{TEL}" style="font-weight:700">Call or text {PHONE}</a></p>
    </div>
    <div class="reveal">
      <form id="quoteForm" class="form-card" novalidate>
        <div class="form-row">
          <div class="field"><label>Name <span class="req">*</span></label><input name="name" required><div class="err">Please enter your name.</div></div>
          <div class="field"><label>Phone <span class="req">*</span></label><input name="phone" type="tel" required><div class="err">Please enter a phone number.</div></div>
        </div>
        <div class="field"><label>Email <span class="req">*</span></label><input name="email" type="email" required><div class="err">Please enter a valid email.</div></div>
        <div class="field"><label>What do you need done? <span class="req">*</span></label><textarea name="message" required placeholder="A few details and we will send your flat-rate quote."></textarea><div class="err">Please tell us about the job.</div></div>
        <button class="btn btn-gold btn-lg" type="submit" style="width:100%">Get my free quote</button>
        <p class="muted" style="font-size:.8rem;margin:12px 0 0;text-align:center">No obligation. W-9, EIN and Certificate of Insurance provided on request.</p>
      </form>
      <div id="formOk" class="form-ok"><b>Thanks, your request is in.</b><br>We will reach out shortly with your flat-rate quote. For anything urgent, call {PHONE}.</div>
    </div>
  </div>
</div></section>
{footer()}</body></html>'''

def services():
    groups=[
     ("drop","Plumbing &amp; Drains","Leaks, clogs and worn fixtures fixed before they become water damage.",
      ["Replace running toilet flapper and fill valve","Replace kitchen, bath and shower faucets","Clear sink, tub and shower drains","Replace P-traps and accessible shutoff valves","Replace refrigerator water lines","Re-seat and re-set leaking toilets"]),
     ("zap","Electrical &amp; Fixtures","Common, code-conscious electrical swaps where allowed.",
      ["Replace light fixtures and vanity lights","Replace ceiling fans on existing boxes","Replace switches, dimmers and outlets","Replace hardwired smoke and CO alarms","Install fixture remote kits","Replace exterior light fixtures"]),
     ("paint","Drywall, Patch &amp; Paint","Walls and ceilings made smooth and ready.",
      ["Patch nail holes and dings","Patch holes from 2 in to over a foot","Repair ceiling stress cracks","Texture-match and prime patches","Touch-up painting","Re-caulk and seal trim seams"]),
     ("door","Doors, Windows &amp; Weatherization","Smooth-operating doors and a tighter, warmer home.",
      ["Adjust sticking and dragging doors","Replace knobs, levers and deadbolts","Replace door sweeps and thresholds","Install weatherstripping and seal drafts","Replace foggy or broken glass panes","Tune closet and sliding doors"]),
     ("hammer","Hanging &amp; Assembly","If it goes on the wall or comes in a box, we handle it.",
      ["Mount TVs and floating shelves","Hang pictures, mirrors and gallery walls","Install blinds, shades and curtain rods","Assemble flat-pack furniture","Install closet systems and hooks","Garage storage, racks and bike hooks"]),
     ("ruler","Finish Carpentry &amp; Repair","Clean trim and small carpentry that looks built-in.",
      ["Install and repair baseboard and casing","Repair cabinet doors and hinges","Replace damaged fence pickets and gates","Replace interior door slabs","Build and install simple shelving","Repair squeaky floors and stairs"]),
     ("home","Flooring &amp; Trim","Targeted floor repairs without a full remodel.",
      ["Replace damaged vinyl plank and laminate","Replace broken ceramic tiles","Install transition and threshold strips","Repair loose and lifting boards","Re-grout small areas","Refresh worn trim"]),
     ("snow","Arctic &amp; Winter Prep","Alaska-specific work that protects your home through breakup and freeze-up.",
      ["Install heat tape on exposed pipe","Insulate exposed water lines","Seasonal hose-bib shutdown and restart","Ice-dam inspection and mitigation","Storm-window film and outlet gaskets","Snow and entry clearing"]),
     ("shield","Safety &amp; Accessibility","Aging-in-place and peace-of-mind installs.",
      ["Install grab bars into framing","Install handrails on stairs and entries","Replace and add smoke / CO detectors","Secure rugs and trip hazards","Install lever handles and easy hardware","Mount security cameras and lighting"]),
     ("building","Exterior &amp; Curb Appeal","Make the outside match the inside.",
      ["Gutter cleaning and splash blocks","Power-wash siding, drives and walks","Repair siding, trim and fascia","Replace house numbers and mailboxes","Touch-up exterior paint","Minor landscaping and outdoor lighting"]),
    ]
    sec="".join(
      f'''<div class="split {"flip" if idx%2 else ""} reveal" style="margin-bottom:46px">
        <div class="split-body"><div class="icon">{ic(i)}</div><h2>{t}</h2><p class="lead">{d}</p>
        <ul class="area-list" style="columns:2;margin-top:14px">{"".join(f"<li>{x}</li>" for x in items)}</ul>
        <a class="btn btn-green" style="margin-top:18px" href="pricing.html">See flat-rate prices {ic("arrow")}</a></div>
      </div>''' for idx,(i,t,d,items) in enumerate(groups))
    svc_ld={"@context":"https://schema.org","@type":"ItemList","itemListElement":[
       {"@type":"ListItem","position":n+1,"item":{"@type":"Service","name":t.replace("&amp;","&"),
        "provider":{"@id":BASE+"/#business"},"areaServed":"Fairbanks North Star Borough"}}
       for n,(i,t,d,items) in enumerate(groups)]}
    return head(
      "Handyman Services in Fairbanks &amp; North Pole | Husband for an Hour",
      "Plumbing, electrical, drywall, doors, carpentry, flooring, arctic winter prep and more. Hundreds of flat-rate handyman services across the Fairbanks North Star Borough.",
      "services.html",extra=svc_ld
    )+header("services.html")+page_hero("Services","Everything on your list, handled.",
      "Hundreds of common repairs and installs across ten categories, each with a set price in our book. One call covers the whole punch list."
    )+f'<section class="sec"><div class="wrap">{sec}</div></section>'+cta_band()+footer()+"</body></html>"

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def slugify(s):
    return "cat-"+re.sub(r"[^a-z0-9]+","-",s.lower().replace("&amp;","")).strip("-")

def render_pricebook():
    book=json.load(open(os.path.join(OUT,"pricebook.json"),encoding="utf-8"))
    search_icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>'
    chips=""; cats=""
    for gi,g in enumerate(book):
        slug=slugify(g["name"])
        chips+=f'<a class="pb-chip" href="#{slug}" data-target="{slug}">{g["name"]}<span>{g["count"]}</span></a>'
        rows=""
        for it in g["items"]:
            svc=esc(it["s"]); unit=esc(it.get("u","each"))
            if "p" in it:
                price=f'<td class="num eco">${it["p"]}</td><td class="num"><span class="flat-tag">flat rate</span></td>'
            else:
                price=f'<td class="num eco">${it["e"]}</td><td class="num">${it["m"]}</td>'
            rows+=f'<tr data-s="{svc.lower()}"><td>{svc}</td><td class="muted">per {unit}</td>{price}</tr>'
        op=" open" if gi==0 else ""
        cats+=(f'<details class="pb-cat" id="{slug}"{op}><summary>'
               f'<span class="pb-cat-name">{ic(g["icon"])}{g["name"]}</span>'
               f'<span class="pb-cat-meta">{g["count"]} services <span class="pb-range">${g["lo"]}&ndash;${g["hi"]}</span><span class="pb-chev">&#8250;</span></span>'
               f'</summary><div class="pb-body"><table class="price-table">'
               f'<thead><tr><th>Service</th><th>Unit</th><th>Economy</th><th>Premium</th></tr></thead>'
               f'<tbody>{rows}</tbody></table></div></details>')
    total=sum(g["count"] for g in book)
    return (f'<div class="pb-toolbar reveal"><div class="pb-search">{search_icon}'
            f'<input id="pbSearch" type="search" placeholder="Search {total} services, e.g. faucet, drywall, deadbolt..." autocomplete="off" aria-label="Search the price book"></div>'
            f'<div class="pb-chips">{chips}</div></div>'
            f'<p class="pb-noresult" id="pbNoResult" hidden>No services match that search. Try another word, or <a href="contact.html">ask us for a quote</a>.</p>'
            f'<div class="pb-cats">{cats}</div>')

def pricing():
    book_html=render_pricebook()
    faqs=[
     ("How is this different from time and materials?","Time-and-materials means the clock and the receipts decide your bill, and you only learn the total at the end. We work the opposite way: a published flat rate per job, quoted and approved before we start."),
     ("What is the diagnosis fee?","For jobs that need an onsite look, the standard diagnosis is $200. That fee is discounted when you have more than one price-book service done on the same visit. Many jobs can also be quoted from a few photos for free."),
     ("Why are there two prices per job?","Economy uses dependable standard-grade parts; Premium uses higher-end materials and finishes. Labor and workmanship are the same. You pick the tier."),
     ("Do add-on prices save me money?","Yes. Once a technician is onsite for a main item, additional same-visit tasks are billed at the lower add-on rate because the trip and setup are already covered."),
    ]
    faqhtml="".join(f'<details class="q reveal"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q,a in faqs)
    return head(
      "Flat-Rate Handyman Pricing &amp; Price Book | Husband for an Hour",
      "See how our fixed handyman pricing works. Flat rates from a published price book with Economy and Premium options, so you get certainty on cost before work begins in Fairbanks, AK.",
      "pricing.html",
      extra={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    )+header("pricing.html")+page_hero("Fixed Pricing","Fixed pricing, from a real price book.",
      "Most handymen run an hourly meter and hand you a time-and-materials bill at the end. We quote a flat rate from a published book first, so you decide with the number in front of you."
    )+f'''
<section class="sec"><div class="wrap">
  <div class="grid g-3 reveal">
    <div class="card"><div class="icon">{ic("list")}</div><h3>400+ priced jobs</h3><p>Our price book covers more than 400 common repairs and installs across 13 categories, each with a set rate. The full book is right below.</p></div>
    <div class="card"><div class="icon">{ic("tag")}</div><h3>Quoted before we start</h3><p>You see and approve the flat price before any work begins. The number you approve is the number you pay.</p></div>
    <div class="card"><div class="icon">{ic("sparkle")}</div><h3>Economy or Premium</h3><p>Two material tiers on most jobs. Same skilled labor, your choice of parts and finish level.</p></div>
  </div>
  <div class="card reveal" style="margin-top:24px;background:var(--green);color:#eaf3ee;border:0">
    <div class="grid g-2" style="gap:24px;align-items:center">
      <div><h3 style="color:#fff">The estimate fee, plainly</h3>
      <p style="color:#cfe0d6;margin:0">A standard onsite diagnosis is <b style="color:var(--gold)">$200</b>, and it is <b style="color:#fff">discounted</b> when you have more than one price-book service done on the same visit. Many jobs can also be quoted from a few photos at no charge.</p></div>
      <div style="text-align:center"><a class="btn btn-gold btn-lg" href="contact.html">Get my flat quote {ic("arrow")}</a></div>
    </div>
  </div>
</div></section>

<section class="sec value"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">The full price book</p><h2>Every job, with its price.</h2>
  <p class="lead center">Search it or browse by category. Prices are flat rates for standalone work in the Fairbanks area; your written quote confirms the exact number for your job.</p>
  <div class="center" style="margin-top:14px"><span class="chip" style="background:var(--green);color:#fff"><span style="color:var(--gold);font-weight:800">Economy</span> &nbsp;standard-grade &nbsp;|&nbsp; <span style="font-weight:800">Premium</span>&nbsp; higher-end &nbsp;|&nbsp; <span style="font-weight:800">Flat rate</span>&nbsp; service-only, no materials</span></div>
  </div>
  <div style="margin-top:22px">{book_html}</div>
  <p class="muted center reveal" style="margin-top:26px">Prices are from our current Fairbanks price book and may vary with conditions. Larger projects and custom work are quoted as a flat project price after a quick look.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">Questions</p><h2>Fixed pricing, explained.</h2></div>
  <div class="faq" style="margin-top:34px">{faqhtml}</div>
</div></section>
'''+cta_band()+footer()+"</body></html>"

def service_area():
    comms=[("Fairbanks",1),("North Pole",1),("College",0),("Fort Wainwright",0),("Eielson AFB",0),
           ("Fox",0),("Ester",0),("Two Rivers",0),("Salcha",0),("Pleasant Valley",0),
           ("Moose Creek",0),("Harding-Birch Lakes",0),("Goldstream",0),("Chena Hot Springs Rd",0),
           ("Badger",0),("Steele Creek",0)]
    li="".join(f'<li class="{"core" if c else ""}">{n}</li>' for n,c in comms)
    mapembed=('<iframe title="Fairbanks North Star Borough map" loading="lazy" '
      'style="width:100%;height:420px;border:0;border-radius:18px;box-shadow:var(--shadow)" '
      'referrerpolicy="no-referrer-when-downgrade" '
      'src="https://www.google.com/maps?q=Fairbanks+North+Star+Borough,+Alaska&z=8&output=embed"></iframe>')
    return head(
      "Service Area: Fairbanks North Star Borough | Husband for an Hour",
      "We serve the entire Fairbanks North Star Borough: Fairbanks, North Pole, Fox, Ester, Two Rivers, Salcha, Eielson AFB, Fort Wainwright and surrounding communities.",
      "service-area.html"
    )+header("service-area.html")+page_hero("Service Area","We cover the whole Borough.",
      "Husband for an Hour serves the Fairbanks North Star Borough end to end. If you are inside the Borough, we will give you a flat-rate quote.",
      extra=seal(txt="")
    )+f'''
<section class="sec"><div class="wrap">
  <div class="area-grid">
    <div class="reveal">{area_map()}</div>
    <div class="reveal"><p class="eyebrow">Communities we serve</p><h2>From downtown to the edges of the Borough.</h2>
    <p class="lead">Same flat-rate price book whether you are in the heart of Fairbanks or out past North Pole. Travel within the Borough is built into our pricing.</p>
    <ul class="area-list" style="margin-top:18px">{li}</ul>
    <a class="btn btn-gold" style="margin-top:22px" href="contact.html">Request a quote {ic("arrow")}</a></div>
  </div>
  <div class="reveal" style="margin-top:50px">
    <div class="center"><p class="eyebrow">On the map</p><h2>Fairbanks North Star Borough</h2></div>
    <div style="margin-top:22px">{mapembed}</div>
  </div>
</div></section>
{cta_band()}
{footer()}</body></html>'''

def about():
    return head(
      "About Husband for an Hour | Fairbanks Handyman Service",
      "A fun name for serious work. Husband for an Hour is a licensed, bonded and insured Fairbanks handyman service with skilled field technicians, an organized back office and honest flat-rate pricing.",
      "about.html"
    )+header("about.html")+page_hero("About","A fun name. Serious work.",
      "People remember the name. What keeps them calling is skilled technicians, an organized back office and a price they can trust."
    )+f'''
<section class="sec"><div class="wrap">
  <div class="split">
    <div class="reveal"><p class="eyebrow">Our story</p><h2>The backup husband Fairbanks actually relies on.</h2>
    <p>The honey-do list never ends. The faucet drips, the door sticks, the shelf still is not hung, and the weekend disappears. Husband for an Hour started to take that list off your plate, with a name that makes people laugh and work that makes them call back.</p>
    <p>For more than five years we have served Fairbanks and North Pole with the jobs people do not have time for. Today we run a full price book of flat-rate services, so the work comes with something most handymen will not give you: certainty.</p>
    <p style="font-family:var(--disp);font-weight:800;color:var(--green);font-size:1.25rem">&ldquo;People love our skilled field technicians and highly organized back office.&rdquo;</p>
    </div>
    <div class="split-media reveal"><img src="assets/img/mascot.jpg" alt="Husband for an Hour mascot, a polar bear hugging a friendly Fairbanks handyman by the van"></div>
  </div>
</div></section>

<section class="sec value"><div class="wrap">
  <div class="center reveal"><p class="eyebrow">What you can count on</p><h2>Serious about the details.</h2></div>
  <div class="grid g-3" style="margin-top:42px">
    <div class="card reveal"><div class="icon">{ic("shield")}</div><h3>Licensed, bonded, insured</h3><p>We carry the coverage that protects your home and our crew, and we provide a W-9, EIN and Certificate of Insurance on request.</p></div>
    <div class="card reveal"><div class="icon">{ic("tag")}</div><h3>Honest flat pricing</h3><p>A published price book instead of an hourly meter. You approve the number before we start, so there are no surprise invoices.</p></div>
    <div class="card reveal"><div class="icon">{ic("users")}</div><h3>Skilled technicians</h3><p>Experienced field techs who show up on schedule, treat your home with respect and finish the job clean.</p></div>
    <div class="card reveal"><div class="icon">{ic("list")}</div><h3>Organized back office</h3><p>Clear quotes, clean documentation and one tidy invoice. Realtors and property managers love how easy we are to work with.</p></div>
    <div class="card reveal"><div class="icon">{ic("pin")}</div><h3>Local to the Borough</h3><p>Fairbanks based and Fairbanks proud. We know Interior homes, Interior winters and what they need.</p></div>
    <div class="card reveal"><div class="icon">{ic("globe")}</div><h3>Built for everyone</h3><p>Our site reads in more than 80 languages so every neighbor in the Borough can get the help they need.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="proof">
  <div class="reveal"><img src="assets/img/van-fairbanks.jpg" alt="Husband for an Hour service van in Fairbanks, Alaska"></div>
  <div class="reveal"><span class="proof-badge">{ic("star")}109,000+ reach on one local post</span>
  <h2>Get the work done. Get your day back.</h2>
  <p class="lead">That line is on the back of our van for a reason. You have better things to do than chase a punch list. Hand it to us, get a flat price, and get your weekend back.</p>
  <a class="btn btn-gold btn-lg" href="contact.html">Get your flat quote {ic("arrow")}</a></div>
</div></div></section>
{cta_band()}
{footer()}</body></html>'''

def contact():
    cats=["Plumbing &amp; drains","Electrical &amp; fixtures","Drywall, patch &amp; paint",
      "Doors &amp; windows","Hanging &amp; assembly","Carpentry &amp; trim","Flooring &amp; tile",
      "Arctic &amp; winter prep","Safety &amp; accessibility","Exterior &amp; gutters","Multiple items / punch list","Not sure, please advise"]
    opts="".join(f'<option>{c}</option>' for c in cats)
    return head(
      "Contact &amp; Free Quote | Husband for an Hour, Fairbanks AK",
      "Request a free flat-rate handyman quote in Fairbanks or North Pole. Call (907) 759-8080 or send a few photos and we will price the job from our book before any work starts.",
      "contact.html"
    )+header("contact.html")+page_hero("Contact","Tell us the job. Get a flat price.",
      "Send a few details and photos and we will quote a flat rate from our price book, often before we ever set foot in your home."
    )+f'''
<section class="sec"><div class="wrap">
  <div class="split" style="align-items:start">
    <div class="reveal">
      <h2>Request your free quote</h2>
      <p class="muted">Most jobs can be quoted from photos. We reply fast, usually the same business day.</p>
      <form id="quoteForm" class="form-card" novalidate>
        <div class="form-row">
          <div class="field"><label>Name <span class="req">*</span></label><input name="name" required><div class="err">Please enter your name.</div></div>
          <div class="field"><label>Phone <span class="req">*</span></label><input name="phone" type="tel" required><div class="err">Please enter a phone number.</div></div>
        </div>
        <div class="form-row">
          <div class="field"><label>Email <span class="req">*</span></label><input name="email" type="email" required><div class="err">Please enter a valid email.</div></div>
          <div class="field"><label>City / area <span class="req">*</span></label><input name="city" placeholder="Fairbanks, North Pole..." required><div class="err">Please enter your city or area.</div></div>
        </div>
        <div class="form-row">
          <div class="field"><label>I am a</label><select name="who"><option>Homeowner</option><option>Realtor</option><option>Property manager</option><option>Business</option><option>Renter</option></select></div>
          <div class="field"><label>Type of work</label><select name="category">{opts}</select></div>
        </div>
        <div class="field"><label>Describe the job <span class="req">*</span></label><textarea name="message" required placeholder="What needs fixing? The more detail, the faster we can price it."></textarea><div class="err">Please describe the job.</div></div>
        <button class="btn btn-gold btn-lg" type="submit" style="width:100%">Send my request</button>
        <p class="muted" style="font-size:.82rem;margin:12px 0 0">Prefer to talk? Call or text <a href="tel:{TEL}">{PHONE}</a>. We provide W-9, EIN and Certificate of Insurance on request.</p>
      </form>
      <div id="formOk" class="form-ok"><b>Thanks, your request is in.</b><br>We will reach out shortly with your flat-rate quote. For anything urgent, call us at {PHONE}.</div>
    </div>
    <div class="reveal">
      <h2>Reach us</h2>
      <ul class="cinfo">
        <li><div class="icon">{ic("phone")}</div><div><b>Call or text</b><br><a href="tel:{TEL}">{PHONE}</a></div></li>
        <li><div class="icon">{ic("mail")}</div><div><b>Email</b><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><div class="icon">{ic("pin")}</div><div><b>Mailing address</b><br>{PO}<br>{ADDR_CITY}, {ADDR_REGION} {ADDR_ZIP}</div></li>
        <li><div class="icon">{ic("clock")}</div><div><b>Hours</b><br>Monday&ndash;Saturday, 8am&ndash;6pm</div></li>
        <li><div class="icon">{ic("pin")}</div><div><b>Service area</b><br>Fairbanks North Star Borough &mdash; <a href="service-area.html">see communities</a></div></li>
      </ul>
      <div class="card" style="margin-top:18px;background:var(--green);color:#eaf3ee;border:0">
        <h3 style="color:#fff">Why a flat quote?</h3>
        <p style="color:#cfe0d6;margin:0">No hourly meter, no time-and-materials surprises. You approve the price from our book before we start. <a style="color:var(--gold)" href="pricing.html">See how it works.</a></p>
      </div>
    </div>
  </div>
</div></section>
{footer()}</body></html>'''

# ---------------- write ----------------
PAGES={"index.html":home,"services.html":services,"pricing.html":pricing,
       "service-area.html":service_area,"about.html":about,"contact.html":contact}
for slug,fn in PAGES.items():
    with open(os.path.join(OUT,slug),"w") as f: f.write(fn())
    print("wrote",slug)

with open(os.path.join(OUT,"robots.txt"),"w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
urls="".join(
  f"<url><loc>{BASE}/{'' if s=='index.html' else s}</loc><changefreq>monthly</changefreq>"
  f"<priority>{'1.0' if s=='index.html' else '0.8'}</priority></url>" for s in PAGES)
with open(os.path.join(OUT,"sitemap.xml"),"w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>')
print("wrote robots.txt + sitemap.xml")
