#!/usr/bin/env python3
"""Assemble a reviewable image-generation plan. This does not call an API."""
from pathlib import Path
import html
import json

folder = Path(__file__).resolve().parent
selection = json.loads((folder / 'word-list.json').read_text())
entries = []
for name in ['briefs-001-037.json', 'briefs-038-074.json', 'briefs-075-111.json']:
    entries.extend(json.loads((folder / name).read_text()))
entries.sort(key=lambda e: e['index'])
assert len(entries) == 111
assert [e['index'] for e in entries] == list(range(1, 112))
required = {'index', 'slug', 'word', 'definition', 'explanation', 'etymology', 'literary_sentence', 'image_brief'}
for entry, expected in zip(entries, selection):
    assert required <= entry.keys(), (entry.get('slug'), required - entry.keys())
    assert entry['slug'] == expected['slug']
    for key in required - {'index'}:
        assert isinstance(entry[key], str) and entry[key].strip(), (entry['slug'], key)

plan = {
    'status': 'prepared_not_generated',
    'image_count': 111,
    'proposed_method': 'AI-generated illustrations with precisely typeset explanatory text',
    'proposed_api_model': 'gpt-image-2',
    'proposed_quality': 'high',
    'proposed_native_illustration_size': '3840x2160',
    'proposed_final_poster_size': '3840x5120',
    'output_format': 'png',
    'final_destination': 'current working directory',
    'final_filename_pattern': 'ai-atlas-{index:03d}-{slug}.png',
    'generation_calls_made': 0,
    'required_before_generation': [
        'User explicitly confirms the CLI/API fallback.',
        'OPENAI_API_KEY is configured locally and available to the generating process.'
    ],
    'billing': 'API usage is billed separately; no cost estimate has been verified.',
    'quality_note': 'The art uses the proposed native model output size; the explanatory page adds typography rather than enlarging the artwork.',
    'entries': entries,
}
(folder / 'batch-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')

prompts = []
for e in entries:
    prompt = (
        'Use case: stylized-concept\n'
        'Asset type: original editorial illustration for an advanced illustrated lexicon\n'
        f"Primary subject: {e['word']}\n"
        f"Concept: {e['definition']}\n"
        f"Important distinction: {e['explanation']}\n"
        f"Visual direction: {e['image_brief']}\n"
        'Composition: landscape 16:9; a coherent focal composition with finished edges and sufficient margin for a clean editorial crop.\n'
        'Quality: exceptionally detailed materials, purposeful lighting, clear visual hierarchy, and a distinctive artistic treatment matched to this concept.\n'
        'Constraints: the illustration is a visual metaphor, not scientific evidence or a medical diagnostic image. No text, letters, captions, logos, signatures, or watermark. Explanatory typography will be added separately.\n'
    )
    prompts.append({'index': e['index'], 'slug': e['slug'], 'prompt': prompt})
(folder / 'image-prompts.jsonl').write_text(''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in prompts))

markdown = ['# 111 illustrated word studies: generation plan\n',
            '**Status: prepared; no images have been generated for this batch.**\n',
            'Proposed execution: 111 AI-generated illustrations at high quality and 3840 × 2160, composed into 3840 × 5120 PNG pages with locally typeset explanations. Final PNGs will be saved directly in the current working directory.\n',
            'The built-in image-generation tool is unavailable in this session. The API fallback requires an explicitly authorized run and a locally configured `OPENAI_API_KEY`. No API request has been made.\n',
            'These briefs are a reviewable starting point. Philosophical usages are attributed to their frameworks, clinical terms are not presented as diagnoses, and all literary sentences are original.\n']
cards = []
for e in entries:
    title = f"{e['index']:03d}. {e['word']}"
    markdown.extend([f'\n## {title}\n', e['definition'] + '\n', e['explanation'] + '\n',
                     '**Etymology:** ' + e['etymology'] + '\n',
                     '**Original literary sentence:** ' + e['literary_sentence'] + '\n',
                     '**Image brief:** ' + e['image_brief'] + '\n'])
    esc = html.escape
    search = ' '.join([e['word'], e['slug'], e['definition'], e['explanation']])
    cards.append(f'''<article data-search="{esc(search, quote=True)}">
      <div class="title"><span>{e['index']:03d}</span><h2>{esc(e['word'])}</h2></div>
      <p class="definition">{esc(e['definition'])}</p>
      <details><summary>Read the explanation and image brief</summary>
        <p>{esc(e['explanation'])}</p><p><b>Etymology.</b> {esc(e['etymology'])}</p>
        <blockquote>{esc(e['literary_sentence'])}</blockquote>
        <p><b>Proposed illustration.</b> {esc(e['image_brief'])}</p>
      </details></article>''')
