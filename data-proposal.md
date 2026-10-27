# 1. De ce acest dataset?
**La ce e bun si cine l-ar folosi?**
Datasetul poate fi folositor pentru antrenarea si evaluarea modelelor de limbaj pe sarcini de rationament matematic si algoritmic in limba romana. Ar putea fi folosit de dezvoltatori de platforme educationale, dar si de profesori sau elevi care cauta o exemple structurate de teste grila si probleme.

**Ce aduce in plus fata de ce exista deja / De ce nu ajunge unul existent?**
In prezent, subiectele sunt publicate doar sub forma de fisiere PDF, fapt care duce la dificultatea de a extrage automat formulele matematice sau secventele de cod fara greseli sau distorsionari. Dataset-ul acesta va oferi o forma curata si bine structurate, formule fiind reprezentate in format LaTeX, structurate pe itemi individuali. De asemenea, in momentul de fata nu exista un set de date similar, complet structurat, dedicat admiterii la aceasta facultate.

## 2. Surse
* **Link:** Site-ul oficial al facultatii (https://fmi.unibuc.ro/admitere-licenta-iulie-2025/ - sectiunea informatii generale).
* **Licenta:** Materialele sunt materiale educationale oficiale facute publice pentru informare. Nu este necesara nicio licenta pentru obtinerea acestor informatii.
* **Dimensiune aproximativa:** Aproximativ 500 de probleme/grile unice, rezultand intr-un fisier JSON de aproximativ 2-5 MB.

## 3. Date sensibile
* **Contin datele informatii personale?**
Datasetul contine strict enunturi de matematica si informatica, optiuni de raspuns si bareme oficiale de notare. Nu exista nicio informatie personala legata de candidati anteriori sau alte persoane.
* **Management**
Datele extrase(fisiere de tip JSON) vor putea fi publicate complet pe GitHub. PDF-urile brute folosite la extragere pot fi pastrate local.

## 4. Schema
Datele vor fi salvate in format JSON. Schema propusa este urmatoarea:

**Schema:**
```json
{
  "id": "string",
  "disciplina": "string",
  "an": "integer",
  "sesiune": "string",
  "tip_item": "string",
  "enunt_latex": "string",
  "optiuni": "dict",
  "raspuns_corect": "string",
  "barem": "string"
}
```
