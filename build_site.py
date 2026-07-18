#!/usr/bin/env python3
"""
Perk General Contracting — photo build.

You do NOT need to touch any code to swap photos. Just manage the folders in
`site-photos/` and run this script (or double-click `rebuild.command`).

  site-photos/
    hero/         one image -> the big homepage banner
    featured/     up to 6 images -> the "A look at our work" grid on the homepage
    owner/        one image -> the portrait on the About page
    gallery/
      dealerships/   \
      commercial/     |
      kitchens/       |-> each folder is a gallery category (a filter button)
      interiors/      |
      exteriors/     /

Rules of thumb:
  * The FILE NAME becomes the caption. Name it what you want shown, e.g.
    "Modern kitchen remodel.jpg" -> caption "Modern kitchen remodel".
  * To control ORDER, start the file name with a number: "01 ...", "02 ...".
    The number is only for sorting and is removed from the caption.
  * The FOLDER a photo sits in decides its category (and filter button).
  * Accepts .jpg .jpeg .png .webp. Big photos are fine — they get resized.

Then run:  python3 build_site.py
"""
import os, re, glob, json, shutil, hashlib
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "site-photos")
IMG  = os.path.join(ROOT, "assets", "img")

# folder name -> (filter key used by the gallery buttons, badge label on the tile)
CATEGORIES = {
    "dealerships": ("commercial", "Dealership"),
    "commercial":  ("commercial", "Commercial"),
    "kitchens":    ("kitchen",    "Kitchen"),
    "interiors":   ("interior",   "Interior"),
    "exteriors":   ("exterior",   "Exterior"),
}

EXTS = (".jpg", ".jpeg", ".png", ".webp")
GALLERY_WIDTHS  = [400, 640, 800, 1200, 1600]
FEATURED_WIDTHS = [400, 640, 960, 1280]
HERO_WIDTHS     = [960, 1280, 1600, 1920, 2400]
OWNER_WIDTHS    = [400, 600, 800, 1000]

