#!/usr/bin/env python3
"""
Build gate for anointedink.

Nestor's advertising is wired to his Illinois body art establishment registration:
A conviction for false or deceptive advertising is a ground to suspend or revoke it (77 Ill.
Adm. Code 797.1600(b)); any violation of the Act or Part 797 carries up to $1,000 for each day
the registrant remains in violation (797.1700(b)); and the claims are reachable directly under
815 ILCS 510. So this is a gate, not a checklist.

  python3 lint.py      exit 0 = clean, exit 1 = do not ship
"""
import glob, html, json, os, re, sys
from _data import ARTISTS, BIZ, CITY

FAIL = []
WARN = []

# ---------------------------------------------------------------- banned terms
# Grouped by the rule each one breaks. See ../CLIENT-BRIEF.md for citations.
CREDENTIAL = [  # 815 ILCS 510/2(a)(5). Illinois licenses ESTABLISHMENTS, not artists,
                # so "licensed tattoo artist" names a credential that does not exist.
    "licensed", "certified", "board-certified", "state-certified", "accredited",
    "credentialed", "award-winning", "award winning", "voted best", "top-rated",
    "top rated", "premier", "industry-leading",
]
HEALTH = [  # FTC 16 CFR 255.2(a) substantiation; IDPH routes health questions to physicians
    "heals", "healing", "will heal", "healed perfectly", "risk-free", "risk free",
    "sterile", "sterilized", "medical-grade", "medical grade", "hospital-grade",
    "hospital grade", "infection-free", "hypoallergenic", "non-toxic", "nontoxic",
    "scar-free", "no scarring", "fda-approved", "fda approved",
]
PAIN = [  # FDA March 2024 warning letters to tattoo numbing sellers
    "painless", "pain-free", "pain free", "numbing", "virtually painless",
]
SUPERIORITY = [  # 815 ILCS 510/2(a)(7). Four named local rivals have a private right of action.
    "best in chicago", "best in the suburbs", "best tattoo shop", "cleanest shop",
    "safest shop", "most experienced", "better than any", "#1 in",
]
AFTERCARE = [  # 797.600(b)-(c): verbal + written aftercare in the shop. Off the web by choice
    "aftercare instructions", "how to care for your tattoo", "aftercare guide",
]
BANNED = [(t, "credential") for t in CREDENTIAL] + [(t, "health") for t in HEALTH] + \
         [(t, "pain") for t in PAIN] + [(t, "superiority") for t in SUPERIORITY] + \
         [(t, "aftercare") for t in AFTERCARE]

# Phrases that are legal to say only in the negative, eg "we do not offer numbing".
ALLOWED_CONTEXT = re.compile(r"(do not|does not|never|no |without |cannot|can't)\s*\w*\s*$", re.I)

STOCK = ["unsplash", "pexels", "shutterstock", "istockphoto", "gettyimages", "freepik"]
UK = ["colour", "centre", "organise", "recognise", "specialis", "favourite", "honours",
      "stencilled", "stencilling", "travelled", "jewellery", "cancelled", "labelled", "modelled"]

# Aftercare slips in as a one-line imperative, not as a heading. 2026-09-24 a blog post shipped
# "Keep the piece covered when you are out in it", which no term above catches (797.600).
CARE_IMPERATIVE = re.compile(
    r"\bkeep (it|the piece|the tattoo|your tattoo|your new tattoo) "
    r"(covered|out of the sun|moisturi[sz]ed|clean|wrapped)\b"
    r"|\b(sunscreen|sunblock|spf ?\d+)\b|\bmoisturi[sz]e\b|\b(do not|don't|never) (swim|soak)\b", re.I)
# Things the artist must not promise or prescribe. Warn, then a human reads the sentence.
PROMISE = re.compile(r"\b(in|after) (twenty|thirty|\d+) years\b|\bhow many (laser )?sessions\b"
                     r"|\bguarantee", re.I)


