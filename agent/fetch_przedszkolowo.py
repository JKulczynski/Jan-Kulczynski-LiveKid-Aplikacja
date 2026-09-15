"""Krok 2: pobiera listę profili placówek z Przedszkolowo (sitemapy).

Źródło: przedszkolowo.pl/sitemap.xml (robots.txt: Allow /). 32 pliki po 1000 adresów.
Z adresu /placowka/<slug> bierzemy slug; nazwa jest w slugu, miejscowości nie ma.
Wynik: data/przedszkolowo_slugs.json (lista slugów).
"""
import io, json, re, sys, time
import urllib.request
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (agent Jan Kulczynski, kontakt: kulczynski.jan.tomasz@gmail.com)"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")

def main():
    t0 = time.time()
    idx = ET.fromstring(get("https://przedszkolowo.pl/sitemap.xml"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    parts = [l.text for l in idx.findall(".//s:loc", ns) if "/sitemaps/facilities/" in l.text]
    slugs = []
    for u in parts:
        x = ET.fromstring(get(u))
        for l in x.findall(".//s:loc", ns):
            m = re.search(r"/placowka/([^/?#]+)$", l.text)
            if m: slugs.append(m.group(1))
        time.sleep(0.2)
    slugs = sorted(set(slugs))
    with io.open("data/przedszkolowo_slugs.json", "w", encoding="utf-8") as fh:
        json.dump(slugs, fh, ensure_ascii=False)
    print(f"{len(parts)} sitemap, {len(slugs)} unikalnych slugów, {time.time()-t0:.0f} s")

if __name__ == "__main__":
    main()
