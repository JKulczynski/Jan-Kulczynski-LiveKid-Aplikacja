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
| `styles.css` | Gramatyka wizualna: ciemność, jedno zimne źródło światła, złamana biel |
| `app.js` | Element interaktywny (jeszcze nie ma) |

## Gramatyka wizualna

Trzy kolory i koniec:

```
--ground     #06080d   prawie czerń z niebieskim odcieniem
--light      #8fb8e8   jedyne źródło światła, zimne
--text       #e4e7ec   złamana biel
```

Bez gradientów dekoracyjnych, bez stocków, bez ozdobników. Hero to jedno źródło
światła i wiązki zbiegające się w jednym punkcie, zrobione czystym SVG.

Typografia systemowa, żeby nie ładować webfontów. Zero requestów do zewnętrznych domen.

## Stan

- [x] Szkielet, gramatyka wizualna, deploy
- [ ] Treść pięciu sekcji
- [ ] Agent budujący listę pozostałych placówek (dane z RSPO)
- [ ] Element interaktywny w sekcji 3
