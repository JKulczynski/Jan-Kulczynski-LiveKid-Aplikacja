"""Krok 1b: pobiera Rejestr Żłobków i Klubów Dziecięcych (ministerstwo rodziny).

Źródło: rejestrzlobkow.mrpips.gov.pl, publiczna mapa rejestru. `map/getInstytucje` zwraca
cały kraj jednym plikiem (identyfikator, typ, nazwa, adres, współrzędne). Dziennych
opiekunów pomijamy (osoby, nie placówki). Szczegóły (mail, www, telefon, podmiot)
są pod `instytucja/public/getByIdentyfikator`, pobierane w kroku match.py tylko
dla placówek, których nie ma na Przedszkolowo.
Wynik: data/zlobki.json
"""
import io, json, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
API = "https://rejestrzlobkow.mrpips.gov.pl"
UA = "Mozilla/5.0 (agent Jan Kulczynski, kontakt: kulczynski.jan.tomasz@gmail.com)"
WOJ = {1:"Dolnośląskie",2:"Kujawsko-Pomorskie",3:"Lubelskie",4:"Lubuskie",5:"Łódzkie",6:"Małopolskie",7:"Mazowieckie",8:"Opolskie",9:"Podkarpackie",10:"Podlaskie",11:"Pomorskie",12:"Śląskie",13:"Świętokrzyskie",14:"Warmińsko-Mazurskie",15:"Wielkopolskie",16:"Zachodniopomorskie"}

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read().decode("utf-8"))

def main():
    t0 = time.time()
    raw = get(f"{API}/map/getInstytucje")
    out = [x for x in raw if x.get("typRejestru") in ("ZLOBEK", "KLUB_DZIECIECY")]
    for x in out: x["_state"] = WOJ.get(x.get("nrWoj"), "")
    json.dump(out, io.open("data/zlobki.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(f"rejestr: {len(raw)} wpisów, placówek (żłobki + kluby): {len(out)}, {time.time()-t0:.0f} s")

if __name__ == "__main__":
    main()
