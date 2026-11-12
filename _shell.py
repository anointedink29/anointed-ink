# -*- coding: utf-8 -*-
"""Page shell: head, nav, footer, schema, and the image helpers."""
import html, json, re
from _data import *
from _css import CSS
from _js import JS

# Photos held back from every page. A tattoo of an identifiable child is a use of that
# child's likeness; hold it until a parent's written release is on file (765 ILCS 1075/30).
WITHHELD = {"tattoo-child-portrait-with-handprint"}
MAN = [m for m in json.load(open("img/manifest.json")) if m["slug"] not in WITHHELD]
BYSLUG = {m["slug"]: m for m in MAN}


# ------------------------------------------------------------------- artists
# Google Tag Manager (GTM_ID in _data.py). Plain strings, not f-strings: the JS braces stay literal.
GTM_HEAD = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
            "})(window,document,'script','dataLayer','" + GTM_ID + "');</script>")
GTM_BODY = ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' + GTM_ID +
            '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>')


def by_artist(slug):
    """One artist's photos, best first. Counts and claims about an artist use only these."""
    return [m for m in MAN if m["artist"] == slug]


OWN = by_artist(OWNER)          # Nestor's work: the style pages and every "by Nestor" claim


def artist_of(m):
    return ARTIST_BY[m["artist"]]


def person_id(a):
    return BASE + a["person_id"]


def credit(m, cap=None):
    """Caption text with the artist credit every photo on this site carries."""
    cap = (m.get("caption", "") if cap is None else cap).strip()
    name = artist_of(m)["name"]
    if not cap:
        return f"Tattoo by {name}"
    if cap[-1] in ".!?":
        return f"{cap} Tattoo by {name}."
    return f"{cap}, by {name}"


def rel(path):
    """Relative prefix from a page at `path` back to the site root."""
    depth = path.count("/")
    return "../" * depth if depth else ""


def pic(slug, width, p="", cls="", lazy=True, sizes=None, w=None, h=None, widths=None):
    """<picture> with AVIF then WebP then a JPEG fallback at 400. `widths` (eg [400, 1000])
    lists both sizes with their real pixel widths, so the browser picks by `sizes`."""
    m = BYSLUG[slug]
    sw, sh = m["sizes"][str(width)]
    if w and h:
        sw, sh = w, h
    r = rel(p)
    load = ('loading="lazy" decoding="async"' if lazy
            else 'fetchpriority="high" decoding="async"')
    sz = f' sizes="{sizes}"' if sizes else ""
    fb = f"{r}img/{slug}-400.jpg"

    def srcset(ext):
        if not widths:
            return f"{r}img/{slug}-{width}.{ext}"
        return ", ".join(f"{r}img/{slug}-{x}.{ext} {m['sizes'][str(x)][0]}w" for x in widths)
    return (f'<picture>'
            f'<source type="image/avif" srcset="{srcset("avif")}"{sz}>'
            f'<source type="image/webp" srcset="{srcset("webp")}"{sz}>'
            f'<img src="{fb}" alt="{html.escape(m["alt"])}" width="{sw}" height="{sh}" '
            f'{load}{" class=" + cls if cls else ""}></picture>')


def figure(slug, p="", tag_attrs=True, eager=False, cls="", widths=None, sizes=None, ar=False):
    """A gallery figure wired for the filter and the lightbox. `cls` goes on the img (eg op-top).
    `ar` puts the photo's shape on the figure (--ar), for the gallery's rows of even height."""
    m = BYSLUG[slug]
    r = rel(p)
    fw, fh = m["sizes"]["1000"]
    cap = credit(m)
    attrs = f' style="--ar:{fw / fh:.3f}"' if ar else ""
    if tag_attrs:
        attrs += (f' data-styles="{" ".join(m["styles"])}"'
                 f' data-artist="{m["artist"]}"'
                 f' data-full="{r}img/{slug}-1000.webp"'
                 f' data-fw="{fw}" data-fh="{fh}"'
                 f' data-alt="{html.escape(m["alt"], quote=True)}"'
                 f' data-caption="{html.escape(cap, quote=True)}"')
    return (f'<figure{attrs} tabindex="0">{pic(slug, 400, p, cls=cls, lazy=not eager, widths=widths, sizes=sizes)}'
            f'<figcaption>{html.escape(cap)}</figcaption></figure>')


