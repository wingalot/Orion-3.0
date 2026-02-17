# Research Pipeline Piemērs

Šis piemērs demonstrē pētniecības uzdevumu sadalījumu vairākos secīgos posmos.

## Scenārijs: React State Management 2025

Mērķis: Izpētīt modernākos React state management risinājumus un ieteikt labāko lielam projektam.

---

## Fāze 1: Datu vākšana

```javascript
sessions_spawn(
  task=`Izpēti React state management bibliotēkas 2025. gadā.
  
  Meklē informāciju par:
  1. Redux Toolkit (RTK)
  2. Zustand
  3. Jotai
  4. Recoil
  5. TanStack Query (React Query)
  6. Context API + useReducer
  
  Katrai atrodi:
  - GitHub zvaigžņu skaits
  - Pēdējais release datums
  - Weekly npm downloads
  - Licenze
  - Galvenās funkcijas (bullet points)
  
  Saglabā kā STATE_RESEARCH.md`,
  label="state-research",
  model="anthropic/claude-sonnet-4-5"
)
```

---

## Fāze 2: Analīze (pēc Fāzes 1 pabeigšanas)

```javascript
sessions_spawn(
  task=`Analizē STATE_RESEARCH.md datus un izveidi salīdzinājuma matricu.
  
  Salīdzinājuma kritēriji:
  - Learning curve (zemāka = labāk)
  - Performance (ātrāka = labāk)
  - Community support
  - TypeScript atbalsts
  - DevTools pieejamība
  - Bundle size
  
  Izveido secinājumus:
  - Labākais mazam projektam
  - Labākais lielam projektam
  - Labākais komandai bez pieredzes
  
  Saglabā kā STATE_ANALYSIS.md`,
  label="state-analysis"
)
```

---

## Fāze 3: Ieteikums (pēc Fāzes 2 pabeigšanas)

```javascript
sessions_spawn(
  task=`Izveido vadības atskaiti balstoties uz STATE_ANALYSIS.md.
  
  Dokuments: STATE_RECOMMENDATION.md
  
  Struktūra:
  1. Executive Summary (3-4 teikumi)
  2. Ieteikums ar pamatojumu
  3. Risku novērtējums
  4. Ieguldījumu aprēķins (migrācijas laiks)
  5. Alternatīvi varianti
  
  Formāts: Markdown, profesionāls tonis`,
  label="state-recommendation"
)
```

---

## Vadības komandas

### Sekot līdzi progresam:
```javascript
subagents list
```

### Ja aģents ir iestrēdzis:
```javascript
subagents steer target="state-research" message="Vai esi atradis npm download datus?"
```

### Ja nepieciešams papildu meklējums:
```javascript
subagents steer target="state-research" message="Pievieno arī Redux Saga salīdzinājumu"
```

---

## Paredzamais rezultāts

Pēc visu fāžu pabeigšanas tev būs:

1. **STATE_RESEARCH.md** - Sākotnējie dati
2. **STATE_ANALYSIS.md** - Salīdzinājuma matrica
3. **STATE_RECOMMENDATION.md** - Vadības lēmumam gatava atskaite

---

## Pielāgošana citiem scenārijiem

Šo pašu struktūru vari izmantot:

- **UI bibliotēkas:** Tailwind vs MUI vs Chakra
- **Backend framework:** Express vs Fastify vs NestJS
- **Datubāzes:** PostgreSQL vs MySQL vs MongoDB
- **Deployment:** Vercel vs Netlify vs AWS

---

## Laika plānošana

| Fāze | Ilgums | Modelis |
|------|--------|---------|
| Datu vākšana | 5-7 min | sonnet-4-5 |
| Analīze | 3-5 min | sonnet-4-5 |
| Ieteikums | 2-3 min | sonnet-4-5 |
| **Kopā** | **10-15 min** | - |

---

## Alternatīva: Paralēlā izpilde

Ja datu vākšana ir neatkarīga, vari palaist paralēli:

```javascript
// Visas bibliotēkas vienlaikus
sessions_spawn(task="Izpēti Redux Toolkit...", label="rtk-research")
sessions_spawn(task="Izpēti Zustand...", label="zustand-research")
sessions_spawn(task="Izpēti Jotai...", label="jotai-research")
// ...utt

// Tad apvieno rezultātus
sessions_spawn(task="Apvieno visu research doku...", label="merge-research")
```
