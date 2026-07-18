# How to update the website photos

You never need to touch any code. Everything is controlled by the folders inside
**`site-photos/`**. Add, remove, or rename image files there, then rebuild.

## The folders

```
site-photos/
├── hero/        → the big banner photo at the top of the home page (1 photo)
├── featured/    → the "A look at our work" grid on the home page (up to 6 photos)
├── owner/       → the portrait on the About page (1 photo)
└── gallery/     → the Gallery page, split into categories:
    ├── dealerships/   (shows the "Dealership" tag)
    ├── commercial/    (shows the "Commercial" tag)
    ├── kitchens/      (shows the "Kitchen" tag)
    ├── interiors/     (shows the "Interior" tag)
    └── exteriors/     (shows the "Exterior" tag)
```

## The 3 rules

1. **The file name becomes the caption.**
   `Modern kitchen remodel.jpg` shows the caption *"Modern kitchen remodel."*
   This is also the image's alt text (good for Google + screen readers), so name
   it descriptively.

2. **A number at the front sets the order** (and is removed from the caption).
   `01 Modern kitchen.jpg`, `02 Stone fireplace.jpg` … Lower numbers show first.
   The gallery is ordered by these numbers across every category.

3. **The folder sets the category.** Move a photo between category folders to
   recategorize it. Drop a new photo into `kitchens/` and it becomes a kitchen.

Big photos are fine (phone photos, DSLR, etc.) — they're automatically resized and
compressed into fast web versions. Accepts **.jpg .jpeg .png .webp**.

## To make changes

1. Open the `site-photos` folder in Finder.
2. Add / delete / rename photos in the right folders.
3. **Double-click `rebuild.command`** in the main project folder.
   (First time only: right-click it → Open, to get past macOS's security prompt.)
4. Refresh the website. Done.

### Examples

- **Swap a gallery photo:** delete the old file, drop the new one in the same
  category folder, name it what you want shown, rebuild.
- **Change what's on the home page grid:** put the 6 photos you want in
  `featured/`, numbered `1`–`6` for order, rebuild.
- **Change the top banner:** replace the single photo in `hero/`, rebuild.
- **Reorder the gallery:** change the number at the front of the file names,
  rebuild.

## Notes

- `featured/` looks best with exactly **6** photos (the first one becomes the
  large tile).
- If you're comfortable in Terminal, you can rebuild with:
  `python3 build_site.py`
- The category tags/filters themselves (Dealerships, Kitchens, etc.) live at the
  top of `build_site.py` if you ever want to rename or add one.
