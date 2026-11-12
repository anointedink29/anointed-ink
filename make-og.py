#!/usr/bin/env python3
"""
Render the 1200x630 social preview card.

og:image must be an absolute URL and a real JPEG, because social scrapers do not
run JS and several will not take WebP or AVIF. Run after build.py.
  python3 make-og.py <hero-slug>
"""
import json, os, subprocess, sys, base64
from _data import GRATING, GCOUNT, PHONE, RATING_AS_OF, OWNER  # one source with the site

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "img/og.jpg"

def main():
    # The card says "Custom tattoos by Nestor Juarez", so its photo must be his, and never a
    # portfolio-only piece (noPromo, eg a sports team's mark).
    man = [m for m in json.load(open("img/manifest.json"))
           if m.get("artist") == OWNER and not m.get("noPromo")]
    slug = sys.argv[1] if len(sys.argv) > 1 else man[0]["slug"]
    hero = next((m for m in man if m["slug"] == slug), None)
    if not hero:
        sys.exit(f"{slug}: not one of {OWNER}'s promotable photos; the card would misattribute it")
    data = base64.b64encode(open(f"img/{hero['slug']}-1000.webp", "rb").read()).decode()

    font = lambda f: base64.b64encode(open(f"fonts/{f}", "rb").read()).decode()
    html = """<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:C;src:url(data:font/woff2;base64,__CINZEL__) format("woff2");font-weight:400 900}
@font-face{font-family:S;src:url(data:font/woff2;base64,__SCHIB__) format("woff2");font-weight:400 900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;display:flex;color:#f4f1f6;font-family:S,-apple-system,Helvetica,Arial,sans-serif;
 overflow:hidden;background:radial-gradient(75% 95% at 76% 40%,#523863 0%,#3f2a4a 42%,#221827 78%,#120e15 100%)}
.l{flex:1;padding:64px 40px 64px 64px;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-size:19px;font-weight:700;letter-spacing:.22em;color:#e0d2fa;margin-bottom:22px}
.logo{width:600px;height:auto;display:block;margin:0 0 24px;filter:drop-shadow(0 16px 26px rgba(0,0,0,.45))}
.sub{font-size:26px;color:#d6cfdc;line-height:1.45;margin-bottom:30px}
.meta{display:flex;gap:14px;align-items:center;font-size:22px;font-weight:700}
.pill{background:#1e1724;border:1.5px solid #b8b1c2;padding:11px 20px}
.asof{font-size:17px;color:#bcb3c3;margin-top:14px}
.stars{color:#efe8dc;letter-spacing:.06em}
.r{width:420px;flex-shrink:0;display:flex;align-items:center;justify-content:center;padding-right:56px}
.arch{width:330px;height:500px;border:11px solid #0d0a0f;border-radius:50% 50% 6px 6px/30% 30% 6px 6px;overflow:hidden;
 box-shadow:0 0 0 2px #4d4756,0 0 0 4px #b8b1c2,0 40px 60px -20px rgba(0,0,0,.7)}
.arch img{width:100%;height:100%;object-fit:cover;object-position:50% 30%}
</style><body>
<div class="l">
 <div class="eyebrow">CHICAGO RIDGE, ILLINOIS</div>
 <img class="logo" src="data:image/webp;base64,__LOGO__" alt="">
 <div class="sub">Custom tattoos by Nestor Juarez.<br>Black &amp; grey Chicano realism, portraits,
 cover-ups.</div>
 <div class="meta">
  <span class="pill"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> __R__ &middot; __N__ reviews</span>
  <span class="pill">__P__</span>
 </div>
 <div class="asof">Google rating as of __D__</div>
</div>
<div class="r"><div class="arch"><img src="data:image/webp;base64,__IMG__"></div></div>
</body>""".replace("__IMG__", data).replace("__R__", GRATING).replace("__N__", GCOUNT)\
        .replace("__P__", PHONE).replace("__D__", RATING_AS_OF)\
        .replace("__CINZEL__", font("cinzel.woff2")).replace("__LOGO__", base64.b64encode(open("img/logo-reverse.webp", "rb").read()).decode()).replace("__SCHIB__", font("schibsted.woff2"))

    open("_og.html", "w").write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1200,630",
                    "--screenshot=_og.png", "--virtual-time-budget=4000",
                    "file://" + os.path.abspath("_og.html")],
                   check=True, capture_output=True)
    from PIL import Image
    im = Image.open("_og.png").convert("RGB")
    im = im.resize((1200, 630), Image.LANCZOS)
    im.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    os.remove("_og.png"); os.remove("_og.html")
    print(f"og image: {OUT}  {im.size}  {os.path.getsize(OUT)/1024:.0f}KB  hero={hero['slug']}")

if __name__ == "__main__":
    main()
