import sys
import numpy as np
import potrace
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
S = 8
im = Image.open(src).convert('RGBA')
w, h = im.size
a = np.array(im, dtype=float)
inkv = np.clip(a[..., 3] / 255 * (255 - a[..., 0]) / 235 * 255, 0, 255)
inkv[62:76, 86:120] = 255  # SAN: redrawn as vector text
inkv[:22, 182:] = 0  # registered mark: redrawn
ink = Image.fromarray(inkv.astype(np.uint8))
alpha = ink.resize((w * S, h * S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(S * 0.3))
mask = np.array(alpha) > 128

bm = potrace.Bitmap(~mask)
plist = bm.trace(turdsize=S * S // 2, alphamax=1.0, opticurve=True, opttolerance=0.25)


def pt(p):
    return f'{p.x / S:.2f} {p.y / S:.2f}'


parts = []
for curve in plist:
    d = [f'M{pt(curve.start_point)}']
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f'L{pt(seg.c)}L{pt(seg.end_point)}')
        else:
            d.append(f'C{pt(seg.c1)} {pt(seg.c2)} {pt(seg.end_point)}')
    parts.append(''.join(d) + 'Z')

FONT = TTFont(sys.argv[3])
CMAP = FONT.getBestCmap()
GLYPHS = FONT.getGlyphSet()


def text_path(text, size, cx, baseline, length):
    # Same geometry as <text text-anchor="middle" textLength=... lengthAdjust="spacingAndGlyphs">
    scale = size / FONT['head'].unitsPerEm
    names = [CMAP[ord(ch)] for ch in text]
    advance = sum(GLYPHS[n].width for n in names)
    sx = length / advance
    pen = SVGPathPen(GLYPHS, ntos=lambda v: f'{v:.2f}')
    x = 0
    for n in names:
        GLYPHS[n].draw(TransformPen(pen, (sx, 0, 0, -scale, cx - length / 2 + x * sx, baseline)))
        x += GLYPHS[n].width
    return pen.getCommands()


svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Focus SAN">'
       f'<defs><mask id="san" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="#fff"/>'
       f'<path fill="#000" d="{text_path("SAN", 16, 102.6, 75, 31)}"/></mask></defs>'
       f'<path fill="#143f90" fill-rule="evenodd" mask="url(#san)" d="{"".join(parts)}"/>'
       '<circle cx="189.6" cy="12.3" r="5.9" fill="none" stroke="#143f90" stroke-width="0.9"/>'
       f'<path fill="#143f90" d="{text_path("R", 9.5, 189.7, 15.6, 5)}"/></svg>\n')
open(out, 'w', encoding='utf-8').write(svg)
print(len(plist), 'paths', len(svg), 'bytes')
