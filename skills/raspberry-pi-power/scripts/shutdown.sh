#!/bin/bash

# Raspberry Pi drošas izslēgšanas skripts
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

# Paziņot par plānoto izslēgšanu
echo "🔴 Raspberry Pi tiks izslēgts!"
echo "⚠️  Oreo nebūs pieejams, kamēr ierīce netiks manuāli ieslēgta."
echo ""
echo "Izslēgšana notiks pēc 5 sekundēm..."
echo "Nospied Ctrl+C, lai atceltu."

# Gaidīt 5 sekundes, dodot iespēju atcelt
for i in 5 4 3 2 1; do
    echo -ne "\rIzslēgšana pēc: $i sekundēm... "
    sleep 1
done
echo ""

# Ierakstīt žurnālā
log_message "Raspberry Pi izslēgšana uzsākta lietotāja pēc"

# Izpildīt izslēgšanu
log_message "Izpilda: sudo shutdown -h now"
echo "🔌 Izslēdz Raspberry Pi..."

if sudo shutdown -h now; then
    log_message "Izslēgšanas komanda veiksmīgi izpildīta"
else
    error_exit "Neizdevās izpildīt shutdown komandu"
fi
