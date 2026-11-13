"""Render the no-JavaScript exhibition from content.json. Standard library only."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    d = json.loads((ROOT / 'content.json').read_text())
    e = lambda value: html.escape(str(value), quote=True)
    paras = lambda values: ''.join(f'<p>{e(v)}</p>' for v in values)
    def image(m):
        if m.get('image'):
            # Keep assets local and relative to support the GitHub Pages project URL.
            path = Path(m['image'])
            if path.is_absolute() or '..' in path.parts or ':' in m['image']:
                raise ValueError('Images must use local relative asset paths')
            if not (ROOT / path).is_file():
                raise ValueError(f'Missing image: {path}')
            return f'''<div class="image-mat"><img src="{e(m['image'])}" alt="{e(m['imageAlt'])}" loading="{'eager' if m.get('id') in (d.get('heroObject'), 'homepage-sultan') else 'lazy'}"></div>'''
        return ''
    def object_figure(obj):
        title = f'<p class="caption-title"><strong>{e(obj["captionTitle"])}</strong></p>' if obj.get('captionTitle') else ''
        caption_sections = ''.join(
            f'<p class="caption-title"><strong>{e(section["title"])}</strong></p><p>{e(section["text"])}</p>'
            for section in obj.get('captionSections', [])
        )
        caption = e(obj["caption"])
        if caption_sections:
            caption = f'<p>{caption}</p>{caption_sections}'
        introduction = ''
        if obj.get('imageBeforeCaptionSections') and caption_sections:
            introduction = f'<div class="archive-introduction">{title}<p>{e(obj["caption"])}</p></div>'
            title, caption = '', caption_sections
        source_credit = ''
        if obj.get('sourceUrl'):
            source_credit = f'<p><a href="{e(obj["sourceUrl"])}">{e(obj["source"])}</a></p>'
        archive_details = ''
        if obj.get('archiveImages'):
            scans = ''.join(f'<figure>{image(scan)}<figcaption>{e(scan["caption"])}</figcaption></figure>' for scan in obj['archiveImages'])
            archive_details = f'<details><summary>From the Archive</summary>{scans}<p><a href="https://majalahqalam.kyoto.jp/eng/">Qalam Digital Archive, Kyoto University</a></p></details>'
        elif obj.get('archiveObject'):
            archive_details = f'<div class="archive-inline">{object_figure(obj["archiveObject"])}</div>'
        elif not obj.get('hideArchiveDetails'):
            archive_details = f'<details><summary>From the Archive</summary><p>{e(obj["source"])}</p></details>'
        if obj.get('hideCaption'):
            return f'<figure class="archive-object">{image(obj)}</figure>'
        if obj.get('id') == 'alsagoff' and title:
            caption = f'<p class="portrait-caption">{caption}</p>'
        return f'{introduction}<figure class="archive-object">{image(obj)}<figcaption>{title}{caption}{source_credit}{archive_details}</figcaption></figure>'
    def chapter_archive(chapter_id, *, opening=False):
        archive = d.get('chapterArchives', {}).get(chapter_id)
        if not archive:
            return ''
        groups = []
        for group in archive['groups']:
            if (group.get('placement') == 'opening') != opening:
                continue
            figures = []
            for obj in group['objects']:
                archive_details = ''
                if not obj.get('hideArchiveDetails'):
                    archive_details = f'<details><summary>Source and identification</summary><p>{e(obj["source"])}</p></details>'
                figures.append(f'<figure class="archive-object chapter-object" id="archive-{e(obj["id"])}">{image(obj)}<figcaption><h4>{e(obj["title"])}</h4><p>{e(obj["caption"])}</p>{archive_details}</figcaption></figure>')
            groups.append(f'<section class="archive-theme"><h3>{e(group["title"])}</h3><div class="chapter-object-grid">{"".join(figures)}</div></section>')
        if opening:
            return ''.join(groups)
        if not groups:
            return ''
        return f'<aside class="chapter-archive" aria-labelledby="archive-heading-{e(chapter_id)}"><header><p class="eyebrow">{e(archive["title"])}</p><h2 id="archive-heading-{e(chapter_id)}">{e(archive["intro"])}</h2></header>{"".join(groups)}</aside>'
    def milestone(m):
        n = m['id']
        terms = d.get('terms', {}).get(str(n), [])
        definitions = ''.join(f'<p class="term-note"><strong>{e(t["term"])}:</strong> {e(t["definition"])}</p>' for t in terms)
        archive = d.get('archiveNotes', {}).get(str(n))
        source = m.get('source') or 'No archival source or reproduction credit has been supplied.'
        archive_html = f'<p>{e(archive)}</p>' if archive else ''
        caption = m['caption'] if m.get('image') else ''
        context = d.get('contexts', {}).get(str(n))
        context_html = f'''<aside class="context"><p class="eyebrow">Singapore in context</p><h4>{e(context['title'])}</h4><p>{e(context['text'])}</p><details><summary>About this connection</summary><p>{e(context['basis'])}</p></details></aside>''' if context else ''
        def highlight(entry):
            label = e(entry['label'])
            if entry.get('text'):
                label = f'<h5>{label}</h5><p>{e(entry["text"])}</p>'
            else:
                label = f'<p>{label}</p>'
            return f'<div><span>{e(entry["date"])}</span>{label}</div>'
        highlights = ''.join(highlight(entry) for entry in m.get('highlights', []))
        highlight_html = f'<aside class="milestone-highlights" aria-label="Milestone highlights">{highlights}</aside>' if highlights else ''
        extras = ''.join(object_figure(o) for o in d.get('archiveObjects', []) if o['milestone'] == n and o['image'] != m.get('image'))
        visual = f'<div class="object-group">{object_figure(m)}{extras}</div>' if m.get('image') else ''
        feature_answer = ''
        leading = ''
        heading_html = f'<h3 class="milestone-heading" id="title-{n}">{e(m["category"])}</h3>'
        if m.get('displayObjects'):
            figures = []
            leading_figures = []
            for obj in m['displayObjects']:
                if obj.get('id') and obj['id'] == m.get('featureImage'):
                    feature_answer = f'<details class="did-you-know"><summary>Did You Know?</summary><h4>{e(m["title"])}</h4><p>{e(m["description"])}</p>{object_figure(obj)}</details>'
                    continue
                feature_label = '' if obj.get('hideFeatureLabel') else '<p class="eyebrow">Did You Know?</p>'
                feature = f'<aside class="did-you-know">{feature_label}<h4>{e(obj["featureTitle"])}</h4><p>{e(obj["featureText"])}</p></aside>' if obj.get('featureTitle') else ''
                heading = f'<h4 class="milestone-object-heading">{e(obj["groupTitle"])}</h4>' if obj.get('groupTitle') else ''
                placement = leading_figures if obj.get('beforeMilestoneCopy') else figures
                if not obj.get('image'):
                    placement.append(f'<div class="milestone-object">{heading}<p class="caption-title"><strong>{e(obj["captionTitle"])}</strong></p><p class="milestone-object-description">{e(obj["caption"])}</p></div>')
                    continue
                portrait = object_figure(obj["introPortrait"]) if obj.get("introPortrait") else ""
                alignment = " milestone-object-centered" if obj.get("centered") else ""
                placement.append(f'<div class="milestone-object{alignment}">{heading}{feature}{portrait}{object_figure(obj)}</div>')
            visual = '<div class="object-group curated-objects">' + ''.join(figures) + '</div>'
            if leading_figures:
                leading = '<div class="milestone-leading">' + heading_html + ''.join(leading_figures) + '</div>'
                heading_html = ''
        repeated_description = f'<p>{e(m["description"])}</p>' if m.get('repeatDescriptionInArchive', True) else ''
        archive_detail = f'<details class="text-archive"><summary>Explore Further</summary>{archive_html}{repeated_description}</details>' if archive else ''
        subtitle = f'<p class="milestone-subtitle">{e(m["title"])}</p>' if m.get("title") else ""
        copy = feature_answer or f'{subtitle}<p class="description">{e(m["description"])}</p>'
        period = f'<p class="chapter-period">{e(m["period"])}</p>' if m.get('period') else ''
        additional = ''.join(f'<p class="description">{e(paragraph)}</p>' for paragraph in m.get('additionalDescription', []))
        theme_panels = []
        for theme in m.get('themes', []):
            developments = ''.join(
                f'<li><strong>{e(item["label"])}</strong> {e(item["text"])}</li>'
                for item in theme['items']
            )
            source = ''
            if theme.get('sourceUrl'):
                source = f'<p><a href="{e(theme["sourceUrl"])}">{e(theme["source"])}</a></p>'
            review = f'<p class="term-note">{e(theme["review"])}</p>' if theme.get('review') else ''
            placeholder = f'<p class="theme-photo-pending">{e(theme["placeholder"])}</p>' if theme.get('placeholder') else ''
            theme_panels.append(f"""
              <section class="madrasah-theme">
                <h4>{e(theme['title'])}</h4>
                <p>{e(theme['text'])}</p>
                <details>
                  <summary>Selected developments</summary>
                  <ul>{developments}</ul>
                  {source}{review}{placeholder}
                </details>
              </section>""")
        themes = '<div class="madrasah-themes">' + ''.join(theme_panels) + '</div>' if theme_panels else ''
        institution_feature = ''
        if m.get('institutionFeature'):
            institution_feature = f"""
            <details class="institution-feature">
              <summary>From the Archive</summary>
              <h4 id="mendaki-congress">Kongres Pendidikan Anak-Anak Islam, 28–30 May 1982</h4>
              {paras(m['institutionFeature'])}
              <figure class="archive-object">
                <div class="image-mat"><img src="assets/archive/mendaki-congress-1982.jpg" alt="Participants seated on stage at the 1982 MENDAKI congress, with a speaker at the lectern." width="830" height="468" loading="lazy"></div>
                <figcaption>MENDAKI’s inaugural education congress, May 1982. Photograph: Facebook / Abdul Halim Kader, via <a href="https://berita.mediacorp.sg/komentar/alam-melayu-budi-mansor-dalam-gema-gong-mendaki-1005451">BERITA Mediacorp</a>.</figcaption>
              </figure>
              <p><a href="https://www.nas.gov.sg/archivesonline/data/pdfdoc/lky19820528b.pdf">Lee Kuan Yew’s opening address, National Archives of Singapore</a></p>
            </details>"""
        profiles = []
        for profile in m.get('educatorProfiles', []):
            if profile.get('image'):
                profiles.append(object_figure(profile))
            else:
                profiles.append(f'<div><p class="caption-title"><strong>{e(profile["captionTitle"])}</strong></p><p class="milestone-object-description">{e(profile["caption"])}</p></div>')
        educators = f'<div class="institution-feature object-group" id="educator-profiles"><h4 class="milestone-object-heading">Shaping Islamic Education: Scholars, Educators and Curriculum Pioneers</h4>{"".join(profiles)}</div>' if profiles else ''
        subsections = ''.join(
            f'<section class="madrasah-theme"><h4>{e(part["title"])}</h4><p>{e(part["text"])}</p></section>'
            for part in m.get('subsections', [])
        )
        return f'''<article class="milestone layout-{n % 3} {'has-image' if visual else 'typographic'}" id="milestone-{n}" aria-labelledby="title-{n}">
<div class="folio" aria-hidden="true">{n:02}<span> / 12</span></div>
{leading}<div class="milestone-copy">{heading_html}{period}{copy}{additional}{subsections}{definitions}{archive_detail}</div>
{visual}{highlight_html}{themes}{institution_feature}{educators}{context_html}</article>'''
    chapters = []
    by_id = {m['id']: m for m in d['milestones']}
    ids = [i for c in d['chapters'] for i in c['milestones']]
    if len(ids) != 12 or set(ids) != set(by_id):
        raise ValueError('Each of the 12 milestones must appear exactly once')
    for c in d['chapters']:
        chapter_id = c['id']
        intro = f'<p class="chapter-intro">{e(c["intro"])}</p>' if c.get('intro') else ''
        feature = f'<details class="did-you-know chapter-feature"><summary>Did You Know?</summary><p>{e(c["featureText"])}</p></details>' if c.get('featureText') else ''
        history = c.get('historyDetail') or c.get('intro', '')
        entries = ''.join(milestone(by_id[i]) for i in c['milestones'])
        end = f'<div class="chapter-end" aria-hidden="true">— {e(c["number"])} —</div>'
        archive = chapter_archive(chapter_id)
        period = f'<p class="chapter-period">{e(c["period"])}</p>' if c.get("period") else ''
        question = f'''<aside class="question"><span>A question to carry with you</span><p>{e(c['question'])}</p><details><summary>Consider the history</summary><p>{e(history)}</p></details></aside>'''
        chapters.append(f'''<section class="chapter {e(c['id'])}" id="{e(c['id'])}" aria-labelledby="heading-{e(c['id'])}"><header class="chapter-opening"><img class="folio-sprig" src="assets/folio-sprig.svg" alt="" aria-hidden="true" width="160" height="40"><p class="eyebrow">Chapter {e(c['number'])} / {e(c['label'])}</p>{period}{question if chapter_id == 'renewal' else ''}<div class="chapter-title-row"><span class="roman" aria-hidden="true">{e(c['number'])}</span><h2 id="heading-{e(c['id'])}">{e(c['title'])}</h2></div>{intro}{feature}{chapter_archive(chapter_id, opening=True)}{question if chapter_id != 'renewal' else ''}</header><div class="chapter-entries">{entries}</div>{archive}{end}</section>''')
    hero = d.get("homepageImage") or next(o for o in d["archiveObjects"] if o["id"] == d["heroObject"])
    nav = ''.join(f'<a href="#{e(c["id"])}"><span>{e(c["number"])}</span> {e(c["label"])}</a>' for c in d['chapters'])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#10069f"><meta name="description" content="Explore Singapore’s Islamic educational heritage through twelve milestones in a living tradition of learning, exchange and renewal."><title>{e(d['title'])}</title><link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to exhibition</a><div class="progress" aria-hidden="true"><span></span></div>
<header class="masthead"><a class="identity" href="#top"><span class="identity-name">SCIS<span>Exhibition companion</span></span><span class="institution">Singapore College<br>of Islamic Studies</span></a><span class="edition">A digital heritage journal<br><span>Singapore / Exhibition companion</span></span></header>
<main id="main"><section class="hero" id="top"><div class="hero-kicker"><span>Learning. Exchange. Renewal.</span><span>19th Century – Present</span></div><div class="hero-spread"><div class="hero-copy"><p class="eyebrow">{e(d['subtitle'])}</p><h1>A Brief History of<br><em>Islamic Education</em><br>in Singapore</h1><p class="standfirst">{e(d['opening'])}</p></div><figure class="cover-object"><div class="cover-mat">{image(hero)}</div><figcaption>{e(hero['caption'])}</figcaption></figure></div><div class="hero-foot"><span>Three Chapters · Twelve Milestones</span><span>Scroll to explore the history ↓</span></div></section>
<section id="introduction" class="introduction page-width"><p class="eyebrow">A living tradition</p><div class="intro-grid"><div><h2>Inherited knowledge.<br><em>Changing horizons.</em></h2><aside class="opening-question"><span>Before we begin</span><p>{e(d['openingQuestion'])}</p></aside><div class="intro-illustration">{object_figure(d['introductionImage'])}</div></div><div class="intro-prose">{paras(d['introduction'])}</div></div></section>
<nav class="chapter-nav" aria-label="Journal chapters"><div>{nav}</div></nav>
<div class="journal"><div class="history-line" aria-hidden="true"><span></span></div>{''.join(chapters)}</div>
<section class="closing page-width"><p class="eyebrow">An inheritance, still unfolding</p><h2>A Living<br><em>Intellectual Heritage</em></h2><div class="closing-reflection">{paras(d['closingReflection'])}</div><div class="closing-original">{paras(d['closing'])}</div><p class="closing-scis">SCIS is a contemporary chapter in this continuing intellectual tradition.</p><a href="#top" class="journey-link">Return to the first page <span aria-hidden="true">↑</span></a></section></main>
<footer class="site-footer"><div><span class="footer-institution">Singapore College of Islamic Studies</span><p>Rooted in Tradition. Shaped by Singapore.</p></div><p>Digital exhibition / Review edition<br>Archival identifications and reproduction permissions under review</p></footer>
</body></html>\n'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if index.html is not in sync')
    args = parser.parse_args()
    output = render()
    target = ROOT / 'index.html'
    if args.check:
        if target.read_text() != output:
            raise SystemExit('index.html is out of sync: run python3 tools/render.py')
        print('index.html matches content.json')
    else:
        target.write_text(output)
        print('Rendered index.html')
