#!/usr/bin/env python3
"""Assemble the finished local collection. No network dependencies."""
from pathlib import Path
import html
import json
import re

atlas = Path(__file__).resolve().parents[1]
entries = [json.loads(p.read_text()) for p in sorted((atlas / 'source/content').glob('*.json'))]
assert len(entries) == 111
assert [e['index'] for e in entries] == list(range(1, 112))
(atlas / 'catalog.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n')
esc = html.escape


def markdown_to_html(source):
    """Render the deliberately small Markdown vocabulary of these authored notes."""
    blocks = []
    for block in re.split(r'\n\s*\n', source.strip()):
        block = block.strip()
        if not block:
            continue
        match = re.match(r'^(#{1,6})\s+(.+)$', block)
        if match:
            level = min(4, len(match[1]) + 1)
            blocks.append(f'<h{level}>{esc(match[2])}</h{level}>')
        elif block.startswith('> '):
            blocks.append('<blockquote>' + esc(re.sub(r'^>\s?', '', block, flags=re.M)) + '</blockquote>')
        else:
            value = esc(block).replace('\n', ' ')
            value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
            value = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', value)
            blocks.append('<p>' + value + '</p>')
    return '\n'.join(blocks)


cards, collected, rows = [], [], []
words = 0
for entry in entries:
    stem = f"{entry['index']:03d}-{entry['slug']}"
    png = f'atlas-{stem}-8000x10000.png'
    preview = f'previews/{stem}.png'
    notes = f'notes/{stem}.md'
    assert all((atlas / p).is_file() for p in [png, preview, notes])
    note = (atlas / notes).read_text()
    words += len(note.split())
    search = ' '.join([entry['word'], entry['slug'], entry['tagline'], entry['definition']])
    cards.append(f'''<article class="study" data-search="{esc(search, quote=True)}">
<a class="image-link" href="{png}" aria-label="Open the full resolution {esc(entry['word'])} image"><img src="{preview}" alt="An illustrated study of {esc(entry['word'])}: {esc(entry['art_caption'])}" loading="lazy" width="1200" height="1500"></a>
<div class="entry-line"><span class="number">{entry['index']:03d}</span><h2>{esc(entry['word'])}</h2></div>
<p class="tagline">{esc(entry['tagline'])}</p><p class="definition">{esc(entry['definition'])}</p>
<div class="entry-links"><button class="read" data-title="{esc(entry['word'], quote=True)}">Read the full explanation <span aria-hidden="true">↗</span></button><a href="{png}" download>80 MP PNG</a><a href="{notes}" download>Text</a></div>
<template class="reading"><div class="reader-links"><a href="{png}">Full resolution image</a><a href="{notes}" download>Download this essay</a></div>{markdown_to_html(note)}</template>
</article>''')
    collected.append(f'\n\n---\n\n<a id="{stem}"></a>\n\n' + re.sub(r'^(#{1,5}) ', r'#\1 ', note, flags=re.M))
    rows.append(f"| {entry['index']:03d} | [{entry['word']}]({png}) | [Essay]({notes}) | {entry['tagline']} |")

