# Multi-Agent Sistēmas Pamācība

## Saturs

1. [Ievads](#ievads)
2. [Pamata koncepti](#pamata-koncepti)
3. [Iestatīšana](#iestatīšana)
4. [Pirmie soļi](#pirmie-soļi)
5. [Praktiski scenāriji](#praktiski-scenāriji)
6. [Padomi un triki](#padomi-un-triki)
7. [Problēmu risināšana](#problēmu-risināšana)

---

## Ievads

Multi-agent sistēma ļauj vienam "galvenajam" aģentam izveidot vairākus "sub-aģentus", katrs ar savu uzdevumu un izolētu darba vidi. Tas ir kā projektu vadītājs, kurš sadala darbu komandai.

### Priekšrocības

- **Paralēlizācija** - vairāki uzdevumi vienlaikus
- **Izolācija** - katra sesija ir atsevišķa (drošība)
- **Fokuss** - katrs aģents dara vienu lietu
- **Mērogojamība** - var sadalīt lielus projektus

### Trūkumi

- Resursu patēriņš (API kvotas)
- Komunikācijas sarežģītība
- Nav piemērots vienkāršiem uzdevumiem

---

## Pamata koncepti

### Kas ir sub-aģents?

Sub-aģents ir **jauna, neatkarīga OpenClaw sesija**, kas:
- Dara vienu konkrētu uzdevumu
- Ir izolēta no galvenā aģenta
- Var palaista paralēli ar citiem
- Automātiski paziņo, kad pabeigts

### Kā tas darbojas?

```
┌─────────────────────────────────────┐
│         Tavs galvenais aģents       │
│         (Tu runā ar mani)           │
└──────────────┬──────────────────────┘
               │ sessions_spawn()
               ▼
    ┌─────────────────────┐
    │   Sub-aģents #1     │◄──── task="Pētniecība"
    │   (researcher)      │
    └─────────────────────┘
               │
               │ sessions_spawn()
               ▼
    ┌─────────────────────┐
    │   Sub-aģents #2     │◄──── task="Kodēšana"
    │   (coder)           │
    └─────────────────────┘
               │
               │ (automatiski)
               ▼
        Rezultāts atgriežas
        galvenajam aģentam
```

---

## Iestatīšana

### 1. Pārbaudi vai rīki ir pieejami

```javascript
// Pārbaudi vai vari izveidot sub-aģentu
sessions_spawn(task="Saki 'Čau!'", label="test")

// Pēc tam pārbaudi sarakstu
subagents list
```

### 2. Konfigurācija (ja nepieciešams)

Ja rīki nav pieejami, pievieno `openclaw.json`:

```json
{
  "tools": {
    "allow": [
      "sessions_spawn",
      "sessions_list", 
      "subagents"
    ]
  }
}
```

### 3. Pārbaudi piekļuvi

```bash
openclaw tools list | grep -E "(spawn|subagent)"
```

---

## Pirmie soļi

### Soļi 1-2-3: Tavs pirmais multi-agent uzdevums

#### 1. Izveido pētniecības aģentu

```javascript
sessions_spawn(
  task="Izpēti Node.js drošības best practices 2025. gadā. Atsaucies uz OWASP un oficiālo dokumentāciju.",
  label="security-research"
)
```

**Kas notiek:**
- Tiek izveidota jauna sesija `security-research`
- Aģents sāk strādāt uzdevumā
- Tu vari turpināt darīt citas lietas

#### 2. Seko līdzi progresam

```javascript
// Pārbaudi vai aģents strādā
subagents list

// Rezultāts:
// ┌─────────────────────────────────────┐
// │ security-research    │ running      │
// └─────────────────────────────────────┘
```

#### 3. Saņem rezultātu

Kad aģents pabeidz, rezultāts automātiski parādās.

---

## Praktiski scenāriji

### Scenārijs A: Research → Analysis → Report

```javascript
// Fāze 1: Pētniecība
sessions_spawn(
  task="Sameklē 5 populārākās React form bibliotēkas 2025. gadā. Katrai atrodi: GitHub zvaigznes, pēdējo atjauninājumu, licence.",
  label="form-research",
  model="anthropic/claude-sonnet-4-5"
)

// Gaidi līdz pabeidz...
subagents list

// Fāze 2: Analīze (kad Fāze 1 pabeigta)
sessions_spawn(
  task="Salīdzini šīs form bibliotēkas: [ielikti dati no Fāzes 1]. Izvēlies labāko lielam projektam un pamatojies.",
  label="form-analysis"
)

// Fāze 3: Atskaite
sessions_spawn(
  task="Izveido 1 lappuses atskaiti par izvēlēto form bibliotēku priekš vadības",
  label="form-report"
)
```

### Scenārijs B: Paralēla koda pārskatīšana

```javascript
// Visi trīs vienlaikus!

// Aģents 1
sessions_spawn(
  task="Pārskati src/components/ un meklē React anti-pattern",
  label="react-review"
)

// Aģents 2  
sessions_spawn(
  task="Pārskati src/utils/ un meklē dublētu kodu",
  label="dup-review"
)

// Aģents 3
sessions_spawn(
  task="Pārskati src/api/ un meklē nepārbaudītus error handling",
  label="error-review"
)

// Pēc 5 minūtēm:
subagents list
// Redzēsi visus trīs rezultātus
```

### Scenārijs C: Dokumentācijas ģenerēšana

```javascript
// 1. Izveido koda dokumentāciju
sessions_spawn(
  task=`Izveido JSDoc komentārus visām funkcijām src/ mapē.
        Uzdevums:
        - Katrai publiskai funkcijai @param un @returns
        - Klases apraksti
        - TypeScript tipu dokumentācija`,
  label="jsdoc-writer"
)

// 2. Izveido lietotāja dokumentāciju
sessions_spawn(
  task="Izveido lietotāja rokasgrāmatu (USER_GUIDE.md) balstoties uz README.md",
  label="guide-writer"
)

// 3. Izveido API dokumentāciju
sessions_spawn(
  task="Izveido API.md ar visiem endpointiem un piemēriem",
  label="api-writer"
)
```

### Scenārijs D: Datu migrācija

```javascript
// Sadalīts pa datubāzēm/tabula

sessions_spawn(
  task="Migrē 'users' tabulu no MySQL uz PostgreSQL",
  label="migrate-users"
)

sessions_spawn(
  task="Migrē 'orders' tabulu no MySQL uz PostgreSQL",
  label="migrate-orders"
)

sessions_spawn(
  task="Migrē 'products' tabulu no MySQL uz PostgreSQL",
  label="migrate-products"
)

// Kad visi pabeiguši, apvieno
sessions_spawn(
  task="Pārbaudi datu integritāti pēc migrācijas",
  label="verify-migration"
)
```

---

## Padomi un triki

### 1. Labi nosauc savus aģentus

```javascript
// ❌ Slikti
sessions_spawn(task="...", label="a1")

// ✅ Labi  
sessions_spawn(task="...", label="react-security-audit")
```

### 2. Raksti detalizētus uzdevumus

```javascript
// ❌ Vājš uzdevums
sessions_spawn(task="Izveido API")

// ✅ Spēcīgs uzdevums
sessions_spawn(
  task=`Izveido REST API priekš lietotāju pārvaldības:
        
        Endpoints:
        - GET    /api/users      - saraksts (paginēts)
        - GET    /api/users/:id  - viens lietotājs
        - POST   /api/users      - izveidot
        - PUT    /api/users/:id  - atjaunot
        - DELETE /api/users/:id  - dzēst
        
        Prasības:
        - Express.js + TypeScript
        - SQLite datubāze
        - Joi validācija
        - JWT autentifikācija
        - Error handling middleware`
)
```

### 3. Izmanto atbilstošus modeļus

```javascript
// ātri uzdevumi
sessions_spawn(task="...", model="anthropic/claude-sonnet-4-5")

// Kompleksa arhitektūra
sessions_spawn(task="...", model="anthropic/claude-opus-4-6")

// Lieli faili
sessions_spawn(task="...", model="google/gemini-2.5-pro")
```

### 4. Seko līdzi ar `subagents list`

```javascript
// Pievieno alias savā .bashrc
alias agents='subagents list'
```

### 5. Tīri pēc sevis

```javascript
// Pēc darba pabeigšanas pārtrauc aģentus
subagents kill target="vecais-aģents"

// Vai pārtrauc visus
subagents kill target="*"
```

---

## Problēmu risināšana

### Aģents "iestrēga"

**Pazīmes:** `subagents list` rāda "running" >10 minūtes

**Risinājums:**
```javascript
// 1. Pārbaudi statusu
subagents list

// 2. Ja iestrēga, nosūti atgādinājumu
subagents steer target="aģents" message="Kāds ir tavs progress?"

// 3. Ja nekas, pārtrauc
subagents kill target="aģents"
```

### Pārāk daudz aģentu

**Pazīmes:** Lēna reakcija, timeout kļūdas

**Risinājums:**
```javascript
// Maksimums 3-5 vienlaikus
// Prioritizē un secīno
```

### Uzdevums pārāk plašs

**Pazīmes:** Aģents atgriež nepilnīgu rezultātu

**Risinājums:**
```javascript
// Sadali mazākos uzdevumos
sessions_spawn(task="Daļa 1: ...")
sessions_spawn(task="Daļa 2: ...")
```

### Nepareizs modelis

**Pazīmes:** Kvalitāte ir slikta

**Risinājums:**
```javascript
// Pārtrauc
subagents kill target="aģents"

// Mēģini ar spēcīgāku modeli
sessions_spawn(task="...", model="anthropic/claude-opus-4-6")
```

---

## Atsauces

### Ātrā komandu lapa

```javascript
// Izveidot
sessions_spawn(task="...", label="...", model="...")

// Vadīt
subagents steer target="..." message="..."

// Pārtraukt
subagents kill target="..."

// Saraksts
subagents list
```

### Ieteicamie modeļi pēc uzdevuma

| Uzdevums | Modelis | Iemesls |
|----------|---------|---------|
| Koda ģenerēšana | claude-opus-4-6 | Precīzs, sekojošs |
| Pētniecība | claude-sonnet-4-5 | ātrs, lēts |
| Refaktoring | gpt-4o | Labi saprot kontekstu |
| Dokumentācija | claude-sonnet-4-5 | Koncīzs |
| Lieli faili | gemini-2.5-pro | Liels konteksts |

### Noderīgi alias (pievieno .bashrc)

```bash
alias agent='sessions_spawn'
alias agents='subagents list'
alias kill-agent='subagents kill'
alias steer='subagents steer'
```

---

**Veiksmi ar multi-agent sistēmu!** 🚀
