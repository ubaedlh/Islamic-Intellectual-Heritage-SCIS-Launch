# Islamic Intellectual Heritage in Singapore

A mobile-first, single-page exhibition companion. Plain HTML, CSS and JavaScript; no build step, packages, database, API keys or external font services.

## Preview locally

From this repository directory:

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000` in your browser. Stop the server with Ctrl+C. You can also open `index.html` directly for a quick preview. To test on a phone on the same local network, use your computer's LAN IP with port 8000, if your firewall permits it. Cloud environments may require their own supported port access; localhost on your phone refers to the phone itself.

## Publish with GitHub Pages

1. Commit and push `index.html`, `style.css`, `script.js`, `assets/` and this README to `main`.
2. In the GitHub repository, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select **main** and **/ (root)**, then **Save**.
5. Wait for the Pages deployment to finish. Use the published URL shown in Pages settings. The expected project address is `https://ubaedlh.github.io/Islamic-Intellectual-Heritage-SCIS-Launch/`.
6. Test that published page on a smartphone before generating and printing the exhibition QR code. Encode the published HTTPS address, not a local preview address.

All asset links are relative so the site works under a GitHub Pages project path. No special routing configuration is needed.

## Replace sample exhibition content

**The chapter dates, narratives and suggested objects are explicitly labelled editorial placeholders. They are not verified research.** Replace them with reviewed historical content before presenting the website as a factual exhibition. The hero SVG is an original contemporary illustration, not an archival photograph. The decorative map, arches and document are also placeholders.

- Edit chapter text and dates in `index.html`, maintaining chronological order.
- Replace each `.object-placeholder` block with an `<img>` using a relative `assets/` path, descriptive alt text, `width`, `height` and `loading="lazy"`. Add `.object-card img { display: block; width: 100%; height: auto; }` to `style.css` when adding photographs.
- Include creator, date, collection reference, source URL and rights information in each caption. Secure reproduction permission where required.
- Replace the research guidance with actual citations and acknowledgements.
- Update the preview notice and “Sample edition” footer only after reviewing all exhibition content.

## Accessibility and behaviour

Semantic headings, a skip link, visible keyboard focus, native expandable notes and descriptive image text are included. Timeline navigation follows the reader's position. Content works without JavaScript; motion respects the device's reduced-motion setting. All illustrations and styles are local, so the page requires no third-party requests.

## Local checks

```sh
node --check script.js
```

Also preview at narrow and wide screen sizes, follow all chapter links, expand the notes, check keyboard navigation and enable reduced motion. There is no project dependency installation or automated test suite.
