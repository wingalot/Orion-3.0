# Gmail Sender

Sūta e-pastus un pārvalda kontaktus, izmantojot Gmail/People API.

## 🤖 AI Instrukcija (Setup)

Ja lietotājs vēlas izmantot šo prasmi, bet `credentials.json` vai `token.json` neeksistē:

1.  **Pārbaudi:** Vai faili `credentials.json` un `token.json` atrodas prasmju mapē.
2.  **Ja nav `credentials.json`:**
    *   Palūdz lietotājam izveidot **Google Cloud Console** projektu.
    *   Norādi: "Lūdzu, dodies uz https://console.cloud.google.com/apis/credentials".
    *   Instrukcijas lietotājam:
        *   Izveidot jaunu projektu (vai izmantot esošu).
        *   Sadaļā "Library" iespējot **Gmail API** un **People API**.
        *   Sadaļā "Credentials" izveidot **OAuth Client ID** -> **Desktop App**.
        *   Pievienot savu e-pastu kā "Test User" (OAuth consent screen).
        *   Lejupielādēt JSON failu un pārsaukt par `credentials.json`.
        *   Ievietot šo failu prasmju mapē.
3.  **Ja ir `credentials.json`, bet nav `token.json`:**
    *   Palaid komandu: `node auth.js`.
    *   Iedod lietotājam URL, ko izvada skripts.
    *   Palūdz lietotājam autorizēties un iekopēt atpakaļ saņemto kodu.
    *   Padod kodu skriptam (vai ievadi to, ja skripts gaida input).

## Lietošana

### Sūtīt e-pastu
```bash
node send.js --to <epasts> --subject <tēma> --message <ziņa>
```

### Meklēt kontaktus
```bash
node contacts.js --query "Vārds"
```
Lai izvadītu visus kontaktus: `node contacts.js --query "ALL"`

### Atjaunināt kontaktu
Pievieno jaunu e-pastu esošam kontaktam:
```bash
node update-contact.js --query "Vārds" --email "jauns@epasts.lv"
```

## Atkarības

- `googleapis`
