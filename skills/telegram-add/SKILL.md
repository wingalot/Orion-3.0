# SKILL: Telegram Kanāla Pievienošana

## Apraksts
Pievieno vai atjaunina Telegram kanālu sistēmas konfigurācijā.
Darbība ir deterministiska:
- Ja kanāls eksistē (pēc ID), tas tiek **atjaunināts**.
- Ja kanāls neeksistē, tas tiek **izveidots**.
- Rezultāts tiek saglabāts lokālajā `config/channels.json` failā.

## Ievades parametri
1. `channel_id` (Obligāts): Unikāls ID ciparu formātā (piem., `-100123456789`).
2. `name` (Obligāts): Kanāla nosaukums.
3. `invite_link` (Neobligāts): Ielūguma saite (jāsākas ar `https://t.me/`).

## Izsaukšana (Piemērs)
Lai pievienotu kanālu, izmantojiet `node skills/telegram-add/index.js` ar argumentiem.

```bash
node skills/telegram-add/index.js <channel_id> <name> [invite_link]
```

### Piemērs 1 (Jauns kanāls):
```bash
node skills/telegram-add/index.js -100123456789 "Mans Kanāls" "https://t.me/example"
```

### Piemērs 2 (Bez saites):
```bash
node skills/telegram-add/index.js -100987654321 "Privāts Kanāls"
```

## Rezultāts
Prasme atgriež JSON objektu stdout plūsmā:
- `{ "status": "success", "message": "..." }`
- `{ "status": "error", "messages": [...] }`

## Kļūdu apstrāde
Ja saņemat `status: error`, labojiet ievades datus un mēģiniet vēlreiz.
Nemēģiniet labot kodu, labojiet tikai argumentus.
