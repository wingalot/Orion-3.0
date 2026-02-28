# 🧠 Oreo Atmiņa

## ⚠️ Svarīgi - Ko atcerēties

### Kļūdu apstrādes uzlabojumi (2026-02-17)

#### 🚨 Vienmēr ziņot par kļūdām
- **NEKAD** neapklust pēc `exec` kļūdas
- Vienmēr pateikt: "❌ Neizdevās, jo..."
- Piedāvāt risinājumu vai next step

#### 🗺️ Ceļu pārbaude
Pirms failu operācijām:
```
1. Pārbaudi ar `ls` vai `test -f`
2. Ja nav - meklē ar `find`
3. Ja atradi - pastāsti kur
4. Tad dari to, ko vajag
```

#### ⏱️ Timeout ir obligāts
```javascript
exec({ command: "...", timeout: 30 }) // Vienmēr!
```

#### 💬 Progress updates
- Pirms garas operācijas: "Sāku X, tas var aizņemt Y sekundes..."
- Pēc katra soļa: "✅ Solis N izdevās" vai "❌ Solis N neizdevās"

#### ⛓️ Sadalīt komandas
```javascript
// Slikti:
git add X && git commit && git push

// Labi:
git add X      // Pārbauda
[ziņo]
git commit     // Pārbauda  
[ziņo]
git push       // Pārbauda
[ziņo]
```

### Lietotāja preferances

- **Vārds:** Elvis
- **Laika josla:** Europe/Riga (GMT+2)
- **Valoda:** Latviešu (brīva, neformāla)
- **Repo:** github.com:wingalot/Orion-3.0
- **SSH:** Iestatīts un strādā

### Bīstamās zonas (kur biju "uzkāries")

1. **Git push bez timeout** ✅ Labots
2. **Nepareizi failu ceļi** ✅ Labots  
3. **Kļūdu apklusināšana** ✅ Tagad ziņoju
4. **Pārāk daudz && komandās** ✅ Sadalu

### Failu struktūra

```
~/.openclaw/workspace/
├── AGENTS.md, SOUL.md, USER.md, IDENTITY.md
├── orion-skills/           # Galvenais repo
│   ├── skills/             # Visi skilli
│   ├── Instrukcijas/       # Instrukcijas
│   ├── scripts/            # Palīg-skripti
│   └── ui/                 # Canvas UI
├── CRASH_PREVENTION.md     # Kļūdu prevencija
└── SELF_IMPROVEMENT.md     # Pašanalīze
```

## 🔧 Tehniskie iestatījumi

### Drošs exec pattern
```javascript
// 1. Pateikt, ko daru
"Daru X...";

// 2. Izpildīt ar timeout
const result = exec({ command: "X", timeout: 30 });

// 3. Pārbaudīt rezultātu
if (result.error) {
  "❌ Neizdevās: " + result.error;
  "Vai vēlies, lai mēģinu citādi?";
} else {
  "✅ Izdevās!";
}
```

### Git workflow
```bash
# 1. Pārbaudi statusu
git status

# 2. Add ar pārbaudi
ls FAILS.md && git add FAILS.md

# 3. Commit
git commit -m "ziņa"

# 4. Push ar timeout
git push origin master
```

### Balss ziņas (TTS) - 2026-02-28

#### ⚠️ SVARĪGI - TTS rīku atšķirības

**1. OpenClaw iebūvētais `tts` rīks:**
- ❌ **NEATBALSTA** `voice` parametru
- ❌ Izmanto cieti kodētu noklusējumu (nav `echo`)
- ✅ Ērts īsām ziņām

**2. `speak.sh` skripts (ieteicams):**
- ✅ Pilna kontrole pār balsi
- ✅ Noklusējumā `echo` (ja `OPENAI_TTS_VOICE=echo` .env)
- ✅ Var pārrakstīt ar `--voice`

#### ✅ Ieteicamie iestatījumi balss ziņām
- **Balss:** `echo` (vīriešu, silta) - **Noklusējums no 2026-02-28**
- **Ātrums:** `0.9` (nedaudz lēnāks, saprotamāks)
- **Alternatīvas balsis:**
  - `onyx` - vīriešu, dziļa autoritatīva
  - `fable` - britu akcents
  - `nova` - sieviešu, draudzīga

#### 🔑 API Key (AUTO-LOAD)
- **Atrašanās vieta:** `/home/oreo/.openclaw/workspace/orion-skills/skills/openai-tts/.env`
- **Skripts auto-lādē no .env** - vairs NAV jāexportē manuāli!
- **Pārbaudīts:** 2026-02-28 - strādā bez `export`

