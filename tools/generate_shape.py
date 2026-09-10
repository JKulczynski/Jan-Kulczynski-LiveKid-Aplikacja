"""Generator izometrycznego kształtu z kreskowaniem (Chevron Blocks).

Rysowanie takiej bryły ręcznie w SVG jest nie do utrzymania. Ten skrypt
wypluwa gotowy SVG z siatki współrzędnych, więc przesunięcie bloku albo
zmiana gęstości kreskowania to zmiana jednej liczby, a nie przepisywanie
kilkuset punktów.

Uruchomienie:  python tools/generate_shape.py > shape.svg
"""

import math
import sys

S = 100.0                      # bok szescianu
DX = S * math.cos(math.radians(30))   # krok poziomy
DY = S * math.sin(math.radians(30))   # krok pionowy
HATCH = 5.0                    # odstep miedzy kreskami
STROKE = 1.6                   # grubosc kreski

# (i, j, k, id) - id niepuste oznacza sciane klikalna
# k to wysokosc, wieksze k = wyzej
BLOCKS = [
    # rdzen
    (0,  0, 0, None),
    (1,  0, 0, None),
    (0,  1, 0, None),
    (1,  1, 0, None),
    # ramie lewe gorne  ->  01
    (-1, -1, 1, ("01", "Gdzie jesteście")),
    (-1,  0, 0, None),
    # ramie prawe gorne ->  02
    (2,  -1, 1, ("02", "Co przecieka")),
    (1,  -1, 0, None),
    # srodek lewy       ->  03
    (0,  -1, 1, ("03", "Co już zrobiłem")),
    # ramie prawe dolne ->  04
    (2,   1, 0, ("04", "Kto to zrobił")),
    (2,   2, 0, None),
    # dol               ->  05
    (0,   2, 0, ("05", "Co może nie wyjść")),
    (1,   2, 0, None),
]


def origin(i, j, k):
    """Gorny wierzcholek szescianu w rzucie izometrycznym."""
    return ((i - j) * DX, (i + j) * DY - k * S)


def faces(i, j, k):
    ox, oy = origin(i, j, k)
    top = [(ox, oy), (ox + DX, oy + DY), (ox, oy + 2 * DY), (ox - DX, oy + DY)]
    left = [(ox - DX, oy + DY), (ox, oy + 2 * DY), (ox, oy + 2 * DY + S), (ox - DX, oy + DY + S)]
    right = [(ox + DX, oy + DY), (ox, oy + 2 * DY), (ox, oy + 2 * DY + S), (ox + DX, oy + DY + S)]
    return {"top": top, "left": left, "right": right}


def pts(poly):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in poly)


def hatch_pattern(name, angle):
    """Pasek rownoleglych kresek pod zadanym katem."""
    return (
        f'<pattern id="{name}" width="{HATCH}" height="{HATCH}" '
        f'patternUnits="userSpaceOnUse" patternTransform="rotate({angle})">'
        f'<line x1="0" y1="0" x2="0" y2="{HATCH}" stroke="currentColor" '
        f'stroke-width="{STROKE}"/></pattern>'
    )


def build():
    # sortowanie malarskie: dalsze bloki najpierw
    ordered = sorted(BLOCKS, key=lambda b: (b[2], b[0] + b[1]))

    body, xs, ys, labels = [], [], [], []
    for i, j, k, tag in ordered:
        f = faces(i, j, k)
        for poly in f.values():
            xs += [p[0] for p in poly]
            ys += [p[1] for p in poly]

        num = tag[0] if tag else None
        group = [f'<g class="blk{" hit" if tag else ""}"'
                 + (f' data-target="{num}" tabindex="0" role="link"'
                    f' aria-label="Sekcja {num}, {tag[1]}"' if tag else "")
                 + ">"]
        # kolejnosc: prawa, lewa, gorna - gorna zawsze na wierzchu
        group.append(f'<polygon points="{pts(f["right"])}" fill="url(#hr)" class="face"/>')
        group.append(f'<polygon points="{pts(f["left"])}"  fill="url(#hl)" class="face"/>')
        group.append(f'<polygon points="{pts(f["top"])}"   fill="url(#ht)" class="face"/>')
        # krawedzie: to one daja twardosc hard-edge
        for poly in (f["right"], f["left"], f["top"]):
            group.append(f'<polygon points="{pts(poly)}" class="edge"/>')
        group.append("</g>")
        body.append("".join(group))
        if tag:
            ox, oy = origin(i, j, k)
            cx, cy = ox, oy + DY          # srodek gornej sciany
            labels.append((cx, cy, tag[0], tag[1]))

    # etykiety odsuniete na zewnatrz, kierunek liczony od srodka bryly
    mx = sum(x for x, _, _, _ in labels) / len(labels)
    my = sum(y for _, y, _, _ in labels) / len(labels)
    lab_svg, OFF = [], 210.0
    for cx, cy, num, desc in labels:
        vx, vy = cx - mx, cy - my
        d = math.hypot(vx, vy) or 1.0
        lx, ly = cx + vx / d * OFF, cy + vy / d * OFF
        anchor = "end" if lx < mx else "start"
        lab_svg.append(
            f'<g class="lbl" data-target="{num}">'
            f'<line class="tick" x1="{cx:.1f}" y1="{cy:.1f}" x2="{lx:.1f}" y2="{ly:.1f}"/>'
            f'<text class="lbl__no" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}">{num}</text>'
            f'<text class="lbl__txt" x="{lx:.1f}" y="{ly + 34:.1f}" text-anchor="{anchor}">{desc}</text>'
            f"</g>")
        xs += [lx - 170, lx + 170]
        ys += [ly - 60, ly + 60]

    pad = 24
    x0, y0 = min(xs) - pad, min(ys) - pad
    w, h = max(xs) - min(xs) + pad * 2, max(ys) - min(ys) + pad * 2

    defs = "".join([hatch_pattern("ht", 90), hatch_pattern("hl", 30), hatch_pattern("hr", -30)])
    return (
        f'<svg class="shape" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Pięć sekcji jako izometryczne bloki">'
        f"<defs>{defs}</defs>" + "".join(body) + "".join(lab_svg) + "</svg>"
    )


if __name__ == "__main__":
    sys.stdout.write(build())
