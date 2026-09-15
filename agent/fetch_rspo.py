"""Krok 1: pobiera z RSPO wszystkie placówki wychowania przedszkolnego w Polsce.

Źródło: rspo.gov.pl, publiczny rejestr Ministerstwa Edukacji. API bez logowania,
to samo, z którego korzysta wyszukiwarka na stronie rejestru.
Typy: 1 Przedszkole, 81 Punkt przedszkolny, 80 Zespół wychowania przedszkolnego.
Wynik: data/rspo.json (lista słowników, jeden na placówkę).
"""
import io, json, sys, time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://rspo.gov.pl/api/Institution"
UA = "Mozilla/5.0 (agent Jan Kulczynski, kontakt: kulczynski.jan.tomasz@gmail.com)"
TYPES = [1, 81, 80]
PAGE = 500

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    t0 = time.time()
    states = get("https://rspo.gov.pl/api/Dictionary/Teryt/State/")
    out = []
    for st in states:
        body = {"institutionTypeIdList": TYPES, "stateId": st["id"], "includeLiquidated": False}
        offset, total = 0, None
        while True:
            d = post(f"{BASE}?PageSize={PAGE}&PageOffset={offset}", body)
            total = d.get("totalCount", 0)
            items = d.get("items", [])
            for it in items:
                it["_state"] = st["name"].title()
            out.extend(items)
            offset += PAGE
            if not items or offset >= total:
                break
            time.sleep(0.3)
        print(f"{st['name']:<22} {total:>6}")
    with io.open("data/rspo.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False)
    print(f"razem {len(out)} placówek, {time.time()-t0:.0f} s")

if __name__ == "__main__":
    main()
