#!/usr/bin/env python3
import json, time, subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parent
renderer=Path('/tmp/memoryx-word-atlas111/render-atlas')
last=-1
while True:
    complete=list(BASE.glob('atlas-*-8000x10000.png'))
    if len(complete)!=last:
        print('FINAL EXPORTS',len(complete),'/ 111',flush=True);last=len(complete)
    if len(complete)==111:break
    ready=[]
    for p in sorted((BASE/'source/content').glob('*.json')):
        stem=p.stem
        if (BASE/f'atlas-{stem}-8000x10000.png').exists():continue
        art=BASE/'source/art'/f'{stem}.png'
        marker=BASE/'source/proofs'/f'{stem}-art.json'
        if not art.exists() or not marker.exists():continue
        ready.append(json.loads(p.read_text())['index'])
    if ready:
        subprocess.run([str(renderer),'--ids='+','.join(map(str,ready[:5]))],cwd=ROOT,check=True)
    else:time.sleep(8)
print('ALL 111 FINAL IMAGES EXPORTED',flush=True)
