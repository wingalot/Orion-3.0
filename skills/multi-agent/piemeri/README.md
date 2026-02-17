# Multi-Agent Piemēri

Šajā mapē atrodas praktiski piemēri dažādiem multi-agent lietošanas scenārijiem.

## Piemēru saraksts

### 1. Research Pipeline (`research-pipeline.md`)
Pētniecības uzdevumu sadalījums vairākos posmos.
- Piemērs: Jaunas tehnoloģijas izpēte
- Fāzes: Meklēšana → Analīze → Kopsavilkums

### 2. Code Review Team (`code-review-team.md`)
Paralēla koda pārskatīšana ar vairākiem speciālistiem.
- Drošības audits
- Veiktspējas analīze
- Stila pārbaude

### 3. Documentation Generator (`doc-generator.md`)
Automātiska dokumentācijas ģenerēšana.
- API dokumentācija
- README atjaunināšana
- Koda komentāri

### 4. Data Processing (`data-processing.md`)
Lielu datu apstrādes uzdevumu sadalīšana.
- CSV apstrāde
- Datu migrācija
- ETL procesi

### 5. Full Stack Feature (`full-stack-feature.md`)
Pilna funkcionalitātes implementācija.
- Backend API
- Frontend komponenti
- Testi

---

## Kā izmantot šos piemērus

Katrs piemērs ir gatavs izpildei. Kopē komandas un pielāgo savam gadījumam.

### Vispārīgā struktūra:

```javascript
// 1. Izveido aģentus
sessions_spawn(task="...", label="...")

// 2. Seko līdzi
subagents list

// 3. Vadīt ja nepieciešams
subagents steer target="..." message="..."

// 4. Pabeidz
subagents kill target="..."
```
