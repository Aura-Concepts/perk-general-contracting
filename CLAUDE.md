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
  `content/`, `*.md`, `.claude/`, tooling) out of the live site. Cloudflare Git
  integration runs `npx wrangler deploy` on push; non-prod branch builds are
  enabled (feature branches get preview URLs).
- Commit style: subject + body, plus a `Co-Authored-By:` trailer naming
  **whichever model is actually writing the commit** (don't copy a version from
  this file — it goes stale). Branch, don't push to main directly — open PRs.
- Check current branch/status with `git status` / `git branch -a` rather than
  assuming — don't hardcode branch state here, it goes stale.

## Known issues (verify current state before acting — this list can go stale)
1. **Nothing is hand-placed any more.** The barndominium and red-barn photos
   used to sit at the top level of `assets/img/` outside the build; their
   camera originals are lost, so the largest surviving web rendition was
   promoted to a source in `site-photos/editorial/` and they're now normal
   `build_editorial` slots. That caps them at 1280px / 960px — if a real
   original ever turns up, drop it in under the same filename and rebuild.
   `editorial.txt` accepts a path relative to `site-photos/` as well as the
   usual one relative to `site-photos/projects/`. (Hero alt text comes from the
   filename in `site-photos/hero/` — keep it descriptive.)
2. Google review link on `reviews.html` is **still a placeholder** — it points
   at a Google *search* for the business, not the review dialog. Needs the real
   `g.page/r/…` link from Google Business Profile → "Ask for reviews". Only the
   owner can generate it; don't invent one.
3. Hours + street address were never published on the old site — **not
   fabricated**; contact page says "by appointment." Only add if the owner
   provides them.
4. `reviews.html` is reachable from the footer and two home-page links, but is
   **not in the primary nav**. Deliberate so far — raise it with the owner
   rather than silently changing the nav.

## Business facts to preserve (verbatim)
- **Perk General Contracting**, owner **Nikolaus Perkovich**, **est. 2014**, Des Moines, IA.
- Phone **515-599-6934** (`tel:+15155996934`), email **info@perkgc.com**.
- Service area: **all of Iowa + Omaha, NE + Kansas City, MO + Minneapolis, MN +
  Denver, CO + Salt Lake City, UT**.
- Sister company: **Willow Crest Homes** (`https://willowcresthomesdsm.com/`).
- Canonical domain in metadata/sitemap: `https://www.perkgc.com`.
- Built by **Aura Concepts** (`https://auraconcepts.co`). Every page's
  `.footer-bottom` legal line ends with `· Site by` + an `a.site-credit`
  pointing at `https://auraconcepts.co/#perk-general-contracting` — that hash
  scrolls the Aura work grid to this project's card and pulses it (handled by
  Aura's `js/main.js`). Hand-maintained in all six pages; the build doesn't
  touch it. **The bottom bar has almost no slack:** `.container` caps at 1200px
  minus 40px gutters, so the two items get 1120px, and the current copy needs
  ~1002px. "All rights reserved." was dropped from the copyright to buy that
  room — adding words back here wraps the bar to two rows on every screen size,
  since the limit is the container, not the viewport.

## Gotchas when previewing in-browser
**Why screenshots keep coming back blank/white.** The Browser pane runs
**backgrounded** — `document.visibilityState === "hidden"` for the whole
session. A hidden renderer doesn't paint, doesn't run rAF, and doesn't tick CSS
transitions. Everything below follows from that, so don't chase it as a site
bug. Check it any time output looks wrong: `javascript_tool` →
`document.visibilityState`.

1. **The pane can open at a 0×0 viewport.** `resize_window` with the `desktop`
   preset resolves to "native size" = 0×0. Always pass explicit
   `{width, height}` (e.g. 1280×900, or 390×844 for phone). At width 0 every
   `sizes="100vw"` image picks the smallest srcset candidate, `naturalWidth`
   reads 0 (looks like a broken image), and every layout measurement is junk.
2. **`resize_window` is the repaint trigger.** A screenshot only shows what was
   painted at load. To capture anything else: change the viewport (even by 1px)
   *immediately before* `computer{action:"screenshot"}`. Waiting longer does
   **not** help — a hidden pane never repaints on its own.
3. **You cannot screenshot a scrolled page.** Scroll, then screenshot, returns
   white every time. To QA lower sections, use a **tall viewport**
   (e.g. 1280×2600) so the section is inside the initial paint at scroll 0.
4. **`html { scroll-behavior: smooth }` breaks programmatic scrolling here** —
   smooth scroll is rAF-driven, so `window.scrollTo(0, y)` silently stays at 0.
   Use `window.scrollTo({top: y, behavior: "instant"})`, or set
   `document.documentElement.style.scrollBehavior = "auto"` first.
5. **`computer` actions (scroll/click) time out after 30s** with "Browser pane
   is currently hidden," and can wedge the pane until the next `navigate`.
   Drive the page with `javascript_tool` (`el.click()`, synthetic
   `KeyboardEvent`s) instead — that works reliably.
6. **Don't trust `getComputedStyle` after a JS-driven state change** — the
   hidden renderer defers style invalidation, so it hands back stale values and
   you'll "find" bugs that aren't there. Two real examples from this repo, both
   of which turned out to be fine:
   - open mobile menu still reporting `visibility: hidden; transform:
     translateX(100%)` (frozen transition) → inject
     `*{transition:none !important}` before reading;
   - `.rating input:checked ~ label` stars still reading `--line` grey after
     `.click()` (skipped sibling invalidation) → force a recalc with
     `el.style.display='none'; void el.offsetHeight; el.style.display=''`.
   `element.matches(selector)` runs the selector engine fresh and stays
   trustworthy — use it to sanity-check before believing a computed value.
7. `.reveal` starts at `opacity: 0`. Force `.is-visible` on all of them via JS
   before judging a screenshot of anything below the fold.
8. The browser **caches `main.js`/`styles.css`** — bump the `?v=N` on the
   `<link>`/`<script>` in all six HTML files after editing them (they're
   currently `styles.css?v=5`, `main.js?v=5`), or you'll test stale code.