(folder / 'review.md').write_text('\n'.join(markdown) + '\n')

page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>111 word studies — review the image-generation plan</title><style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f5f7f8;color:#213343;font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.wrap{max-width:1200px;margin:auto;padding:60px 35px}h1{font:58px/1.08 Georgia,serif;letter-spacing:-1.5px;max-width:900px;margin:15px 0 25px}.status{font-weight:600;color:#765018}.intro{max-width:900px;color:#536676;font-size:19px}.facts{display:flex;gap:12px 30px;flex-wrap:wrap;font-size:15px;border-block:1px solid #ced7de;padding:20px 0;margin:28px 0}.facts b{display:block;color:#233c52}.links{display:flex;gap:25px;flex-wrap:wrap;margin:20px 0 30px}a{color:#26587b;text-underline-offset:4px}.search{display:flex;align-items:center;gap:20px;flex-wrap:wrap;margin:30px 0}label{font-weight:600}input{font:inherit;padding:10px 14px;max-width:450px;width:100%;border:1px solid #9eafbd;border-radius:3px;background:white}#count{font-size:14px;color:#526673}.grid{display:grid;grid-template-columns:1fr 1fr;gap:0 40px}article{border-top:1px solid #ced7de;padding:25px 0 30px}article[hidden]{display:none}.title{display:flex;align-items:baseline;gap:14px}.title span{font-size:14px;color:#6d7e8b}h2{font:32px/1.2 Georgia,serif;margin:0}.definition{color:#334c5e}summary{cursor:pointer;color:#26587b;font-size:15px}details p{font-size:16px}blockquote{margin:20px 0;border-left:3px solid #9eb5c6;padding:3px 0 3px 20px;font:20px/1.5 Georgia,serif}footer{border-top:1px solid #ced7de;margin-top:30px;padding-top:25px;color:#526673;font-size:14px}a:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid #c69342;outline-offset:4px}@media(max-width:700px){.wrap{padding:35px 20px}.grid{grid-template-columns:1fr}h1{font-size:42px}}
</style></head><body><div class="wrap">
<p class="status">Prepared for review · No images generated</p><h1>111 words. 111 distinct image briefs.</h1>
<p class="intro">A proposed collection of AI illustrations and precisely typeset explanations. Each entry includes a definition, a deeper distinction, an original literary sentence, and its own visual direction.</p>
<div class="facts"><div><b>111 images</b>One word per image</div><div><b>High-quality API generation</b>Proposed model: gpt-image-2</div><div><b>3840 × 2160 artwork</b>3840 × 5120 finished PNG pages</div><div><b>Generation pending</b>API authorization and local key required</div></div>
<nav class="links"><a href="review.md">Complete review document</a><a href="batch-plan.json">Structured batch plan</a><a href="image-prompts.jsonl">All 111 image prompts</a></nav>
<p>The built-in image tool is unavailable. The API fallback requires explicit confirmation and a locally configured <code>OPENAI_API_KEY</code>. API usage is billed separately. No generation request has been sent.</p>
<div class="search"><label for="search">Find a word or idea</label><input id="search" type="search" placeholder="Try “memory”, “grammar”, or “noema”"><span id="count" role="status" aria-live="polite">111 of 111 briefs</span></div>
<main class="grid">''' + '\n'.join(cards) + '''</main>
<footer>All literary sentences are original. The philosophical and visual interpretations are explained in the briefs; no image is represented as already generated.</footer>
</div><script>
const input=document.querySelector('#search'),cards=[...document.querySelectorAll('article')],count=document.querySelector('#count');
const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
input.addEventListener('input',()=>{let n=0;const q=norm(input.value.trim());for(const card of cards){const visible=norm(card.dataset.search).includes(q);card.hidden=!visible;if(visible)n++;}count.textContent=`${n} of 111 briefs`;});
</script></body></html>'''
(folder / 'index.html').write_text(page)
print(json.dumps({'briefs': len(entries), 'prompts': len(prompts), 'generation_calls': 0,
                  'review_words': len(' '.join(markdown).split())}))