def by_tags(tags, limit=None, exclude=(), artist=OWNER):
    """Manifest entries carrying any of `tags`, best first. Nestor's only unless `artist` is
    given (None means every artist), because the style pages and their copy are his."""
    out = [m for m in MAN
           if any(t in m["styles"] for t in tags) and m["slug"] not in exclude
           and (artist is None or m["artist"] == artist)]
    return out[:limit] if limit else out


# --------------------------------------------------------------------- schema
def shop_ld():
    return {
        "@context": "https://schema.org", "@type": ["TattooParlor", "LocalBusiness"],
        "@id": BASE + "/#shop",
        "name": BIZ,
        "description": (f"Custom tattoo shop in {CITY}, {STATE_FULL}. Black and grey Chicano "
                        f"realism, portraits, color realism, memorials, cover-ups and custom "
                        f"work. Owned by {ARTIST}."),
        "url": BASE + "/", "telephone": PHONE, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                    "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": GBP, "priceRange": "$$", "currenciesAccepted": "USD",
        "image": [f"{BASE}/img/{m['slug']}-1000.webp"
                  for m in [m for m in OWN if not m.get("noPromo")][:6]],
        "logo": f"{BASE}/img/logo.png",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": f"https://schema.org/{d}",
             "opens": o, "closes": c} for d, o, c in HOURS] + [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": "https://schema.org/Sunday", "opens": "00:00", "closes": "00:00"}],
        "sameAs": [IG, FB, FBPAGE, SNAP],
        "areaServed": [{"@type": "City", "name": a} for a in AREAS if "'" not in a],
        "founder": {"@type": "Person", "@id": BASE + "/about/#nestor", "name": ARTIST,
                    "alternateName": HANDLE, "jobTitle": "Owner and Tattoo Artist"},
        "knowsAbout": ["Black and grey Chicano realism", "Portrait tattoos", "Cover-up tattoos",
                       "Color realism tattoos", "Memorial tattoos", "Aztec and cultural tattoos",
                       "Religious tattoos", "Body piercing"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Tattoo services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {
                    "@type": "Service",
                    "name": re.sub("<[^>]+>", "", sp["h1"]).replace("&amp;", "and"),
                    "url": f"{BASE}/{sp['slug']}/"}} for sp in STYLE_PAGES] + [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Body piercing",
                                                   "url": f"{BASE}/piercing/"}}]},
        # aggregateRating and review are deliberately absent. Under Google's self-serving
        # review policy a business marking up its own reviews is INELIGIBLE for the star
        # feature, so the markup buys nothing and the only outcomes are neutral or bad.
        # (Verified 2026-09-24: this is an eligibility rule, not an automatic penalty. The
        # manual-action risk attaches to marking up content that is not visible on the page.)
        # The 5.0 from 115 is shown as visible, dated, linked body text instead.
    }


def breadcrumbs(trail, path):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    for i, (name, href) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name,
                      "item": f"{BASE}/{href}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


# ----------------------------------------------------------------- head/foot
# The cross from the shop's sign, drawn once per page and reused by the nav and the home hero.
SPRITE = ('<svg class="ai-sprite" aria-hidden="true" focusable="false"><defs>'
          '<linearGradient id="ai-chrome" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#cfc9d8"/>'
          '<stop offset=".55" stop-color="#6f6879"/><stop offset=".72" stop-color="#e9e5ee"/>'
          '<stop offset="1" stop-color="#8d8697"/></linearGradient>'
          '<symbol id="ai-cross" viewBox="0 0 100 140"><path d="M50 0 59 11 56 13V34H86L88 31 100 40 88 49 '
          '86 46H56V124L59 127 50 140 41 127 44 124V46H14L12 49 0 40 12 31 14 34H44V13L41 11Z" '
          'fill="url(#ai-chrome)" stroke="rgba(0,0,0,.55)" stroke-width="1.6"/>'
          '<path d="M50 4V136M4 40H96" stroke="rgba(255,255,255,.55)" stroke-width="1"/></symbol>'
          '</defs></svg>')


