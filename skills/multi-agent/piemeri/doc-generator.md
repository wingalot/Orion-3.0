# Documentation Generator Piemērs

Šis piemērs demonstrē automātisku dokumentācijas ģenerēšanu ar vairākiem aģentiem.

## Scenārijs: Projekta dokumentācijas atjaunināšana

Mērķis: Pilnībā atjaunināt visu projekta dokumentāciju.

---

## 1. README.md Atjaunināšana

```javascript
sessions_spawn(
  task=`Atjaunini README.md projektam /home/oreo/.openclaw/workspace/project/
  
  Analizē:
  - package.json (dependencies, scripts)
  - src/ struktūra
  - Esošais README.md (ja ir)
  
  Jauns README.md satur:
  1. Projekta nosaukums un 1-teikuma apraksts
  2. Iespējas (bullet points)
  3. Instalācija (step-by-step)
  4. Lietošana (basic example)
  5. API kopsavilkums (ja piemērojams)
  6. Contributing (ja atvērts kods)
  7. Licence
  
  Formāts: Markdown ar emoji ikonām sadaļām
  Stils: Draudzīgs, profesionāls`,
  label="readme-updater",
  model="anthropic/claude-sonnet-4-5"
)
```

---

## 2. API Dokumentācija

```javascript
sessions_spawn(
  task=`Izveido API.md dokumentāciju.
  
  Analizē src/api/ vai src/routes/ mapi:
  - Visi endpointi
  - HTTP metodes
  - URL parametri
  - Request body shēmas
  - Response formāti
  - Error codes
  
  Formāts:
  \`\`\`markdown
  ## GET /api/users
  
  Atgriež visus lietotājus.
  
  ### Parametri
  | Parametrs | Tips | Obligāts | Apraksts |
  
  ### Atbilde
  \`\`\`json
  { "users": [...] }
  \`\`\`
  \`\`\`
  
  Saglabā kā docs/API.md`,
  label="api-doc-writer",
  model="anthropic/claude-opus-4-6"
)
```

---

## 3. Koda Komentāri (JSDoc)

```javascript
sessions_spawn(
  task=`Pievieno JSDoc komentārus visām publiskajām funkcijām src/ mapē.
  
  Katrai funkcijai:
  \`\`\`javascript
  /**
   * Īss apraksts (1 teikums)
   * @param {string} name - Parametra apraksts
   * @param {number} age - Parametra apraksts
   * @returns {Promise<User>} Atgriežamā vērtība
   * @throws {Error} Kad notiek kļūda
   * @example
   * const user = await createUser('John', 25);
   */
  \`\`\`
  
  Fails pa failam, bez pārspīlēšanas.
  Prioritāte: utils/, helpers/, services/.
  
  NEaiztiec:
  - Privātās funkcijas (sākās ar _)
  - Iekšējie handleri
  - Testi`,
  label="jsdoc-writer",
  model="anthropic/claude-sonnet-4-5"
)
```

---

## 4. CHANGELOG.md

```javascript
sessions_spawn(
  task=`Izveido vai atjaunini CHANGELOG.md.
  
  Analizē:
  - git log --oneline -20
  - package.json version
  - GitHub releases (ja pieejami)
  
  Formāts: Keep a Changelog (https://keepachangelog.com/)
  
  ## [1.2.0] - 2025-02-17
  ### Added
  - Jauna funkcija X
  
  ### Changed
  - Uzlabota funkcija Y
  
  ### Fixed
  - Bug fix Z
  
  ### Security
  - Drošības atjauninājums
  
  Saglabā kā CHANGELOG.md`,
  label="changelog-writer"
)
```

---

## 5. Lietotāja Rokasgrāmata

```javascript
sessions_spawn(
  task=`Izveido USER_GUIDE.md galalietotājiem.
  
  Satur:
  1. Ievads (kas ir šis projekts)
  2. Sistemas prasības
  3. Instalācija (vienkārša, bez tehniskiem terminiem)
  4. Pamata lietošana (soļi ar ekrānšāviņiem - apraksti)
  5. Biežāk uzdotie jautājumi (FAQ)
  6. Problēmu risināšana
  7. Atbalsts (kur griezties pēc palīdzības)
  
  Formāts: Markdown, viegli lasāms, draudzīgs tonis
  Mērķauditorija: Ne-tehniski lietotāji
  
  Saglabā kā docs/USER_GUIDE.md`,
  label="user-guide-writer",
  model="anthropic/claude-sonnet-4-5"
)
```

---

## 6. Izstrādātāja Dokumentācija

```javascript
sessions_spawn(
  task=`Izveido DEVELOPMENT.md izstrādātājiem.
  
  Satur:
  1. Development setup (git clone, install, run)
  2. Projekta struktūras apraksts
  3. Kā pievienot jaunu funkciju (soļi)
  4. Testing (kā palaist testus)
  5. Code style un conventions
  6. Commit message format
  7. PR process
  8. Deployment process (ja atklāts)
  
  Formāts: Markdown, tehnisks bet skaidrs
  
  Saglabā kā DEVELOPMENT.md`,
  label="dev-doc-writer"
)
```

---

## Vadība

### Sekot līdzi progresam:
```javascript
subagents list
```

### Ja nepieciešams papildu saturs:
```javascript
subagents steer target="api-doc-writer" message=
"Pievieno arī authentication sekciju ar JWT piemēru"
```

### Kad visi pabeiguši:
```javascript
// Pārbaudi rezultātus
read README.md
read docs/API.md
read DEVELOPMENT.md
```

---

## Rezultāti

Pēc izpildes tev būs:

```
project/
├── README.md              ← Galvenā lapa
├── CHANGELOG.md           ← Versiju vēsture
├── DEVELOPMENT.md         ← Dev instrukcijas
└── docs/
    ├── API.md            ← API dokumentācija
    └── USER_GUIDE.md     ← Lietotāja rokasgrāmata
```

---

## Laika Plānošana

| Dokuments | Ilgums | Secība |
|-----------|--------|--------|
| README.md | 3-5 min | 1 |
| API.md | 5-7 min | 2 |
| JSDoc | 7-10 min | Paralēli ar 2 |
| CHANGELOG.md | 2-3 min | 3 |
| USER_GUIDE.md | 5-7 min | Paralēli ar 3 |
| DEVELOPMENT.md | 3-5 min | Paralēli ar 3 |

**Kopējais laiks:** ~10-15 min

---

## Padomi

### 1. Prioritizē
Ja maz laika, sāc ar:
1. README.md
2. API.md
3. JSDoc

### 2. Secība svarīga
README.md būtu jābūt gatavam pirms citiem, jo citi var atsaukties uz to.

### 3. Pārskati
Lasi un rediģē ģenerēto saturu - aģenti ne vienmēr ir perfekti.

### 4. Saite starp dokumentiem
Pievieno cross-references:
```markdown
[Skatīt API dokumentāciju](./docs/API.md)
```
