"""Krok 3: dokłada do każdej placówki z RSPO status publiczna/niepubliczna.

RSPO nie zwraca statusu w wynikach, ale przyjmuje go jako filtr (publicStatusIdList,
1 = publiczna). Pobieramy więc same publiczne per województwo i oznaczamy resztę.
"""
import io, json, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://rspo.gov.pl/api/Institution"
UA = "Mozilla/5.0 (agent Jan Kulczynski, kontakt: kulczynski.jan.tomasz@gmail.com)"
def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode("utf-8"))
def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode("utf-8"))

rspo = json.load(io.open("data/rspo.json", encoding="utf-8"))
public = set()
for st in get("https://rspo.gov.pl/api/Dictionary/Teryt/State/"):
    body = {"institutionTypeIdList": [1, 81, 80], "stateId": st["id"], "includeLiquidated": False, "publicStatusIdList": [1]}
    off = 0
    while True:
        d = post(f"{BASE}?PageSize=500&PageOffset={off}", body)
        for it in d.get("items", []): public.add(it["id"])
        off += 500
        if off >= d.get("totalCount", 0): break
        time.sleep(0.2)
for x in rspo: x["_public"] = x["id"] in public
json.dump(rspo, io.open("data/rspo.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"publiczne {len(public)}, niepubliczne {len(rspo)-len(public)}")
