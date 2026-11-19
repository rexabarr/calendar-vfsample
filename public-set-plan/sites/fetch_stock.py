"""Fill image placeholders with free, commercially usable Creative Commons photos from Openverse (official API, no key).
Only CC0, public-domain and CC BY licences are used; credits go in img/stock/credits.json and the page footer.
Usage: python3 fetch_stock.py [--force] [ID ...]
Saves img/stock/<ID>.jpg and img/stock/credits.json. Real-only slots (guest reviews, your concierge) are skipped on purpose."""
import json, os, ssl, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "img", "stock")
CA = "/root/.ccr/ca-bundle.crt"; CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()

# placeholder ID -> (search query, orientation)
WANT = {
    "SH-01": ("villa pool", "landscape"), "SH-03": ("living room interior", "landscape"),
    "SH-05": ("terrace dinner table", "landscape"), "SH-08": ("gift basket", "square"),
    "SH-10": ("chef plating", "portrait"), "SH-11": ("chauffeur car", "portrait"),
    "SH-12": ("airport luggage car", "portrait"), "SH-13": ("security guard", "portrait"),
    "SH-15": ("breakfast pool", "landscape"),
    "CR-01": ("infinity pool", "portrait"), "CR-02": ("pool party friends", "landscape"),
    "CR-03": ("breakfast eggs coffee", "landscape"), "CR-04": ("deep sea fishing", "landscape"),
    "CR-05": ("nightclub lounge", "landscape"), "CR-06": ("fishing boat", "portrait"),
    "CR-07": ("golf course", "portrait"), "CR-08": ("quad bike", "portrait"), "CR-09": ("cigars", "portrait"),
    "GW-01": ("women friends beach", "portrait"), "GW-02": ("swimming pool water", "square"),
    "GW-03": ("fruit breakfast", "square"), "GW-04": ("catamaran sailing", "square"),
    "GW-06": ("rooftop bar", "square"), "GW-07": ("caribbean beach", "portrait"),
    "GW-08": ("horses beach", "portrait"), "GW-09": ("cooking class", "portrait"),
    "GW-10": ("massage spa", "portrait"), "GW-11": ("reading by the pool", "square"),
    "CE-01": ("pool sunset", "landscape"), "CE-02": ("gold balloons", "square"),
    "CE-03": ("champagne toast", "square"), "CE-04": ("friends laughing", "square"),
    "CE-05": ("dinner table candles", "square"), "CE-06": ("champagne glasses", "square"),
    "CE-07": ("birthday cake", "portrait"), "CE-08": ("table setting", "landscape"),
}

IMG_HOSTS = ("live.staticflickr.com", "upload.wikimedia.org")
ASPECT = {"landscape": "wide", "portrait": "tall", "square": "square"}

def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "dr-experiences-site-builder/1.0", **(headers or {})})
    with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
        return r.read()

def save_resized(raw, dest, max_w=1400):
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=82, optimize=True)

def main(args):
    force = "--force" in args; ids = [a for a in args if not a.startswith("--")] or list(WANT)
    os.makedirs(OUT, exist_ok=True)
    cpath = os.path.join(OUT, "credits.json"); credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
    for pid in ids:
        dest = os.path.join(OUT, pid + ".jpg")
        if os.path.exists(dest) and not force: continue
        q, orient = WANT[pid]
        qs = urllib.parse.urlencode({"q": q, "license": "cc0,pdm,by", "mature": "false", "page_size": 20})
        try:
            data = json.loads(get("https://api.openverse.org/v1/images/?" + qs))
        except Exception as e:
            print(pid, "search failed:", e); continue
        used = {c["id"] for c in credits.values() if c.get("id")} | set(credits.get("_rejected_ids", {}).get("ids", []))
        ok = False
        def shape_ok(p):
            w, h = p.get("width") or 0, p.get("height") or 1
            return {"landscape": w / h >= 1.2, "portrait": w / h <= 0.9, "square": 0.8 <= w / h <= 1.25}[orient]
        results = sorted(data.get("results", []), key=lambda p: not shape_ok(p))  # right shape first, keep relevance order
        for p in results:
            host = urllib.parse.urlparse(p.get("url", "")).netloc
            if p["id"] in used or host not in IMG_HOSTS or max(p.get("width") or 0, p.get("height") or 0) < 900: continue
            try:
                save_resized(get(p["url"]), dest)
            except Exception as e:
                print(pid, "download failed, trying next:", e); continue
            credits[pid] = {"id": p["id"], "title": p.get("title") or "Untitled", "creator": p.get("creator") or "Unknown",
                            "creator_url": p.get("creator_url"), "license": p["license"].upper(), "license_version": p.get("license_version"),
                            "license_url": p.get("license_url"), "source_url": p.get("foreign_landing_url"), "provider": p.get("provider"), "query": q}
            print(pid, "->", credits[pid]["creator"], credits[pid]["license"], credits[pid]["source_url"]); ok = True; break
        if not ok: print(pid, "no usable result for", repr(q))
        json.dump(credits, open(cpath, "w"), indent=2); time.sleep(1.2)

if __name__ == "__main__":
    main(sys.argv[1:])
