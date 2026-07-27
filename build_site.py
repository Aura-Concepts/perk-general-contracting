#!/usr/bin/env python3
"""
Perk General Contracting — photo build.

You do NOT need to touch any code to manage photos. Edit the folders in
`site-photos/` and run this script (or double-click `rebuild.command`).

  site-photos/
    logo/          the logo(s) -> copied to assets/logo/ + favicons generated
    hero/          one image -> the big homepage banner
    staff/         one headshot per team member (About page)
    staff.txt      -> who is on the team: "Name | Title" + description blocks;
                      first person = owner spotlight, the rest = team cards
    featured.txt   -> which PROJECTS show on the home "A look at our work" grid
    projects/      -> the Gallery, organised as PROJECTS:

      projects/<Category>/<Sub-type>/<NN Project Name>/
          01 first photo.jpg          <- lowest number = the cover
          02 another photo.jpg
          before - kitchen.jpg        <- "before -" / "after -" make a
          after - kitchen.jpg            before/after slider (paired by the
          about.txt                      text after the prefix)
                                      <- about.txt = one-line description (optional)

  * Category (Commercial / Residential / Agricultural) is the badge + filter.
  * Sub-type (Dealership / Kitchen / Pole Barn …) shows inside the project.
  * FILE NAME = caption/alt. A leading number sets order and is dropped.

Then run:  python3 build_site.py
"""
import os, re, json, shutil, hashlib
from PIL import Image, ImageOps, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "site-photos")
IMG  = os.path.join(ROOT, "assets", "img")

# Category folder -> (filter key, badge label). Order here = order on the page.
CATEGORIES = {
    "Commercial":   ("commercial",   "Commercial"),
    "Residential":  ("residential",  "Residential"),
    "Agricultural": ("agricultural", "Agricultural"),
}

EXTS = (".jpg", ".jpeg", ".png", ".webp")
# Rungs chosen against measured slot widths, not round numbers. 500 and 750
# fill gaps where the browser was jumping to an oversized file: the card at 1x
# desktop wants 430 (was pulling 640) and the modal tile at 2x on a phone wants
# 664 (was pulling 900). Both rungs REDUCE transfer.
PHOTO_WIDTHS    = [400, 500, 640, 750, 900, 1400]
# Before/after is the one slot that outgrows 1400: the stage is 917 CSS px, so
# a 2x screen needs 1834. Only these images get the 1800 rung — generating it
# for all ~105 project photos would be dead weight.
BA_WIDTHS       = [400, 640, 750, 900, 1400, 1800]
FEATURED_WIDTHS = [400, 640, 960, 1280]
EDITORIAL_WIDTHS = [640, 960, 1280, 1600]
HERO_WIDTHS     = [960, 1280, 1600, 1920, 2400]
STAFF_WIDTHS    = [400, 600, 800, 1000]

# ---------------------------------------------------------------- helpers
def caption_from(name):
    name = os.path.splitext(os.path.basename(name))[0]
    name = re.sub(r'^\s*\d+[\s._\-)]+', '', name)   # strip leading order token
    name = name.replace('_', ' ').strip()
    return re.sub(r'\s+', ' ', name) or "Project photo"

def natural_key(path):
    base = os.path.basename(path)
    m = re.match(r'\s*(\d+)', base)
    return (int(m.group(1)) if m else 10**9, base.lower())

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:52] or "item"

def uid(text):
    return hashlib.md5(text.encode()).hexdigest()[:6]

def list_images(folder):
    out = []
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            if f.lower().endswith(EXTS) and not f.startswith('.'):
                out.append(os.path.join(folder, f))
    return sorted(out, key=natural_key)

def list_dirs(folder):
    out = [os.path.join(folder, d) for d in os.listdir(folder)
           if os.path.isdir(os.path.join(folder, d)) and not d.startswith('.')]
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
        rim = im.resize((w, round(w * ar)), Image.LANCZOS)
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
    # function replacement so backslashes in `new` (e.g. \u in JSON) aren't
    # treated as regex escapes
    return pat.sub(lambda m: start + "\n" + new + "\n" + end, html, count=1)