def shop_photo(r=""):
    """The sign over the shop's counter, on its violet wall (Eddie's photo, 11-06; no people in
    the crop). It is not a tattoo, so it sits outside the portfolio manifest."""
    return (f'<figure class="shopwall"><picture>'
            f'<source type="image/webp" srcset="{r}img/shop-sign-800.webp 800w, '
            f'{r}img/shop-sign-1400.webp 1400w" sizes="(max-width:940px) 92vw, 1150px">'
            f'<img src="{r}img/shop-sign-800.jpg" alt="The {BIZ} sign on the shop&rsquo;s violet '
            f'wall: wings, a cross and two tattoo machines" width="1400" height="816" '
            f'loading="lazy" decoding="async"></picture>'
            f'<figcaption>The sign over the counter, {STREET}, {CITY}.</figcaption></figure>')


def head(title, desc, path, extra_ld=None, og_img="og", preload=None, crumbs=None,
         extra_head="", lang="en", og_alt=None):
    robots = ("index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
              if INDEXABLE else "noindex,nofollow")
    canon = f"{BASE}/{path}" if path else BASE + "/"
    r = rel(path)
    ld = [shop_ld()]
    if crumbs:
        ld.append(breadcrumbs(crumbs, path))
    if extra_ld:
        ld.extend(extra_ld)
    blocks = "\n".join('<script type="application/ld+json">' +
                       json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "</script>"
                       for x in ld)
    links = "".join(
        f'<a href="{r}{h}"{" aria-current=page" if h == path else ""}>{t}</a>'
        for h, t in NAV)
    pl = ""
    if preload:
        pl = (f'<link rel="preload" as="image" href="{r}img/{preload}-1000.avif" '
              f'type="image/avif" fetchpriority="high">')
    for x in (og_img, preload):
        if x in BYSLUG and BYSLUG[x].get("noPromo"):
            raise SystemExit(f"{path}: {x} is portfolio only, never a share or preload image")
    ogimg = f"{BASE}/img/og.jpg" if og_img == "og" else f"{BASE}/img/{og_img}-1000.webp"
    ogw, ogh = (1200, 630) if og_img == "og" else BYSLUG[og_img]["sizes"]["1000"]
    if og_alt is None:
        if og_img in BYSLUG and BYSLUG[og_img]["artist"] != OWNER:
            raise SystemExit(f"{path}: share image {og_img} is not {ARTIST}'s; pass og_alt")
        og_alt = f"{BIZ}, custom tattoos by {ARTIST} in {CITY}, {STATE}"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
{GTM_HEAD}
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="{ogw}">
<meta property="og:image:height" content="{ogh}">
<meta property="og:image:alt" content="{html.escape(og_alt)}">
<meta property="og:locale" content="{lang}_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{ogimg}">
<meta name="theme-color" content="#120e15">
<meta name="geo.region" content="US-IL">
<meta name="geo.placename" content="{CITY}">
<meta name="geo.position" content="{LAT};{LNG}">
<meta name="ICBM" content="{LAT}, {LNG}">
<link rel="icon" type="image/svg+xml" href="{BASE}/img/icon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{BASE}/img/favicon-32.png">
<link rel="apple-touch-icon" href="{BASE}/img/apple-touch-icon.png">
<link rel="preload" href="/fonts/cinzel.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/schibsted.woff2" as="font" type="font/woff2" crossorigin>
{pl}{extra_head}
<style>{CSS}</style>
{blocks}
</head>
<body>
{GTM_BODY}
{SPRITE}
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap nav">
<a class="brand" href="{r or "./"}"><svg aria-hidden="true" focusable="false"><use href="#ai-cross"/></svg>Anointed <span>Ink</span></a>
<nav class="navlinks" aria-label="Main">{links}</nav>
<a class="callbtn" href="tel:{TEL}">Call {PHONE}</a>
<button class="burger" aria-label="Menu" aria-expanded="false">&#9776;</button>
</div></header>
<main id="main">"""


def hours_table():
    rows = "".join(f"<tr><th>{d}</th><td>12:00pm to 7:00pm</td></tr>" for d, _, _ in HOURS)
    return (f'<table class="hrs"><caption class="sr">Opening hours</caption><tbody>{rows}'
            f"<tr><th>Sunday</th><td>Closed</td></tr></tbody></table>")


def visit(path="", h2="Visit the shop"):
    r = rel(path)
    return f"""<section id="visit" class="alt"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Find us</p><h2>{h2}</h2>
