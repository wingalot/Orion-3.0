# Restore Backup Skill

Atjauno aģenta (Oreo) darba vidi (workspace) no rezerves kopijas.

## Funkcijas

- Parāda sarakstu ar visiem pieejamajiem backup failiem
- Ļauj izvēlēties konkrētu backup
- Pirms atjaunošanas izveido pagaidu backup pašreizējā stāvokļa
- Automātiski restartē OpenClaw pēc atjaunošanas

## Lietošana

### Interaktīvā režīmā (ieteicams)

```bash
node skills/restore-backup/restore.js
```

Tiks parādīts saraksts ar pieejamajiem backup failiem. Ievadiet numuru, lai izvēlētos.

### Automātiskā režīmā (jaunākais backup)

```bash
node skills/restore-backup/restore.js --force
```

⚠️ **Uzmanību!** `--force` izlaiž apstiprinājumu un automātiski izmanto jaunāko backup.

### Parametri

- `--dir`: Ceļš uz mapi, kurā atrodas rezerves kopijas (noklusējums: `/home/oreo/backups`)
- `--force`: Automātiski izmanto jaunāko backup bez apstiprinājuma

Piemēri:
```bash
# Izmantot citu backup mapi
node skills/restore-backup/restore.js --dir /mnt/external/oreo-backups

# Automātiski atjaunot jaunāko backup
node skills/restore-backup/restore.js --force
```

## Brīdinājumi

⚠️ **Svarīgi:**
- Atjaunošana pārraksta visu pašreizējo `workspace` saturu
- Pirms atjaunošanas tiks izveidots pagaidu backup pašreizējā stāvokļa
- Pēc veiksmīgas atjaunošanas OpenClaw tiks automātiski restartēts
- Nesaglabātās izmaiņas kopš pēdējā backup tiks zaudētas

## Backup failu formāts

Atbalstītie formāti:
- `.tar.gz` - ieteicamais formāts
- `.zip` - alternatīvs formāts

Backup faila nosaukumā jāsatur vārds "backup" (piem., `oreo-backup-2025-02-17.tar.gz`).

## Problēmu risināšana

### "Kļūda: Mape /home/oreo/backups neeksistē"
Izveidojiet mapi: `mkdir -p /home/oreo/backups`

### "Kļūda: Rezerves kopijas netika atrastas"
Pārbaudiet vai backup faili atrodas pareizajā mapē un vai to nosaukumos ir vārds "backup".

### Atjaunošana neizdodas
- Pārbaudiet vai backup fails nav bojāts: `tar -tzf backup-fails.tar.gz`
- Pārbaudiet vai ir pietiekami daudz brīvas vietas diskā