# ------------------------------------------------------------- projects (gallery)
def is_before(p): return bool(re.match(r'^\s*(\d+[\s._\-)]+)?before\b', os.path.basename(p), re.I))
def is_after(p):  return bool(re.match(r'^\s*(\d+[\s._\-)]+)?after\b',  os.path.basename(p), re.I))
def ba_key(p):
    n = os.path.splitext(os.path.basename(p))[0].lower()
    n = re.sub(r'^\s*\d+[\s._\-)]+', '', n)
    n = re.sub(r'^(before|after)\b[\s\-_]*', '', n).strip()
    return n

def build_projects():
    outbase = os.path.join(IMG, "projects")
    if os.path.isdir(outbase): shutil.rmtree(outbase)
    root = os.path.join(SRC, "projects")
    cards, data = [], []
    if not os.path.isdir(root):
        return "", "[]", 0

    for cat in CATEGORIES:                       # defined order
        catdir = os.path.join(root, cat)
        if not os.path.isdir(catdir): continue
        filt, label = CATEGORIES[cat]
        for subdir in list_dirs(catdir):         # sub-types
            subtype = os.path.basename(subdir)
            for projdir in list_dirs(subdir):    # projects
                title = caption_from(os.path.basename(projdir))
                pid = slugify(f"{cat}-{subtype}-{title}") + "-" + uid(projdir)
                rel = f"assets/img/projects/{pid}"
                absd = os.path.join(outbase, pid)

                imgs = list_images(projdir)
                photos = [i for i in imgs if not is_before(i) and not is_after(i)]
                befores = [i for i in imgs if is_before(i)]
                afters  = [i for i in imgs if is_after(i)]

                about = os.path.join(projdir, "about.txt")
                desc = open(about).read().strip() if os.path.exists(about) else ""

                def add(src, ladder=PHOTO_WIDTHS):
                    s = slugify(caption_from(src)) + "-" + uid(src)
                    m = render(src, absd, s, ladder)
                    return {"s": s, "w": m["widths"], "ar": m["ar"], "alt": caption_from(src)}

                photo_data = [add(p) for p in photos]

                # before/after pairs — these fill a 917px stage, so they get the
                # taller BA_WIDTHS ladder rather than the grid-sized one
                ba = []
                akeys = {ba_key(a): a for a in afters}
                for b in befores:
                    a = akeys.get(ba_key(b))
                    if not a: continue
                    bd = add(b, BA_WIDTHS); bd["alt"] = f"Before — {title}"
                    ad = add(a, BA_WIDTHS); ad["alt"] = f"After — {title}"
                    ba.append({"before": bd, "after": ad})

                cover = photo_data[0] if photo_data else (
                    add(afters[0]) if afters else (add(befores[0]) if befores else None))
                if not cover:
                    continue

                data.append({"id": pid, "title": title, "cat": filt, "catLabel": label,
                             "subtype": subtype, "desc": desc, "dir": rel,
                             "photos": photo_data, "ba": ba})

                # ---- card (cover rendered server-side) ----
                cw = cover["w"]; car = cover["ar"]
                # The card is ~425 CSS px on desktop, so a 2x screen needs ~850.
                # The srcset used to stop at 640 — the 900 rendition was being
                # generated and used by the modal, but never offered here, which
                # is what made the cards look soft on retina displays.
                thumb = pick(cw, 640)
                # 500 = 1x desktop (430), 750 = 2x mobile (706), 900 = 2x
                # desktop (850). Offering all of them lets the browser land
                # close instead of rounding up a whole rung.
                wset = sorted({pick(cw, t) for t in (400, 500, 640, 750, 900)})
                # Measured against the real grid, not guessed: the card is 91vw
                # at 390, 45vw at 768, 449px at ~1000 (2 cols) and 425px at 1440
                # (3 cols). The old flat "380px" under-declared the desktop case.
                sizes = ("(max-width:560px) 92vw, (max-width:900px) 50vw, "
                         "(max-width:1240px) 47vw, 430px")
                ba_tag = '<span class="proj-card__flag">Before &amp; After</span>' if ba else ''
                sub = subtype + (f' · {len(photo_data)} photos' if len(photo_data) > 1 else '')
                cards.append(
f'''        <button class="proj-card" type="button" data-id="{pid}" data-cat="{filt}" aria-label="View project: {esc(title)}">
          <span class="proj-card__media">
            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset(rel, cover['s'], wset, 'webp')}">
              <img src="{rel}/{cover['s']}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset(rel, cover['s'], wset, 'jpg')}" alt="{esc(title)}" width="{thumb}" height="{round(thumb*car)}" loading="lazy" decoding="async">
            </picture>
          </span>
          <span class="proj-card__badge">{esc(label)}</span>
          {ba_tag}
          <span class="proj-card__body">
            <span class="proj-card__title">{esc(title)}</span>
            <span class="proj-card__sub">{esc(sub)}</span>
            <span class="proj-card__view">View project <span aria-hidden="true">&rarr;</span></span>
          </span>
        </button>''')

    return "\n".join(cards), json.dumps(data, separators=(',', ':')), data

