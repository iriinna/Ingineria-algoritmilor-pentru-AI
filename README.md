# Dataset: subiectele de admitere FMI UniBuc (2018–2019)

121 de itemi unici din concursul de admitere la licență, sesiunea iulie 2018 și 2019, Facultatea de Matematică și Informatică, Universitatea din București. Formulele sunt scrise în LaTeX (`$...$`), iar textul păstrează diacriticele.

## Conținut

| Categorie | 2018 | 2019 |
|---|---|---|
| Grile CTI – Matematică | 15 | 15 |
| Grile CTI – Informatică | 15 | 15 |
| Probleme cu rezolvare – Matematică (algebră, analiză, geometrie) | 24 | 30 |
| Probleme cu rezolvare – Informatică (programare) | 4 | 3 |
| **Total** | **58** | **63** |

Problemele cu rezolvare provin de la domeniile Matematică și Informatică; fiecare subpunct (a, b, c…) este un item separat.

## Surse

Paginile de admitere de pe fmi.unibuc.ro trimit la foldere Google Drive cu subiectele și baremele din fiecare an. S-au folosit 18 PDF-uri:
- CTI 2018 și 2019, variantele 1–4, plus baremul CTI 2019;
- domeniile Matematică și Informatică, 2018 și 2019, cu baremele lor.

Enunțurile aparțin FMI-UniBuc și sunt folosite în scop educațional și de cercetare, cu citarea sursei. Setul nu conține date personale.

## Schema unui item

| Câmp | Tip | Descriere |
|---|---|---|
| `id` | string | ex. `FMI_CTI_2019_I_04`, `FMI_INFO_2019_IV_b` (domeniu, an, disciplină sau subiect, număr) |
| `an`, `sesiune`, `data_examen` | int, string, string | anul, `Iulie`, data în format ISO |
| `domeniu_admitere` | string | `Matematică`, `Informatică` sau `Calculatoare și Tehnologia Informației` |
| `disciplina` | string | `Matematică` sau `Informatică` |
| `subiect` | string / null | ex. `II. Analiză` (doar la probleme) |
| `tip_item` | string | `grila` sau `problema` |
| `numar_item` | string | ex. `4` sau `II.c` |
| `context` | string / null | enunțul comun al problemei, sau convențiile de pseudocod de la CTI 2019 |
| `enunt_latex` | string | enunțul itemului |
| `optiuni` | object / null | variantele A–D (doar la grile) |
| `raspuns_corect` | string / null | litera la grile; rezultatul final la probleme; `null` la demonstrații și programe |
| `sursa_raspuns` | string / null | proveniența răspunsului (vezi mai jos) |
| `barem` | string / null | baremul oficial al subpunctului, cu punctajele pașilor |
| `punctaj` | number / null | punctajul subpunctului (fiecare subiect are 9 p + 1 p oficiu) |
| `sursa_pdf`, `sursa_barem` | string / null | fișierele din care provine itemul |

## Prelucrare

1. Textul a fost extras cu `pdftotext`. Paginile cu formule au fost randate ca imagini, iar formulele au fost transcrise în LaTeX.
2. Cele 4 variante CTI conțin aceleași grile, în altă ordine: din 240 de grile (Matematică și Informatică) au rămas 60 unice. Se păstrează varianta 1, iar răspunsurile sunt luate din coloana variantei 1 a baremului.
3. La grilele de Informatică cu cod pe două coloane (C/C++ și Pascal) se păstrează versiunea C/C++.
4. Grilele de Fizică de la CTI nu sunt incluse.

## Limitări

- **Baremul CTI 2018 nu a fost printre sursele descărcate.** Cele 30 de răspunsuri CTI 2018 sunt rezolvate de echipă (unele verificate și prin cod) și marcate în `sursa_raspuns`. Toate celelalte răspunsuri provin din baremele oficiale.
- Transcrierea în LaTeX a fost făcută manual după PDF; pot exista greșeli de transcriere.

## Validare

`python3 build.py dataset.json` reconstruiește setul din fișierele `cti2018.py`, `cti2019.py`, `probleme.py` și verifică:
- JSON Schema pentru fiecare item;
- ID-uri și enunțuri unice;
- grile cu exact 4 variante distincte și răspuns A–D;
- `$` și acolade echilibrate în LaTeX;
- punctajul fiecărui subiect este 9 (+1 oficiu).

Necesită `pip install jsonschema`.
