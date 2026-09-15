"""Krok 4: dopasowuje rejestr do Przedszkolowo i buduje wynik dla strony.

Zasada: placówka jest "obecna", jeśli jej nazwa (po normalizacji, na kilka sposobów)
występuje gdziekolwiek wśród slugów Przedszkolowo. Nazwy powtarzające się w wielu
miastach liczymy jako obecne, bo rozstrzygnięcie po miejscowości wymagałoby pobrania
kilkunastu tysięcy profili. Lista brakujących jest więc raczej za krótka niż za długa.
Wynik: ../data/luka.json (czyta go strona, bez backendu).
"""
import io, json, re, sys, time, collections, datetime
sys.stdout.reconfigure(encoding="utf-8")

PL = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
STOP = {"niepubliczne","niepubliczny","niepubliczna","publiczne","publiczny","publiczna","przedszkole",
        "przedszkola","punkt","przedszkolny","zespol","wychowania","przedszkolnego","w","we","im","nr",
        "samorzadowe","miejskie","gminne","integracyjne","specjalne","oddzialami","integracyjnymi",
        "jezykowe","dwujezyczne","sportowe","artystyczne","katolickie","montessori","z","i","o","na"}
def toks(s):
    s = s.translate(PL).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return [t for t in s.split() if t not in STOP]
def norm(s): return " ".join(toks(s))
def slug_norm(sl): return norm(re.sub(r"-\d+$", "", sl).replace("-", " "))

def main():
    t0 = time.time()
    rspo = json.load(io.open("data/rspo.json", encoding="utf-8"))
    slugs = json.load(io.open("data/przedszkolowo_slugs.json", encoding="utf-8"))
    slug_full = set()
    slug_tokens = []
    for s in slugs:
        n = slug_norm(s); slug_full.add(n); slug_tokens.append(set(n.split()))
    # indeks: token -> zbiory slugow (do reguly zawierania)
    tok_index = collections.defaultdict(set)
    for i, ts in enumerate(slug_tokens):
        for t in ts: tok_index[t].add(i)

    def present(x):
        name = x["name"]; loc = (x.get("hqAddressLocality") or {}).get("name", "")
        n = norm(name)
        if not n: return None
        if n in slug_full: return "exact"
        # bez slow wygladajacych na miejscowosc (wspolny 4-literowy prefiks z nazwa miejscowosci)
        lt = {t[:4] for t in toks(loc) if len(t) >= 4}
        core = [t for t in n.split() if t[:4] not in lt]
        if core and " ".join(core) in slug_full: return "no-locality"
        # nazwa w cudzyslowie
        q = re.findall(r'["„”“]([^"„”“]{3,})["„”“]', name)
        if q:
            qn = norm(q[0])
            if qn and qn in slug_full: return "quoted"
        # zawieranie: wszystkie tokeny rdzenia (min. 2, nie same liczby) w jednym slugu
        core_set = {t for t in core if not t.isdigit()}
        if len(core_set) >= 2:
            cand = None
            for t in core_set:
                cand = tok_index.get(t, set()) if cand is None else cand & tok_index.get(t, set())
                if not cand: break
            if cand: return "contains"
        return None

    out_missing = []
    stats = collections.defaultdict(lambda: {"rspo": 0, "nonpublic": 0, "on_pz": 0, "missing": 0, "missing_nonpublic": 0})
    how = collections.Counter()
    for x in rspo:
        st = x["_state"]; s = stats[st]; s["rspo"] += 1
        if not x["_public"]: s["nonpublic"] += 1
        p = present(x); how[p] += 1
        if p:
            s["on_pz"] += 1
        else:
            s["missing"] += 1
            if not x["_public"]: s["missing_nonpublic"] += 1
            addr = " ".join(v for v in [x.get("hqAddressStreet",""), x.get("hqAddressBuildingNr","")] if v).strip()
            out_missing.append({
                "n": x["name"].strip(), "t": x["type"]["name"], "w": st,
                "m": (x.get("hqAddressLocality") or {}).get("name",""),
                "a": addr, "k": x.get("hqAddressZipCode",""),
                "p": bool(x["_public"]), "d": x.get("studentsNr"),
                "www": (x.get("website") or "").strip(), "tel": (x.get("telephone") or "").strip(),
                "mail": (x.get("email") or "").strip(), "rspo": x.get("rspo"),
                "org": ((x.get("leadAuthorities") or [{}])[0].get("name","")).strip(),
            })
    out_missing.sort(key=lambda r: (r["w"], r["m"], r["n"]))
    result = {
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source_rspo": len(rspo), "source_pz": len(slugs),
        "matched": sum(v for k, v in how.items() if k), "missing": how[None],
        "how": dict(how), "states": dict(sorted(stats.items())), "rows": out_missing,
        "duration_s": round(time.time() - t0, 1),
    }
    json.dump(result, io.open("../data/luka.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("dopasowania:", dict(how))
    print(f"brakuje {how[None]} (w tym niepublicznych {sum(1 for r in out_missing if not r['p'])})")
    for k, v in sorted(stats.items()): print(f"  {k:<22} rejestr {v['rspo']:>5}  niepubl {v['nonpublic']:>5}  na PZ {v['on_pz']:>5}  brak {v['missing']:>5}  brak niepubl {v['missing_nonpublic']:>4}")
    import os; print("luka.json:", os.path.getsize("../data/luka.json")//1024, "kB")

if __name__ == "__main__":
    main()
