#!/bin/bash
# OpenClaw CI & Cron Setup Script
# Šis skripts atjauno Cron darbu un tiesības pēc repozitorija klonēšanas.

REPO_DIR="/home/elvis/.openclaw/workspace"
CI_DIR="$REPO_DIR/skills/ci"
LOG_FILE="$CI_DIR/setup.log"

echo "$(date): Sāku CI uzstādīšanu..." >> "$LOG_FILE"

# 1. Piešķirt tiesības skriptiem
chmod +x "$CI_DIR/run_ci.sh"
if [ -f "$CI_DIR/notify_on_fail.sh" ]; then
    chmod +x "$CI_DIR/notify_on_fail.sh"
fi

# 2. Pievienot Cron darbu (ja nav jau pievienots)
CRON_JOB="*/5 * * * * $CI_DIR/run_ci.sh >> $CI_DIR/cron.log 2>&1"

# Pārbaudām, vai cron jau satur šo rindu
CURRENT_CRON=$(crontab -l 2>/dev/null)
if echo "$CURRENT_CRON" | grep -q "$CI_DIR/run_ci.sh"; then
    echo "Cron darbs jau eksistē. Izlaižu." >> "$LOG_FILE"
else
    echo "Pievienoju Cron darbu..." >> "$LOG_FILE"
    (echo "$CURRENT_CRON"; echo "$CRON_JOB") | crontab -
fi

echo "$(date): CI uzstādīšana pabeigta." >> "$LOG_FILE"