def check_text(path, text):
    low = text.lower()
    for term, kind in BANNED:
        for m in re.finditer(re.escape(term), low):
            before = low[max(0, m.start() - 40):m.start()]
            if ALLOWED_CONTEXT.search(before):
                WARN.append(f"{path}: '{term}' ({kind}) appears in a negated sentence, verify")
                continue
            ctx = text[max(0, m.start() - 55):m.start() + len(term) + 45].replace("\n", " ")
            FAIL.append(f"{path}: BANNED [{kind}] '{term}'  ...{ctx}...")
    if "—" in text or "&mdash;" in text:
        FAIL.append(f"{path}: em dash present ({text.count(chr(8212)) + text.count('&mdash;')}x)")
    for u in UK:
        if u in low:
            FAIL.append(f"{path}: UK spelling '{u}'")
    for sdk in STOCK:
        if sdk in low:
            FAIL.append(f"{path}: stock photo source '{sdk}'")
    for m in CARE_IMPERATIVE.finditer(text):
        ctx = text[max(0, m.start() - 55):m.end() + 45].replace("\n", " ")
        FAIL.append(f"{path}: aftercare instruction '{m.group(0)}'  ...{ctx}...")
    for m in PROMISE.finditer(text):
        ctx = text[max(0, m.start() - 55):m.end() + 45].replace("\n", " ")
        WARN.append(f"{path}: promise or prescription, read it: '{m.group(0)}'  ...{ctx}...")
    if re.search(r"18\s*\+?\s*(or|,)?\s*(with|unless)\s+(a\s+)?parent", low):
        FAIL.append(f"{path}: implies parental consent can authorize tattooing a minor. "
                    "Illinois has no such exception (720 ILCS 5/12C-35).")


# ---------------------------------------------------------------- artist credit
# Every photo belongs to an artist in _data.ARTISTS, every figure credits that artist, and no
# copy claims one artist's work beside another artist's photo. Showing one artist's portfolio
# as another's, or as shop work, is the deceptive-advertising exposure described at the top
# (815 ILCS 510; 797.1600(b)). Added 2026-10-01 with the second artist.
ART = {a["slug"]: a for a in ARTISTS}
SHOWN = re.compile(r'(?:src|srcset|data-full)="[^"]*?img/(tattoo-[a-z0-9-]+?)-(?:400|1000)\.')
NAME = r"[A-Z][a-z]+(?: [A-Z][a-z]+)?"
# "tattoo/tattooed/tattoos/tattooing by X" and "work by X". The footer said "Custom tattooing
# by Nestor Juarez" under another artist's photos and the first version of this rule missed it.
TATTOOED_BY = re.compile(rf"\b(?:[Tt]attoo(?:ed|s|ing)?|[Ww]ork) by ({NAME})"
                         rf"|\b({NAME}) tattooed (?:himself|herself|themselves)\b")
OWN_WORK = re.compile(r"\bown (?:work|tattooing|tattoos|pieces)\b", re.I)
# Provenance. A photo with "atShop": false in the manifest was tattooed somewhere else (an
# artist's own portfolio). A page showing one must say so, and must never say the work was
# done here. Anchored on the verb, so "tattoo artist at Anointed Ink" (a role) is not a claim.
SHOP = (rf"(?:here|in-house|in (?:the|our) shop|at (?:the|our) shop|at {re.escape(BIZ)}"
        rf"|in {re.escape(CITY)}|on 111th Street)")
PROVENANCE = re.compile(rf"\b(?:tattooed|done|inked|made|completed|finished|created)\s+"
                        rf"(?:by {NAME}\s+)?(?:(?:right|all|both)\s+)?{SHOP}\b"
                        rf"|\b(?:tattoos|pieces|work)\s+(?:by|from)\b[^.!?:]{{0,40}}?\s{SHOP}\b",
                        re.I)
NEGATED = re.compile(r"\b(?:not|never|none|no|neither|nor|wasn't|weren't|isn't|aren't)\b", re.I)
DISCLOSED = re.compile(rf"\b(?:not|none|never)\b[^.!?]{{0,40}}?\btattooed at {re.escape(BIZ)}\b",
                       re.I)
SITE_WIDE = re.compile(r"\b(?:every|all)\b[^.!?]{0,60}\b(?:photo|photograph|image|picture|tattoo|"
                       r"piece)s?\b[^.!?]{0,60}\b(?:this|the) (?:site|website)\b", re.I)


def artist_named(name):
    for a in ARTISTS:
        if name in (a["name"], a["short"]) or name.split()[0] == a["short"]:
            return a["slug"]
    return None


def names_in(text):
    """Artist slugs named in `text`, in order of their last mention."""
    hits = []
    for a in ARTISTS:
        for n in (a["name"], a["short"]):
            for m in re.finditer(rf"\b{re.escape(n)}\b", text):
                hits.append((m.start(), a["slug"]))
    return [slug for _, slug in sorted(hits)]


