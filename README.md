# A Brief History of Islamic Education in Singapore

A single-page digital heritage journal for SCIS. Semantic HTML, CSS and vanilla JavaScript. No packages, backend, external fonts or build service required by GitHub Pages.

## Preview the redesign

The redesign lives on `website/illustrated-historical-journal`; merging and deployment are separate review steps. The live main-branch website is unchanged until the pull request is merged.

**Without Terminal:** open the redesign branch on GitHub, choose **Code → Download ZIP**, extract it, and open `index.html` in a browser. All text, styles, images and native expandable archive notes work directly from the folder. JavaScript adds motion, reading progress and the image viewer. GitHub's file view shows source code, not the rendered website. Do not merge just to preview it.

For an HTTP preview, run this from the repository directory:

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000` on that computer. Stop with Ctrl+C. A phone on the same local network can use the computer's LAN IP and port 8000 if permitted by the firewall. A cloud environment needs its supported port access; localhost on a phone refers to the phone.

## Maintain the content

`content.json` is the authoritative editable source. It retains every field of the existing 12 milestone objects, introduction and closing. It also holds the three chapter groupings, questions, glossary notes, context interpretations and closing reflection.

After editing content, regenerate the complete static HTML with the dependency-free standard-library tool:

```sh
python3 tools/render.py
python3 tools/render.py --check
```

Commit both `content.json` and `index.html`. Python is needed only when generating edited content, not to serve or deploy the website. Do not edit generated index.html directly: use content.json or the layout template in tools/render.py. This avoids a JavaScript-disabled visitor seeing outdated text. The browser no longer fetches JSON or replaces historical content at runtime.

Milestone placement is set by each chapter's `milestones` list. Each of the 12 original IDs must occur once. The reading order is 1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, grouping the three 1960s-onwards themes before 1980s onwards. Overlapping time periods are preserved and documented in CONTENT-REVIEW.md.

## Approved images and institutional assets

No historical photographs, documents, official logo or image rights were supplied. Every requested image is labelled as pending, not represented by imaginary evidence. The opening cartographic illustration is clearly marked contemporary and nonhistorical. The earlier illustration is retained unused in assets.

To add an approved object image:

1. Save a web-optimised image in assets (preferably under 300 KB where archival legibility permits).
2. Set its milestone's `image` to the relative local path, e.g. `assets/approved-photo.jpg`.
3. Set `imageAlt` to a descriptive alternative text, `caption` to the approved caption and `source` to the actual creator/date/collection/rights reference.
4. Run the renderer and check the result. It rejects missing files and nonlocal paths. Images retain aspect ratio and load lazily. Their caption and source appear in the enlarged-image viewer; Escape, the Close button and clicking outside dismiss it. Focus returns to the original image. Without JavaScript, an image link opens the original asset directly.

Replace the header's explicitly labelled text identifier with the official logo only once supplied. Opening-image and header layout changes belong in tools/render.py. No official links, archival credits or new factual claims should be guessed. See CONTENT-REVIEW.md for editorial approvals still needed.

## Review and publish

Open the branch's pull request and review before merging. Do not change the existing Pages settings unnecessarily. The existing main-branch Pages deployment can publish the revision after merge. If Pages is not enabled, use **Settings → Pages → Deploy from a branch → main → / (root) → Save**.

Expected live URL: `https://ubaedlh.github.io/Islamic-Intellectual-Heritage-SCIS-Launch/`. The site uses relative assets and works beneath this project path. Test the published result on a phone before printing the QR code. Preserve content.json, tools/render.py, index.html, style.css, script.js and assets in the repository.

## Validation

```sh
python3 tools/render.py --check
node --check script.js
git diff --check
```

Browser validation for this redesign covered 360, 390, 430, 768 and 1440 px viewports, exact milestone content and order, no horizontal overflow, working chapter anchors and current-chapter state, four reflective questions, archive notes, reading progress, image asset loading, reduced motion including changes during a visit, keyboard skip navigation and the complete no-JavaScript narrative. A test-only local image fixture exercised enlargement, caption/credit preservation, focus containment, Escape and focus restoration. GitHub Pages project-path behaviour was simulated locally.

No full screen-reader audit, physical-phone performance measurement or real archival-image legibility review was performed. Approved archival images are still needed; the present page is lightweight and makes no third-party requests. No new dependencies were installed.
