# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### SSH Hosts

| Alias | Adrese | Lietotājs | Piezīmes |
|-------|--------|-----------|----------|
| `elvis` | 192.168.1.145 | oreo | Raspberry Pi + OpenClaw gateway |
| `kimi-local` | 192.168.1.145 | - | LLM API (key-based auth) |

**Piekļuve:** `ssh elvis`

---

### TTS (Teksts → Runa)

| Parametrs | Vērtība | Piezīmes |
|-----------|---------|----------|
| **Noklusējuma balss** | `onyx` | Dziļa vīriešu balss |
| **Alternatīvas** | `echo` | Silta vīriešu |
| | `fable` | Britu akcents |
| | `nova` | Draudzīga sieviešu |
| **Ātrums** | `1.0` | Noklusējuma |
| **Audio atskaņošana** | `ffplay -nodisp -autoexit` | Raspberry Pi |

**Piemērs:**
```bash
/home/oreo/.openclaw/workspace/orion-skills/skills/openai-tts/scripts/speak.sh \
  "Teksts" --voice onyx --speed 0.9 --out /tmp/output.mp3
```

---

### Ierīces

| Ierīce | Lokācija | Piezīmes |
|--------|----------|----------|
| **Raspberry Pi** | 192.168.1.145 | OpenClaw gateway (port 18789), VNC (5900), Tailscale |
| **OpenAI API** | api.openai.com | TTS, Whisper, GPT - key saglabāts env |

---

### LLM Endpoints

- **kimi-local** → 192.168.1.145, key-based auth, bez lietotāja/paroles

---

### Noderīgas Komandas

```bash
# Sistēmas statuss
openclaw gateway status
openclaw cron list

# Atmiņas pārvalde
ls -la ~/.openclaw/workspace/memory/
cat ~/.openclaw/workspace/MEMORY.md

# Git operācijas
~/workspace/ git status
cd ~/.openclaw/workspace && git log --oneline -5
```

Add whatever helps you do your job. This is your cheat sheet.