def ld_descriptions(s):
    """Every "description" string in the page's JSON-LD (the shop blurb rides on every page)."""
    out = []
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            stack = [json.loads(blk)]
        except Exception:
            continue  # reported in main()
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "description" and isinstance(v, str):
                        out.append(v)
                    else:
                        stack.append(v)
            elif isinstance(o, list):
                stack.extend(o)
    return out


def provenance_claims(text):
    """'tattooed here' style claims in `text` whose sentence carries no negation."""
    hits = []
    for m in PROVENANCE.finditer(text):
        start = max(text.rfind(c, 0, m.start()) for c in ".!?") + 1
        if not NEGATED.search(text[start:m.start()]):
            hits.append((m, text[max(0, m.start() - 60):m.end() + 40]))
    return hits


def check_credit(path, s, man):
    # 1. every figure with a photo credits the photo's artist, and only that artist
    for fig in re.finditer(r"<figure\b([^>]*)>(.*?)</figure>", s, re.S):
        slugs = set(SHOWN.findall(fig.group(0)))
        for slug in slugs:
            m = man.get(slug)
            if not m:
                FAIL.append(f"{path}: figure shows {slug}, which is not in the manifest"); continue
            a = ART.get(m.get("artist"))
            if not a:
                continue  # reported by the manifest check
            caps = re.findall(r"<figcaption>(.*?)</figcaption>", fig.group(2), re.S)
            caps += re.findall(r'data-caption="([^"]*)"', fig.group(1))
            if not caps:
                FAIL.append(f"{path}: figure {slug} has no caption crediting {a['name']}")
            for c in caps:
                c = html.unescape(re.sub("<[^>]+>", "", c))
                if f"by {a['name']}" not in c:
                    FAIL.append(f"{path}: caption on {slug} does not credit {a['name']}: {c[:80]}")
                for o in ARTISTS:
                    if o["slug"] != a["slug"] and o["name"] in c:
                        FAIL.append(f"{path}: caption on {slug} names {o['name']}, "
                                    f"but the photo is {a['name']}'s")

    # 2. claims in the copy, checked against whose photos the page actually shows
    on_page = {man[x].get("artist") for x in SHOWN.findall(s) if x in man}
    meta = " ".join(re.findall(r'<meta name="description" content="([^"]*)"', s))
    body = re.sub(r"<(script|style|figure)\b.*?</\1>", " ", s, flags=re.S)
    visible = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).replace("\u2019", "'")
    text = ". ".join([visible, html.unescape(meta)] + ld_descriptions(s))
    text = re.sub(r"\s+", " ", text).replace("\u2019", "'")
    for m in TATTOOED_BY.finditer(text):
        who = artist_named(m.group(1) or m.group(2))
        ctx = text[max(0, m.start() - 50):m.end() + 40]
        if not who:
            FAIL.append(f"{path}: credits work to someone not in ARTISTS: ...{ctx}...")
        elif on_page - {who}:
            FAIL.append(f"{path}: says '{m.group(0)}' on a page showing another artist's "
                        f"photos: ...{ctx}...")
    for m in OWN_WORK.finditer(text):
        named = names_in(text[max(0, m.start() - 80):m.start()])
        ctx = text[max(0, m.start() - 60):m.end() + 40]
        if named and on_page - {named[-1]}:
            FAIL.append(f"{path}: '{m.group(0)}' claim for {ART[named[-1]]['name']} beside "
                        f"another artist's photo: ...{ctx}...")
        elif not named and len(on_page) > 1:
            FAIL.append(f"{path}: '{m.group(0)}' on a page showing more than one artist: "
                        f"...{ctx}...")
    if len({m.get("artist") for m in man.values()}) > 1:
        for m in SITE_WIDE.finditer(text):
            sent = m.group(0) + text[m.end():m.end() + 80].split(".")[0]
            if "credited" not in sent and names_in(sent):
                FAIL.append(f"{path}: site-wide claim names one artist, but the site shows "
                            f"several: ...{sent[:140]}...")

    # 3. work not done at the shop is disclosed, and never claimed as done here
    away = sorted({x for x in SHOWN.findall(s) if man.get(x, {}).get("atShop") is False})
    if away:
        caps = [html.unescape(re.sub("<[^>]+>", "", c)) for c in
                re.findall(r"<figcaption>(.*?)</figcaption>", s, re.S) +
                re.findall(r'data-caption="([^"]*)"', s)]
        for m, ctx in provenance_claims(". ".join([text] + caps)):
            FAIL.append(f"{path}: says '{m.group(0)}' on a page showing work not tattooed at "
                        f"{BIZ} ({', '.join(away)}): ...{ctx}...")
        if not DISCLOSED.search(visible):
            FAIL.append(f"{path}: shows {', '.join(away)}, which was not tattooed at {BIZ}, but "
                        f"the page never says so (eg 'not tattooed at {BIZ}')")

    # 4. portfolio-only photos never become a share, preload or business image
    for slug, m in man.items():
        if not m.get("noPromo"):
            continue
        for tag in re.findall(r"<(?:meta|link)\b[^>]*>", s):
            if f"img/{slug}-" in tag:
                FAIL.append(f"{path}: {slug} is portfolio only, but it is in {tag[:90]}")
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                obj = json.loads(blk)
            except Exception:
                continue  # reported below
            stack = [obj]
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in ("image", "logo") and f"img/{slug}-" in json.dumps(v):
                            FAIL.append(f"{path}: {slug} is portfolio only, but JSON-LD uses "
                                        f"it as an {k}")
                        stack.append(v)
                elif isinstance(o, list):
                    stack.extend(o)


