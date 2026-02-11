# SKILL: Telegram Ziņu Sūtīšana

## Apraksts
Nosūta teksta ziņojumu uz norādīto Telegram kanālu vai lietotāju.
Izmanto `config/telegram.json` konfigurāciju, lai iegūtu `bot_token`.

## Ievades parametri
1. `channel_id` (Obligāts): Skaitlisks ID (piem., `123456789` vai `-100...`).
2. `message` (Obligāts): Teksts, kas jānosūta.
3. `parse_mode` (Neobligāts): Formatēšanas stils (`HTML`, `Markdown`, `None`). Pēc noklusējuma `HTML`.

## Izsaukšana (Piemērs)
Lai nosūtītu ziņu, izmantojiet `node skills/telegram-send/index.js` ar argumentiem.

```bash
node skills/telegram-send/index.js <channel_id> <message> [parse_mode]
```

### Piemērs 1 (Vienkārša ziņa):
```bash
node skills/telegram-send/index.js 395239117 "Labrīt!"
```

### Piemērs 2 (Ar HTML formatējumu):
```bash
node skills/telegram-send/index.js -100123456789 "<b>Svarīgi:</b> Sistēma atjaunināta." "HTML"
```

## Rezultāts
Prasme atgriež JSON objektu stdout plūsmā:
- `{ "status": "success", "message_id": 12345 }`
- `{ "status": "error", "error": "Kļūdas apraksts" }`

## Kļūdu apstrāde
Ja status=error, pārbaudiet:
1. Vai kanāla ID ir pareizs.
2. Vai bots ir pievienots kanālam kā administrators (ja tas ir kanāls).
3. Vai ziņas teksts nav pārāk garš (>4096 simboli).
