# Agent: luka Przedszkolowo

Trzy skrypty, uruchamiane po kolei. Razem około minuty.

```
python fetch_rspo.py           # rejestr RSPO -> data/rspo.json
python tag_public.py           # status publiczna/niepubliczna -> data/rspo.json
python fetch_przedszkolowo.py  # slugi profili z sitemapy -> data/przedszkolowo_slugs.json
python match.py                # dopasowanie -> ../data/luka.json (czyta go strona)
```

Bez zależności poza biblioteką standardową Pythona.

Źródła: `rspo.gov.pl` (publiczne API rejestru, bez logowania) i `przedszkolowo.pl/sitemap.xml`
(robots.txt: `Allow: /`). Dopasowanie po nazwie, kilka reguł normalizacji, opis w `match.py`.
Nazwy powtarzające się w wielu miastach liczone jako obecne, więc lista brakujących jest
raczej za krótka niż za długa.