# ---------------------------------------------------------------- helpers
def caption_from(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    name = re.sub(r'^\s*\d+[\s._\-)]+', '', name)   # strip leading order token
    name = name.replace('_', ' ').strip()
    name = re.sub(r'\s+', ' ', name)
    return name or "Project photo"

def natural_key(path):
    base = os.path.basename(path)
    m = re.match(r'\s*(\d+)', base)
    return (int(m.group(1)) if m else 10**9, base.lower())

def slug_for(path):
    cap = caption_from(path)
    s = re.sub(r'[^a-z0-9]+', '-', cap.lower()).strip('-')[:48] or "photo"
    h = hashlib.md5(path.encode()).hexdigest()[:6]
    return f"{s}-{h}"

def list_images(folder):
    out = []
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            if f.lower().endswith(EXTS) and not f.startswith('.'):
                out.append(os.path.join(folder, f))
    return sorted(out, key=natural_key)

def render(src, outdir, slug, ladder, q_webp=80, q_jpg=82):
    os.makedirs(outdir, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    sw, sh = im.size
    ar = sh / sw
    widths = [w for w in ladder if w < sw]
    native = min(sw, ladder[-1])
    if native not in widths:
        widths.append(native)
    widths = sorted(set(widths))
    for w in widths:
        h = round(w * ar)
        rim = im.resize((w, h), Image.LANCZOS)
        rim.save(os.path.join(outdir, f"{slug}-{w}.webp"), "WEBP", quality=q_webp, method=6)
        rim.save(os.path.join(outdir, f"{slug}-{w}.jpg"),  "JPEG", quality=q_jpg, optimize=True, progressive=True)
    return {"widths": widths, "ar": round(ar, 4), "w": sw, "h": sh}

def pick(widths, target):
    c = [w for w in widths if w >= target]
    return c[0] if c else widths[-1]

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def srcset(rel, slug, widths, ext):
    return ", ".join(f"{rel}/{slug}-{w}.{ext} {w}w" for w in widths)

def replace_between(html, start, end, new):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    return pat.sub(start + "\n" + new + "\n" + end, html, count=1)

# ---------------------------------------------------------------- build gallery
def build_gallery():
    outdir = os.path.join(IMG, "gallery")
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    items = []
    for folder, (filt, badge) in CATEGORIES.items():
        for src in list_images(os.path.join(SRC, "gallery", folder)):
            items.append((src, filt, badge))
    items.sort(key=lambda t: natural_key(t[0]))     # global order via number prefix

    html = []
    for src, filt, badge in items:
        slug = slug_for(src)
        meta = render(src, outdir, slug, GALLERY_WIDTHS)
        ws = meta["widths"]; ar = meta["ar"]
        cap = caption_from(src)
        thumb = pick(ws, 640); small = pick(ws, 400); full = ws[-1]
        wset = [small] + ([thumb] if thumb != small else [])
        sizes = "(max-width:560px) 100vw, (max-width:900px) 50vw, 33vw"
        html.append(
f'''        <a class="g-item" data-cat="{filt}" href="assets/img/gallery/{slug}-{full}.jpg" data-full="assets/img/gallery/{slug}-{full}.jpg" data-alt="{esc(cap)}">
          <span class="g-badge">{esc(badge)}</span>
          <picture>
            <source type="image/webp" sizes="{sizes}" srcset="{srcset('assets/img/gallery', slug, wset, 'webp')}">
            <img src="assets/img/gallery/{slug}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset('assets/img/gallery', slug, wset, 'jpg')}" alt="{esc(cap)}" width="{thumb}" height="{round(thumb*ar)}" loading="lazy" decoding="async">
          </picture>
          <span class="g-cap">{esc(cap)}</span>
        </a>''')
    return "\n".join(html), len(items)

# ---------------------------------------------------------------- build featured (home mosaic)
def build_featured():
    outdir = os.path.join(IMG, "featured")
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    srcs = list_images(os.path.join(SRC, "featured"))[:6]
    # layout classes recreate the designed mosaic when there are 6 tiles
    layout = {0: "wide tall", 5: "wide"}
    html = []
    for i, src in enumerate(srcs):
        slug = slug_for(src)
        meta = render(src, outdir, slug, FEATURED_WIDTHS)
        ws = meta["widths"]; ar = meta["ar"]
        cap = caption_from(src)
        thumb = pick(ws, 640); small = pick(ws, 400)
        wset = [small] + ([thumb] if thumb != small else [])
        cls = layout.get(i, "")
        class_attr = f' class="{cls}"' if cls else ""
        sizes = "(max-width:900px) 100vw, 50vw" if cls else "(max-width:900px) 50vw, 25vw"
        html.append(
f'''          <a href="gallery.html"{class_attr}>
            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset('assets/img/featured', slug, wset, 'webp')}">
              <img src="assets/img/featured/{slug}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset('assets/img/featured', slug, wset, 'jpg')}" alt="{esc(cap)}" width="{thumb}" height="{round(thumb*ar)}" loading="lazy" decoding="async">
            </picture>
            <span class="cap">{esc(cap)}</span>
          </a>''')
    return "\n".join(html), len(srcs)

# ---------------------------------------------------------------- build hero
def build_hero():
    outdir = os.path.join(IMG, "hero")
    srcs = list_images(os.path.join(SRC, "hero"))
    if not srcs:
        return None
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    src = srcs[0]
    slug = slug_for(src)
    meta = render(src, outdir, slug, HERO_WIDTHS)
    ws = meta["widths"]; cap = caption_from(src)
    base = pick(ws, 1600)
    # refresh the social-share image from the hero
    og = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert("RGB"), (1200, 630), Image.LANCZOS)
    og.save(os.path.join(IMG, "og-cover.jpg"), "JPEG", quality=84, optimize=True)
    html = (
f'''        <picture>
          <source type="image/webp" sizes="100vw" srcset="{srcset('assets/img/hero', slug, ws, 'webp')}">
          <img src="assets/img/hero/{slug}-{base}.jpg" sizes="100vw" srcset="{srcset('assets/img/hero', slug, ws, 'jpg')}" alt="{esc(cap)}" width="{meta['w']}" height="{meta['h']}" fetchpriority="high" decoding="async">
        </picture>''')
    return html

# ---------------------------------------------------------------- build owner portrait
def build_owner():
    outdir = os.path.join(IMG, "owner")
    srcs = list_images(os.path.join(SRC, "owner"))
    if not srcs:
        return None
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    src = srcs[0]
    slug = slug_for(src)
    meta = render(src, outdir, slug, OWNER_WIDTHS)
    ws = meta["widths"]
    cap = caption_from(src) or "Portrait of Nikolaus Perkovich, owner of Perk General Contracting"
    thumb = pick(ws, 600)
    sizes = "(max-width:800px) 80vw, 34vw"
    html = (
f'''            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset('assets/img/owner', slug, ws, 'webp')}">
              <img src="assets/img/owner/{slug}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset('assets/img/owner', slug, ws, 'jpg')}" alt="{esc(cap)}" width="{meta['w']}" height="{meta['h']}" loading="lazy" decoding="async">
            </picture>''')
    return html

# ---------------------------------------------------------------- inject
def inject(page, blocks):
    path = os.path.join(ROOT, page)
    html = open(path).read()
    for start, end, new in blocks:
        if new is not None and start in html:
            html = replace_between(html, start, end, new)
    open(path, "w").write(html)

def main():
    print("Building photos from site-photos/ …")
    gal_html, gal_n = build_gallery();   print(f"  gallery:  {gal_n} photos")
    feat_html, feat_n = build_featured(); print(f"  featured: {feat_n} photos")
    hero_html = build_hero();             print(f"  hero:     {'set' if hero_html else 'unchanged (no image)'}")
    owner_html = build_owner();           print(f"  owner:    {'set' if owner_html else 'unchanged (no image)'}")

    inject("gallery.html", [
        ("<!-- PHOTOS:GALLERY:START -->", "<!-- PHOTOS:GALLERY:END -->", gal_html),
    ])
    inject("index.html", [
        ("<!-- PHOTOS:FEATURED:START -->", "<!-- PHOTOS:FEATURED:END -->", feat_html),
        ("<!-- PHOTOS:HERO:START -->", "<!-- PHOTOS:HERO:END -->", hero_html),
    ])
    inject("about.html", [
        ("<!-- PHOTOS:OWNER:START -->", "<!-- PHOTOS:OWNER:END -->", owner_html),
    ])
    print("Done. Refresh the site to see your changes.")

if __name__ == "__main__":
    main()
