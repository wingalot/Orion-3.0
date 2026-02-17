# Backup Manager Skill

Uztur kārtību rezerves kopiju mapē, saglabājot tikai jaunākos failus.

## Lietošana

```bash
node skills/backup-manager/cleanup.js --dir <path_to_backups> --keep 10
```

## Parametri

- `--dir`: Ceļš uz mapi, kurā atrodas rezerves kopijas (noklusējums: `/home/elvis/backups`).
- `--keep`: Saglabājamo failu skaits (noklusējums: 10).
