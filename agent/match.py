"""Krok 4: dopasowuje rejestry do Przedszkolowo i buduje wynik dla strony.

Dwa rejestry: RSPO (przedszkola, punkty, zespoły) i Rejestr Żłobków (żłobki, kluby dziecięce).
Zasada: placówka jest "obecna", jeśli jej nazwa (po normalizacji, na kilka sposobów)
występuje gdziekolwiek wśród slugów Przedszkolowo. Nazwy powtarzające się w wielu
miastach liczymy jako obecne, bo rozstrzygnięcie po miejscowości wymagałoby pobrania
kilkunastu tysięcy profili. Lista brakujących jest więc raczej za krótka niż za długa.
Dla brakujących żłobków dociągamy szczegóły (mail, www, telefon, podmiot, liczba dzieci i miejsc) z rejestru.
Wynik: ../data/luka.json (czyta go strona, bez backendu).
"""
import io, json, re, sys, time, collections, datetime, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")

PL = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
STOP = {"niepubliczne","niepubliczny","niepubliczna","publiczne","publiczny","publiczna","przedszkole",
        "przedszkola","punkt","przedszkolny","zespol","wychowania","przedszkolnego","w","we","im","nr",
        "samorzadowe","miejskie","miejski","gminne","gminny","integracyjne","specjalne","oddzialami","integracyjnymi",
        "jezykowe","dwujezyczne","sportowe","artystyczne","katolickie","montessori","z","i","o","na",
        "zlobek","zlobki","zlobka","klub","klubik","dzieciecy","dzieciecego","maluszka","maluch","malucha",
        "prywatny","prywatne","prywatna"}
QUOTES = '"„”“'

def toks(s):
    s = s.translate(PL).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return [t for t in s.split() if t not in STOP]
def norm(s): return " ".join(toks(s))
def slug_norm(sl): return norm(re.sub(r"-\d+$", "", sl).replace("-", " "))

UA = "Mozilla/5.0 (agent Jan Kulczynski, kontakt: kulczynski.jan.tomasz@gmail.com)"
def get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

class Matcher:
    def __init__(self, slugs):
        self.full = set(); self.tok_index = collections.defaultdict(set)
        for i, s in enumerate(slugs):
            n = slug_norm(s); self.full.add(n)
            for t in n.split(): self.tok_index[t].add(i)
    def present(self, name, loc):
        n = norm(name)
        if not n: return None
        if n in self.full: return "exact"
        lt = {t[:4] for t in toks(loc) if len(t) >= 4}
        core = [t for t in n.split() if t[:4] not in lt]
        if core and " ".join(core) in self.full: return "no-locality"
        q = re.findall("[" + QUOTES + "]([^" + QUOTES + "]{3,})[" + QUOTES + "]", name)
        if q:
            qn = norm(q[0])
            if qn and qn in self.full: return "quoted"
        core_set = {t for t in core if not t.isdigit()}
        if len(core_set) >= 2:
            cand = None
            for t in core_set:
                cand = self.tok_index.get(t, set()) if cand is None else cand & self.tok_index.get(t, set())
                if not cand: break
            if cand: return "contains"
        return None

