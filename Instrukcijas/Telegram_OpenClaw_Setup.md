# OpenClaw Telegram Konfigurācijas Rokasgrāmata (2026.2.x Versija)

Šī instrukcija apraksta soli pa solim, kā savienot OpenClaw ar Telegram botu, balstoties uz veiksmīgu iestatīšanu.

## 1. Solis: Bota Iegūšana
1. Atver Telegram.
2. Atrodi **@BotFather**.
3. Uzraksti `/newbot` un seko instrukcijām.
4. Saglabā iegūto **Bot Token** (piemēram: `123456789:ABCDefGhIjKlmnOpqrStUvWxYz`).
5. Iegūsti savu **User ID** (uzraksti `/start` botam **@userinfobot**).

## 2. Solis: Konfigurācijas Faila Sagatavošana
Fails atrodas: `/home/elvis/.openclaw/openclaw.json`

**SVARĪGI:** Jaunajās OpenClaw versijās (2026.2.x) parametrs `allowedUsers` vairs netiek atbalstīts un izraisa kļūdu! Izmanto `dmPolicy: "pairing"`.

### Pareizais JSON fragments:
```json
{
  "plugins": {
    "entries": {
      "telegram": {
        "enabled": true
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "TAVS_TOKEN_ŠEIT",
      "dmPolicy": "pairing"
    }
  }
}
```

## 3. Solis: Servisa Restartēšana
Lai izmaiņas stātos spēkā, restartē OpenClaw gateway servisu terminālī:

```bash
openclaw gateway restart
```

Pārbaudi statusu, vai nav kļūdu:
```bash
openclaw gateway status
# VAI
tail -f /tmp/openclaw/openclaw-YYYY-MM-DD.log
```

## 4. Solis: Pārošana (Pairing)
Kad serviss darbojas:

1. Atver savu botu Telegramā.
2. Uzraksti `/start`.
3. Bots atbildēs ar **Pairing Code** (piemēram: `EF99Q7N8`).
4. Atgriezies terminālī (kur darbojas OpenClaw) un ievadi komandu:

```bash
openclaw pairing approve telegram TAVS_KODS
```
Piemēram: `openclaw pairing approve telegram EF99Q7N8`

## 5. Solis: Pārbaude
Ja komanda atgriež "Approved telegram sender <ID>", viss ir kārtībā.
Uzraksti botam: "Sveiks!" — ja saņem atbildi, sistēma darbojas.

---
**Piezīmes:**
- Ja redzi kļūdu `Unrecognized key: "allowedUsers"`, izdzēs šo rindu no `openclaw.json`.
- Ja `openclaw pairing approve` neatrod komandu, pārbaudi, vai pareizi uzrakstīji `approve telegram` (kanāls ir obligāts).
