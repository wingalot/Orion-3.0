# Subaģentu Pievienošana un Konfigurācija OpenClaw

Šī instrukcija apraksta, kā pareizi pievienot jaunus aģentus (piemēram, "Kimi" un "Gemi") un atļaut galvenajam aģentam ("main") tos izsaukt (`spawn`).

## 1. Konfigurācijas fails
Visi iestatījumi tiek veikti failā:
`~/.openclaw/openclaw.json`

## 2. Pareizā Struktūra (`agents.list`)

Aģenti tiek definēti sadaļā `agents` -> `list`.
**Svarīgi:** `subagents` atļaujas (`allowAgents`) ir jādefinē tam aģentam, KURS izsauc (parasti "main"), nevis globāli.

### Piemērs:

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "google/gemini-3-pro-preview" },
      // ... citi noklusējuma iestatījumi
    },
    "list": [
      {
        "id": "main",
        "subagents": {
          "allowAgents": [
            "Kimi",
            "Gemi"
          ]
        }
      },
      {
        "id": "Kimi",
        "model": "google/gemini-2.0-flash"
      },
      {
        "id": "Gemi",
        "model": "google/gemini-2.0-flash"
      }
    ]
  }
  // ... pārējā konfigurācija
}
```

## 3. Soļu skaidrojums

1.  **Definēt "main" aģentu:**
    Pievienojiet ierakstu ar `id: "main"`.
    Iekš tā pievienojiet `subagents: { "allowAgents": ["ID1", "ID2"] }`.
    Tas dod tiesības `main` aģentam izmantot `sessions_spawn` ar šiem ID.

2.  **Definēt subaģentus:**
    Katram subaģentam pievienojiet savu ierakstu sarakstā.
    Obligāti: `id` (unikāls nosaukums).
    Ieteicams: `model` (lai norādītu specifisku modeli, piemēram, lētāku vai ātrāku).

3.  **Restartēt Gateway:**
    Pēc izmaiņu saglabāšanas, OpenClaw gateway ir jārestartē, lai iestatījumi stātos spēkā.
    `openclaw gateway restart`

## 4. Biežākās kļūdas

*   ❌ `agents.subagents` — Šāda atslēga augstākajā līmenī neeksistē. Subaģentu politika ir per-agent iestatījums.
*   ❌ Aizmirsts definēt `main` aģentu sarakstā — ja "main" nav sarakstā, tas izmanto noklusējuma iestatījumus un tam nav tiesību spawnēt citus.

---
*Ģenerēts: 2026-02-13 | Or3o System*
