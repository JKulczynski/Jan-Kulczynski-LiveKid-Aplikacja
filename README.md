# Jan Kulczyński &middot; LiveKid

Aplikacja na rolę **CEO of Agents (AI-Native Product CEO)**.

Zamiast CV: jedna strona, która celuje w biznes LiveKid, a nie w mój życiorys.

## Zasady, według których to powstaje

1. **Zero autopromocji.** Sekcja o mnie jest najkrótsza z całości. Pierwszy ekran nie ma o mnie ani słowa.
2. **Zero oczywistości.** Jeśli Jakub wpadłby na to sam w trzy minuty, wypada.
3. **Wszystko sprawdzalne** na `livekid.com/pl` w kilkanaście sekund.
4. **Prostota jest argumentem**, nie ograniczeniem.
5. **Trzy minuty czytania. Jeden element interaktywny.**

## Dlaczego bez frameworka

Czysty HTML, CSS i JavaScript. Zero zależności, zero kroku budowania, zero `node_modules`.

Powód nie jest lenistwem. W ogłoszeniu stoi "żadnego AI slopu ani vibecoded shitu",
a Jakub napisał esej pod tytułem *Complexity is a death by 1000 cuts*. Next.js
z trzystoma pakietami na pięć sekcji tekstu i jeden filtr byłby dokładnie tą
złożonością, o której pisał.

Całość czyta się w trzech plikach.

## Struktura

| Plik | Co robi |
|---|---|
| `index.html` | Pięć sekcji, treść i struktura |
| `styles.css` | Gramatyka wizualna: hard-edge, czerń, biel, jedna szarość |
| `app.js` | Nawigacja przez bryłę |
| `shape.svg` | Bryła, generowana skryptem z `tools/` |
| `tools/build_shape.py` | Składa bryłę: spłaszcza transformacje, grupuje bloki, dokłada etykiety, wkleja wynik do `index.html` |
| `fonts/` | Space Grotesk i Space Mono, `.woff2`, serwowane z własnej domeny |

## Bryła

Wzór **Chevron Blocks** z [bookofshapes.com](https://bookofshapes.com), autor Nikolaj Sokolowski.
Licencja pozwala na dowolne użycie i modyfikację bez atrybucji, kopia w `tools/LICENSE-bookofshapes.txt`.
Kredyt jest tu mimo to, bo nie kosztuje nic.

Oryginał miał 1356 zagnieżdżonych grup i 218 kB. `tools/build_shape.py` spłaszcza
transformacje do współrzędnych, grupuje wielokąty w 15 bloków, pięciu z nich nadaje
identyfikatory sekcji i zamienia sztywny `#cccccc` na `currentColor`. Wynik: 85 kB
i struktura, w którą da się kliknąć.

**Bryła jest nawigacją.** Pięć bloków prowadzi do pięciu sekcji. Przewijanie działa
normalnie, więc bryła jest skrótem, a nie jedyną drogą. Na telefonie etykiety znikają,
a pod bryłą pojawia się zwykła lista.

## Gramatyka wizualna

**Geometric Hard-Edge.** Trzy kolory i koniec:

```
--ink    #0a0a0a   czerń
--paper  #f2f2f0   biel łamana
--dim    #6e6e6e   jedna szarość
```

Zero gradientów, zero poświaty, zero rozmycia, zero obrazów rastrowych.
Całą robotę wizualną robi kreskowanie bryły.

**Space Grotesk** na nagłówki i tekst, **Space Mono** na etykiety. Jedna rodzina, dwa
warianty: mono jest pierwowzorem, grotesk został z niego wyprowadzony, więc podpis
i nagłówek mają tę samą konstrukcję liter. Płaskie zakończenia, kwadratowe brzuszki
i prostokątne kropki są tą samą geometrią co bryła.

Etykiety przy bryle to podpisy monem na końcu odnośnika, czyli adnotacja rysunku
technicznego. Bryła jest izometrycznym rysunkiem technicznym, więc opisana jest tak,
jak się opisuje rysunek techniczny.

Pliki `.woff2` leżą w `fonts/` (73 kB, cztery podzbiory: latin i latin-ext dla obu
krojów). **Zero requestów do zewnętrznych domen** - font jedzie z tej samej domeny
co reszta. Licencja SIL OFL 1.1, kopia w `fonts/LICENSE-fonts.txt`.

## Stan

- [x] Szkielet, gramatyka wizualna, deploy
- [ ] Treść pięciu sekcji
- [ ] Agent budujący listę pozostałych placówek (dane z RSPO)
- [ ] Element interaktywny w sekcji 3
