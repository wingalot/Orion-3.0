#!/bin/bash
# Wrapper skripts priekš Cron
# Palaiž run_ci.sh un izvada kļūdu tekstu, ja tāds ir.

/home/elvis/.openclaw/workspace/skills/ci/run_ci.sh

FAILURE_FILE="/home/elvis/.openclaw/workspace/skills/ci/last_failure.json"

if [ -f "$FAILURE_FILE" ]; then
    echo "❌ Or3o CI: Validācijas kļūda!"
    echo "Kļūdas detaļas:"
    cat "$FAILURE_FILE"
    # Pēc ziņošanas izdzēšam failu, lai neatkārtotos
    rm "$FAILURE_FILE"
fi
