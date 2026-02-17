# Multi-Agent Coordinator

## Ko šis skills dara

Šis skills nodrošina pilnvērtīgu multi-aģentu koordinācijas sistēmu OpenClaw vidē. Tas ļauj:

- **Izveidot sub-aģentus** (`sessions_spawn`) - specifiskiem uzdevumiem ar izolētām sesijām
- **Pārvaldīt aktīvās sesijas** (`sessions_list`, `subagents list`) - redzēt visus aktīvos aģentus
- **Sūtīt komandas** sub-aģentiem (`subagents steer`) - vadīt aģentus pēc izveidošanas
- **Pārtraukt aģentus** (`subagents kill`) - droši izslēgt neaktīvus vai aizķērušos aģentus
- **Koordinēt kompleksus uzdevumus** - sadalīt lielus uzdevumus mazākos, paralēlos darbos

Šis ir **konfigurācijas un rīku kopums**, nevis parastā "prasme" - tas izmanto OpenClaw iebūvēto multi-aģentu arhitektūru.

---

## Kad izmantot multi-agent sistēmu

### Ieteicams izmantot, kad:

| Scenārijs | Kāpēc multi-agent? |
|-----------|-------------------|
| **Zinātniskā pētniecība** | Viens aģents meklē avotus, cits analizē, trešais apkopo |
| **Liela koda bāze** | Viens aģents analizē, cits raksta testus, trešais dokumentē |
| **Paralēli uzdevumi** | Vairāki neatkarīgi uzdevumi, kas var notikt vienlaikus |
| **Izolēta darba vide** | Bīstamas operācijas sandboxā, galvenais aģents - drošs |
| **Ilgstoši uzdevumi** | Uzdevumi, kas var aizņemt >10 minūtes - neatkarīgās sesijās |
| **Kompleksa problēmu risināšana** | Dažādi aģenti ar dažādām kompetencēm |

### Kad **NEIZMANTOT** multi-agent:

- Vienkāršiem, ātriem uzdevumiem (< 2 minūtes)
- Kad vajag tūlītēju atbildi
- Kad uzdevums ir secīgs un nevar dalīt
- Kad resursi (API kvotas) ir ierobežoti

### Multi-Agent vs Cron:

| | **Sub-aģents** | **Cron** |
|---|----------------|----------|
| **Laiks** | "Tagad" vai "Tūlīt" | "Katru dienu 9:00" vai "Pēc 30 min" |
| **Mērķis** | Kompleksi, sadalāmi uzdevumi | Periodiski, atgādinājumi |
| **Dzīves ilgums** | Kamēr uzdevums nav pabeigts | Vienreizējs vai atkārtojošs |
| **Interakcija** | Var sazināties ar galveno aģentu | Parasti neatkarīgs |

**Noteikums:**
- Vajag **sadalis uzdevumu** → `sessions_spawn`
- Vajag **atkārtot katru dienu** → `cron`
- Vajag **atgādināt pēc 20 min** → `cron`

---

## Kā to izmantot

### 1. Pamata sub-aģenta izveide

```javascript
// Vienkāršākais veids
sessions_spawn(task="Izveido React komponentu pogai")
```

```javascript
// Ar pielāgotu modeli un etiķeti
sessions_spawn(
  task="Izveido datubāzes migrāciju lietotāju tabulai",
  label="db-migrator",
  model="anthropic/claude-sonnet-4-5"
)
```

### 2. Sub-aģenta vadīšana

Pēc izveidošanas vari sūtīt komandas:

```javascript
// Apskati visus sub-aģentus
subagents list

// Sūti komandu konkrētam aģentam
subagents steer target="db-migrator" message="Pievieno arī indeksu e-pasta laukam"

// Pārtrauc aģentu, ja nepieciešams
subagents kill target="db-migrator"
```

### 3. Kompleksa uzdevuma sadalīšana

```javascript
// 1. Izsaki pētniecības uzdevumu
sessions_spawn(
  task="Izpēti React 18 jaunās funkcijas un sagatavo kopsavilkumu",
  label="react-research"
)

// 2. Izsaki implementācijas uzdevumu (var sākt pēc pētniecības)
sessions_spawn(
  task="Izveido Next.js projektu ar TypeScript",
  label="setup-project"
)

// 3. Seko līdzi abiem
subagents list
```

---

## sessions_spawn parametri

| Parametrs | Tips | Obligāts | Apraksts |
|-----------|------|----------|----------|
| `task` | string | ✅ Jā | Detalizēts uzdevuma apraksts sub-aģentam |
| `label` | string | ❌ Nē | Viegli atpazīstams nosaukums (piem., "researcher", "coder") |
| `model` | string | ❌ Nē | LLM modelis (noklusējums: kā galvenajam aģentam) |

### Ieteicamie modeļi:

| Modelis | Kad izmantot |
|---------|--------------|
| `anthropic/claude-opus-4-6` | Kompleksa kodēšana, arhitektūra |
| `anthropic/claude-sonnet-4-5` | ātra kodēšana, ikdienas uzdevumi |
| `openai/gpt-4o` | Daudzveidīgi uzdevumi |
| `google/gemini-2.5-pro` | Lielu kontekstu apstrāde |

---

## Praktiski lietošanas piemēri

### Piemērs 1: Web lapas analīze un atskaite

```javascript
// Izveido pētniecības aģentu
sessions_spawn(
  task="Izpēti https://example.com un analizē: 1) UX dizainu, 2) Ielādes ātrumu, 3) SEO. Sagatavo detalizētu atskaiti.",
  label="site-analyzer",
  model="anthropic/claude-sonnet-4-5"
)

// Pēc laika pārbaudi rezultātus
subagents list

// Ja nepieciešams - papildu instrukcijas
subagents steer target="site-analyzer" message="Pievieno arī mobilo responsivitātes novērtējumu"
```

