# SCIS launch palette — design review

Prepared 3 November 2026. Review branch: `website/scis-launch-palette-review-20261103`.
Base: `main` at `af3ae144967a6db0a88d7cbaef88bf4cac1fbfe1`.

## Changes

- `style.css`: supplied nine-colour launch palette as CSS properties; warm ivory pages; royal-blue institutional opening and closing; blue/purple Connections, orange/coral Transformation and teal/turquoise Renewal. Dark orange and teal variants are used for readable text on pale backgrounds.
- Self-hosted variable Montserrat for institutional text, chapter headings, dates and navigation; Georgia retained for historical prose and article headings. The font is bundled in `assets/fonts/Montserrat-variable.ttf` with its SIL Open Font License in `assets/fonts/OFL.txt`. Source: https://github.com/google/fonts/tree/main/ofl/montserrat . No remote font requests.
- CSS-only geometric opening ornament, unrotated archival frames, clearer captions, comfortable body typography, 44px or larger disclosure/close controls, chapter-specific navigation indicators and visible keyboard focus.
- `tools/render.py`: browser theme colour changed to royal blue; opening call to action now reads “Explore the timeline” and links to the first chapter. No manual generated-HTML edits.
- `index.html`: regenerated through the existing renderer.

## Preservation

`content.json`, `script.js`, all existing assets, historical wording, captions, alt text, provenance notes and milestone order are byte-for-byte unchanged from the base. Generated page text differs only in the opening timeline link wording. All twelve milestones retain their existing reading order: 1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12.

No framework, backend or external runtime dependency added. Existing source images remain untouched. The legacy decorative sprig remains in the repository and generated markup but is hidden by CSS in this design.

## Validation

Passed:

- `python3 tools/render.py`
- `python3 tools/render.py --check`
- `python3 tools/validate.py`
- Content, JavaScript and existing asset equality against the base.
- Rendered-text comparison, allowing only the changed timeline link label.
- Browser layout inspection at 360, 390, 768 and 1440 CSS-pixel widths; document scroll width equals viewport width at each size.
- Mobile navigation to Transformation and Renewal, with correct active chapter indicator.
- Mobile image modal, Escape dismissal and focus return; desktop image modal, Close button and focus return.
- Expandable archive note opens; no broken loaded images or browser warning/error logs observed.
- Principal text/background contrast pairs: blue/ivory 13.28:1; dark orange/peach 6.41:1; dark teal/mint 6.64:1; caption grey on the three pale page backgrounds at least 5.90:1. These exceed 4.5:1 for normal text.

Reduced-motion CSS disables smooth scrolling, transitions and reveal transforms; this was inspected in source, not tested by changing the operating system setting. Static narrative validation covers the generated no-JavaScript content. No physical-device or full screen-reader audit was performed.

## Preview

Download the branch as a ZIP, extract it, and open `index.html`; all content and assets are local. For browser testing through a server:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit http://127.0.0.1:8000 . This work does not change hosting settings, merge into main or publish.

## Remaining review

The actual launch graphic was not attached. Colours and CSS geometry follow the supplied written brief; they are not a verified reproduction of the official artwork or an official SCIS logo. Existing provisional archival identifications and credit qualifications remain intact. Original slide-derived images retain their existing resolution limits.
