# A Brief History of Islamic Education in Singapore

An image-led Malay-Nusantara heritage journal for the SCIS exhibition. Static HTML, CSS, vanilla JavaScript and an authoritative `content.json`; compatible with GitHub Pages beneath a project path. No runtime dependencies, backend, remote fonts or third-party image requests.

## Preview without publishing

Use the new review branch `website/nusantara-image-journal-review-20261030`. On GitHub, choose **Code → Download ZIP**, extract it and open `index.html`. This displays the complete exhibition locally, including images and native expandable notes. No merge or deployment is needed.

Or run from the extracted repository:

```sh
python3 tools/render.py
python3 tools/render.py --check
python3 tools/validate.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000 and stop with Ctrl+C when finished. This review must not be merged or published automatically. No Pages settings were changed.

## Archival material

Two uploaded presentation sheets were found on `main`, commit `7596929973546dc116b7f19af1c9f4ffc3965303`: `Pasted Graphic.tiff` and `image.png`. Both are retained unchanged. Six cropped WebP object views total approximately 220 KB and are stored in `assets/archive/`. Their crop coordinates, dimensions, source files and review needs are listed in `IMAGE-INVENTORY.md`.

The uploads contain a map, a mosque sketch, two portraits and two printed-text views relevant to Chapter I. No suitable later-period images or standalone official logo were found across the four branches. Later chapters use varied editorial typography without empty image frames. Existing contemporary SVGs remain in the repository but are not displayed as archival evidence. The masthead is a text identifier.

Object identifications and dates follow captions in the supplied presentation sheets and remain provisional. Collections, reproduction credits and rights have not been supplied. See `CONTENT-REVIEW.md` before approval. Web copies cannot recover detail absent from these small slide reproductions; obtain archival masters for higher-resolution examination.

## Content and rendering

Edit `content.json`, then regenerate and commit `index.html` with `python3 tools/render.py`. Do not edit the generated HTML directly. The renderer validates local image paths and the exact 12-milestone chapter coverage. All original dates, milestone titles, institutional names and descriptions are preserved. Original archive notes are also retained in `previousArchiveNotes`; the displayed printing note now acknowledges the uploads.

The inherited reading order remains 1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, grouping overlapping 1960s themes before the 1980s section. Four reflective questions remain. Introductions, glossary definitions, captions, source notes and optional historical details are rendered as HTML and remain available without JavaScript.

Objects use the existing `image`, `imageAlt`, `caption` and `source` fields. Additional views are in `archiveObjects`; `heroObject` selects the frontispiece. Every archival image links directly to its web copy without JavaScript. JavaScript adds a native modal dialog, Escape and Close dismissal, focus return, chapter tracking, reading progress and restrained reveals. Reduced-motion preferences disable motion. System Georgia provides editorial typography without external font dependencies.

## Validation and limits

Renderer consistency, local asset/anchor references, exact original milestone text, and unchanged original-image hashes were checked. Browser checks covered 360, 390 and 1440 px widths with no document overflow, loading of all six archival views, chapter navigation, mobile image enlargement, Close/Escape dismissal and focus restoration. Static validation confirms the complete no-JavaScript narrative. The reduced-motion stylesheet disables transitions and smooth scrolling; no physical-device or full screen-reader audit was performed.

Publication remains subject to curatorial identification, reproduction permissions and institutional approval. This branch is a design review, not a published exhibition.
