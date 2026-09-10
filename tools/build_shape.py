"""Składa finalny shape.svg z bryły Chevron Blocks.

Źródło: bookofshapes.com, wzór "Chevron Blocks", licencja pozwala na
dowolne użycie i modyfikację (kopia w tools/LICENSE-bookofshapes.txt).

Co ten skrypt robi z oryginałem:
  1. spłaszcza zagnieżdżone transformacje do współrzędnych (było 1356 grup)
  2. zaokrągla do jednego miejsca po przecinku
  3. grupuje wielokąty w 15 bloków i nadaje pięciu z nich identyfikatory sekcji
  4. zamienia sztywny #cccccc na currentColor, żeby kolorem sterował CSS
  5. dokłada etykiety liczone z pozycji bloków, nie wpisane ręcznie

Uruchomienie:  python tools/build_shape.py
"""

import io
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# indeks bloku w bryle -> (numer sekcji, podpis)
SECTIONS = {
    0:  ("01", "Gdzie jesteście"),
    5:  ("02", "Co przecieka"),
    6:  ("03", "Co już zrobiłem"),
    12: ("04", "Kto to zrobił"),
    13: ("05", "Co może nie wyjść"),
}

OFFSET = 165.0     # jak daleko od bryły odsunięta etykieta
PAD = 28.0


def build():
    with io.open(os.path.join(HERE, "chevron-blocks.json"), encoding="utf-8") as fh:
        blocks = json.load(fh)

    cx0 = sum(b["cx"] for b in blocks) / len(blocks)
    cy0 = sum(b["cy"] for b in blocks) / len(blocks)

    body, labels = [], []
    xs, ys = [], []

    for b in blocks:
        tag = SECTIONS.get(b["i"])
        attrs = 'class="blk"'
        if tag:
            attrs = (f'class="blk blk--hit" data-target="{tag[0]}" tabindex="0" '
                     f'role="link" aria-label="Sekcja {tag[0]}, {tag[1]}"')
        polys = "".join(f'<polygon points="{p}"/>' for p in b["p"])
        body.append(f"<g {attrs}>{polys}</g>")

        for p in b["p"]:
            for pair in p.split(" "):
                x, y = pair.split(",")
                xs.append(float(x)); ys.append(float(y))

        if tag:
            vx, vy = b["cx"] - cx0, b["cy"] - cy0
            d = math.hypot(vx, vy) or 1.0
            lx, ly = b["cx"] + vx / d * OFFSET, b["cy"] + vy / d * OFFSET
            anchor = "end" if lx < cx0 else "start"
            labels.append(
                f'<g class="lbl" data-target="{tag[0]}" aria-hidden="true">'
                f'<line class="tick" x1="{b["cx"]:.1f}" y1="{b["cy"]:.1f}" '
                f'x2="{lx:.1f}" y2="{ly:.1f}"/>'
                f'<text class="lbl__no" x="{lx:.1f}" y="{ly:.1f}" '
                f'text-anchor="{anchor}">{tag[0]}</text>'
                f'<text class="lbl__txt" x="{lx:.1f}" y="{ly + 26:.1f}" '
                f'text-anchor="{anchor}">{tag[1]}</text></g>')
            xs += [lx - 150, lx + 150]
            ys += [ly - 45, ly + 40]

    x0, y0 = min(xs) - PAD, min(ys) - PAD
    w, h = max(xs) - min(xs) + PAD * 2, max(ys) - min(ys) + PAD * 2

    svg = (f'<svg class="shape" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="Bryła: pięć bloków prowadzi do pięciu sekcji">'
           + "".join(body) + "".join(labels) + "</svg>")

    with io.open(os.path.join(ROOT, "shape.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"shape.svg: {len(svg)} znakow, {len(blocks)} blokow, {len(labels)} etykiet")


if __name__ == "__main__":
    build()
