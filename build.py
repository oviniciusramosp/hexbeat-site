#!/usr/bin/env python3
"""Writes the landing page (index.html) and sitemap.xml for HexBeat, in the scheme of the Bíblia Duo site: one URL per
language (only English for now: the app's only language), Smart App Banner, MobileApplication JSON-LD without ratings,
Open Graph, Apple's official badge. support.html and privacy.html are hand-written pages next to it.
usage: python3 build.py   (then commit the generated files; GitHub Pages serves them as they are)
Images (img/): real simulator captures from ../docs/media/shots (aso-play15, aso-play19, aso-sheet, aso-results),
cropped and converted to WebP with ffmpeg; hero.webp and og.jpg are the text-free App Store header art
(../store/ai/in/header.png)."""
import html, json, os

BASE = "https://oviniciusramosp.github.io/hexbeat-site/"
APP_ID = "6827372551"
STORE = f"https://apps.apple.com/app/id{APP_ID}"
HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = {
    "en": dict(path="", html_lang="en", og_locale="en_US", badge="en-us",
               name="HexBeat: Boxing Rhythm", short="HexBeat",
               title="HexBeat: Boxing Rhythm — punch to the beat on Apple Vision Pro",
               description="A boxing rhythm game for Apple Vision Pro: punch six glowing pads in time with the music, "
                           "play the HexBeat Originals or songs you own, and save every song as a boxing workout.",
               tagline="Punch to the beat on Apple Vision Pro.",
               facts="Hand tracking · Five levels · Game Center",
               badge_alt="Download on the App Store",
               hero_alt="Two fists in boxing wraps punching a glowing hexagon of six neon pads",
               sections=[
                   ("Punch to the beat",
                    "Pulses of light race from the center of a hexagon to six pads around you. Hit each pad the moment the "
                    "light arrives: every punch is scored on timing, power and accuracy.",
                    "play", "The neon hexagon in a living room, with light pulses on its spokes"),
                   ("Chain hits. Go gold.",
                    "Every combo raises your multiplier. Reach 8x and the arena turns gold in Fever mode, with your hands on "
                    "fire.",
                    "gold", "The hexagon glowing gold with an 8X multiplier and bursts of particles"),
                   ("Climb the leaderboards",
                    "Five levels on every song, from Easy to Expert+, each with its own Game Center leaderboard. Songs you add "
                    "can be compared with players who have the same recording, ranked by accuracy.",
                    "ranking", "A song sheet with five levels and the top of its leaderboard"),
                   ("Every punch, scored",
                    "After each song, see your rank, best combo, timing, power and accuracy on every pad, and the calories "
                    "you burned.",
                    "results", "The results screen with an S rank, score, timing, power and accuracy per pad"),
               ],
               cards=[
                   ("Your music", "Add audio files you own. HexBeat maps every beat into punches on five levels and "
                                  "recognizes the song to show its cover and artist."),
                   ("A real workout", "Watch your calories live in the arena and save a whole session, or each song, as a "
                                      "boxing workout in the Health app."),
                   ("Fits your space", "Set the distance, height and size of the hexagon. Play in your room or inside the "
                                       "HexBeat arena. No controllers needed."),
               ],
               privacy="Privacy policy", support="Support",
               requirements_title="What you need",
               requirements=["Apple Vision Pro with visionOS 27 or later",
                             "About 1 meter (3 feet) of clear space around you",
                             "Internet only for leaderboards and song recognition"],
               cta_title="Get HexBeat",
               cta="On the App Store for Apple Vision Pro.",
               credits="Music: HexBeat Originals, made for HexBeat.",
               legal="Apple, the Apple logo, Apple Vision Pro, visionOS, Game Center and Shazam are trademarks of Apple Inc., "
                     "registered in the U.S. and other countries. App Store is a service mark of Apple Inc."),
}
SHOTS = {"play": (1400, 788), "gold": (1400, 788), "ranking": (1400, 788), "results": (1400, 788)}


def badge(p):
    # Apple's official badge, served by Apple Marketing Tools (their embed code hotlinks it). No Vision Pro badge there.
    src = f"https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/{p['badge']}"
    return (f"<a class='badge' href='{STORE}'><img src='{src}' alt='{html.escape(p['badge_alt'])}' "
            f"width='200' height='67'></a>")


def page(code):
    p = PAGES[code]
    e = html.escape
    root = "../" if p["path"] else ""
    url = BASE + p["path"]
    data = {
        "@context": "https://schema.org", "@type": "MobileApplication",
        "name": p["name"], "alternateName": p["short"], "description": p["description"],
        "operatingSystem": "visionOS 27", "applicationCategory": "GameApplication",
        "inLanguage": ["en"], "url": url, "downloadUrl": STORE,
        "image": f"{BASE}img/og.jpg",
        "screenshot": [f"{BASE}img/{s}.webp" for s in SHOTS],
        "author": {"@type": "Person", "name": "Vinicius Ramos"},
    }   # no offers until the price is set, no aggregateRating until there are real ratings
    sections = ""
    for i, (title, text, shot, alt) in enumerate(p["sections"]):
        w, h = SHOTS[shot]
        cls = "feature" + (" flip" if i % 2 else "")
        sections += (f"<section class='{cls}'><div><h2>{e(title)}</h2><p>{e(text)}</p></div>"
                     f"<figure><img src='{root}img/{shot}.webp' alt='{e(alt)}' width='{w}' height='{h}' loading='lazy'>"
                     f"</figure></section>\n")
    cards = "".join(f"<div><h3>{e(t)}</h3><p>{e(x)}</p></div>" for t, x in p["cards"])
    requirements = "".join(f"<li>{e(t)}</li>" for t in p["requirements"])
    return f"""<!doctype html>
<html lang="{p['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['description'])}">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og.jpg">
<meta property="og:locale" content="{p['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}img/icon.png">
<link rel="apple-touch-icon" href="{root}img/icon.png">
<link rel="stylesheet" href="{root}style.css">
<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>
</head>
<body class="landing">
<header class="hero wrap">
<img class="app-icon" src="{root}img/icon.png" alt="" width="96" height="96">
<h1>{e(p['short'])}</h1>
<p class="tagline">{e(p['tagline'])}</p>
{badge(p)}
<p class="facts">{e(p['facts'])}</p>
</header>
<img class="key-art" src="{root}img/hero.webp" alt="{e(p['hero_alt'])}" width="1920" height="824">
<main class="wrap">
{sections}<section class="cards">{cards}</section>
<section class="requirements"><h2>{e(p['requirements_title'])}</h2><ul>{requirements}</ul></section>
<section class="cta"><h2>{e(p['cta_title'])}</h2><p>{e(p['cta'])}</p>{badge(p)}</section>
</main>
<footer class="wrap site">
<p><a href="{root}support.html">{e(p['support'])}</a> · <a href="{root}privacy.html">{e(p['privacy'])}</a></p>
<p>{e(p['credits'])}</p>
<p>{e(p['legal'])}</p>
</footer>
</body>
</html>
"""


def sitemap():
    urls = "".join(f"<url><loc>{BASE + PAGES[c]['path']}</loc></url>\n" for c in PAGES)
    urls += "".join(f"<url><loc>{BASE}{f}</loc></url>\n" for f in ("support.html", "privacy.html"))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


if __name__ == "__main__":
    for code, p in PAGES.items():
        out = os.path.join(HERE, p["path"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(page(code))
        print("wrote", out)
    open(os.path.join(HERE, "sitemap.xml"), "w").write(sitemap())
    print("wrote sitemap.xml")
