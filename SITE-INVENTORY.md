# Perk General Contracting — Website Inventory

**Inventory only — no redesign, no recommendations.** This is a factual capture of the existing site as reconstructed from the files in this folder.

## Source notes

- **Live domain:** `https://www.perkgc.com` (Squarespace; internal build URL `perk-gc.squarespace.com`)
- **Sister/related site:** Willow Crest Homes — `https://willowcresthomesdsm.com/`
- **Platform:** Squarespace 7.1
- **Local image copies:** All referenced images have been downloaded to [`assets/original/`](assets/original/), preserving original filenames. Content images (logos, home/about/contact photos, backgrounds) were pulled at full resolution from the Squarespace CDN. The **Gallery professional photos (`205A*`) and category tiles (`webp_*.jpg`) are ~400px thumbnail copies** — the full-resolution originals were not present in this project or served by `localhost:8901`, so the best available versions (from `.thumbs/`) were used. The gallery `.webp` originals were unavailable; the `webp_*.jpg` thumbnails are used in their place.
- **Files used for this inventory:**
  - `recovered-pages/home-wayback-2025.html` — Home, Wayback capture 2025-02-23
  - `recovered-pages/about-wayback.html` — About, Wayback capture 2024-03-30
  - `recovered-pages/contact-wayback.html` — Contact, Wayback capture 2024-03-30
  - `recovered-pages/contact-sheet.html` + `.thumbs/` — local index of downloaded photo assets (gallery source photos)
  - `PERK GENERAL CONTRACTING.html` — NOT the live site; this is a screen capture of the Squarespace **editor dashboard** and contains no public page content.
- **Pages in the site navigation:** ABOUT, GALLERY, CONTACT (plus Home logo link). No HTML capture of the **Gallery** page was provided — see the Gallery section for the photo assets that were downloaded.

---

## Global elements (all pages)

### Primary navigation
`ABOUT` · `GALLERY` · `CONTACT` (with a mobile "Open Menu / Close Menu" toggle). Logo links to Home.

### Footer (identical on every captured page)
```
Located — Des Moines, IA
Project Locations — All of Iowa, Omaha, NE and Kansas City, MO
515-599-6934
info@perkgc.com
[Contact Us button]
©2024 PERK GENERAL CONTRACTING | ALL RIGHTS RESERVED | WEBSITE DESIGNED BY TANDEMHART
```
- Footer social-icons block is present in markup but **no social accounts are linked** (empty).

### Contact info (site-wide)
| Field | Value |
|---|---|
| Phone | 515-599-6934 (`tel:+15155996934`) |
| Email | info@perkgc.com (`mailto:` uses `Info@perkgc.com`) |
| Base location | Des Moines, IA |
| Service area | All of Iowa; Omaha, NE; Kansas City, MO |
| Hours | **Not listed anywhere on the site** |
| Street address | **Not listed** (city only) |

### Brand / logo assets
- [`PERK_White_Secondary.png`](assets/original/PERK_White_Secondary.png) — primary logo (alt text: "PERK GENERAL CONTRACTING"; 1368×641)
- [`PERK_CONSTRUCTION_Full_White.png`](assets/original/PERK_CONSTRUCTION_Full_White.png) — full white logo variant
- [`PERK_White_Secondary(1).png`](assets/original/PERK_White_Secondary%281%29.png) — duplicate logo variant

---

## Page 1 — Home (`/`)

### SEO metadata
| Field | Value |
|---|---|
| `<title>` | PERK GENERAL CONTRACTING |
| Meta description | *(empty)* |
| og:site_name | PERK GENERAL CONTRACTING |
| og:title | PERK GENERAL CONTRACTING |
| og:type | website |
| og:url | https://www.perkgc.com/ |
| og:image | `PERK_White_Secondary.png` (1368×641) |
| twitter:card | summary |
| twitter:title / twitter:image | PERK GENERAL CONTRACTING / logo |
| Canonical | https://www.perkgc.com/ |

### Text content

**Hero / intro:**
> We pride ourselves in our responsiveness, attention to detail, and our craftsmanship.

> Our roots are in rural Iowa constructing pole barns and quickly grew to new construction, remodeling, carpentry, and even home handyman work. We believe in a strong work ethic with an Iowa nice attitude — working on projects like friends and neighbors.

> It all begins with an idea. Maybe you want to launch a business. Maybe you want to turn a hobby into something more.
> *(Note: this last line is Squarespace placeholder/boilerplate text left in place. A "Make It" placeholder button link `#` also exists.)*