# ---------------------------------------------------------------- featured (home)
def build_featured(projects):
    """Home 'A look at our work' tiles reference PROJECTS (so clicking a tile
    opens that project on the gallery page). Which projects, in what order, and
    the short caption come from site-photos/featured.txt:

        Audi Dealership | Audi Showroom      <- Project name | optional caption
        Modern Kitchen Remodel

    Falls back to the first up-to-6 projects if the file is missing. The tile
    reuses the project's already-rendered cover image."""
    stale = os.path.join(IMG, "featured")           # old per-image folder, no longer used
    if os.path.isdir(stale): shutil.rmtree(stale)

    by_title = {}
    for p in projects:
        by_title[p["title"].lower()] = p

    sel = []
    ftxt = os.path.join(SRC, "featured.txt")
    if os.path.exists(ftxt):
        for line in open(ftxt):
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = line.split("|")
            key = re.sub(r'^\s*\d+[\s._\-)]+', '', parts[0].strip()).lower()
            p = by_title.get(key)
            if p: sel.append((p, parts[1].strip() if len(parts) > 1 else p["title"]))
    else:
        for p in projects[:6]: sel.append((p, p["title"]))
    sel = sel[:6]

    layout = {0: "wide tall", 5: "wide"}
    html = []
    for i, (p, cap) in enumerate(sel):
        cov = p["photos"][0] if p["photos"] else None
        if not cov: continue
        d = p["dir"]; ws = cov["w"]; ar = cov["ar"]
        cls = layout.get(i, ""); class_attr = f' class="{cls}"' if cls else ""
        # spanning tiles render ~2 columns wide — include the larger renditions
        # so they stay sharp on high-DPI screens
        targets = (400, 640, 900, 1400) if cls else (400, 640, 900)
        wset = sorted({pick(ws, t) for t in targets})
        thumb = pick(ws, 900 if cls else 640)
        # measured at 1440: spanning tile is 652px, plain tile 318px
        sizes = ("(max-width:900px) 100vw, (max-width:1240px) 50vw, 660px" if cls
                 else "(max-width:900px) 50vw, (max-width:1240px) 25vw, 320px")
        html.append(
f'''          <a href="gallery.html?project={p['id']}"{class_attr}>
            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset(d, cov['s'], wset, 'webp')}">
              <img src="{d}/{cov['s']}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset(d, cov['s'], wset, 'jpg')}" alt="{esc(cov['alt'])}" width="{thumb}" height="{round(thumb*ar)}" loading="lazy" decoding="async">
            </picture>
            <span class="cap">{esc(cap)}</span>
          </a>''')
    return "\n".join(html), len(sel)

# ---------------------------------------------------------------- editorial (fixed page photos)
def build_editorial():
    """The fixed photos on index/services that aren't gallery cards.

    site-photos/editorial.txt maps a slot -> a project photo + alt text, so these
    are regenerated from the same originals as everything else instead of being
    hand-placed files. Returns {slot: <picture> html}."""
    outdir = os.path.join(IMG, "editorial")
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    txt = os.path.join(SRC, "editorial.txt")
    blocks = {}
    if not os.path.exists(txt): return blocks
    # the split column is 498px at a 1440 viewport = ~35vw; the old 45vw
    # over-declared and pulled a 960px file into a 498px box
    sizes = "(max-width:800px) 90vw, 36vw"
    d = "assets/img/editorial"
    for line in open(txt):
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3: continue
        slot, rel, alt = parts[0], parts[1], parts[2]
        src = os.path.join(SRC, "projects", rel)
        if not os.path.isfile(src):
            print(f"  ! editorial: no such photo for '{slot}': {rel}")
            continue
        m = render(src, outdir, slot, EDITORIAL_WIDTHS)
        ws = m["widths"]; base = pick(ws, 960)
        blocks[slot] = (
f'''            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset(d, slot, ws, 'webp')}">
              <img src="{d}/{slot}-{base}.jpg" sizes="{sizes}" srcset="{srcset(d, slot, ws, 'jpg')}" alt="{esc(alt)}" width="{base}" height="{round(base * m['ar'])}" loading="lazy" decoding="async">
            </picture>''')
    return blocks

