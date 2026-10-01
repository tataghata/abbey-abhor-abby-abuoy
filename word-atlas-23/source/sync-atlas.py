#!/usr/bin/env python3
"""Collect complete, validated entries from the three independent art workspaces."""
from pathlib import Path
import json
import shutil
import struct

ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / 'word-atlas-23'
STAGING = Path('/tmp/memoryx-word-atlas23')
ART = ATLAS / 'source' / 'art'
ART.mkdir(exist_ok=True)
entries = []
ready = []
for group in ['group-a', 'group-b', 'group-c']:
    for path in sorted((STAGING / group).glob('[0-9][0-9]-*.json')):
        try:
            entry = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        required = {'index', 'slug', 'word', 'pronunciation', 'tagline', 'definition',
                    'etymology', 'sections', 'literary', 'art_caption', 'accent', 'theme'}
        assert required <= entry.keys(), (path.name, required - entry.keys())
        assert len(entry['sections']) == 4, path.name
        assert all(set(s) >= {'heading', 'text'} for s in entry['sections']), path.name
        assert 1 <= entry['index'] <= 23, path.name
        entry['word'] = entry['word'].lower()
        for key in ['accent', 'theme']:
            entry[key] = entry[key].lstrip('#')
            assert len(entry[key]) == 6
            int(entry[key], 16)
        stem = f"{entry['index']:02d}-{entry['slug']}"
        assert path.stem == stem, (path.stem, stem)
        note = ATLAS / 'notes' / (stem + '.md')
        assert note.exists(), str(note)
        entries.append(entry)
        source = path.with_suffix('.png')
        if source.exists():
            raw = source.read_bytes()
            if len(raw) < 40 or raw[-12:-8] != b'\0\0\0\0' or raw[-8:-4] != b'IEND':
                continue  # A render may still be saving.
            assert raw[:8] == b'\x89PNG\r\n\x1a\n', source
            assert struct.unpack('>II', raw[16:24]) == (7200, 3200), source
            target = ART / source.name
            if not target.exists() or source.stat().st_mtime_ns > target.stat().st_mtime_ns:
                temporary = target.with_suffix('.partial')
                shutil.copy2(source, temporary)
                temporary.replace(target)
            ready.append(entry['index'])
    for script in (STAGING / group).iterdir():
        if script.suffix in {'.py', '.swift', '.cpp', '.hpp', '.h', '.c', '.sh'}:
            shutil.copy2(script, ATLAS / 'source' / (group + '-' + script.name))

entries.sort(key=lambda e: e['index'])
assert len({e['index'] for e in entries}) == len(entries)
(ATLAS / 'catalog.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'content_entries': len(entries), 'ready_art': len(ready), 'ready_ids': sorted(ready)}))
