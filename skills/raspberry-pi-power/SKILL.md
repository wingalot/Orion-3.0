# raspberry-pi-power

Raspberry Pi vadība (izslēgšana, restartēšana) caur Oreo komandām.

## Apraksts

Šis skills ļauj Oreo (galvenajam aģentam) kontrolēt Raspberry Pi barošanu - izslēgt vai restartēt ierīci pēc lietotāja komandas.

## Kad izmantot

- Kad lietotājs vēlas izslēgt Raspberry Pi
- Kad lietotājs vēlas restartēt Raspberry Pi
- Kad nepieciešams attālināti pārvaldīt Raspberry Pi barošanas stāvokli

## Drošības brīdinājumi

⚠️ **Uzmanību!**

- Izslēgšana vai restartēšana pārtrauks visas tekošās operācijas
- Pēc izslēgšanas Oreo nebūs pieejams, kamēr ierīce netiks manuāli ieslēgta
- Restartēšana aizņems 30-60 sekundes, laikā kura Oreo nebūs pieejams
- Pārliecinieties, ka nav svarīgu, nesaglabātu darbu pirms izslēgšanas
- Nepieciešamas sudo tiesības bez paroles (skatīt instrukciju)

## Lietošana

### Izslēgt Raspberry Pi:
Lietotājs saka: "Oreo, izslēdz datoru"
→ Oreo izpilda: `sudo shutdown -h now`

### Restartēt Raspberry Pi:
Lietotājs saka: "Oreo, restartē datoru"
→ Oreo izpilda: `sudo reboot`

## Failu struktūra

```
skills/raspberry-pi-power/
├── SKILL.md              # Šis fails
├── skill.json            # Metadati
└── scripts/
    ├── shutdown.sh       # Izslēgšanas skripts
    └── reboot.sh         # Restartēšanas skripts
```

## Skripti

- `scripts/shutdown.sh` - Droša Raspberry Pi izslēgšana ar apstiprinājuma pārbaudi un žurnālu
- `scripts/reboot.sh` - Droša Raspberry Pi restartēšana ar apstiprinājuma pārbaudi un žurnālu

## Atkarības

- `sudo` tiesības bez paroles komandām `shutdown` un `reboot`
- Shell skriptu izpildes tiesības

## Autors

Izveidots Oreo ekosistēmai
