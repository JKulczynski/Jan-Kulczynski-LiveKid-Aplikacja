# Jan Kulczyński &middot; LiveKid

Aplikacja na rolę **CEO of Agents** w LiveKid. Zamiast CV: jedna strona i działający agent.

Strona: https://jan-kulczynski-live-kid-aplikacja.vercel.app

## Co tu jest

Pięć sekcji, każda za jednym blokiem bryły na ekranie głównym:

1. **Co wiem** o LiveKid: produkt, cena, liczby z KRS i prasy, kierunek. Wszystko ze źródłami.
2. **Dziesięć razy**: cel z ogłoszenia (trzy mini-produkty, z 500 tys. do 5 mln ARR) i jeden mechanizm, jak do niego dojść.
3. **Agent**: narzędzie, które porównuje dwa rejestry państwowe z bazą Przedszkolowo i podrzuca placówki bez profilu. Wynik z filtrami i CSV, na stronie.
4. **Kto to zrobił**: kim jestem, co robię teraz, skąd to umiem.
5. **Porozmawiajmy**: kontakt.

## Dlaczego bez frameworka

Czysty HTML, CSS i JavaScript. Zero zależności, zero kroku budowania, zero `node_modules`,
zero requestów do zewnętrznych domen (fonty i dane jadą z tej samej domeny).

W ogłoszeniu stoi "żadnego AI slopu ani vibecoded shitu", a CEO napisał esej
*Complexity is a death by 1000 cuts*. Next.js z trzystoma pakietami na pięć sekcji
tekstu i jedną tabelę byłby dokładnie tą złożonością, o której pisał.

## Struktura

| Plik | Co robi |
|---|---|
| `index.html` | Pięć sekcji, treść i struktura, bryła inline |
| `styles.css` | Gramatyka wizualna: hard-edge, czerń, biel, jedna szarość |
| `app.js` | Nawigacja: bryła jest bramą, kliknięcie bloku otwiera sekcję |
| `agent.js` | Sekcja 03: filtry, tabela, CSV, leniwe dociąganie pełnego rejestru |
| `data/luka.json` | Wynik agenta: placówki bez profilu na Przedszkolowo (ładowany na start) |
| `data/rejestr.json` | Wynik agenta: cały rejestr z flagą (dociągany po odznaczeniu filtra) |
| `agent/` | Pięć skryptów agenta, opis w `agent/README.md` |
| `shape.svg`, `tools/build_shape.py` | Bryła: spłaszczenie SVG z Book of Shapes, 15 bloków, etykiety, wklejenie do `index.html` |
| `fonts/` | Space Grotesk i Space Mono, `.woff2`, SIL OFL |

## Agent

`agent/` to pięć skryptów bez zależności poza biblioteką standardową Pythona:
RSPO przez publiczne API (przedszkola i punkty, status publiczna/niepubliczna),
Rejestr Żłobków przez publiczną mapę i kartę placówki, profile Przedszkolowo z sitemapy,
dopasowanie po nazwie. Wynik: dwa pliki JSON w `data/`, które strona czyta bez backendu.

Dopasowanie jest po nazwie, nie po adresie. Nazwy powtarzające się w wielu miastach
liczone są jako obecne, więc lista brakujących jest raczej za krótka niż za długa.
Szczegóły i ograniczenia w `agent/README.md` i w sekcji 03 na stronie.

## Bryła

Wzór **Chevron Blocks** z [bookofshapes.com](https://bookofshapes.com), autor Nikolaj Sokolowski.
Licencja pozwala na dowolne użycie i modyfikację bez atrybucji, kopia w `tools/LICENSE-bookofshapes.txt`.
Kredyt jest tu mimo to, bo nie kosztuje nic.

Oryginał miał 1356 zagnieżdżonych grup i 218 kB. `tools/build_shape.py` spłaszcza
transformacje do współrzędnych, grupuje wielokąty w 15 bloków, pięciu z nich nadaje
identyfikatory sekcji i zamienia sztywny `#cccccc` na `currentColor`. Wynik: 85 kB
i struktura, w którą da się kliknąć.

**Bryła jest jedynym wejściem.** Pod nią nie ma nic do przewijania. Kliknięcie bloku
(albo pozycji na liście obok) otwiera dokument ustawiony na wybranej sekcji. Bez JavaScriptu
strona zostaje zwykłą, przewijalną stroną.

## Gramatyka wizualna

Trzy kolory i koniec:

```
--ink    #0a0a0a   czerń
--paper  #f2f2f0   biel łamana
--dim    #6e6e6e   jedna szarość
```

Zero gradientów, zero poświaty, zero rozmycia, zero obrazów rastrowych.

**Space Grotesk** na nagłówki i tekst, **Space Mono** na etykiety. Jedna rodzina, dwa
warianty: mono jest pierwowzorem, grotesk został z niego wyprowadzony. Płaskie zakończenia,
kwadratowe brzuszki i prostokątne kropki są tą samą geometrią co bryła.
