# -*- coding: utf-8 -*-
"""
Verified facts for anointedink.

Every value here was checked against a named public source on 2026-09-24 and the
source is recorded in ../CLIENT-BRIEF.md. Do not add a value without one.
"""

# ---- launch switches -------------------------------------------------------
INDEXABLE = False                                    # noindex until Nestor approves
BASE = "https://anointed.ink"                       # custom domain (HTTPS works once GoDaddy has all 4 GitHub A records)
BUILT = "2026-09-24"
GTM_ID = "GTM-5V38S4MR"                              # Anointed Ink's own GTM account (6380221591); fires GA4 G-MCC1ZVKMPR (property 557063878). Moved 2026-10-02.

# ---- NAP, matches the Google Business Profile exactly ----------------------
BIZ    = "Anointed Ink"
ARTIST = "Nestor Juarez"
HANDLE = "Tat2Nestuhh"
STREET = "5920 W 111th St"
CITY   = "Chicago Ridge"
STATE  = "IL"
STATE_FULL = "Illinois"
ZIP    = "60415"
PHONE  = "(708) 770-2754"
TEL    = "+17087702754"
EMAIL  = "anointed.ink29@gmail.com"
LAT, LNG = 41.6907469, -87.7673829
PLUSCODE = "M6RM+72 Chicago Ridge, Illinois"
RATE   = "$150"          # his Instagram bio. CONFIRM
YEARS  = "25+"           # his Popl card and Instagram bio. His own claim.
GRATING, GCOUNT = "5.0", "115"    # Google Business Profile

GBP = "https://www.google.com/maps/place/Anointed+Ink/@41.6907469,-87.7673829,672m"
IG  = "https://www.instagram.com/tat2nestuhh/"
IG_HANDLE = "@tat2nestuhh"
FB  = "https://www.facebook.com/ghtto.mex/"
FBPAGE = "https://www.facebook.com/profile.php?id=61590253627999"
SNAP = "https://www.snapchat.com/add/tat2nestuh0610"

