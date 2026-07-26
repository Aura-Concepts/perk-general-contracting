# Perk General Contracting — CLAUDE.md

> Persistent project context for Claude Code. `*.md` is excluded from the
> deployed site by `.assetsignore`, so this file is safe to keep at repo root.

## What this is
A hand-built **static marketing website** for **Perk General Contracting** (a
Des Moines, IA general contractor — homes, remodels, commercial build-outs,
auto dealerships, agricultural/pole barns). Only the old Squarespace site's
*content + photos* were reused; the build is fresh. Pages: `index`, `services`,
`gallery`, `about`, `contact`, `reviews`.

## Stack / environment
- **Plain HTML/CSS/JS, no framework, no bundler.** Shared `css/styles.css` +
  `js/main.js`. Fonts: **Archivo** (headings) + **Inter** (body) via Google Fonts.
- **This machine has no Node/npm.** Image + page generation is a **Python 3.9 +
  Pillow** script (`build_site.py`). Don't reach for `npm`.
- **Local preview:** `python3 -m http.server 8123` then open `http://localhost:8123`.
- macOS. `gh` CLI is installed and authenticated (GitHub user **Tennessene**).

## Design system (CSS variables in `:root` at top of `css/styles.css`)
- **Palette = red / white / blue.** Navy base `--ink:#14273f`, heartland
  red-orange `--accent:#d24a26` (+ `--accent-2/-ink/-soft`), `--blue:#1f4e79`,
  white/cool-gray surfaces. Recolor the whole site from those vars — also
  update two hard-coded accent glows: `.page-hero::after`, `.cta-band::before`.
