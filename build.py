"""Construiește dataset.json din fișierele transcrise și îl validează."""
import json, sys
import cti2018, cti2019, probleme

items = []

def grile(mod, cod_an):
    for disc, cod_disc, lista in (("Matematică", "M", mod.MATE), ("Informatică", "I", mod.INFO)):
        for k, (enunt, opt, rasp) in enumerate(lista, 1):
            items.append({
                "id": f"FMI_CTI_{cod_an}_{cod_disc}_{k:02d}",
                "an": mod.META["an"], "sesiune": mod.META["sesiune"], "data_examen": mod.META["data"],
                "domeniu_admitere": mod.META["domeniu_admitere"], "disciplina": disc,
                "subiect": None, "tip_item": "grila", "numar_item": str(k),
                "context": getattr(mod, "CONTEXT_INFO", None) if disc == "Informatică" else None,
                "enunt_latex": enunt,
                "optiuni": dict(zip("ABCD", opt)),
                "raspuns_corect": rasp, "sursa_raspuns": mod.SURSA_RASPUNS,
                "barem": None, "punctaj": None, "sursa_pdf": mod.SRC,
            })

grile(cti2018, 2018)
grile(cti2019, 2019)

for exam in (probleme.MATE_2018, probleme.INFO_2018, probleme.MATE_2019, probleme.INFO_2019):
    cod_dom = "MATE" if exam["domeniu"] == "Matematică" else "INFO"
    for cod, nume, disc, context, subpuncte in exam["subiecte"]:
        for lit, enunt, rasp, barem, pct in subpuncte:
            items.append({
                "id": f"FMI_{cod_dom}_{exam['an']}_{cod}" + ("" if lit == "-" else f"_{lit}"),
                "an": exam["an"], "sesiune": "Iulie", "data_examen": exam["data"],
                "domeniu_admitere": exam["domeniu"], "disciplina": disc,
                "subiect": f"{cod}. {nume}", "tip_item": "problema",
                "numar_item": cod if lit == "-" else f"{cod}.{lit}",
                "context": context, "enunt_latex": enunt, "optiuni": None,
                "raspuns_corect": rasp, "sursa_raspuns": "barem oficial" if rasp else None,
                "barem": barem, "punctaj": pct,
                "sursa_pdf": exam["src"], "sursa_barem": exam["barem_src"],
            })

for it in items:
    it.setdefault("sursa_barem", None)

SCHEMA = {
  "type": "object",
  "required": ["id", "an", "sesiune", "data_examen", "domeniu_admitere", "disciplina", "subiect", "tip_item",
               "numar_item", "context", "enunt_latex", "optiuni", "raspuns_corect", "sursa_raspuns",
               "barem", "punctaj", "sursa_pdf", "sursa_barem"],
  "additionalProperties": False,
  "properties": {
    "id": {"type": "string", "pattern": "^FMI_(CTI|MATE|INFO)_20[0-9]{2}_[A-Z0-9_a-z]+$"},
    "an": {"type": "integer", "minimum": 2000},
    "sesiune": {"enum": ["Iulie", "Septembrie"]},
    "data_examen": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
    "domeniu_admitere": {"enum": ["Matematică", "Informatică", "Calculatoare și Tehnologia Informației"]},
    "disciplina": {"enum": ["Matematică", "Informatică"]},
    "subiect": {"type": ["string", "null"]},
    "tip_item": {"enum": ["grila", "problema"]},
    "numar_item": {"type": "string"},
    "context": {"type": ["string", "null"]},
    "enunt_latex": {"type": "string", "minLength": 10},
    "optiuni": {"oneOf": [{"type": "null"}, {"type": "object", "required": ["A", "B", "C", "D"],
                "additionalProperties": False, "patternProperties": {"^[A-D]$": {"type": "string", "minLength": 1}}}]},
    "raspuns_corect": {"type": ["string", "null"]},
    "sursa_raspuns": {"type": ["string", "null"]},
    "barem": {"type": ["string", "null"]},
    "punctaj": {"type": ["number", "null"]},
    "sursa_pdf": {"type": "string"},
    "sursa_barem": {"type": ["string", "null"]},
  },
}

def checks():
    import jsonschema
    errs = []
    v = jsonschema.Draft7Validator(SCHEMA)
    for it in items:
        errs += [f"{it['id']}: {e.message}" for e in v.iter_errors(it)]
        if it["tip_item"] == "grila":
            if it["raspuns_corect"] not in "ABCD" or len(it["raspuns_corect"]) != 1:
                errs.append(f"{it['id']}: răspuns de grilă invalid")
            if len(set(it["optiuni"].values())) != 4:
                errs.append(f"{it['id']}: opțiuni duplicate")
        else:
            if it["optiuni"] is not None or not it["barem"]:
                errs.append(f"{it['id']}: problemă fără barem sau cu opțiuni")
        for field in ("enunt_latex", "context", "raspuns_corect", "barem"):
            t = it[field] or ""
            if t.count("$") % 2:
                errs.append(f"{it['id']}.{field}: număr impar de $")
            if t.count("{") != t.count("}"):
                errs.append(f"{it['id']}.{field}: acolade neechilibrate")
            if any(ch in t for ch in "ı̂ş0ţ") and "ı" in t:
                errs.append(f"{it['id']}.{field}: diacritice stricate")
    ids = [it["id"] for it in items]
    if len(ids) != len(set(ids)):
        errs.append("ID-uri duplicate")
    enunturi = [(it["context"] or "") + it["enunt_latex"] for it in items]
    if len(enunturi) != len(set(enunturi)):
        errs.append("enunțuri duplicate")
    # punctajul total pe subiect trebuie să fie 9 (+1 oficiu = 10)
    from collections import defaultdict
    tot = defaultdict(float)
    for it in items:
        if it["tip_item"] == "problema":
            tot[(it["domeniu_admitere"], it["an"], it["subiect"])] += it["punctaj"]
    for k, s in tot.items():
        if abs(s - 9) > 1e-9:
            errs.append(f"punctaj subiect {k} = {s}, așteptat 9 (+1 oficiu)")
    return errs

if __name__ == "__main__":
    errs = checks()
    for e in errs:
        print("EROARE:", e)
    with open(sys.argv[1] if len(sys.argv) > 1 else "dataset.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"{len(items)} itemi, {len(errs)} erori")
