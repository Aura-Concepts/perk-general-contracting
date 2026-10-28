# Perk General Contracting

Website for [Perk General Contracting](https://www.perkgc.com), a local general contractor. Designed, built, and maintained by [Aura Concepts](https://auraconcepts.co).

## Stack

- Plain HTML, CSS, and JavaScript. No framework, so pages load fast and are easy to hand off.
- `build_site.py` processes the project photos into sharpened, multi-size renditions for the gallery lightbox and generates the favicons from the logo.
- Hosted on Cloudflare as static assets (`wrangler.toml`). Cloudflare is connected to this repo, so every push to `main` redeploys the live site automatically.
- Files that aren't part of the public site (source photos, build tooling, docs) are excluded from the upload by `.assetsignore`.

## Pages

Home, Services, Gallery, Reviews, About, and Contact, plus `sitemap.xml` and `robots.txt` for SEO.

## Updating photos

See [UPDATING-PHOTOS.md](UPDATING-PHOTOS.md).
