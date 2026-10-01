#!/usr/bin/env python3
"""Verify the delivered image collection, metadata, and local gallery links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse
import hashlib
import json
import struct

root = Path(__file__).resolve().parents[2]
atlas = root / 'word-atlas-23'
entries = json.loads((atlas / 'catalog.json').read_text())
assert len(entries) == 23
assert {e['index'] for e in entries} == set(range(1, 24))

def inspect_png(path):
    density = None
    profile = False
    dimensions = None
    with path.open('rb') as f:
        assert f.read(8) == b'\x89PNG\r\n\x1a\n', path
        while True:
            header = f.read(8)
            assert len(header) == 8, path
            size, kind = struct.unpack('>I4s', header)
            if kind in [b'IHDR', b'pHYs', b'iCCP', b'sRGB']:
                data = f.read(size)
                if kind == b'IHDR':
                    dimensions = struct.unpack('>II', data[:8])
                elif kind == b'pHYs':
                    x, y, unit = struct.unpack('>IIB', data)
                    density = (round(x * .0254), round(y * .0254), unit)
                elif kind in [b'iCCP', b'sRGB']:
                    profile = True
            else:
                f.seek(size, 1)
            f.read(4)
            if kind == b'IEND':
                break
    return dimensions, density, profile

hashes = []
note_words = 0
total_bytes = 0
for entry in entries:
    stem = f"{entry['index']:02d}-{entry['slug']}"
    png = root / f'atlas-{stem}-8000x10000.png'
    dimensions, density, profile = inspect_png(png)
    assert dimensions == (8000, 10000), (png, dimensions)
    assert density == (400, 400, 1), (png, density)
    assert profile, png
    hashes.append(hashlib.sha256(png.read_bytes()).hexdigest())
    total_bytes += png.stat().st_size
    assert inspect_png(atlas / 'previews' / f'{stem}.png')[0] == (1200, 1500)
    assert inspect_png(atlas / 'source' / 'art' / f'{stem}.png')[0] == (7200, 3200)
    note = (atlas / 'notes' / f'{stem}.md').read_text()
    words = len(note.split())
    assert words >= 550, (stem, words)
    note_words += words
assert len(set(hashes)) == 23, 'Each delivered image must be distinct.'

class LinkCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.cards = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and attrs.get('class') == 'study':
            self.cards += 1
        for key in ['href', 'src']:
            if key in attrs:
                self.links.append(attrs[key])

checker = LinkCheck()
checker.feed((root / 'word-atlas-23.html').read_text())
assert checker.cards == 23
for link in checker.links:
    parsed = urlparse(link)
    if not parsed.scheme and parsed.path:
        assert (root / unquote(parsed.path)).exists(), link

result = {
    'images': 23,
    'dimensions_each': [8000, 10000],
    'megapixels_each': 80,
    'dpi': 400,
    'srgb_tagged_images': 23,
    'unique_images': len(set(hashes)),
    'image_bytes': total_bytes,
    'companion_words': note_words,
    'valid_gallery_links': len(checker.links),
}
(atlas / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