- Headings weight 800 (Archivo). Ampersands in headings are wrapped by JS into
  `.amp` spans rendered in Inter 800 (Archivo's `&` looks like an "e").
- SEO is built in: per-page meta title/description, one H1/page, descriptive
  alt text, JSON-LD (GeneralContractor + Breadcrumb/etc.), `sitemap.xml`,
  `robots.txt`. Scroll reveal animations + hover effects, `prefers-reduced-motion`
  respected. Images: responsive `<picture>` WebP+JPEG, lazy-loaded.

## The build system — `build_site.py` (run via `rebuild.command` or `python3 build_site.py`)
Everything photo/content-related is generated from **`site-photos/`** (+ `content/`)
and injected into the HTML between `<!-- PHOTOS:*:START/END -->` markers.
- **`build_projects`** → the Gallery. Reads
  `site-photos/projects/<Category>/<Sub-type>/<NN Project>/`. Categories
  (Commercial / Residential / Agricultural) = card badge + filter; sub-type
  (Dealership, Kitchen, Pole Barn…) shows inside the project. `before -` /
  `after -` filename prefixes → before/after slider. `about.txt` = description.
  Emits gallery cards + a JSON data island (`#projects-data`).
- **`build_featured`** → home "A look at our work" tiles. Reads
  `site-photos/featured.txt` (`Project name | Short caption`, max 6). Tiles reuse
  each project's cover and link to `gallery.html?project=<id>`.
- **`build_hero`** (home banner) — one image from `site-photos/hero/`.
- **`build_editorial`** → the fixed photos on index/services that aren't gallery
  cards. `site-photos/editorial.txt` maps `slot | project photo | alt text`;
  output goes to `assets/img/editorial/` and is injected at
  `<!-- PHOTOS:EDITORIAL:<slot>:START/END -->`. Slots today: `dealership-cafe`
  (home "Built to brand standards"), `kitchen-modern` + `commercial-shop`
  (services). Swap a photo by re-pointing the middle column and rebuilding.
- **`build_staff`** (About page) — `site-photos/staff.txt` (blocks of
  `Name | Title` + description) + one headshot per person in `site-photos/staff/`
  (matched by name in the file name). First person = owner spotlight portrait
  (story text hand-written in `about.html`); rest = "Meet the team" cards.
  Markers: `STAFF:PORTRAIT` + `STAFF:GRID`.
- **`build_logo`** → copies `site-photos/logo/perk-logo-white.png` (+ redblue) to
  `assets/logo/`. **`build_icons`** → regenerates all favicons/app icons from
  the white logo. So a logo swap updates header/footer/tab icon in one rebuild.
  **Don't edit `assets/logo/` or `assets/img/` directly — regenerated each build.**
- **`build_reviews`** → reads `content/reviews.txt` (blocks:
  `Name | Role/town | Stars | Source(optional)` + text), injects the first 5 on
  the homepage and all on `reviews.html`.

Full owner-facing guide: `UPDATING-PHOTOS.md` (covers projects, featured, hero,
staff/team, logo, reviews). Keep it in sync if you change the build.

## Gallery UX (`js/main.js`)
Project cards → click opens a **pop-up modal** (title, sub-type, description,
drag-to-compare before/after slider(s), photo grid). Photo grid → full-screen
**lightbox** (z-index 230, above the 210 modal). Filters: All / Commercial /
Residential / Agricultural, with `?cat=` and `?project=` deep-links.

## Forms (Formspree — live)
- **Quote/contact form** (`contact.html`): `formspree.io/f/xbdnkplv`.
- **"Leave a review" form** (`reviews.html`): `formspree.io/f/mvzebvwn`.
  Submissions email in; good ones get pasted into `content/reviews.txt` and the
  site rebuilt (nothing auto-posts). Reviews page also has a "Review us on
  Google" button — **its link is a placeholder**, needs the real `g.page/r/…` URL.
Don't change/regenerate these endpoints without reason.

## Git & deployment
- Repo: **`Aura-Concepts/perk-general-contracting`** (private). Default branch
  **`main`** is the up-to-date integration branch.
- **Deploys via Cloudflare Workers static assets.** `wrangler.toml` points
  `[assets] directory = "."`; `.assetsignore` keeps source (`site-photos/`,
  `*.md`, tooling) out of the live site. Cloudflare Git
  integration runs `npx wrangler deploy` on push; non-prod branch builds are
  enabled (feature branches get preview URLs).
- Commit style: subject + body, `Co-Authored-By: Claude Opus 4.8`. Branch,
  don't push to main directly — open PRs.
- Check current branch/status with `git status` / `git branch -a` rather than
  assuming — don't hardcode branch state here, it goes stale.

## Known issues (verify current state before acting — this list can go stale)
1. Two hand-placed images remain at the TOP LEVEL of `assets/img/`:
   `new-construction-*` (barndominium, on index) and `pole-barn-*` (red barn,
   on about). No high-res originals survive for either, so the build does NOT
   regenerate them — if `assets/` gets wiped, restore them with `git restore`.
   Everything else that used to live there is now built by `build_editorial`
   from `site-photos/editorial.txt`. (Hero alt text was fixed by renaming the
   file in `site-photos/hero/` — keep hero filenames descriptive.)
2. Google review link on `reviews.html` may still be a placeholder — swap in
   the real `g.page/r/…` URL if so.
3. `.assetsignore` may not yet exclude `content/` — `content/reviews.txt` is
   built into the HTML, so the raw file needn't ship.
4. Hours + street address were never published on the old site — **not
   fabricated**; contact page says "by appointment." Only add if the owner
   provides them.

## Business facts to preserve (verbatim)
- **Perk General Contracting**, owner **Nikolaus Perkovich**, **est. 2014**, Des Moines, IA.
- Phone **515-599-6934** (`tel:+15155996934`), email **info@perkgc.com**.
- Service area: **all of Iowa + Omaha, NE + Kansas City, MO**.
- Sister company: **Willow Crest Homes** (`https://willowcresthomesdsm.com/`).
- Canonical domain in metadata/sitemap: `https://www.perkgc.com`.

## Gotchas when previewing in-browser
- Screenshots anchor to scroll-0 on pages with the fixed hero. To QA lower
  sections: resize to a **tall viewport**, or `translateY(-Npx)` the `<main>`/
  footer, and force `.reveal` elements visible via JS.
- The browser **caches `main.js`/`styles.css`** — hard-reload
  (`location.reload(true)`) or append `?v=N` after editing them, or you'll test
  stale code.