def main():
    t0 = time.time()
    rspo = json.load(io.open("data/rspo.json", encoding="utf-8"))
    zlob = json.load(io.open("data/zlobki.json", encoding="utf-8"))
    slugs = json.load(io.open("data/przedszkolowo_slugs.json", encoding="utf-8"))
    M = Matcher(slugs)
    rows, how = [], collections.Counter()
    def fresh():
        return {"rspo": 0, "nonpublic": 0, "on_pz": 0, "missing": 0, "missing_nonpublic": 0,
                "z_rspo": 0, "z_on_pz": 0, "z_missing": 0, "z_missing_nonpublic": 0}
    stats = collections.defaultdict(fresh)

    # przedszkola (RSPO)
    for x in rspo:
        st = x["_state"]; s = stats[st]; s["rspo"] += 1
        if not x["_public"]: s["nonpublic"] += 1
        loc = (x.get("hqAddressLocality") or {}).get("name", "")
        p = M.present(x["name"], loc); how["p:" + str(p)] += 1
        if p:
            s["on_pz"] += 1; continue
        s["missing"] += 1
        if not x["_public"]: s["missing_nonpublic"] += 1
        addr = " ".join(v for v in [x.get("hqAddressStreet", ""), x.get("hqAddressBuildingNr", "")] if v).strip()
        rows.append({"kat": "przedszkole", "n": x["name"].strip(), "t": x["type"]["name"], "w": st, "m": loc,
                     "a": addr, "k": x.get("hqAddressZipCode", ""), "p": bool(x["_public"]), "d": x.get("studentsNr"),
                     "www": (x.get("website") or "").strip(), "tel": (x.get("telephone") or "").strip(),
                     "mail": (x.get("email") or "").strip(), "id": str(x.get("rspo")),
                     "org": ((x.get("leadAuthorities") or [{}])[0].get("name", "")).strip()})

    # zlobki i kluby dzieciece (Rejestr Zlobkow)
    missing_z = []
    for x in zlob:
        st = x["_state"]; s = stats[st]; s["z_rspo"] += 1
        adres = x.get("adres") or ""; loc = adres.split(",")[0].strip()
        p = M.present(x.get("nazwa") or "", loc); how["z:" + str(p)] += 1
        if p:
            s["z_on_pz"] += 1; continue
        s["z_missing"] += 1; missing_z.append(x)
    print(f"żłobki i kluby bez profilu: {len(missing_z)}, dociągam szczegóły...")
    PUBLIC_TYPES = {"GMINA", "POWIAT", "INSTYTUCJA_PUBLICZNA"}
    for i, x in enumerate(missing_z):
        det = {}
        try:
            det = get_json("https://rejestrzlobkow.mrpips.gov.pl/instytucja/public/getByIdentyfikator?"
                           + urllib.parse.urlencode({"formaOpieki": x["typRejestru"], "identyfikator": x["identyfikator"]}))
        except Exception:
            how["z:detail-error"] += 1
        da = det.get("daneAdresowe") or {}
        pod = det.get("podmiot") or {}
        public = (pod.get("rodzajPodmiotu") or "") in PUBLIC_TYPES
        st = x["_state"]; s = stats[st]
        if not public: s["z_missing_nonpublic"] += 1
        parts = [p.strip() for p in (x.get("adres") or "").split(",")]
        loc = parts[0] if parts else ""
        street = " ".join(v for v in [(da.get("ulica") or {}).get("nazwa", ""), da.get("numerBudynku") or ""] if v).strip()
        if not street and len(parts) >= 3: street = ", ".join(parts[2:])
        rows.append({"kat": "zlobek", "n": (x.get("nazwa") or "").strip(),
                     "t": "Żłobek" if x["typRejestru"] == "ZLOBEK" else "Klub dziecięcy", "w": st, "m": loc,
                     "a": street, "k": da.get("kodPocztowy") or "", "p": public, "d": det.get("liczbaDzieci"),
                     "miejsca": det.get("liczbaMiejsc"),
                     "www": (det.get("adresWWW") or "").strip(), "tel": (det.get("telefon") or "").strip(),
                     "mail": (det.get("email") or "").strip(), "id": x["identyfikator"],
                     "org": (pod.get("nazwa") or "").strip()})
        if i % 25 == 0: time.sleep(0.5)
        if i % 200 == 0: print(f"  {i}/{len(missing_z)}")

    rows.sort(key=lambda r: (r["kat"], r["w"], r["m"], r["n"]))
    result = {
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source_rspo": len(rspo), "source_zlobki": len(zlob), "source_pz": len(slugs),
        "matched": sum(v for k, v in how.items() if not k.endswith("None") and "error" not in k),
        "missing": sum(1 for r in rows if r["kat"] == "przedszkole"),
        "missing_z": sum(1 for r in rows if r["kat"] == "zlobek"),
        "how": dict(how), "states": dict(sorted(stats.items())), "rows": rows,
        "duration_s": round(time.time() - t0, 1),
    }
    json.dump(result, io.open("../data/luka.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("dopasowania:", dict(how))
    nz = sum(1 for r in rows if r["kat"] == "zlobek" and not r["p"])
    print(f"przedszkola bez profilu {result['missing']} | żłobki i kluby bez profilu {result['missing_z']} (niepubliczne {nz}) | {result['duration_s']} s")
    import os; print("luka.json:", os.path.getsize("../data/luka.json") // 1024, "kB")

if __name__ == "__main__":
    main()