#### 🛠️ Pareizais veids balss ziņu sūtīšanai

```javascript
// ❌ SLIKTI - tts neatbalsta voice parametru
tts({ text: "Sveiki!", channel: "telegram" })  // Nav echo balss!

// ✅ LABI - izmantot speak.sh + message
const result = exec({
  command: './scripts/speak.sh "Sveiki, Elvis!" --out /tmp/msg.mp3',
  timeout: 30
});
message({ asVoice: true, filePath: "/tmp/msg.mp3", target: "395239117" });
```

**Pilna komanda:**
```bash
/home/oreo/.openclaw/workspace/orion-skills/skills/openai-tts/scripts/speak.sh \
  "Sveiki, Elvis! Šeit Oreo." \
  --voice echo \
  --speed 0.9 \
  --out /tmp/message.mp3
```
1. **OpenAI TTS** (labākā kvalitāte) - API key saglabāts
   - `voice=nova` - draudzīga sieviešu
   - `voice=onyx` - dziļa vīriešu (izmanto šo!)
   - `voice=alloy` - neitrāla
   - `voice=echo` - silta vīriešu
   - `voice=shimmer` - maiga sieviešu
   - `voice=fable` - britu akcents

2. **espeak** (bezmaksas, robotiska) - ar latviešu valodu
   - `espeak -vlv "Teksts" -w output.wav`

3. **pico2wave** - labāka kvalitāte par espeak, bet tikai EN/DE/ES/FR/IT

#### 🔊 Audio atskaņošana uz Raspberry Pi
```bash
ffplay -nodisp -autoexit /tmp/audio.mp3
# vai
aplay /tmp/audio.wav
```

#### 📤 Balss ziņu sūtīšana uz Telegram
```bash
# TTS ar OpenAI + sūtīšana
export OPENAI_API_KEY="..."
/home/oreo/.openclaw/workspace/orion-skills/skills/openai-tts/scripts/speak.sh "Teksts" --voice onyx --speed 0.9 --out /tmp/output.mp3
# Tad message tool ar asVoice=true un filePath
```

#### 📥 Balss ziņu uztveršana no Telegram
- Audio fails tiek saglabāts: `/home/oreo/.openclaw/media/inbound/`
- Formāts: `.ogg` (opus codec)
- Transkripcija ar Whisper API

### 🎙️ Whisper (Runa → Teksts)

#### OpenAI Whisper API
- **Lokācija:** `/home/oreo/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/`
- **Skripts:** `scripts/transcribe.sh`
- **Izmantošana:**
```bash
export OPENAI_API_KEY="..."
/home/oreo/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh audio.ogg --language lv --out result.txt
```

**Piezīmes:**
- Labāk darbojas ar angļu valodu (`--language en`)
- Latviešu saprot, bet ar kļūdām
- Atbalsta: `.ogg`, `.mp3`, `.wav`, `.m4a`

#### Lokālais Whisper
- Statuss: ❌ Nav instalēts (smags uz Raspberry Pi)
- Alternatīva: API versija ir ātrāka un vienkāršāka

#### 🎙️ Voicebox (balss klonēšana)
- **Links:** https://github.com/jamiepine/voicebox
- **Kas tas:** Lokāls balss klonēšanas rīks (Qwen3-TTS)
- **Statuss:** Linux builds "coming soon" - pagaidām tikai macOS/Windows
- **Var iespējot vēlāk, kad būs Linux versija**

### 📧 Gmail Sender Skill

**Lokācija:** `/home/oreo/.openclaw/workspace/orion-skills/skills/gmail-sender/`

**Pielabojums (2026-02-20):**
- ✅ RFC 2047 encoding latviešu burtiem virsrakstos
- Commit: `1c41f1b` - Fix: Add RFC 2047 encoding for non-ASCII email subjects

**Lietošana:**
```bash
node send.js --to "epasts@example.com" --subject "Virsraksts" --message "Teksts"
```

### 🔗 SSH Piekļuve Raspberry Pi (Elvis)

**Adrese:** `192.168.1.145`  
**SSH Alias:** `elvis`  
**Auth:** Key-based (bez paroles)  
**Piekļuve:** `ssh elvis`  

**Kas tur ir:**
- Raspberry Pi ar OpenClaw gateway (port 18789)
- VNC serveris (port 5900)
- Tailscale
- Trading dashboard (felix_dashboard.py)

**Nav lokāla LLM API** — pašlaik tikai OpenClaw gateway, kas savienojas ar ārējo API.

---
*Atjaunots: 2026-02-20*
*Nākamā pārbaude: Kad lietotājs atgādinās*