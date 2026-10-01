#!/usr/bin/env python3
"""Build the self-contained local index for the finished word atlas."""
from pathlib import Path
import html
import json
import re

root = Path(__file__).resolve().parents[2]
atlas = root / 'word-atlas-23'
entries = json.loads((atlas / 'catalog.json').read_text())
assert len(entries) == 23, 'Finish all 23 entries before building the final gallery.'

cards = []
for entry in entries:
    stem = f"{entry['index']:02d}-{entry['slug']}"
    png = f'atlas-{stem}-8000x10000.png'
    preview = f'word-atlas-23/previews/{stem}.png'
    notes = f'word-atlas-23/notes/{stem}.md'
    assert all((root / p).exists() for p in [png, preview, notes])
    esc = html.escape
    search = ' '.join([entry['word'], entry['slug'], entry['tagline'], entry['definition']])
    cards.append(f'''<article class="study" data-search="{esc(search, quote=True)}">
      <a class="image-link" href="{png}" aria-label="Open the full-resolution {esc(entry['word'])} image">
        <img src="{preview}" alt="Illustrated explanation of {esc(entry['word'])}" loading="lazy" width="1200" height="1500">
      </a>
      <div class="entry-line"><span class="number">{entry['index']:02d}</span><h2>{esc(entry['word'])}</h2></div>
      <p class="tagline">{esc(entry['tagline'])}</p>
      <p class="definition">{esc(entry['definition'])}</p>
      <div class="entry-links"><a href="{png}">Full-resolution PNG</a><a href="{notes}">Companion essay</a></div>
    </article>''')

