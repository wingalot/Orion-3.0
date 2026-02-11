# SKILL: Sub-aģents "Kodētājs"

## Apraksts
Šī prasme izveido un darbina specializētu sub-aģentu **"Kodētājs"**, izmantojot OpenRouter API.

## Konfigurācija
- **API Atslēga:** Tiek droši glabāta failā `~/.openclaw/auth.json`.
- **Modelis:** `qwen/qwen-3-32b` (lietotāja norādītais).
- **Loma:** Programmēšanas eksperts, kas fokusējas uz koda kvalitāti un dokumentāciju.

## Lietošana
Skripts automātiski pārbauda API atslēgu. Ja tā nav atrasta, tā tiek pieprasīta interaktīvi (tikai pirmajā reizē) un saglabāta.

```bash
# Izsaukums no termināļa vai cita aģenta
node skills/subagent-manager/index.js "Uzraksti hello world python valodā"
```

## Atkarības
- `openai` (npm pakotne komunikācijai ar OpenRouter)
