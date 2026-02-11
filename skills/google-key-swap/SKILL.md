# Google Key Swap Skill

Droša Google API atslēgas nomaiņas prasme. Tā veic validāciju pirms izmaiņu saglabāšanas, lai novērstu sistēmas darbības traucējumus ar nederīgu atslēgu.

## Lietošana

Lai nomainītu galveno Google API atslēgu (`google:default` profilam):

```bash
node skills/google-key-swap/swap.js <JAUNĀ_API_ATSLĒGA>
```

## Kā tas strādā

1.  **Validācija:** Skripts vispirms veic testa pieprasījumu Google Generative AI API (saraksta modeļus), izmantojot jauno atslēgu.
2.  **Drošības slēdzis:** Ja API atgriež kļūdu (403, 400, tīkla kļūda utt.), skripts apstājas un **NEVEIC** izmaiņas konfigurācijā. Vecā atslēga paliek aktīva.
3.  **Atjaunināšana:** Ja jaunā atslēga ir derīga, skripts atjaunina `openclaw.json` failu (`env.vars.GOOGLE_API_KEY_google_default`).
4.  **Restarts:** Skripts automātiski izsauc `openclaw gateway restart`, lai lietotu jauno konfigurāciju.

## Atkarības

- Node.js (v18+)
- `openclaw` CLI (jābūt pieejamam PATH vai instalētam globāli)
- Tiek izmantotas tikai iebūvētās Node.js bibliotēkas (`fs`, `https`, `child_process`).