HOURS = [(d, "12:00", "19:00") for d in
         ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")]
HOURS_HUMAN = "Monday to Saturday, 12pm to 7pm. Closed Sunday."

AREAS = ["Chicago Ridge", "Oak Lawn", "Worth", "Alsip", "Palos Heights", "Bridgeview",
         "Burbank", "Evergreen Park", "Hometown", "Palos Hills", "Hickory Hills",
         "Chicago's Southwest Side"]

TAGLINE = "Don't be average. Be set apart."

# ---- verified Google reviews ----------------------------------------------
REVIEWS = [
    # Verbatim from the Google Business Profile, including original spelling and punctuation.
    # 16 CFR 255.1(a)-(b): editing a review so it no longer fairly reflects its substance is
    # deceptive, so these are NOT cleaned up. Ellipsis only where the review continues.
    ("Owner and Main Tattoo Artist Nestor never disappoints. I Have had 2 tattoos done by Nestor "
     "one was a complete cover up and the 2nd was a partial cover up and add on.&hellip;",
     "Timothy C."),
    ("I always have a good experience getting tattooed by Nestor- his artwork is top notch and "
     "always keeps me coming back!&hellip;", "Marie E."),
    ("We got 2 tattoos that look like stickers!! Awesome work I loved the work so much I booked "
     "another appointment! Book it dont wait!", "Sean M."),
]
# Deliberately NOT republished: a review opening "Best tattoo shop in town". Lifting it onto our
# own site converts it into our own superiority claim (16 CFR 255.1(a)-(b)), which 815 ILCS
# 510/2(a)(7) reaches and which four named local rivals have a private right of action over.

RATING_AS_OF = "September 24, 2026"   # date-stamp the rating so it is true-as-of, not a promise
RATING_AS_OF_ES = "24 de septiembre de 2026"   # same date for the Spanish page; update both together

# ---- contact routes, ordered by how Nestor actually works -------------------
SMS_BODY = ("Hi Nestor, I saw your site.%0A%0AIdea:%0APlacement:%0ARough size in inches:"
            "%0ABlack and grey or color:%0ACover-up (yes/no):%0ABest days for me:")
SMS = f"sms:{TEL}?&body={SMS_BODY}"
IG_DM = "https://ig.me/m/tat2nestuhh"

# ---- artists ---------------------------------------------------------------
# Every photo in img/manifest.json carries an "artist" key that must be a slug here;
# lint.py fails the build on any other value. Each artist gets /artists/<slug>/.
# Write only what each artist has confirmed. For Cristhian that is his name, his Instagram
# handle and display name (Nestor's 2026-09-29 email: his QR code plus three photos of his
# work). NOT known, so never written: resident or guest, start date, years, rate, booking
# days. His three photos are his own portfolio: photo metadata shows none of the three was
# taken at Anointed Ink, so each carries "atShop": false and the site says none was tattooed
# there (lint.py fails a page that shows one and says otherwise, or leaves that out).
OWNER = "nestor-juarez"
ARTISTS = [
    dict(slug="nestor-juarez", name=ARTIST, short="Nestor", alt_names=[HANDLE],
         handle=IG_HANDLE, ig=IG, dm=IG_DM, role="Owner and tattoo artist",
         person_id="/about/#nestor",
         photo_note=("Several carry his watermark, which reads <em>Ghtto_Mex</em> or "
                     "<em>Tattoonestor_juarez</em>. Some pieces are photographed fresh, still "
                     "under wrap, which is why a few of them look glossy or soft.")),
    dict(slug="cristhian-oyola", name="Cristhian Oyola", short="Cristhian",
         alt_names=["Oyola Ink"], handle="@andrees_ink",
         ig="https://www.instagram.com/andrees_ink/", dm="https://ig.me/m/andrees_ink",
         role="Tattoo artist", person_id="/artists/cristhian-oyola/#person",
         photo_note=("These come from his portfolio and were not tattooed at "
                     "Anointed Ink.")),
]
ARTIST_BY = {a["slug"]: a for a in ARTISTS}

# ---- Illinois rules we are allowed to state, with citations -----------------
LAW_AGE = ("18 and over, no exceptions. Illinois law does not allow a parent to consent to a "
           "minor being tattooed (720 ILCS 5/12C-35).")
LAW_ID = ("Bring a government-issued photo ID showing your date of birth. Illinois rules require "
          "the shop to verify age from it every visit, including for people we already know "
          "(77 Ill. Adm. Code 797.400(k)).")
LAW_MINORS_PRESENT = ("Anyone under 18 has to be with a parent or legal guardian just to be on "
                      "the premises while tattooing is happening (720 ILCS 5/12C-35(b)).")

# ---- style pages -----------------------------------------------------------
# slug, nav label, h1, style tags pulled from the photo manifest
STYLE_PAGES = [
    dict(slug="black-and-grey-chicano-realism", nav="Black &amp; Grey",
         h1="Black &amp; grey Chicano realism",
         tags=["chicano", "black-and-grey-realism"], hero="tattoo-catrina-woman-with-roses"),
    dict(slug="cover-up-tattoos", nav="Cover-Ups", h1="Cover-up tattoos",
         tags=["cover-up"], hero="tattoo-crowned-skull-cover-up"),
    dict(slug="portrait-tattoos", nav="Portraits", h1="Portrait tattoos",
         tags=["portrait"], hero="tattoo-woman-and-lioness-split-portrait"),
    dict(slug="religious-tattoos", nav="Religious", h1="Religious tattoos",
         tags=["religious"], hero=None),
    dict(slug="memorial-tattoos", nav="Memorials", h1="Memorial tattoos",
         tags=["memorial"], hero=None),
    dict(slug="aztec-and-chicano-culture-tattoos", nav="Aztec &amp; Cultural",
         h1="Aztec and cultural tattoos",
         tags=["aztec-cultural"], hero="tattoo-aztec-warrior-bear"),
    dict(slug="color-realism-tattoos", nav="Color", h1="Color realism tattoos",
         tags=["color-realism"], hero=None),
    dict(slug="tattoo-sleeves", nav="Sleeves", h1="Tattoo sleeves",
         tags=["sleeve"], hero=None),
]

# human labels for the gallery filter chips
STYLE_LABELS = {
    "black-and-grey-realism": "Black &amp; grey realism",
    "chicano": "Chicano",
    "portrait": "Portraits",
    "religious": "Religious",
    "memorial": "Memorials",
    "aztec-cultural": "Aztec &amp; cultural",
    "color-realism": "Color realism",
    "animal": "Animals",
    "floral": "Floral",
    "sleeve": "Sleeves",
    "lettering-script": "Script &amp; lettering",
    "ornamental": "Ornamental",
    "cover-up": "Cover-ups",
    "anime-character": "Anime &amp; characters",
    "fine-line": "Fine line",
}

# ---- main nav --------------------------------------------------------------
NAV = [("", "Home"), ("gallery/", "Gallery"),
       ("black-and-grey-chicano-realism/", "Black &amp; Grey"),
       ("cover-up-tattoos/", "Cover-Ups"), ("pricing/", "Pricing"),
       ("blog/", "Blog"), ("about/", "About"), ("book/", "Send your idea")]
