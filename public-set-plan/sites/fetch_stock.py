"""Fill image placeholders with free Pexels stock photos (via the official Pexels API, not scraping).
Usage: PEXELS_API_KEY=proxy-injected python3 fetch_stock.py [--force] [ID ...]
Saves img/stock/<ID>.jpg and img/stock/credits.json. Real-only slots (guest reviews, your concierge) are skipped on purpose."""
import json, os, ssl, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "img", "stock")
CA = "/root/.ccr/ca-bundle.crt"; CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
KEY = os.environ.get("PEXELS_API_KEY", "")

# placeholder ID -> (search query, orientation)
WANT = {
    "SH-01": ("luxury villa private pool", "landscape"), "SH-03": ("tropical villa living room", "landscape"),
    "SH-05": ("outdoor dinner table terrace evening", "landscape"), "SH-08": ("welcome gift basket", "square"),
    "SH-10": ("chef plating food", "portrait"), "SH-11": ("chauffeur opening car door", "portrait"),
    "SH-12": ("driver loading luggage car", "portrait"), "SH-13": ("security guard suit", "portrait"),
    "SH-15": ("breakfast by the pool", "landscape"),
    "CR-01": ("friends swimming pool villa", "portrait"), "CR-02": ("men relaxing pool drinks", "landscape"),
    "CR-03": ("poolside breakfast", "landscape"), "CR-04": ("deep sea fishing", "landscape"),
    "CR-05": ("vip lounge bottle service", "landscape"), "CR-06": ("fishing charter boat", "portrait"),
    "CR-07": ("golf course ocean", "portrait"), "CR-08": ("atv ride dirt", "portrait"), "CR-09": ("cigar smoke", "portrait"),
    "GW-01": ("women friends pool vacation", "portrait"), "GW-02": ("feet in swimming pool", "square"),
    "GW-03": ("breakfast table fruit coffee", "square"), "GW-04": ("catamaran caribbean", "square"),
    "GW-06": ("rooftop bar night", "square"), "GW-07": ("tropical island beach palm", "portrait"),
    "GW-08": ("horseback riding beach", "portrait"), "GW-09": ("cooking class", "portrait"),
    "GW-10": ("spa massage", "portrait"), "GW-11": ("woman reading book pool lounger", "square"),
    "CE-01": ("friends toast sunset pool", "landscape"), "CE-02": ("birthday balloons party", "square"),
    "CE-03": ("champagne toast", "square"), "CE-04": ("group of friends laughing", "square"),
    "CE-05": ("romantic dinner table", "square"), "CE-06": ("celebration toast glasses", "square"),
    "CE-07": ("birthday cake candles", "portrait"), "CE-08": ("decorated dinner table celebration", "landscape"),
}

def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "dr-experiences-site-builder", **(headers or {})})
    with urllib.request.urlopen(req, context=CTX, timeout=40) as r:
        return r.read()

def main(args):
    force = "--force" in args; ids = [a for a in args if not a.startswith("--")] or list(WANT)
    os.makedirs(OUT, exist_ok=True)
    cpath = os.path.join(OUT, "credits.json"); credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
    for pid in ids:
        dest = os.path.join(OUT, pid + ".jpg")
        if os.path.exists(dest) and not force: continue
        q, orient = WANT[pid]
        qs = urllib.parse.urlencode({"query": q, "orientation": orient, "per_page": 5, "size": "medium"})
        data = json.loads(get("https://api.pexels.com/v1/search?" + qs, {"Authorization": KEY}))
        used = {c["id"] for c in credits.values()}
        photo = next((p for p in data.get("photos", []) if p["id"] not in used), None)
        if not photo: print(pid, "no result for", q); continue
        open(dest, "wb").write(get(photo["src"]["large"]))
        credits[pid] = {"id": photo["id"], "photographer": photo["photographer"], "photographer_url": photo["photographer_url"],
                        "pexels_url": photo["url"], "alt": photo.get("alt", ""), "query": q}
        print(pid, "->", photo["photographer"], photo["url"]); time.sleep(0.4)
    json.dump(credits, open(cpath, "w"), indent=2)

if __name__ == "__main__":
    main(sys.argv[1:])
