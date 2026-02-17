# Code Review Team Piemērs

Šis piemērs demonstrē paralēlu koda pārskatīšanu ar specializētiem aģentiem.

## Scenārijs: Pull Request Review

Mērķis: Pārskatīt lielu Pull Request ar vairākiem aspektiem vienlaikus.

---

## Priekšnoteikumi

Pieņemam, ka kods atrodas:
- `/home/oreo/.openclaw/workspace/project/src/`

---

## Review Aģenti

### 1. Drošības Auditors

```javascript
sessions_spawn(
  task=`Veic drošības auditu koda bāzei: /home/oreo/.openclaw/workspace/project/src/
  
  Fokuss uz:
  - SQL injection riski
  - XSS iespējamība
  - Autentifikācijas/Autorizācijas problēmas
  - Hardcoded secrets/passwords
  - Unsafe eval() vai Function()
  - Path traversal risks
  - Input validācijas trūkumi
  
  Formāts:
  - Katrs atrasts risks ar: FAILA_NOSAUKUMS:LĪNIJA - APRAKSTS - RISKA LĪMENIS (High/Medium/Low)
  - Kopējais novērtējums (Safe/Needs Review/Critical)
  - Ieteikumi labojumiem
  
  Saglabā kā SECURITY_AUDIT.md`,
  label="security-auditor",
  model="anthropic/claude-opus-4-6"
)
```

### 2. Veiktspējas Analītiķis

```javascript
sessions_spawn(
  task=`Veic veiktspējas analīzi koda bāzei: /home/oreo/.openclaw/workspace/project/src/
  
  Fokuss uz:
  - N+1 vaicājumi datubāzē
  - Memory leaks
  - Inefficient loops
  - Unnecessary re-renders (React)
  - Large bundle imports (tree-shaking issues)
  - Synchronous blocking operations
  - Caching opportunities
  
  Formāts:
  - Atrastā problēma ar: FAILS:LĪNIJA - APRAKSTS - IETEKME
  - Optimizācijas priekšlikumi
  - Kopējais novērtējums
  
  Saglabā kā PERFORMANCE_AUDIT.md`,
  label="performance-auditor",
  model="anthropic/claude-opus-4-6"
)
```

### 3. Stila Pārbaudītājs

```javascript
sessions_spawn(
  task=`Veic koda stila pārbaudi: /home/oreo/.openclaw/workspace/project/src/
  
  Pārbaudi pret standartiem:
  - ESLint/Prettier konfigurācija
  - Naming conventions (camelCase, PascalCase)
  - Function length (max 50 lines)
  - File organization
  - Comment quality
  - Consistent formatting
  - Dead code detection
  
  Formāts:
  - Stila problēmas ar FAILS:LĪNIJA - APRAKSTS - KATEGORIJA
  - Pozitīvi piemēri (kas izdarīts labi)
  - Ieteikumi uzlabojumiem
  
  Saglabā kā STYLE_AUDIT.md`,
  label="style-checker",
  model="anthropic/claude-sonnet-4-5"
)
```

### 4. Arhitektūras Rezensents

```javascript
sessions_spawn(
  task=`Veic arhitektūras pārskatīšanu: /home/oreo/.openclaw/workspace/project/src/
  
  Fokuss uz:
  - SOLAD principi
  - DRY (Don't Repeat Yourself)
  - Separation of Concerns
  - Dependency management
  - Testability
  - Scalability patterns
  - Error handling strategy
  
  Formāts:
  - Arhitektūras stiprās puses
  - Arhitektūras problēmas ar ieteikumiem
  - Refactoring priekšlikumi
  
  Saglabā kā ARCHITECTURE_AUDIT.md`,
  label="arch-reviewer",
  model="anthropic/claude-opus-4-6"
)
```

---

## Vadība

### Sekot līdzi:
```javascript
subagents list
// Gaidi līdz visi rāda "completed"
```

### Ja aģents atradis kritisku kļūdu:
```javascript
subagents steer target="security-auditor" message="Pievieno konkrētus fix piemērus SQL injection problēmai"
```

### Pārtraukt visus:
```javascript
subagents kill target="*"
```

---

## Rezultātu Apvienošana

Kad visi aģenti pabeiguši, izveido kopsavilkumu:

```javascript
sessions_spawn(
  task=`Apvieno visus audit rezultātus vienā PR_REPORT.md.
  
  Iekļauj:
  - SECURITY_AUDIT.md kopsavilkumu
  - PERFORMANCE_AUDIT.md kopsavilkumu
  - STYLE_AUDIT.md kopsavilkumu
  - ARCHITECTURE_AUDIT.md kopsavilkumu
  
  Secinājumu sadaļa:
  - Vai PR ir apstiprināms? (Approved/Needs Changes/Rejected)
  - Kritiskie blokējošie jautājumi (ja ir)
  - Ieteikumi nākotnei
  
  Formāts: Markdown, profesionāls PR review tonis`,
  label="report-compiler"
)
```

---

## Laika Plānošana

| Aģents | Ilgums | Prioritāte |
|--------|--------|------------|
| Security | 5-7 min | KRITISKA |
| Performance | 5-7 min | Augsta |
| Style | 3-5 min | Vidēja |
| Architecture | 5-7 min | Augsta |
| **Kopā (paralēli)** | **~7 min** | - |

---

## Pielāgošana

### Frontend projektam:
- Pievieno "Accessibility Auditor"
- Pievieno "Responsive Design Checker"

### Backend projektam:
- Pievieno "API Design Reviewer"
- Pievieno "Database Schema Analyst"

### Mobile projektam:
- Pievieno "Battery Usage Analyzer"
- Pievieno "Platform Guidelines Checker"

---

## Droša izpilde (bez overfetch)

Ja koda bāze ir milzīga, ierobežo aģentus:

```javascript
sessions_spawn(
  task=`Pārskati TIKAI src/auth/ un src/api/ mapes.
  NEaiztiec src/components/ vai src/utils/ šoreiz.`,
  label="security-auditor"
)
```
