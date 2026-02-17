# ⚠️ Zināmie "uzkāršanās" riski un risinājumi

## 🔴 Augsta riska operācijas (bija problēmas)

### 1. Git/SSH komandas bez timeout
**Problēma:** `git pull/push` var gaidīt input vai tīklu uz bezgalību  
**Risinājums:** Vienmēr lietot `timeout` parametru
```javascript
// ❌ Nedroši
exec({ command: "git pull..." })

// ✅ Droši
exec({ command: "git pull...", timeout: 30 })
```

### 2. Garas exec komandas
**Problēma:** Komandas, kas aizņem >60 sekundēm var izraisīt timeout  
**Risinājums:**
- Lietot `background: true` ilgstošām operācijām
- Vai sadalīt mazākos gabaliņos

## 🟡 Vidēja riska operācijas

### 3. Sub-aģentu gaidīšana
**Problēma:** `sessions_spawn` + `subagents list` polling var aizņemt ilgu laiku  
**Risinājums:**
- Neveikt polling loop (nav jāpārbauda katras 10 sekundes)
- Izmantot `runTimeoutSeconds` sub-aģentiem
- Paļauties uz push-based completion

### 4. Atmiņas ierobežojumi
**Pašreizējais stāvoklis:**
- RAM: 3.7GB (1.2GB lietots, OK)
- Diska vieta: 29GB (11GB lietots, 17GB brīvi, OK)
- Swap: 2GB (neizmantots, OK)

**Risinājums:** Sekot līdzi `/tmp` un `~/.openclaw/logs` izmēram

### 5. API limits
**Problēma:** Kimi API var atgriezt rate limit kļūdas  
**Risinājums:**
- Nekādā gadījumā nestrādāt ar >150k tokeniem vienā sesijā
- Izmantot `compaction.mode = "safeguard"` (jau iestatīts)

## 🟢 Zema riska operācijas

### 6. Gateway restarts
**Problēma:** `openclaw gateway restart` pārtrauc visus procesus  
**Risinājums:**
- Neizpildīt gateway restart kamēr ir aktīvi sub-aģenti
- Pārbaudīt `openclaw status` pirms restarta

### 7. Canvas komandas bez node
**Problēma:** `canvas snapshot` kļūdājas, ja nav aktīva node  
**Risinājums:** Vienmēr pārbaudīt `nodes status` pirms canvas lietošanas

## 📋 Pārbaudes saraksts (ja iestrēgstu)

1. **Pārbaudīt timeout:** Vai komandai bija `timeout` parametrs?
2. **Pārbaudīt tīklu:** `curl -m 5 https://api.github.com`
3. **Pārbaudīt resursus:** `df -h && free -h`
4. **Pārbaudīt gateway:** `openclaw status`
5. **Pārbaudīt sub-aģentus:** `subagents list`

## 🛠️ Iestatījumi, kas palīdz izvairīties no problēmām

### ~/.openclaw/openclaw.json
```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8
      },
      "compaction": {
        "mode": "safeguard"
      }
    }
  }
}
```

## 🚨 Ko darīt, ja iestrēgstu

1. **Nosūtīt `/new`** - izveidot jaunu sesiju
2. **Nosūtīt `/reset`** - atiestatīt esošo sesiju  
3. **Pagaidīt 30 sekundes** - varbūt komanda tikai ir lēna
4. **Pārbaudīt** vai nav kāda fona procesa: `process(action="list")`

---
*Atjaunots: 2026-02-17*