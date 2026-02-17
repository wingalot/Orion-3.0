# Oreo Backup & Restore Sistēma

Pilnīga rezerves kopiju pārvaldība Oreo (OpenClaw aģents) darba videi.

## 🎯 Ātrais sākums

```bash
# Izveidot backup
oreo-backup create

# Atjaunot no backup
oreo-backup restore

# Skatīt pieejamos backup
oreo-backup list
```

## 📁 Struktūra

```
orion-skills/
├── skills/
│   ├── backup-manager/
│   │   ├── create.js      # Backup izveide
│   │   ├── cleanup.js     # Veco backup dzēšana
│   │   └── SKILL.md       # Dokumentācija
│   └── restore-backup/
│       ├── restore.js     # Atjaunošana
│       └── SKILL.md       # Dokumentācija
├── scripts/
│   └── oreo-backup.sh     # Palaišanas skripts
└── Instrukcijas/
    └── backup_restore.md  # Šī faila
```

## 🚀 Lietošana

### 1. Backup izveide

**Pamata lietošana:**
```bash
# Ar galveno skriptu
oreo-backup create

# Vai tieši caur Node.js
cd ~/.openclaw/workspace/orion-skills
node skills/backup-manager/create.js
```

**Ar pielāgotu nosaukumu:**
```bash
oreo-backup create --name pirms-eksperimenta
```

**Cita atrašanās vieta:**
```bash
oreo-backup create --dir /mnt/usb/oreo-backups
```

### 2. Atjaunošana

**Interaktīvā režīmā (ieteicams):**
```bash
oreo-backup restore
```
Tiks parādīts saraksts ar visiem backup failiem. Ievadiet numuru, lai izvēlētos.

**Ātrā režīmā (jaunākais backup):**
```bash
oreo-backup restore --force
```

### 3. Backup saraksts

```bash
oreo-backup list
```

### 4. Veco backup tīrīšana

```bash
# Saglabāt 5 jaunākos
oreo-backup cleanup --keep 5

# Noklusējums - 10 jaunākie
oreo-backup cleanup
```

## 📺 Canvas Interfeiss

Vizuālais interfeiss pieejams uz ekrāna:
- Atver `~/.openclaw/canvas/index.html` jebkurā pārlūkā
- Piedāvā pogas ērtai backup/restore vadībai

## ⚙️ Konfigurācija

### Noklusējuma ceļi

| Parametrs | Noklusējuma vērtība | Apraksts |
|-----------|---------------------|----------|
| Backup mape | `/home/oreo/backups` | Kur tiek saglabāti backup |
| Source | `~/.openclaw/workspace` | Kas tiek backupēts |
| Formāts | `.tar.gz` | Arhīva formāts |
| Saglabāt | 10 | Cik backup turēt |

### Mainīt noklusējumus

Rediģējiet skriptus vai izmantojiet `--dir`, `--name`, `--keep` parametrus.

## 🔒 Drošība

1. **Pirms atjaunošanas** - tiek izveidots pagaidu backup pašreizējā stāvokļa
2. **Apstiprinājums** - interaktīvajā režīmā jāapstiprina atjaunošana
3. **Pārrakstīšana** - atjaunošana pilnībā aizvieto pašreizējo workspace

## 🔄 Automatizācija

### Cron piemērs

```bash
# Katru dienu plkst. 3:00 izveidot backup un notīrīt vecos
0 3 * * * cd ~/.openclaw/workspace/orion-skills && node skills/backup-manager/create.js && node skills/backup-manager/cleanup.js --keep 7
```

## 🐞 Problēmu risināšana

### "Mape neeksistē"
```bash
mkdir -p /home/oreo/backups
```

### "Nav atrasts neviens backup"
- Pārbaudiet vai backup failu nosaukumos ir vārds "backup"
- Pārbaudiet vai formāts ir `.tar.gz` vai `.zip`

### Atjaunošana neizdodas
```bash
# Pārbaudīt backup integritāti
tar -tzf /home/oreo/backups/oreo-backup-YYYY-MM-DD.tar.gz

# Pārbaudīt diskvietu
df -h
```

### Permission denied
```bash
# Padarīt skriptu izpildāmu
chmod +x ~/.openclaw/workspace/orion-skills/scripts/oreo-backup.sh
```

## 📝 Backup formāts

Backup ir `.tar.gz` arhīvs ar šādu struktūru:

```
oreo-backup-2025-02-17T15-30-00.tar.gz
└── workspace/
    ├── AGENTS.md
    ├── SOUL.md
    ├── USER.md
    ├── memory/
    ├── orion-skills/
    └── ... (citi faili)
```

## 🔧 Manuāla backup izveide

Ja vēlaties izveidot backup manuāli:

```bash
cd ~
tar -czf backups/oreo-backup-$(date +%Y-%m-%d-%H%M).tar.gz .openclaw/workspace
```

## 📧 Palīdzība

Ja rodas problēmas:
1. Pārbaudiet loģus: `~/.openclaw/logs/`
2. Pārbaudiet vai Node.js ir instalēts: `node --version`
3. Pārbaudiet ceļus savā sistēmā

---

**Versija:** 1.0  
**Autors:** Oreo Backup System  
**Platforma:** OpenClaw
