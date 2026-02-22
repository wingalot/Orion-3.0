# ⚠️ CRASH PREVENTION - Neiznīcināma Sistēma

## 🎯 Galvenie principi

1. **NEKAD** neizmet izņēmumus uz augšu - vienmēr apķīlā
2. **NEKAD** neatstāj `exec` bez `timeout`
3. **NEKAD** nelieto `pkill -9 -f` (SIGKILL + full match)
4. **Vienmēr** turpini darbu pēc kļūdas
5. **Vienmēr** ziņo par problēmām

---

## 🔒 Safe Executor Pattern

### ❌ NEDRĪKST (būs katastrofa)
```javascript
// Slikti - kļūda iznīcina visu sesiju
const result = exec({ command: "git push" });
if (result.error) throw result.error;  // 💥
```

### ✅ JĀ (droši)
```javascript
// Labi - kļūda apķīlāta, turpinām darbu
const { safeExec, safeKill } = require('./orion-skills/scripts/safe-executor');

async function doWork() {
  const result = await safeExec("git push", { timeout: 30 });
  
  if (!result.success) {
    console.log('❌ Neizdevās:', result.error);
    // Ziņojam, bet turpinām!
    await notifyTelegram(`Kļūda: ${result.error}`);
    return { ok: false };
  }
  
  return { ok: true, output: result.output };
}
```

---

## 🛡️ Watchdog Loop - Neiznīcināms

```javascript
async function immortalLoop() {
  while (true) {
    try {
      await doWork();
      await heartbeat();
    } catch (error) {
      // Kļūda APĶĪLĀTA - nekad neapstājamies!
      console.error('💥 Crash:', error.message);
      await sendTelegram(`⚠️ Recovered from crash: ${error.message}`);
      await sleep(5000); // 5 sekunžu pauze
    }
  }
}
```

---

## 🔪 Droša Procesu Nobeigšana

### ❌ BĪSTAMI (var nogalināt OpenClaw)
```bash
# NEDRĪKST - SIGKILL var novest pie sistēmas nestabilitātes
pkill -9 -f felix_auto_executor

# NEDRĪKST - -f var atrast nepareizus procesus
pkill -f "python.*felix"
```

### ✅ DROŠI
```bash
# 1. SIGTERM (polite) + exact match
pkill -15 -x felix_auto_executor || true

# 2. Ja vēl dzīvs, SIGTERM ar full match
pkill -15 -f "felix_auto_executor" || true

# 3. Tikai ja nekas cits nepalīdz, SIGKILL
pkill -9 -x felix_auto_executor || true
```

### Skripta variants
```bash
# Izmanto gatavo skriptu
./orion-skills/scripts/safe-process-kill.sh felix_auto_executor
```

---

## ⏱️ Heartbeat Sistēma

### Cron job (aktīvs)
```json
{
  "name": "orion-heartbeat",
  "schedule": { "kind": "every", "everyMs": 60000 },
  "payload": { "kind": "systemEvent", "text": "🟢 Agent alive" }
}
```

ID: `8d3923d8-01da-4bb9-9363-4fdd6987d453`

---

## 📋 Kļūdu Apstrādes Šablons

```javascript
const { safeExec, notifyTelegram } = require('./orion-skills/scripts/safe-executor');

async function robustOperation() {
  // 1. Paziņojam par sākumu (nav obligāti, bet noderīgi)
  console.log('🚀 Sāku operāciju...');
  
  // 2. Izpildām ar safeExec
  const result = await safeExec("komanda", { timeout: 30 });
  
  // 3. Pārbaudām rezultātu
  if (!result.success) {
    // 4. Ziņojam par kļūdu
    await notifyTelegram(`❌ Kļūda: ${result.error}`, { severity: 'error' });
    
    // 5. Atgriežam kļūdas objektu, NEIZMETAM izņēmumu!
    return { 
      ok: false, 
      error: result.error,
      exitCode: result.exitCode 
    };
  }
  
  // 6. Veiksmīgi!
  return { ok: true, output: result.output };
}
```

---

## 🚨 Ko darīt pie dažādām kļūdām

| Kļūda | Iemesls | Risinājums |
|-------|---------|------------|
| SIGTERM | Cits process nogalināja | Pārbaudi `safeKill` izsaukumus |
| timeout | Komanda pārāk ilga | Palielini `timeout` vai lieto `background: true` |
| ECONNREFUSED | Tīkla/API problēma | Gaidi 5s un mēģini vēlreiz |
| ENOSPC | Disks pilns | Pārbaudi `df -h` |
| OOM | Atmiņas trūkums | Samazini `maxBuffer` |

---

## 🔧 Failu Struktūra

```
orion-skills/scripts/
├── safe-executor.js      # Galvenā kļūdu apstrādes bibliotēka
├── watchdog.js           # Neiznīcināmais cikls
└── safe-process-kill.sh  # Droša procesu nobeigšana
```

---

## 🧪 Testēšana

```bash
# 1. Testē safe executor
node -e "const {safeExec} = require('./orion-skills/scripts/safe-executor'); safeExec('ls -la').then(r => console.log(r.success))"

# 2. Testē process kill
./orion-skills/scripts/safe-process-kill.sh not_existing_process

# 3. Pārbaudi heartbeat
cron list
```

---

## 📚 Saistītā informācija

- **MEMORY.md** - Lietotāja preferences un vēsture
- **AGENTS.md** - Darba režīma noteikumi
- **SKILL.md** skills - Konkrētās prasmes

---

*Atjaunots: 2025-01-23*  
*Sistēma: crash-proof, self-healing, immortal*  
*Heartbeat: 8d3923d8-01da-4bb9-9363-4fdd6987d453*
