# Restore Backup Skill

Atjauno aģenta darba vidi (workspace) no jaunākās pieejamās rezerves kopijas.

## Lietošana

```bash
node skills/restore-backup/restore.js --dir <path_to_backups>
```

## Parametri

- `--dir`: Ceļš uz mapi, kurā atrodas rezerves kopijas (noklusējums: `/home/elvis/backups`).

## Brīdinājums

Šī darbība pārraksta pašreizējo `.openclaw/workspace` saturu un restartē aģentu. Pārliecinieties, ka esat gatavi zaudēt nesaglabātās izmaiņas kopš pēdējā backup.
