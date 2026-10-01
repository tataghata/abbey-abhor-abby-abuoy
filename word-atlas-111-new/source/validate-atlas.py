#!/usr/bin/env python3
"""Verify the delivered image collection, metadata, and local gallery links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse
import hashlib
import json
import struct
import zlib

atlas = Path(__file__).resolve().parents[1]
root = atlas
entries = json.loads((atlas / 'catalog.json').read_text())
assert len(entries) == 111
assert {e['index'] for e in entries} == set(range(1, 112))

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
            data = f.read(size)
            assert len(data) == size, ('Truncated PNG chunk', path, kind)
            if kind in [b'IHDR', b'pHYs', b'iCCP', b'sRGB']:
                if kind == b'IHDR':
                    dimensions = struct.unpack('>II', data[:8])
                elif kind == b'pHYs':
                    x, y, unit = struct.unpack('>IIB', data)
                    density = (round(x * .0254), round(y * .0254), unit)
                elif kind in [b'iCCP', b'sRGB']:
                    profile = True
            crc = f.read(4)
            assert len(crc) == 4, ('Missing PNG checksum', path, kind)
            assert struct.unpack('>I', crc)[0] == zlib.crc32(kind + data) & 0xffffffff, ('PNG checksum mismatch', path, kind)
            if kind == b'IEND':
                break
    return dimensions, density, profile

hashes = []
art_hashes = []
files = []
note_words = 0
total_bytes = 0
for entry in entries:
    stem = f"{entry['index']:03d}-{entry['slug']}"
    png = root / f'atlas-{stem}-8000x10000.png'
    dimensions, density, profile = inspect_png(png)
    assert dimensions == (8000, 10000), (png, dimensions)
    assert density == (400, 400, 1), (png, density)
    assert profile, png
    hashes.append(hashlib.sha256(png.read_bytes()).hexdigest())
    total_bytes += png.stat().st_size
    assert inspect_png(atlas / 'previews' / f'{stem}.png')[0] == (1200, 1500)
    art_path = atlas / 'source' / 'art' / f'{stem}.png'
    assert inspect_png(art_path)[0] == (7200, 3200)
    art_hashes.append(hashlib.sha256(art_path.read_bytes()).hexdigest())
    files.append({'image': png.name, 'sha256': hashes[-1], 'bytes': png.stat().st_size, 'art_sha256': art_hashes[-1]})
    note = (atlas / 'notes' / f'{stem}.md').read_text()
    words = len(note.split())
    assert words >= 420, (stem, words)
    note_words += words
assert len(set(hashes)) == 111, 'Each delivered image must be distinct.'
assert len(set(art_hashes)) == 111, 'Each native sculpture must be distinct.'
assert len(list(atlas.glob('atlas-*-8000x10000.png'))) == 111

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
checker.feed((root / 'index.html').read_text())
assert checker.cards == 111
for link in checker.links:
    parsed = urlparse(link)
    if not parsed.scheme and parsed.path:
        assert (root / unquote(parsed.path)).exists(), link

result = {
    'images': 111,
    'dimensions_each': [8000, 10000],
    'megapixels_each': 80,
    'dpi': 400,
    'srgb_tagged_images': 111,
    'unique_images': len(set(hashes)),
    'unique_native_artworks': len(set(art_hashes)),
    'png_chunk_checksums': 'passed',
    'image_bytes': total_bytes,
    'companion_words': note_words,
    'valid_gallery_links': len(checker.links),
}
(atlas / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
(atlas / 'file-manifest.json').write_text(json.dumps(files, indent=2) + '\n')
print(json.dumps(result))
