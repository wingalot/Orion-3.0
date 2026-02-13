# Restore Backup Skill

Šī prasme ļauj atjaunot OpenClaw aģenta darba vidi (`.openclaw/workspace`) no jaunākās pieejamās rezerves kopijas.

## Lietošana

### Atjaunošana no rezerves kopijas

```bash
node skills/Orion-3.0/skills/restore-backup/restore.js [parametri]
```

**Parametri:**
- `--dir`: Mape, kurā meklēt rezerves kopijas (noklusējums: `/home/elvis/backups`).
- `--target`: Mape, kurā atjaunot saturu (noklusējums: `/home/elvis/.openclaw/workspace`).
- `--force`: (Nav obligāts) Piespiedu kārtā veic atjaunošanu, ignorējot brīdinājumus (nav implementēts šobrīd, bet ir kodā).

## Brīdinājums

1.  Šī darbība **pārraksta** pašreizējo `.openclaw/workspace` saturu.
2.  Pirms atjaunošanas tiek izveidota pagaidu drošības kopija (piem., `workspace_pre_restore_...`), ja kaut kas noiet greizi.
3.  Lai izmaiņas stātos spēkā, skripts automātiski mēģina restartēt `openclaw gateway`.

## Process

1.  Pārbauda vai eksistē rezerves kopijas mapē.
2.  Atrod jaunāko rezerves kopiju (pēc faila laika).
3.  Izveido pašreizējā `workspace` satura drošības kopiju (ja tāds eksistē).
4.  Izdzēš esošo `workspace` saturu.
5.  Izveido jaunu `workspace` mapi un atspiež tajā rezerves kopiju.
6.  Dzēš pagaidu drošības kopiju, ja process noritējis veiksmīgi.
7.  Restartē aģenta servisu.