# ---------------------------------------------------------------- hero
def build_hero():
    srcs = list_images(os.path.join(SRC, "hero"))
    if not srcs: return None
    outdir = os.path.join(IMG, "hero")
    if os.path.isdir(outdir): shutil.rmtree(outdir)
    src = srcs[0]; slug = slugify(caption_from(src)) + "-" + uid(src)
    m = render(src, outdir, slug, HERO_WIDTHS); ws = m["widths"]; cap = caption_from(src)
    base = pick(ws, 1600)
    og = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert("RGB"), (1200, 630), Image.LANCZOS)
    og.save(os.path.join(IMG, "og-cover.jpg"), "JPEG", quality=84, optimize=True)
    return (
f'''        <picture>
          <source type="image/webp" sizes="100vw" srcset="{srcset('assets/img/hero', slug, ws, 'webp')}">
          <img src="assets/img/hero/{slug}-{base}.jpg" sizes="100vw" srcset="{srcset('assets/img/hero', slug, ws, 'jpg')}" alt="{esc(cap)}" width="{m['w']}" height="{m['h']}" fetchpriority="high" decoding="async">
        </picture>''')

# ---------------------------------------------------------------- staff (About page)
def parse_staff():
    """site-photos/staff.txt -> [{"name", "title", "desc"}] in file order.
    Blocks separated by blank lines: "Name | Title" then description lines."""
    path = os.path.join(SRC, "staff.txt")
    if not os.path.exists(path):
        return []
    blocks, cur = [], []
    for raw in open(path):
        line = raw.rstrip("\n")
        if line.strip().startswith("#"):
            continue
        if not line.strip():
            if cur: blocks.append(cur); cur = []
            continue
        cur.append(line)
    if cur: blocks.append(cur)
    people = []
    for b in blocks:
        parts = [p.strip() for p in b[0].split("|")]
        people.append({"name": parts[0],
                       "title": parts[1] if len(parts) > 1 else "",
                       "desc": " ".join(l.strip() for l in b[1:]).strip()})
    return people

def build_staff():
    """The About-page team. staff.txt says who (and in what order); staff/ holds
    one headshot per person, matched by the person's name in the file name.
    The first person becomes the owner spotlight portrait (their story text is
    hand-written in about.html); everyone else becomes a "Meet the team" card."""
    people = parse_staff()
    srcs = list_images(os.path.join(SRC, "staff"))
    if not people or not srcs:
        return None, None, 0
    outdir = os.path.join(IMG, "staff")
    if os.path.isdir(outdir): shutil.rmtree(outdir)

    def photo_for(name):
        key = slugify(name)
        for s in srcs:
            if key in slugify(caption_from(s)):
                return s
        return None

    spotlight, cards, n = None, [], 0
    for i, p in enumerate(people):
        src = photo_for(p["name"])
        if not src:
            print(f"  ! staff: no photo in staff/ matches \"{p['name']}\" — skipped")
            continue
        slug = slugify(p["name"]) + "-" + uid(src)
        m = render(src, outdir, slug, STAFF_WIDTHS); ws = m["widths"]
        cap = f"Portrait of {p['name']}, {p['title']} at Perk General Contracting" if p["title"] \
              else f"Portrait of {p['name']}"
        n += 1
        if i == 0:
            thumb = pick(ws, 600); sizes = "(max-width:800px) 80vw, 34vw"
            spotlight = (
f'''            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset('assets/img/staff', slug, ws, 'webp')}">
              <img src="assets/img/staff/{slug}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset('assets/img/staff', slug, ws, 'jpg')}" alt="{esc(cap)}" width="{m['w']}" height="{m['h']}" loading="lazy" decoding="async">
            </picture>''')
        else:
            thumb = pick(ws, 600); sizes = "(max-width:640px) 92vw, (max-width:980px) 46vw, 370px"
            delay = f' data-reveal-delay="{min(len(cards), 3)}"' if cards else ''
            bio = f'\n            <p class="team-card__bio">{esc(p["desc"])}</p>' if p["desc"] else ''
            cards.append(
f'''        <article class="team-card reveal"{delay}>
          <div class="team-card__media">
            <picture>
              <source type="image/webp" sizes="{sizes}" srcset="{srcset('assets/img/staff', slug, ws, 'webp')}">
              <img src="assets/img/staff/{slug}-{thumb}.jpg" sizes="{sizes}" srcset="{srcset('assets/img/staff', slug, ws, 'jpg')}" alt="{esc(cap)}" width="{m['w']}" height="{m['h']}" loading="lazy" decoding="async">
            </picture>
          </div>
          <div class="team-card__body">
            <h3>{esc(p['name'])}</h3>
            <p class="team-card__role">{esc(p['title'])}</p>{bio}
          </div>
        </article>''')

    return spotlight, "\n".join(cards) if cards else None, n

