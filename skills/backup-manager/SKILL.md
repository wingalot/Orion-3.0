# Backup Manager Skill

Pārvalda Oreo (aģenta) rezerves kopijas - izveido, attīra vecās un uztur kārtību backup mapē.

## Funkcijas

- **create.js** - Izveido jaunu rezerves kopiju
- **cleanup.js** - Attīra vecās rezerves kopijas, saglabājot tikai jaunākos failus

## Lietošana

### Backup izveide

```bash
node skills/backup-manager/create.js [--dir <ceļš>] [--name <nosaukums>]
```

Parametri:
- `--dir`: Ceļš uz mapi, kurā saglabāt backup (noklusējums: `/home/oreo/backups`)
- `--name`: Backup faila nosaukums bez paplašinājuma (noklusējums: `oreo-backup-YYYY-MM-DDTHH-mm-ss`)

Piemēri:
```bash
# Izveidot backup ar noklusējuma nosaukumu
node skills/backup-manager/create.js

# Izveidot backup ar pielāgotu nosaukumu
node skills/backup-manager/create.js --name pirms-izmaiņam

# Saglabāt citā mapē
node skills/backup-manager/create.js --dir /mnt/external/oreo-backups
```

### Veco backup tīrīšana

```bash
node skills/backup-manager/cleanup.js [--dir <ceļš>] [--keep <skaits>]
```

Parametri:
- `--dir`: Ceļš uz mapi, kurā atrodas rezerves kopijas (noklusējums: `/home/oreo/backups`)
- `--keep`: Saglabājamo jaunāko failu skaits (noklusējums: 10)

Piemērs:
```bash
# Saglabāt tikai 5 jaunākos backup failus
node skills/backup-manager/cleanup.js --keep 5
```

## Automatizācija

Ieteicams iestatīt cron job, lai automātiski izveidotu backup:

```bash
# Katru dienu plkst. 3:00
0 3 * * * cd /home/oreo/.openclaw/workspace/orion-skills && node skills/backup-manager/create.js && node skills/backup-manager/cleanup.js --keep 7
```

## Backup struktūra

Backup fails ir `tar.gz` arhīvs, kas satur visu `workspace` mapi:

```
oreo-backup-2025-02-17T15-14-30.tar.gz
└── workspace/
    ├── AGENTS.md
    ├── SOUL.md
    ├── memory/
    └── ... (citi faili)
```

## Atjaunošana

Lai atjaunotu no backup, izmanto **restore-backup** skillu:

```bash
node skills/restore-backup/restore.js
```