<p>We are on 111th Street in {CITY}, minutes from Oak Lawn, Worth, Alsip and Burbank.</p></div>
{shop_photo(r)}
<div class="visit">
 <div>
  <address class="addr"><strong>{BIZ}</strong><br>{STREET}<br>{CITY}, {STATE} {ZIP}<br>
   <a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
  <p style="margin-top:20px"><a class="btn btn-s" href="{GBP}" rel="noopener">Get directions</a></p>
  <p class="areas" style="margin-top:24px"><strong style="color:var(--tx)">Serving</strong><br>
  {", ".join(AREAS)}.</p>
 </div>
 <div><h3>Hours</h3>{hours_table()}
  <p class="areas" style="margin-top:20px"><strong style="color:var(--tx)">Walk-ins welcome</strong>
  when an artist is free. <a href="{r}walk-in-tattoos/">What to expect</a>.</p>
  <p class="areas" style="margin-top:12px">Plus code {PLUSCODE}</p></div>
</div></div></section>"""


def lightbox():
    return """<div class="lb" aria-hidden="true" role="dialog" aria-label="Tattoo photograph">
<button class="x" aria-label="Close">&times;</button>
<button class="prev" aria-label="Previous">&#8249;</button>
<button class="next" aria-label="Next">&#8250;</button>
<figure><img src="" alt=""><figcaption></figcaption></figure></div>"""


def foot(path=""):
    r = rel(path)
    pages = "".join(f'<li><a href="{r}{h}">{t}</a></li>'
                    for h, t in NAV[:-1] + [("artists/", "Artists"), NAV[-1]])
    styles = "".join(f'<li><a href="{r}{s["slug"]}/">{s["nav"]}</a></li>' for s in STYLE_PAGES[:6])
    return f"""</main>
<footer><div class="wrap"><div class="foot">
 <div>
  <img class="footlogo" src="{r}img/logo-footer.webp" alt="{BIZ} Tattoo Studio" width="520" height="244" loading="lazy" decoding="async">
  <h3 class="sr">{BIZ}</h3>
  <p>Custom tattooing in {CITY}, {STATE_FULL}. Owned by {ARTIST}.<br>
  Black &amp; grey Chicano realism, portraits, color, memorials and cover-ups.</p>
  <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p><a href="{IG}" rel="noopener me">Instagram</a> &middot;
     <a href="{FB}" rel="noopener me">Facebook</a> &middot;
     <a href="{GBP}" rel="noopener">Google</a></p>
 </div>
 <div><h3>Pages</h3><ul>{pages}</ul></div>
 <div><h3>Work</h3><ul>{styles}</ul></div>
 <div><h3>Visit</h3><ul>
   <li>{STREET}</li><li>{CITY}, {STATE} {ZIP}</li>
   <li>Mon to Sat, 12pm to 7pm</li><li>Sunday closed</li>
   <li><a href="{r}walk-in-tattoos/">Walk-ins welcome</a></li>
   <li><a href="{GBP}" rel="noopener">Directions</a></li></ul></div>
</div>
<div class="legal">&copy; 2026 {BIZ}. Every tattoo photograph on this site is
credited to the artist who tattooed it.</div>
</div></footer>
<div class="stickybar">
 <a class="btn btn-p" href="{SMS}">Text your idea</a>
 <a class="btn btn-s" href="tel:{TEL}">Call</a>
</div>
<script>{JS}</script>
</body></html>"""