# ---------------------------------------------------------------- favicons
LOGO      = os.path.join(SRC, "logo", "perk-logo-white.png")   # source of truth
ICON_BG   = (20, 39, 63, 255)     # navy, matches --ink / theme-color
ICON_ROUND = 0.22                 # corner radius as a fraction of the icon size
# (filename, size, padding fraction, full_bleed)
#   full_bleed=False -> rounded square with transparent corners (browser tabs)
#   full_bleed=True  -> solid square, no transparency. iOS and Android apply
#                       their own mask, and iOS renders transparency as black.
ICONS = [("favicon-16.png",        16,  .12, False),
         ("favicon-32.png",        32,  .12, False),
         ("icon-192.png",          192, .12, False),
         ("icon-512.png",          512, .12, False),
         ("apple-touch-icon.png",  180, .12, True),
         ("icon-512-maskable.png", 512, .20, True)]   # .20 keeps art in Android's safe zone

def build_logo():
    """Sync the logo files from their source (site-photos/logo/) to assets/logo/,
    which the pages load. Keeps the model consistent: you edit site-photos/, the
    build writes assets/. Copies bytes as-is (deterministic, no git churn)."""
    src = os.path.join(SRC, "logo")
    if not os.path.isdir(src):
        return 0
    dst = os.path.join(ROOT, "assets", "logo")
    if os.path.isdir(dst): shutil.rmtree(dst)
    os.makedirs(dst)
    n = 0
    for f in sorted(os.listdir(src)):
        if f.lower().endswith((".png", ".svg", ".webp")) and not f.startswith("."):
            shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
            n += 1
    return n

