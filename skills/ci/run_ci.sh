#!/bin/bash
# Or3o CI - Local Validation Script
# Šis skripts pārbauda jaunas izmaiņas, veic 'git pull' un palaiž 'ci/skill_validator.py'.
# Ja validācija neizdodas, tas sūta ziņu caur 'openclaw message send'.

# Nodrošinām, ka openclaw komanda ir atrasta (pieņemot standarta instalāciju)
export PATH="$PATH:/usr/local/bin:/usr/bin:/home/elvis/.npm-global/bin"

REPO_DIR="/home/elvis/.openclaw/workspace"
VALIDATOR="$REPO_DIR/ci/skill_validator.py"
LOG_FILE="$REPO_DIR/skills/ci/ci.log"
FAILURE_FILE="$REPO_DIR/skills/ci/last_failure.json"

# Pārliecināmies, ka esam pareizajā mapē
cd "$REPO_DIR" || { echo "Nevaru atrast $REPO_DIR"; exit 1; }

# Pārbauda, vai ir jaunas izmaiņas (fetch bez merge)
git fetch origin main > /dev/null 2>&1
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

# Ja lokālais HEAD atšķiras no attālinātā, veicam atjauninājumu
if [ "$LOCAL" != "$REMOTE" ]; then
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$TIMESTAMP] Saņemtas izmaiņas ($REMOTE). Atjaunoju..." >> "$LOG_FILE"
    
    # Veicam pull
    if git pull origin main >> "$LOG_FILE" 2>&1; then
        echo "[$TIMESTAMP] Git pull veiksmīgs. Palaižu validāciju..." >> "$LOG_FILE"
        
        # Palaižam validatoru un saglabājam izeju
        OUTPUT=$(python3 "$VALIDATOR" 2>&1)
        EXIT_CODE=$?

        if [ $EXIT_CODE -ne 0 ]; then
            echo "❌ Validācijas kļūda!" >> "$LOG_FILE"
            echo "$OUTPUT" > "$FAILURE_FILE"
            
            # Sūtam ziņu caur OpenClaw
            # Jāpārliecinās, ka pēdiņas netraucē JSON
            ESCAPED_OUTPUT=$(echo "$OUTPUT" | sed 's/"/\\"/g' | head -n 20) # Ierobežojam garumu
            MESSAGE="❌ Or3o CI Kļūda!\n\nKods nav validēts:\n$ESCAPED_OUTPUT"
            
            openclaw message send --message "$MESSAGE"
        else
            echo "✅ Validācija veiksmīga." >> "$LOG_FILE"
            rm -f "$FAILURE_FILE"
            
            # Optional: Ziņot par veiksmīgu atjauninājumu?
            # openclaw message send --message "✅ Or3o CI: Atjaunināts veiksmīgi ($REMOTE)"
        fi
    else
        echo "❌ Git pull neizdevās!" >> "$LOG_FILE"
        openclaw message send --message "❌ Or3o CI: Neizdevās veikt git pull!"
    fi
else
    # Nav izmaiņu - neko nedarām
    :
fi
