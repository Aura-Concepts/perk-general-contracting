# How to update the website photos

You never touch any code. Everything is controlled by the folders inside
**`site-photos/`**. Change the files, then **double-click `rebuild.command`**
(first time: right-click → Open to get past the macOS prompt) and refresh.

```
site-photos/
├── hero/          → the big banner photo at the top of the home page (1 photo)
├── owner/         → the portrait on the About page (1 photo)
├── featured.txt   → which PROJECTS show on the home "A look at our work" grid
└── projects/      → the Gallery
```

---

## Projects (the Gallery)

The gallery is organized into **projects**. Each project is a folder that holds
its own photos. A project folder lives inside a **category** and a **sub-type**:

```
projects/<Category>/<Sub-type>/<NN Project Name>/
```

Example:

```
projects/
  Commercial/
    Dealership/
      01 Audi Dealership/
          01 Showroom with vehicles.jpg     ← lowest number = the cover photo
          02 Customer lounge.jpg
          03 Service center.jpg
          before - service bay.jpg          ┐  these two make a
          after - service bay.jpg           ┘  before/after slider
          about.txt                         ← one-line description (optional)
  Residential/
    Kitchen/
      Smith Kitchen Remodel/
          01 Finished kitchen.jpg
  Agricultural/
    Pole Barn/
      Miller Barn/
          01 Red barn.jpg
```

### The rules

1. **Category** = the top folder. It's the badge on the card and the filter
   button. Use **Commercial**, **Residential**, or **Agricultural**.
   *(To add or rename a category, edit `CATEGORIES` at the top of
   `build_site.py`.)*
2. **Sub-type** = the next folder (Dealership, Kitchen, Basement, Pole Barn …).
   It shows inside the project when someone opens it. Make up whatever fits.
3. **Project folder** = one job. A number at the front (`01 `, `02 `) sets the
   order it appears in the gallery; the number is dropped from the name shown.
4. **Photo file name = caption/alt text.** Name it what you want shown. A leading
   number sets the order the photos appear inside the project.
5. **The cover** (shown on the gallery card) is the lowest-numbered photo. To
   change a project's cover, just renumber the photo you want as `01`.

### Before / after sliders

Put two photos of the same spot in a project folder named with **`before -`**
and **`after -`** and the *same* text after the dash:

```
before - kitchen.jpg
after - kitchen.jpg
```

They become a drag-to-compare slider inside the project. You can have several
pairs in one project (`before - kitchen`, `after - kitchen`, `before - bath`,
`after - bath`, …).

### Descriptions

Add a file named **`about.txt`** to a project folder with one sentence about the
job. It shows under the title when the project is opened. Optional.

---

## Home page "A look at our work"

These tiles now point at **specific projects** — clicking one opens that project
on the gallery page. Choose which projects appear (and their order) by editing
**`site-photos/featured.txt`**:

```
# One project per line, in order. Max 6. The first line is the big tile.
# Format:   Project name | Optional short caption
Audi Dealership | Audi Showroom
Modern Kitchen Remodel | Modern Kitchen
Stone Fireplace Living Room | Stone Fireplace
Commercial Outbuilding | Before & After
Custom Deck
Volkswagen Dealership | VW Dealership
```

- Use the **project's name** (the folder name, minus any leading number).
- Add `| Short caption` to control the label on the tile; otherwise the project
  title is used. Keep captions short — they read best as 1–3 words.
- The tile image is that project's **cover** photo.

---

## Hero & About photo

- **`hero/`** — drop in one image for the big home-page banner. Name it
  descriptively (that becomes its alt text).
- **`owner/`** — one portrait for the About page.

---

## To publish changes

1. Edit the folders/files in `site-photos/`.
2. **Double-click `rebuild.command`** (or run `python3 build_site.py`).
3. Refresh the site. To put it live, commit & push:
   ```
   git add -A
   git commit -m "Update project photos"
   git push
   ```

Accepts **.jpg .jpeg .png .webp**. Big photos are fine — they're automatically
resized and compressed into fast web versions.