document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The difficult word atlas — 23 illustrated inquiries</title>
<style>
:root{color-scheme:light;--ink:#202c38;--muted:#546471;--paper:#f5f6f7;--line:#d4dce2;--accent:#244e70}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--accent);text-underline-offset:4px}a:hover{color:#102e46}a:focus-visible,input:focus-visible{outline:3px solid #e1a448;outline-offset:5px}
.wrap{max-width:1500px;margin:auto;padding:0 48px}header{padding:70px 0 38px;display:grid;grid-template-columns:1fr auto;gap:36px;align-items:end}
.edition{font-size:14px;color:var(--muted);margin:0 0 17px}h1{font:clamp(42px,5vw,74px)/1.07 Georgia,serif;letter-spacing:-2px;max-width:850px;margin:0 0 24px}
.intro{max-width:820px;font-size:19px;color:var(--muted);margin:0}.edition-number{font:150px/.85 Georgia,serif;letter-spacing:-8px;color:#c2cdd6;padding-bottom:5px}
.downloads{display:flex;gap:26px;flex-wrap:wrap;margin:28px 0 0}.downloads a{font-weight:600}
.toolbar{display:flex;justify-content:space-between;align-items:center;gap:25px;border-block:1px solid var(--line);padding:22px 0;margin:0 0 38px}
.search{display:flex;align-items:center;gap:18px;flex:1}.search label{font-weight:600}input{font:inherit;background:white;border:1px solid #aab8c3;border-radius:3px;padding:10px 14px;max-width:420px;width:100%;color:var(--ink)}
.count{white-space:nowrap;color:var(--muted);font-size:14px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:55px 30px}.study[hidden]{display:none}
.image-link{display:block;background:#e3e8ec;box-shadow:0 8px 28px #26374512;transition:transform 160ms ease}.image-link:hover{transform:translateY(-3px)}img{display:block;width:100%;height:auto;aspect-ratio:4/5}
.entry-line{display:flex;align-items:baseline;gap:13px;margin-top:23px}.number{font-size:14px;color:var(--muted)}h2{font:33px/1.2 Georgia,serif;letter-spacing:-.5px;margin:0}
.tagline{font-size:16px;margin:10px 0 8px;font-weight:600}.definition{font-size:15px;color:var(--muted);margin:0 0 14px;max-width:58ch}.entry-links{display:flex;gap:20px;flex-wrap:wrap;font-size:14px}
.empty{padding:40px 0;font:30px Georgia,serif}footer{border-top:1px solid var(--line);margin-top:65px;padding:28px 0 50px;color:var(--muted);font-size:14px}footer p{max-width:1000px;margin:0 0 9px}
@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.edition-number{font-size:110px}.wrap{padding:0 30px}}
@media(max-width:650px){.wrap{padding:0 20px}header{padding-top:40px;grid-template-columns:1fr}.edition-number{display:none}h1{letter-spacing:-1px}.grid{grid-template-columns:1fr;gap:45px}.toolbar{display:block}.search{display:block}.search label{display:block;margin-bottom:9px}.count{margin-top:12px}.downloads{gap:18px}}
@media(prefers-reduced-motion:reduce){.image-link{transition:none}.image-link:hover{transform:none}}
</style></head><body><div class="wrap">
<header><div><p class="edition">An illustrated collection of language, philosophy, perception and systems</p>
<h1>The difficult word atlas</h1><p class="intro">Twenty-three words, twenty-three visual inquiries. Each opens into a detailed explanation, a careful distinction, and an original sentence with a little linguistic vertigo.</p>
<nav class="downloads" aria-label="Collection downloads"><a href="word-atlas-23-print.pdf">Open the complete print edition</a><a href="word-atlas-23/contact-sheet.png">View all 23 images together</a><a href="word-atlas-23/essays.md">Read the collected essays</a><a href="word-atlas-23/README.md">Collection notes</a></nav></div>
<div class="edition-number" aria-hidden="true">23</div></header>
<div class="toolbar"><div class="search"><label for="search">Find a word</label><input id="search" type="search" placeholder="Try “meaning”, “identity”, or “hysteresis”" autocomplete="off"></div><div class="count" id="count" role="status" aria-live="polite">23 of 23 word studies</div></div>
<main><div class="grid">''' + '\n'.join(cards) + '''</div><p class="empty" id="empty" hidden>No matching words. Try a broader idea.</p></main>
<footer><p>Every full-resolution image is an 8000 × 10000 lossless PNG with an sRGB profile and 400 dpi print metadata. The PDF preserves vector typography and includes a bookmark for each word.</p>
<p>The illustrations are locally rendered procedural artwork. Each companion essay examines uses, examples, neighboring concepts, and limits. All literary sentences are original.</p></footer>
</div><script>
const input=document.querySelector('#search'),cards=[...document.querySelectorAll('.study')],count=document.querySelector('#count'),empty=document.querySelector('#empty');
const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
input.addEventListener('input',()=>{const query=normalize(input.value.trim());let n=0;for(const card of cards){const match=normalize(card.dataset.search).includes(query);card.hidden=!match;if(match)n++;}count.textContent=`${n} of 23 word studies`;empty.hidden=n!==0;});
</script></body></html>'''
(root / 'word-atlas-23.html').write_text(document)

rows = []
for entry in entries:
    stem = f"{entry['index']:02d}-{entry['slug']}"
    rows.append(f"| {entry['index']:02d} | [{entry['word']}](../atlas-{stem}-8000x10000.png) | [Essay](notes/{stem}.md) | {entry['tagline']} |")
readme = '''# The difficult word atlas

23 original illustrated studies, each saved directly in the current working directory as an **8000 × 10000, 80-megapixel lossless PNG**. Together the images contain 1.84 billion pixels. Each uses an sRGB color profile and 400 dpi metadata, corresponding to a 20 × 25 inch print.

- [Browse the searchable gallery](../word-atlas-23.html).
- [Open the 23-page print edition](../word-atlas-23-print.pdf), with vector text and per-word bookmarks.
- [See the contact sheet](contact-sheet.png).
- [Read all 23 companion essays in one document](essays.md).

Each image contains a definition, pronunciation approximation, etymology, four explanatory sections, a concept-specific illustration, and an original literary sentence. The companion essays go further into distinctions, examples, limits, and suggested reading. Joyce supplies the playful ambition of the commission; none of the sentences is presented as his work.

The images were rendered locally using procedural graphics and native macOS typography. The artwork is a visual interpretation, and each entry identifies relevant limits of its metaphor. Philosophical frameworks, rhetorical usages, and scientific mechanisms are distinguished where needed.

| No. | Full-resolution image | Companion | Inquiry |
| --- | --- | --- | --- |
''' + '\n'.join(rows) + '''

## Source and reproduction

`catalog.json` contains the complete poster text. `source/art/` contains all 23 native-resolution transparent artwork layers. The renderer in `source/render-atlas.swift` composes the print typography, images, previews, PDF, and contact sheet. The group source scripts record the procedural constructions.

On macOS with Swift and AppKit, compile the renderer from the parent CWD:

```sh
swiftc -O word-atlas-23/source/render-atlas.swift -o /tmp/render-word-atlas
/tmp/render-word-atlas --preview-only
/tmp/render-word-atlas --pdf
/tmp/render-word-atlas --contact-sheet
```

Running the renderer without flags creates any missing full-resolution PNGs and preserves existing final PNGs. Previews, the PDF, and the contact sheet are generated artifacts. `--ids=1,2,3` selects individual entries. The full art inputs are retained locally, so rendering the finished collection does not require a network service.
'''
(atlas / 'README.md').write_text(readme)
collected = ['# The difficult word atlas: collected essays\n',
             'Twenty-three deeper readings to accompany the illustrated collection. All literary sentences are original; the artwork was rendered locally.\n']
for entry in entries:
    stem = f"{entry['index']:02d}-{entry['slug']}"
    collected.append(f"- [{entry['word']}](#{stem})")
for entry in entries:
    stem = f"{entry['index']:02d}-{entry['slug']}"
    note = (atlas / 'notes' / (stem + '.md')).read_text()
    note = re.sub(r'^(#{1,5}) ', r'#\1 ', note, flags=re.MULTILINE)
    collected.append(f'\n\n---\n\n<a id="{stem}"></a>\n\n' + note)
(atlas / 'essays.md').write_text('\n'.join(collected) + '\n')
print('Saved word-atlas-23.html, README.md, and collected essays.md')
