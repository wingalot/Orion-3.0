# SKILL.md - Multi-Agent Coordinator

## Apraksts
Šis skills nodrošina rīkus un piemērus darbam ar OpenClaw multi-aģentu arhitektūru. Tas ļauj vieglāk pārvaldīt, spawn-ot un komunicēt ar citiem aģentiem, izmantojot `sessions_spawn` un `sessions_send` rīkus, balstoties uz OpenClaw dokumentācijas principiem.

## Iespējas
- **Spawn Sub-Agent:** Izveido jaunu izolētu sesiju specifiskam uzdevumam.
- **Inter-Agent Communication:** Sūta ziņas starp aģentiem (ja konfigurēts).

## Lietošana
Šis skills ir "wrapper" ap OpenClaw iebūvētajiem rīkiem, lai standartizētu multi-aģentu uzdevumu deleģēšanu.

### Piemērs (Spawn)
```javascript
// Izmanto sessions_spawn rīku tieši, vai caur wrapper skriptu (ja tādu izveidosim)
```

## Konfigurācija
Lai pilnvērtīgi izmantotu multi-aģentu iespējas, `openclaw.json` failā jābūt definētiem aģentiem vai jāizmanto `sessions_spawn` (sub-aģentiem).

Skatīt: https://docs.openclaw.ai/concepts/multi-agent