def main():
    pages = sorted(glob.glob("**/*.html", recursive=True))
    if not pages:
        print("no pages built"); return 1
    man = {}
    if os.path.exists("img/manifest.json"):
        man = {m["slug"]: m for m in json.load(open("img/manifest.json"))}
    for p in pages:
        s = open(p).read()
        check_text(p, s)
        check_credit(p, s, man)

        # one h1, present
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if len(h1) != 1:
            FAIL.append(f"{p}: {len(h1)} h1 tags, expected exactly 1")

        # title and description within range
        t = re.search(r"<title>(.*?)</title>", s)
        d = re.search(r'name="description" content="(.*?)"', s)
        if not t or not d:
            FAIL.append(f"{p}: missing title or meta description")
        else:
            if len(t.group(1)) > 62: WARN.append(f"{p}: title {len(t.group(1))} chars")
            if len(d.group(1)) > 158: WARN.append(f"{p}: description {len(d.group(1))} chars")

        # every img needs alt, width, height
        for img in re.findall(r"<img\b[^>]*>", s):
            if 'alt="' not in img:
                FAIL.append(f"{p}: <img> without alt: {img[:90]}")
            elif 'alt=""' in img and "lb" not in p:
                pass  # the lightbox img is populated by JS
            if "width=" not in img or "height=" not in img:
                if 'src=""' not in img:
                    WARN.append(f"{p}: <img> without width/height: {img[:80]}")

        # JSON-LD must parse, and must never carry a self-serving rating
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                obj = json.loads(blk)
            except Exception as e:
                FAIL.append(f"{p}: invalid JSON-LD: {e}"); continue
            flat = json.dumps(obj)
            if "aggregateRating" in flat or '"review"' in flat:
                FAIL.append(f"{p}: JSON-LD carries aggregateRating/review. Google's self-serving "
                            "review policy makes this ineligible and risks a manual action.")
        if "<html lang=" not in s:
            FAIL.append(f"{p}: missing lang attribute")
        if 'name="viewport"' not in s:
            FAIL.append(f"{p}: missing viewport meta")

    # manifest alt text sanity
    if os.path.exists("img/manifest.json"):
        for m in json.load(open("img/manifest.json")):
            if len(m["alt"]) < 20:
                WARN.append(f"manifest: thin alt text on {m['slug']}")
            check_text(f"manifest:{m['slug']}", m["alt"] + " " + m.get("caption", ""))
            if m.get("atShop") is False:
                for hit, ctx in provenance_claims(m["alt"] + ". " + m.get("caption", "")):
                    FAIL.append(f"manifest: {m['slug']} was not tattooed at {BIZ}, but its alt "
                                f"or caption says '{hit.group(0)}'")
            if m.get("artist") not in ART:
                FAIL.append(f"manifest: {m['slug']} has artist {m.get('artist')!r}, which is not "
                            "in ARTISTS (_data.py). Every photo is credited to a known artist.")

    print(f"checked {len(pages)} pages")
    for w in WARN[:25]:
        print("  WARN ", w)
    if len(WARN) > 25:
        print(f"  ... and {len(WARN)-25} more warnings")
    for f in FAIL:
        print("  FAIL ", f)
    print()
    if FAIL:
        print(f"RESULT: {len(FAIL)} FAILURES, {len(WARN)} warnings. DO NOT SHIP.")
        return 1
    print(f"RESULT: PASS. 0 failures, {len(WARN)} warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