**Services section — heading: "Our Services"**

*RESIDENTIAL*
- Remodel & Room Additions
- Exteriors, Roofing & Siding
- Custom Cabinetry
- Fencing
- Decking
- Concrete
- Painting
- All handyman needs

*COMMERCIAL*
- Outbuildings
- Concrete 
- Floor Epoxy
- Custom Remodels
- Painting
- Roofing
- Gutters
- Paving
- Parking lot stripping & lighting
- Landscaping & hardscape
- HVAC & Electrical
- New construction

**Testimonials (carousel):**

| Author | Quote |
|---|---|
| Joe Knapp | "Remodeled my home and it came out great. They treat the home like they would be fixing it for themselves to live in. Very trustworthy and honest people." |
| Sam Yoder | "They do great work! Nicholas is honest and thorough. I highly recommend him for your next home project." |
| Logan Patrick | "Had them rewire and move multiple outlets and switches. Did a great job. Looking forward to seeing what I can have them do next!" |
| Deanne Bottenfield | "Nikolaus and his team installed a new front glass storm door and also did a couple of repairs to an outside door and an inside door. "If you are looking for someone to work on your home like they were working on their own home then this is the company for you." |
| Alesha Burgraff | "We had the unusual project of adding a laundry shoot to our turn-of-the-century home. They brought ideas on how to do it and made the shoot door look like it had always been a part of the house." |

**Closing / cross-promo:**
> Looking to build your custom home, visit our sister company **Willow Crest Homes** → `https://willowcresthomesdsm.com/`

### Images on Home
| File | Depicts (inferred) |
|---|---|
| [`64588102_1293955994097933_4057204232980267008_n.jpg`](assets/original/64588102_1293955994097933_4057204232980267008_n.jpg) | Project photo (Facebook-sourced), 620×620 |
| [`302745837_616059513284276_3151663136353434631_n.jpg`](assets/original/302745837_616059513284276_3151663136353434631_n.jpg) | Project photo (Facebook-sourced), 1078×1078 |
| [`104332901_…_n.jpg`](assets/original/104332901_1623608207799375_200827072205127497_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`109290202_…_n.jpg`](assets/original/109290202_1659539467539582_8921033308391469138_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`123570944_…_n.jpg`](assets/original/123570944_1755293271297534_8134187090527820597_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`251405306_…_n.jpg`](assets/original/251405306_2038001753026683_1271686426540713872_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`73372263_…_n.jpg`](assets/original/73372263_1386204648206400_584676874416816128_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`79823924_…_n.jpg`](assets/original/79823924_1456951834465014_2263379565206306816_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`84330660_…_n.jpg`](assets/original/84330660_1511933108966886_5943546520694423552_n.jpg) | Project/gallery photo (Facebook-sourced) |
| [`Screen+Shot+2022-10-18+at+10.05.06+AM.png`](assets/original/Screen+Shot+2022-10-18+at+10.05.06+AM.png) | Screenshot graphic, 1672×1115 |
| [`Screen+Shot+2022-10-18+at+10.22.19+AM.png`](assets/original/Screen+Shot+2022-10-18+at+10.22.19+AM.png) | Screenshot graphic |
| [`PERK_White_Secondary.png`](assets/original/PERK_White_Secondary.png), [`PERK_CONSTRUCTION_Full_White.png`](assets/original/PERK_CONSTRUCTION_Full_White.png) | Logos |

- **All content images have empty `alt` text** except the logo.

---

## Page 2 — About (`/about`)

### SEO metadata
| Field | Value |
|---|---|
| `<title>` | ABOUT — PERK GENERAL CONTRACTING |
| Meta description | *(empty)* |
| og:title | ABOUT — PERK GENERAL CONTRACTING |
| og:url | https://www.perkgc.com/about |
| og:type | website |
| twitter:card | summary |
| Canonical | https://www.perkgc.com/about |

### Text content
**Heading: NIKOLAUS PERKOVICH**
> Once I taught myself the trade of hard work, I excelled at cabinetry and trim. I have a passion for building quality products and developing intentional relationships with customers.

Contact block (same as footer):
> Located — Des Moines, IA · Project Locations — All of Iowa, Omaha, NE and Kansas City, MO · 515-599-6934 · info@perkgc.com

Includes a **"Contact Us"** button.

