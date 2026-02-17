# Raspberry Pi Power Control - Instrukcija

## Kā lietot

### No Oreo (galvenais aģents)

1. **Izslēgšana** - Saki: *"Oreo, izslēdz datoru"*
2. **Restartēšana** - Saki: *"Oreo, restartē datoru"*

Oreo automātiski:
- Jautās apstiprinājumu
- Paziņos par gaidāmo dīkstāvi
- Izpildīs attiecīgo komandu

### Tiešā veidā (terminalā)

```bash
# Izslēgšana
cd /home/oreo/.openclaw/workspace/orion-skills/skills/raspberry-pi-power
./scripts/shutdown.sh

# Restartēšana
./scripts/reboot.sh
```

## Drošības ieteikumi

### Pirms izslēgšanas:
- ✅ Pārliecinies, ka nav nesaglabātu failu
- ✅ Pārbaudi vai nevienam citam lietotājam nav aktīvu sesiju
- ✅ Aizver visas atvērtās programmas
- ✅ Saglabā svarīgos datus

### Pēc izslēgšanas:
- 🔴 Oreo nebūs pieejams, kamēr ierīce netiks manuāli ieslēgta
- 🔴 Fiziski jānospiež barošanas poga vai jāpieslēdz barošana

### Pēc restartēšanas:
- ⏱️ Jāgaida 30-60 sekundes, līdz Raspberry Pi pilnībā ielādējas
- ⏱️ Oreo kļūs pieejams automātiski pēc sistēmas ielādes

## Nepieciešamās tiesības (sudo bez paroles)

Lai skripti strādātu, lietotājam `oreo` jābūt sudo tiesībām bez paroles šīm komandām:

### 1. Atver sudoers failu
```bash
sudo visudo
```

### 2. Pievieno šo rindiņu faila beigās
```
oreo ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/poweroff, /sbin/reboot, /sbin/halt
```

### 3. Saglabā un aizver (Ctrl+X, tad Y, tad Enter)

### 4. Pārbaudi vai darbojas
```bash
sudo -n shutdown --help
```

Ja neizmet kļūdu par paroli - viss ir kārtībā!

## Alternatīvas (ja skripts nestrādā)

### Ja Oreo nav pieejams, vari izmantot SSH:
```bash
ssh oreo@<raspberry-pi-ip>
sudo shutdown -h now      # Izslēgšana
sudo reboot               # Restartēšana
```

### Fiziska piekļuve:
- Nospied un turi barošanas pogu 3-5 sekundes (izslēgšana)
- Atslēdz un pieslēdz barošanu (restartēšana)

### Caur sistēmas komandām:
```bash
# Izslēgšana
sudo poweroff
sudo halt
sudo shutdown -P now

# Restartēšana
sudo reboot
sudo shutdown -r now
sudo systemctl reboot
```

## Žurnālu apskate

Visas darbības tiek reģistrētas:
```bash
sudo tail -f /var/log/raspberry-pi-power.log
```

## Problēmu risināšana

| Problēma | Risinājums |
|----------|------------|
| "Nepieciešamas sudo tiesības" | Pievieno lietotāju sudoers failā (skatīt augšpusē) |
| "Permission denied" | Pārbaudi skriptu izpildes tiesības: `chmod +x scripts/*.sh` |
| Komanda nestrādā | Pārbaudi vai komandas eksistē: `which shutdown` |
| Nevar saglabāt žurnālu | Pārbaudi `/var/log` direktorijas tiesības |

## Saistītie faili

- `skills/raspberry-pi-power/SKILL.md` - Skill dokumentācija
- `skills/raspberry-pi-power/skill.json` - Skill metadati
- `skills/raspberry-pi-power/scripts/shutdown.sh` - Izslēgšanas skripts
- `skills/raspberry-pi-power/scripts/reboot.sh` - Restartēšanas skripts

---

*Izveidots: 2026-02-17*  
*Versija: 1.0.0*