### Piemērs 2: Paralēla koda pārskatīšana

```javascript
// Aģents 1: Drošības audit
sessions_spawn(
  task="Pārskati /home/oreo/.openclaw/workspace/project/src/auth.js un meklē drošības ievainojamības",
  label="security-auditor"
)

// Aģents 2: Veiktspējas optimizācija
sessions_spawn(
  task="Pārskati /home/oreo/.openclaw/workspace/project/src/database.js un meklē veiktspējas uzlabojumus",
  label="performance-auditor"
)

// Aģents 3: Koda stils
sessions_spawn(
  task="Pārskati /home/oreo/.openclaw/workspace/project/src/utils.js un pārbaudi koda stilu atbilstoši ESLint noteikumiem",
  label="style-checker"
)

// Seko līdzi visiem
subagents list
```

### Piemērs 3: Dokumentācijas ģenerēšana

```javascript
// 1. Analizē koda bāzi
sessions_spawn(
  task="Analizē /home/oreo/.openclaw/workspace/project/src mapi un izveido API dokumentāciju visām publiskajām funkcijām",
  label="doc-writer"
)

// 2. Izveido README
sessions_spawn(
  task="Izveido README.md projektam balstoties uz package.json un src struktūru",
  label="readme-creator"
)
```

### Piemērs 4: Datu apstrāde

```javascript
// Liela CSV apstrāde sadalīta daļās
sessions_spawn(
  task="Apstrādā /home/oreo/.openclaw/workspace/data/customers_part1.csv - attīri, validē e-pastus, eksportē uz JSON",
  label="data-processor-1"
)

sessions_spawn(
  task="Apstrādā /home/oreo/.openclaw/workspace/data/customers_part2.csv - attīri, validē e-pastus, eksportē uz JSON",
  label="data-processor-2"
)

// Vēlāk apvieno rezultātus
subagents steer target="data-processor-1" message="Saglabā rezultātus kā customers_clean_1.json"
```

---

## Tipiskas kļūdas un to novēršana

### Kļūda 1: "Sub-aģents neatbild"

**Simptomi:**
```
subagents list rāda aģentu, bet nav rezultātu
```

**Iemesli:**
- Uzdevums ir pārāk sarežģīts vai pārāk vienkāršs
- API kvota ir izsmelta
- Tīkla problēmas

**Risinājumi:**
```javascript
// 1. Pārbaudi aģenta statusu
subagents list

// 2. Ja "stuck", nosūti atgādinājumu
subagents steer target="aģenta-label" message="Vai esi pabeidzis? Ja nē, kādi ir bloki?"

// 3. Ja nekas nenotiek 5+ minūtes, pārtrauc un mēģini vēlreiz
subagents kill target="aģenta-label"
```

### Kļūda 2: "sessions_spawn nav atrodams"

**Simptomi:**
```
Tool not found: sessions_spawn
```

**Iemesls:**
Rīks nav iespējots `openclaw.json` konfigurācijā.

**Risinājums:**
```json
// ~/.openclaw/openclaw.json
{
  "tools": {
    "allow": ["sessions_spawn", "sessions_list", "subagents"]
  }
}
```

### Kļūda 3: "Pārāk daudz vienlaicīgu aģentu"

**Simptomi:**
- Lēna atbilde
- API kļūdas

**Iemesls:**
Resursu ierobežojumi (kvotas, atmiņa).

**Risinājums:**
```javascript
// Ierobežo vienlaicīgos aģentus (maksimums 3-5)
// Secīgi, nevis paralēli

sessions_spawn(task="Uzdevums 1", label="task-1")
// Gaidi līdz pabeidz...

sessions_spawn(task="Uzdevums 2", label="task-2")
```

### Kļūda 4: "Sub-aģents dara nepareizas lietas"

**Iemesls:**
Uzdevums nav pietiekami detalizēts.

**Risinājums:**
```javascript
// ❌ Slikti
sessions_spawn(task="Izveido API")

// ✅ Labi
sessions_spawn(
  task="Izveido REST API ar Express.js: 1) GET /users - atgriež visus lietotājus, 2) POST /users - izveido jaunu, 3) Izmanto SQLite datubāzi, 4) Pievieno input validāciju"
)
```

---

## Komandas kopsavilkums

| Komanda | Mērķis | Piemērs |
|---------|--------|---------|
| `sessions_spawn` | Izveidot jaunu sub-aģentu | `sessions_spawn(task="...", label="...")` |
| `sessions_list` | Redzēt visas sesijas | `sessions_list()` |
| `subagents list` | Redzēt sub-aģentus | `subagents list` |
| `subagents steer` | Komandēt aģentam | `subagents steer target="..." message="..."` |
| `subagents kill` | Pārtraukt aģentu | `subagents kill target="..."` |

---

## Papildu resursi

- [Oficiālā dokumentācija](https://docs.openclaw.ai/concepts/multi-agent)
- [Multi-Agent Sandbox & Tools](https://docs.openclaw.ai/tools/multi-agent-sandbox-tools)
- Instrukcijas: `skills/multi-agent/instrukcijas/multi-agent_instrukcija.md`

---

## Versija un atjauninājumi

- **Versija:** 2.0.0
- **Pēdējais atjauninājums:** 2025-02-17
- **Izmaiņas:** Pilnībā pārrakstīts, pievienoti praktiski piemēri, kļūdu apstrāde