### Images on About
| File | Depicts (inferred) |
|---|---|
| [`Screenshot+2022-11-02+at+12.26.44+PM.png`](assets/original/Screenshot+2022-11-02+at+12.26.44+PM.png) | Portrait/photo of Nikolaus Perkovich (owner) |
| [`PERK_White_Secondary.png`](assets/original/PERK_White_Secondary.png), [`PERK_CONSTRUCTION_Full_White.png`](assets/original/PERK_CONSTRUCTION_Full_White.png) | Logos |

---

## Page 3 — Contact (`/contact`)

### SEO metadata
| Field | Value |
|---|---|
| `<title>` | CONTACT — PERK GENERAL CONTRACTING |
| Meta description | *(empty)* |
| og:title | CONTACT — PERK GENERAL CONTRACTING |
| og:url | https://www.perkgc.com/contact |
| og:type | website |
| twitter:card | summary |
| Canonical | https://www.perkgc.com/contact |

### Text content
**Heading: CONTACT US**
> Reach out using the contact form below or contact us directly by phone or email.
> 515-599-6934 · Info@perkgc.com

### Form — Squarespace native Form Block
- **Handling:** Squarespace form submission (posts to `perk-gc.squarespace.com` / Squarespace form endpoint; no custom action, JS-handled). Success message: **"Thank you!"**
- **Fields collected:**

| Label | Field name | Type | Required |
|---|---|---|---|
| Name → First Name | `fname` | text (given-name) | Yes |
| Name → Last Name | `lname` | text (surname) | Yes |
| Email | `email` | email | Yes |
| Subject | *(unnamed)* | text | Yes |
| Message | *(unnamed)* | textarea | Yes |
| — | — | submit button | — |

### Images on Contact
| File | Depicts (inferred) |
|---|---|
| [`PERK_White_Secondary.png`](assets/original/PERK_White_Secondary.png), [`PERK_CONSTRUCTION_Full_White.png`](assets/original/PERK_CONSTRUCTION_Full_White.png) | Logos |

---

## Page 4 — Gallery (`/gallery`) — *no page HTML captured*

The Gallery page is present in the site navigation but no HTML snapshot was provided. The following photo assets were downloaded locally (`.thumbs/`, indexed by `recovered-pages/contact-sheet.html` and `.thumbs/seen.txt`) and are the gallery's source images.

### Gallery category tiles (originally `gallery-images/*.webp`)
Original `.webp` files were unavailable; the links below point to the ~400px `webp_*.jpg` thumbnail copies (the best available versions).
- [`webp_basement.jpg`](assets/original/webp_basement.jpg) — Basement (orig. `basement.webp`)
- [`webp_bathroom.jpg`](assets/original/webp_bathroom.jpg) — Bathroom (orig. `bathroom.webp`)
- [`webp_commercial.jpg`](assets/original/webp_commercial.jpg) — Commercial (orig. `commercial.webp`)
- [`webp_exterior.jpg`](assets/original/webp_exterior.jpg) — Exterior (orig. `exterior.webp`)
- [`webp_kitchen.jpg`](assets/original/webp_kitchen.jpg) — Kitchen (orig. `kitchen.webp`)
- [`webp_living-room.jpg`](assets/original/webp_living-room.jpg) — Living Room (orig. `living-room.webp`)

### Professional project photos (originally `professional photos/`, 33 images)
HDR project photography credited to **Nikolaus Perkovich**. Links point to the ~400px thumbnail copies (full-resolution originals unavailable):

*From `iCloud Photos from Nikolaus Perkovich/` (16 images):*
[`205A0887-HDR.jpeg`](assets/original/205A0887-HDR.jpeg) · [`205A0890-HDR.jpeg`](assets/original/205A0890-HDR.jpeg) · [`205A0893-HDR.jpeg`](assets/original/205A0893-HDR.jpeg) · [`205A0902-HDR-1.jpeg`](assets/original/205A0902-HDR-1.jpeg) · [`205A0905-HDR-1.jpeg`](assets/original/205A0905-HDR-1.jpeg) · [`205A0908-HDR.jpeg`](assets/original/205A0908-HDR.jpeg) · [`205A0913-HDR.jpeg`](assets/original/205A0913-HDR.jpeg) · [`205A0914-HDR.jpeg`](assets/original/205A0914-HDR.jpeg) · [`205A0917-HDR.jpeg`](assets/original/205A0917-HDR.jpeg) · [`205A0920-HDR.jpeg`](assets/original/205A0920-HDR.jpeg) · [`205A0923-HDR.jpeg`](assets/original/205A0923-HDR.jpeg) · [`205A0926-HDR.jpeg`](assets/original/205A0926-HDR.jpeg) · [`205A0929-HDR.jpeg`](assets/original/205A0929-HDR.jpeg) · [`205A0932-HDR.jpeg`](assets/original/205A0932-HDR.jpeg) · [`205A0935-HDR.jpeg`](assets/original/205A0935-HDR.jpeg) · [`205A0938-HDR.jpeg`](assets/original/205A0938-HDR.jpeg)

