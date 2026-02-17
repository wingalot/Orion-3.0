#!/bin/bash

# Raspberry Pi drošas restartēšanas skripts
# Autors: Oreo
# Versija: 1.0.0

LOG_FILE="/var/log/raspberry-pi-power.log"

# Funkcija žurnāla ierakstīšanai
log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE" 2>/dev/null || echo "[$timestamp] $1"
}

# Funkcija kļūdas paziņošanai un iziešanai
error_exit() {
    echo "❌ Kļūda: $1" >&2
    log_message "KĻŪDA: $1"
    exit 1
}

# Pārbaudīt vai skripts darbojas uz Raspberry Pi (Linux)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    error_exit "Šis skripts ir paredzēts tikai Linux/Raspberry Pi sistēmām"
fi

# Pārbaudīt sudo tiesības
if ! sudo -n true 2>/dev/null; then
    error_exit "Nepieciešamas sudo tiesības bez paroles. Skatīt Instrukcijas/raspberry_pi_power_instrukcija.md"
fi

# Paziņot par plānoto restartēšanu
echo "🔄 Raspberry Pi tiks restartēts!"
echo "⚠️  Oreo nebūs pieejams ~30-60 sekundes."
echo ""
echo "Restartēšana notiks pēc 5 sekundēm..."
echo "Nospied Ctrl+C, lai atceltu."

# Gaidīt 5 sekundes, dodot iespēju atcelt
for i in 5 4 3 2 1; do
    echo -ne "\rRestartēšana pēc: $i sekundēm... "
    sleep 1
done
echo ""

# Ierakstīt žurnālā
log_message "Raspberry Pi restartēšana uzsākta lietotāja pēc"

# Izpildīt restartēšanu
log_message "Izpilda: sudo reboot"
echo "🔄 Restartē Raspberry Pi..."

if sudo reboot; then
    log_message "Restartēšanas komanda veiksmīgi izpildīta"
else
    error_exit "Neizdevās izpildīt reboot komandu"
fi
