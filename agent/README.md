# Agent: luka Przedszkolowo

Pięć skryptów, uruchamiane po kolei. Razem kilka minut (najdłużej trwa dociąganie
kontaktów do brakujących żłobków, ok. 1 000 zapytań z przerwami).

```
python fetch_rspo.py           # RSPO, przedszkola i punkty -> data/rspo.json
python tag_public.py           # status publiczna/niepubliczna (RSPO) -> data/rspo.json
python fetch_zlobki.py         # Rejestr Zlobkow, zlobki i kluby -> data/zlobki.json
python fetch_przedszkolowo.py  # slugi profili z sitemapy -> data/przedszkolowo_slugs.json
python match.py                # dopasowanie + kontakty -> ../data/luka.json (czyta go strona)
```

Bez zależności poza biblioteką standardową Pythona.

Źródła: `rspo.gov.pl` (publiczne API rejestru oświaty), `rejestrzlobkow.mrpips.gov.pl`
(publiczna mapa i karta placówki), `przedszkolowo.pl/sitemap.xml` (robots.txt: `Allow: /`).
Dopasowanie po nazwie, kilka reguł normalizacji, opis w `match.py`. Nazwy powtarzające się
w wielu miastach liczone jako obecne, więc lista brakujących jest raczej za krótka niż za długa.