def build_icons():
    """Regenerate the browser-tab / app icons from the source logo
    so swapping the logo also updates the favicons. Output is deterministic, so
    re-running with an unchanged logo rewrites identical bytes (no git churn)."""
    if not os.path.exists(LOGO):
        return 0
    badge = Image.open(LOGO).convert("RGBA")
    box = badge.getbbox()                 # trim transparent padding so the mark fills the icon
    if box: badge = badge.crop(box)

    def make(size, pad_ratio, full_bleed=False):
        if full_bleed:
            canvas = Image.new("RGBA", (size, size), ICON_BG)
        else:
            mask = Image.new("L", (size, size), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [0, 0, size - 1, size - 1], radius=int(size * ICON_ROUND), fill=255)
            canvas = Image.composite(Image.new("RGBA", (size, size), ICON_BG),
                                     Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
        pad = int(size * pad_ratio)
        b = badge.copy()
        b.thumbnail((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
        canvas.alpha_composite(b, ((size - b.width) // 2, (size - b.height) // 2))
        return canvas

    for name, size, pad, bleed in ICONS:
        make(size, pad, bleed).save(os.path.join(IMG, name))
    make(48, .12).save(os.path.join(IMG, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    return len(ICONS) + 1

# ---------------------------------------------------------------- reviews
def build_reviews():
    """Parse content/reviews.txt into testimonial cards.
    Returns (home_html, all_html): first 5 for the homepage, all for reviews.html."""
    path = os.path.join(ROOT, "content", "reviews.txt")
    if not os.path.exists(path):
        return "", ""
    blocks, cur = [], []
    for raw in open(path):
        line = raw.rstrip("\n")
        if line.strip().startswith("#"):
            continue
        if not line.strip():
            if cur: blocks.append(cur); cur = []
            continue
        cur.append(line)
    if cur: blocks.append(cur)

    cards = []
    for b in blocks:
        parts = [p.strip() for p in b[0].split("|")]
        name = parts[0] if parts else "Anonymous"
        role = parts[1] if len(parts) > 1 and parts[1] else ""
        try: stars = max(1, min(5, int(parts[2]))) if len(parts) > 2 and parts[2] else 5
        except ValueError: stars = 5
        source = parts[3] if len(parts) > 3 and parts[3] else ""
        text = " ".join(l.strip() for l in b[1:]).strip()
        words = [w for w in re.split(r'\s+', name) if w]
        initials = (words[0][0] + (words[-1][0] if len(words) > 1 else "")).upper()
        star_row = "★" * stars + "☆" * (5 - stars)
        badge = f'<span class="tst-source">via {esc(source)}</span>' if source else ""
        role_html = f'<span class="role">{esc(role)}</span>' if role else ""
        cards.append(
f'''          <figure class="tst reveal">
            <div class="stars" aria-label="{stars} out of 5 stars">{star_row}</div>
            <blockquote>&ldquo;{esc(text)}&rdquo;</blockquote>
            <figcaption><span class="avatar" aria-hidden="true">{esc(initials)}</span><span><span class="who">{esc(name)}</span>{role_html}</span>{badge}</figcaption>
          </figure>''')

    return "\n".join(cards[:5]), "\n".join(cards)

# ---------------------------------------------------------------- inject + main
def inject(page, blocks):
    path = os.path.join(ROOT, page)
    html = open(path).read()
    for start, end, new in blocks:
        if new is not None and start in html:
            html = replace_between(html, start, end, new)
    open(path, "w").write(html)

def main():
    print("Building photos from site-photos/ …")
    cards, projects_json, projects_data = build_projects(); print(f"  gallery:  {len(projects_data)} projects")
    feat_html, feat_n = build_featured(projects_data);      print(f"  featured: {feat_n} projects")
    hero_html = build_hero();                   print(f"  hero:     {'set' if hero_html else 'unchanged (no image)'}")
    editorial = build_editorial();              print(f"  editorial: {len(editorial)} fixed page photos")
    staff_spot, staff_grid, n_staff = build_staff(); print(f"  staff:    {n_staff} people (spotlight + {staff_grid.count('team-card reveal') if staff_grid else 0} cards)")
    rev_home, rev_all = build_reviews();        print(f"  reviews:  {rev_all.count('<figure')} reviews")
    n_logo = build_logo();                      print(f"  logo:     {n_logo} logo files synced to assets/logo")
    n_icons = build_icons();                    print(f"  icons:    {n_icons} favicons from the logo")

    data_script = '  <script type="application/json" id="projects-data">' + projects_json + '</script>'
    ed_blocks = [(f"<!-- PHOTOS:EDITORIAL:{s}:START -->", f"<!-- PHOTOS:EDITORIAL:{s}:END -->", h)
                 for s, h in editorial.items()]
    inject("gallery.html", [
        ("<!-- PHOTOS:GALLERY:START -->", "<!-- PHOTOS:GALLERY:END -->", cards),
        ("<!-- PHOTOS:DATA:START -->", "<!-- PHOTOS:DATA:END -->", data_script),
    ])
    inject("index.html", [
        ("<!-- PHOTOS:FEATURED:START -->", "<!-- PHOTOS:FEATURED:END -->", feat_html),
        ("<!-- PHOTOS:HERO:START -->", "<!-- PHOTOS:HERO:END -->", hero_html),
        ("<!-- REVIEWS:HOME:START -->", "<!-- REVIEWS:HOME:END -->", rev_home),
        ("<!-- PHOTOS:DATA:START -->", "<!-- PHOTOS:DATA:END -->", data_script),
    ] + ed_blocks)
    inject("services.html", ed_blocks)
    inject("about.html", [
        ("<!-- STAFF:PORTRAIT:START -->", "<!-- STAFF:PORTRAIT:END -->", staff_spot),
        ("<!-- STAFF:GRID:START -->", "<!-- STAFF:GRID:END -->", staff_grid),
    ])
    inject("reviews.html", [
        ("<!-- REVIEWS:ALL:START -->", "<!-- REVIEWS:ALL:END -->", rev_all),
    ])
    print("Done. Refresh the site to see your changes.")

if __name__ == "__main__":
    main()
