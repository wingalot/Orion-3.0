# Backup Manager Skill

Šī prasme nodrošina OpenClaw aģenta darba vides (`.openclaw/workspace`) rezerves kopiju veidošanu un pārvaldību. Tā ietver divus galvenos skriptus:

1.  `create.js` - Izveido jaunu rezerves kopiju.
2.  `cleanup.js` - Dzēš vecās rezerves kopijas, lai ietaupītu vietu.

## Lietošana

### Rezerves kopijas izveide

```bash
node skills/Orion-3.0/skills/backup-manager/create.js [parametri]
```

**Parametri:**
- `--dir`: Mape, kurā saglabāt rezerves kopijas (noklusējums: `/home/elvis/backups`).
- `--source`: Mape, kuru arhivēt (noklusējums: `/home/elvis/.openclaw/workspace`).

### Veco kopiju tīrīšana

```bash
node skills/Orion-3.0/skills/backup-manager/cleanup.js [parametri]
```

**Parametri:**
- `--dir`: Mape, kurā tīrīt rezerves kopijas (noklusējums: `/home/elvis/backups`).
- `--keep`: Saglabājamo jaunāko kopiju skaits (noklusējums: 10).

## Piezīmes

- Skripti automātiski izveido nepieciešamās mapes, ja tās neeksistē.
- Rezerves kopijas tiek saglabātas `.tar.gz` formātā ar laika zīmogu nosaukumā (piem., `backup-2023-10-27-103000.tar.gz`).