*From `iCloud Photos from Nikolaus Perkovich 2/` (14 images):*
[`205A2759-HDR-Enhanced-NR.jpeg`](assets/original/205A2759-HDR-Enhanced-NR.jpeg) · [`205A2765-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2765-HDR-Enhanced-NR-1.jpeg) · [`205A2768-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2768-HDR-Enhanced-NR-1.jpeg) · [`205A2771-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2771-HDR-Enhanced-NR-1.jpeg) · [`205A2774-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2774-HDR-Enhanced-NR-1.jpeg) · [`205A2777-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2777-HDR-Enhanced-NR-1.jpeg) · [`205A2780-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2780-HDR-Enhanced-NR-1.jpeg) · [`205A2786-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2786-HDR-Enhanced-NR-1.jpeg) · [`205A2789-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2789-HDR-Enhanced-NR-1.jpeg) · [`205A2795-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2795-HDR-Enhanced-NR-1.jpeg) · [`205A2798-HDR-Enhanced-NR.jpeg`](assets/original/205A2798-HDR-Enhanced-NR.jpeg) · [`205A2801-HDR-Enhanced-NR.jpeg`](assets/original/205A2801-HDR-Enhanced-NR.jpeg) · [`205A2808-HDR-Enhanced-NR-1.jpeg`](assets/original/205A2808-HDR-Enhanced-NR-1.jpeg) · [`205A2811-HDR-Enhanced-NR.jpeg`](assets/original/205A2811-HDR-Enhanced-NR.jpeg)

*Additional (3 images):*
[`205A2814-Enhanced-NR.JPEG`](assets/original/205A2814-Enhanced-NR.JPEG) · [`205A2820-Enhanced-NR_(1).JPEG`](assets/original/205A2820-Enhanced-NR_%281%29.JPEG) · [`205A2826-Enhanced-NR_(1).JPEG`](assets/original/205A2826-Enhanced-NR_%281%29.JPEG)

*(Content of each photo not individually labeled — no alt text or captions available. Full checksummed list is in `.thumbs/seen.txt`. Note: two files use `_(1)` in the actual filename where the source path had ` (1)`.)*

---

## Third-party embeds & integrations

| Integration | Status | Notes |
|---|---|---|
| Google Analytics 4 | **Present** | Measurement ID `G-YQSS9LLCP8` |
| Google Tag Manager | Script bundled (`gtm.js` in `_files`) | No confirmed GTM container ID firing on captured pages |
| Facebook Pixel | Script bundled (`fbevents.js`, `connect.js` in `_files`) | No pixel ID / `fbq()` init confirmed on live pages |
| Stripe | Script bundled (`stripe.js` in `_files`) | Squarespace default; no checkout/commerce flow on these pages |
| Squarespace Forms | **Present** | Contact form (see Contact page) |
| Squarespace Commerce | Bundle referenced | No storefront/checkout content on captured pages |
| Google Maps / embedded map | **None** | No map iframe on any captured page |
| Live chat (Intercom/Drift/Tawk/Messenger) | **None** | Not found |
| Booking/scheduling (Acuity/Calendly/SqSp Scheduling) | **None** | Not found |
| Newsletter / mailing list signup | **None** | Not found |
| Social media links | **None linked** | Social-icons block exists but empty |

---

## Summary of gaps / notable absences (factual, not recommendations)

- Meta descriptions are **empty** on all pages.
- Content images carry **no alt text** (only the logo does).
- **No business hours** and **no street address** published (city + service-area only).
- Home page retains some **Squarespace placeholder text/buttons** ("It all begins with an idea…", "Make It" → `#`).
- No **Gallery** page HTML was available for capture; only its source image assets.
- One testimonial (Deanne Bottenfield) has an attributed name but no captured quote text.
- Website credit: **TandemHart** (designer).
