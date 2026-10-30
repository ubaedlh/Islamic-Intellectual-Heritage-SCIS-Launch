# A Brief History of Islamic Education in Singapore

A single-page, mobile-first exhibition companion for SCIS. Plain HTML, CSS and JavaScript, with no package installation or build step.

## Preview

Run from this repository directory if Python is available:

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Visit `http://localhost:8000` on your computer. Stop with Ctrl+C. The complete static text also works when opening index.html directly; JSON-based updates require an HTTP preview. A phone on the same local network can use your computer's LAN address and port if your firewall permits it. Cloud preview access depends on your environment's port support.

## Edit exhibition content

`content.json` contains the title, subtitle, introduction, all 12 milestones and closing text. It loads automatically, without a backend. Each milestone has its original brief ID. The HTML places milestone 10 before 9 to group the overlapping 1960s dates chronologically. Keep the static text in index.html in sync when editing so visitors without JavaScript see the same exhibition. If adding or reordering milestones, update the matching article structure in index.html too.

For each approved image, place the file in assets and set its milestone fields:

- `image`: relative path, such as `assets/approved-photo.jpg` (currently null).
- `imageAlt`: accurate descriptive alternative text.
- `caption`: approved caption.
- `source`: collection reference, creator, date and rights credit as appropriate.

Images retain their proportions, load lazily and open in an accessible enlarged-image dialog. Escape closes the dialog and focus returns to the image button. Placeholders are not offered as historical images. Keep mobile image files reasonably small; do not upscale low-resolution originals.

The logo and opening banner remain clearly labelled placeholders. Replace them with approved assets when supplied. Do not treat the SCIS wordmark placeholder as the official institutional logo. See CONTENT-REVIEW.md for outstanding editorial checks. No external fonts, trackers, invented citations or third-party requests are included.

## GitHub Pages

1. Commit and push the updated files to your repository, preferably through a branch and pull request.
2. Merge the reviewed pull request into main.
3. In **Settings → Pages**, choose **Deploy from a branch**, **main**, **/ (root)**, then **Save**.
4. Wait for deployment and open the published URL shown by GitHub. Expected address: `https://ubaedlh.github.io/Islamic-Intellectual-Heritage-SCIS-Launch/`.
5. Check on a smartphone before printing a QR code. Use the published HTTPS URL in the QR code.

Keep index.html, style.css, script.js, content.json and assets together. All paths support a GitHub Pages project subdirectory.

## Validation

`node --check script.js` checks syntax without installing dependencies. Test period links, expandable source notes, keyboard focus, reduced motion and narrow layouts. When approved photos are added, verify enlarged-image captions and credits. Static HTML supplies the complete exhibition when JavaScript is disabled or JSON cannot load.