document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The improbable lexicon — 111 illustrated word studies</title>
<style>
:root{color-scheme:light;--ink:#272335;--muted:#6d6674;--paper:#f7f4ee;--line:#d8d0c8;--accent:#795233}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--accent);text-underline-offset:4px}a:hover{color:#352440}button,input{font:inherit}button{cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #bd8345;outline-offset:5px}
.wrap{max-width:1570px;margin:auto;padding:0 56px}header{padding:75px 0 44px;display:grid;grid-template-columns:1fr auto;gap:36px;align-items:end}
.edition{font-size:12px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);margin:0 0 24px}h1{font:clamp(48px,6vw,93px)/1.01 Georgia,serif;letter-spacing:-.045em;max-width:880px;margin:0 0 29px}
.intro{max-width:730px;font-size:19px;color:var(--muted);margin:0}.edition-number{font:clamp(120px,15vw,220px)/.85 Georgia,serif;letter-spacing:-.06em;color:#ddd1c1;padding-bottom:5px}
.downloads{display:flex;gap:23px;flex-wrap:wrap;margin:29px 0 0;font-size:14px}.downloads a{font-weight:600}
.toolbar{display:flex;align-items:center;gap:20px;border-block:1px solid var(--line);padding:22px 0;margin:0 0 42px;flex-wrap:wrap}.search{display:flex;align-items:center;gap:18px;flex:1;min-width:290px}.search label{font-weight:600;white-space:nowrap}input{background:#fffdf9;border:1px solid #b8aaa0;border-radius:2px;padding:10px 14px;width:100%;max-width:400px;color:var(--ink)}
.action{border:1px solid #b8aaa0;background:transparent;color:var(--ink);padding:10px 15px;border-radius:2px}.action:hover{background:#eee7df}.count{white-space:nowrap;color:var(--muted);font-size:13px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:56px 31px}.study[hidden]{display:none}.image-link{display:block;background:#e8e0d8;box-shadow:0 9px 28px #35243b12;transition:transform 160ms ease}.image-link:hover{transform:translateY(-4px)}img{display:block;width:100%;height:auto;aspect-ratio:4/5}
.entry-line{display:flex;align-items:baseline;gap:12px;margin-top:22px}.number{font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}h2{font:clamp(24px,2.5vw,35px)/1.2 Georgia,serif;letter-spacing:-.025em;margin:0;overflow-wrap:anywhere}.tagline{font-size:15px;margin:11px 0 7px;font-weight:600}.definition{font-size:14px;color:var(--muted);margin:0 0 15px;max-width:58ch}.entry-links{display:flex;gap:10px 20px;flex-wrap:wrap;align-items:center;font-size:13px}.read{padding:0;border:0;border-bottom:1px solid currentColor;color:var(--accent);background:none}.read span{font-size:18px;margin-left:3px}
.empty{padding:40px 0;font:30px Georgia,serif}footer{border-top:1px solid var(--line);margin-top:65px;padding:28px 0 50px;color:var(--muted);font-size:13px}footer p{max-width:1000px;margin:0 0 9px}
dialog{border:1px solid var(--line);background:var(--paper);color:var(--ink);width:min(850px,calc(100% - 30px));max-height:90vh;padding:0;box-shadow:0 30px 90px #170f3445}dialog::backdrop{background:#201a32aa;backdrop-filter:blur(4px)}.reader-toolbar{display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:var(--paper);padding:16px 25px;border-bottom:1px solid var(--line);z-index:1}.reader-toolbar span{font-size:13px;text-transform:uppercase;letter-spacing:.1em}.close{font-size:18px;border:0;background:transparent;padding:4px 10px;color:var(--ink)}#reading{padding:30px clamp(24px,6vw,65px) 55px;font:19px/1.7 Georgia,serif}#reading h2{font-size:45px;margin:25px 0 20px}#reading h3{font-size:25px;margin:30px 0 10px}#reading h4{font-size:21px;margin:25px 0 10px}#reading p{margin:0 0 20px}#reading blockquote{margin:25px 0;border-left:3px solid #b28756;padding:5px 0 5px 24px;font-style:italic}.reader-links{display:flex;gap:20px;font:13px/1.5 -apple-system,BlinkMacSystemFont,sans-serif;flex-wrap:wrap}
@media(max-width:1100px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.wrap{padding:0 32px}.edition-number{font-size:125px}h2{font-size:31px}}
@media(max-width:650px){.wrap{padding:0 20px}header{padding-top:40px;grid-template-columns:1fr}.edition-number{display:none}.grid{grid-template-columns:1fr;gap:42px}.toolbar{gap:14px}.search{min-width:100%;display:block}.search label{display:block;margin-bottom:8px}input{max-width:none}.downloads{gap:13px 20px}.count{min-width:100%}#reading{font-size:18px}}
@media(prefers-reduced-motion:reduce){.image-link{transition:none}.image-link:hover{transform:none}}
</style></head><body><div class="wrap">
<header><div><p class="edition">Language · philosophy · perception · form</p><h1>The improbable<br>lexicon.</h1><p class="intro">111 words at the edge of easy explanation. Sculptures for the eye, close readings for the mind, and original sentences that enjoy getting a little lost.</p>
<nav class="downloads" aria-label="Collection downloads"><a href="word-atlas-111-print.pdf">The print edition</a><a href="contact-sheet.png">All 111 images</a><a href="essays.md">Collected essays</a><a href="README.md">About the collection</a></nav></div><div class="edition-number" aria-hidden="true">111</div></header>
<div class="toolbar"><div class="search"><label for="search">Find a word</label><input id="search" type="search" placeholder="Meaning, identity, time…" autocomplete="off"></div><button class="action" id="shuffle">Shuffle the gallery</button><button class="action" id="random">Read a random word</button><div class="count" id="count" role="status" aria-live="polite">111 of 111 word studies</div></div>
<main><div class="grid">''' + '\n'.join(cards) + '''</div><p class="empty" id="empty" hidden>No matching words. Try a broader idea.</p></main>
<footer><p>111 original local renderings. Every full resolution image is an 8000 × 10000 lossless PNG, tagged sRGB with 400 dpi print metadata. The 111-page PDF preserves vector typography and bookmarks.</p><p>Companion essays contain WORD_COUNT words. Illustrations are conceptual metaphors made with procedural 3D geometry; they were not generated by an AI image model. All literary sentences are original.</p></footer></div>
<dialog id="reader" aria-labelledby="reader-title"><div class="reader-toolbar"><span id="reader-title">The improbable lexicon</span><button class="close" aria-label="Close the explanation">Close ×</button></div><div id="reading"></div></dialog>
<script>
const input=document.querySelector('#search'),cards=[...document.querySelectorAll('.study')],count=document.querySelector('#count'),empty=document.querySelector('#empty'),grid=document.querySelector('.grid'),reader=document.querySelector('#reader'),reading=document.querySelector('#reading');
const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
input.addEventListener('input',()=>{const query=normalize(input.value.trim());let n=0;for(const card of cards){const match=normalize(card.dataset.search).includes(query);card.hidden=!match;if(match)n++;}count.textContent=`${n} of 111 word studies`;empty.hidden=n!==0;document.querySelector('#random').disabled=n===0;});
const randomInt=n=>{const u=new Uint32Array(1);crypto.getRandomValues(u);return Math.floor(u[0]/4294967296*n)};
document.querySelector('#shuffle').addEventListener('click',()=>{const order=[...cards];for(let i=order.length-1;i>0;i--){const j=randomInt(i+1);[order[i],order[j]]=[order[j],order[i]]}order.forEach(c=>grid.append(c));});
function show(card){reading.replaceChildren(card.querySelector('template').content.cloneNode(true));document.querySelector('#reader-title').textContent=card.querySelector('.read').dataset.title;reader.showModal();reader.scrollTop=0;}
document.querySelectorAll('.read').forEach(button=>button.addEventListener('click',()=>show(button.closest('.study'))));
document.querySelector('#random').addEventListener('click',()=>{const visible=cards.filter(c=>!c.hidden);if(visible.length)show(visible[randomInt(visible.length)]);});
document.querySelector('.close').addEventListener('click',()=>reader.close());
reader.addEventListener('click',event=>{if(event.target===reader){const r=reader.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)reader.close()}});
</script></body></html>'''
document = document.replace('WORD_COUNT', f'{words:,}')
(atlas / 'index.html').write_text(document)
contents = '\n'.join(f"- [{e['word']}](#{e['index']:03d}-{e['slug']})" for e in entries)
(atlas / 'essays.md').write_text('# The improbable lexicon: collected essays\n\n111 close readings accompanying original local illustrations.\n\n' + contents + ''.join(collected) + '\n')
readme = '''# The improbable lexicon

111 new illustrated word studies, created locally in this folder. Each final image is an **8000 × 10000, 80-megapixel lossless PNG**, with sRGB color tagging and 400 dpi metadata. This supports a 20 × 25 inch print at 400 dpi. Across the collection: 8.88 billion final pixels.

- [Open the searchable gallery](index.html): search, shuffle, or read a random word. Full essays open within the page; no server or internet is needed.
- [Open the 111-page print edition](word-atlas-111-print.pdf), with vector typography and a bookmark for each word.
- [View the contact sheet](contact-sheet.png).
- [Read all companion essays](essays.md).

The artwork consists of newly constructed procedural 3D sculptures rendered locally. No AI image-generation service was used. The earlier AI artwork prompts in `briefs.json` remain a record of planning; the delivered sculptures have their own captions and source geometry. The word studies build on the prepared briefs with definitions, etymologies, four explanatory sections, detailed examples, distinctions, and original literary sentences. Joyce provides the playful ambition, not an attribution.

Each illustration is an interpretive metaphor. Philosophical frameworks and disputed meanings are identified in the text rather than presented as settled physical mechanisms. Companion notes extend beyond the text on the poster.

## The collection

| No. | Full resolution image | Companion | Inquiry |
| --- | --- | --- | --- |
''' + '\n'.join(rows) + '''

## Files and reproduction

The 111 `atlas-*.png` files in this folder are the finished images. `previews/` holds smaller browsing copies; `notes/` holds the essays. `catalog.json` contains the poster text. `source/art/` holds native 7200 × 3200 transparent artwork. `source/proofs/` holds artwork proofs and render metadata. Group scripts preserve each new construction and its authored explanations.

On macOS with Swift/AppKit, Python, NumPy, and a C++ compiler, run the following from the parent current working directory:

```sh
mkdir -p /tmp/memoryx-word-atlas111
clang++ -O3 -std=c++17 -dynamiclib word-atlas-111-new/source/raster.cpp -o /tmp/memoryx-word-atlas111/raster.dylib
swiftc -O -module-cache-path /tmp/memoryx-word-atlas111/module-cache word-atlas-111-new/source/render-atlas.swift -o /tmp/memoryx-word-atlas111/render-atlas
/tmp/memoryx-word-atlas111/render-atlas --preview-only
/tmp/memoryx-word-atlas111/render-atlas --pdf
/tmp/memoryx-word-atlas111/render-atlas --contact-sheet
python3 word-atlas-111-new/source/build-gallery.py
python3 word-atlas-111-new/source/validate-atlas.py
```

The page renderer preserves existing final PNGs. Without flags, it creates missing finals and refreshes previews. `--ids=1,2,3` selects entries. The complete native art is retained, so rebuilding pages does not require rerendering the sculptures or contacting a network service.
'''
(atlas / 'README.md').write_text(readme)
print(json.dumps({'gallery_entries': len(entries), 'companion_words': words, 'gallery': str(atlas / 'index.html')}))
