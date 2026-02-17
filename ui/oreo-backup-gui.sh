#!/bin/bash
# Oreo Backup/Restore GUI

while true; do
    CHOICE=$(zenity --list \
        --title="🦝 Oreo Backup" \
        --text="Izvēlies darbību:" \
        --column="Darbība" --column="Apraksts" \
        "💾 Backup" "Izveidot jaunu backup" \
        "🔄 Restore" "Atjaunot no backup" \
        "📋 Saraksts" "Apskatīt backup failus" \
        "🧹 Cleanup" "Notīrīt vecos backup'us" \
        "❌ Iziet" "Aizvērt programmu" \
        --width=400 --height=300 2>/dev/null)

    case "$CHOICE" in
        "💾 Backup")
            NAME=$(zenity --entry --title="Backup nosaukums" --text="Ievadi backup nosaukumu (vai atstāj tukšu):" --entry-text="oreo-$(date +%Y%m%d-%H%M)")
            if [ $? -eq 0 ]; then
                (echo "10"; echo "# Sagatavo..."
                 sleep 1
                 echo "50"; echo "# Veido backup..."
                 oreo-backup create --name "$NAME" 2>&1
                 echo "100"; echo "# Pabeigts!") | \
                zenity --progress --title="Backup" --text="Notiek backup izveide..." --percentage=0 --auto-close
                zenity --info --title="✅ Gatavs" --text="Backup veiksmīgi izveidots!"
            fi
            ;;
        "🔄 Restore")
            if zenity --question --title="⚠️ Brīdinājums" --text="Atjaunošana pārrakstīs esošo workspace!\n\nTurpināt?" 2>/dev/null; then
                (echo "10"; echo "# Atjauno..."
                 cd ~/.openclaw/workspace && node orion-skills/skills/restore-backup/restore.js --force 2>&1
                 echo "100"; echo "# Pabeigts!") | \
                zenity --progress --title="Restore" --text="Notiek atjaunošana..." --percentage=0 --auto-close
                zenity --info --title="✅ Gatavs" --text="Atjaunošana pabeigta!\n\nRestartē OpenClaw lai ielādētu atjaunoto workspace."
            fi
            ;;
        "📋 Saraksts")
            LIST=$(oreo-backup list 2>&1)
            zenity --text-info --title="Backup saraksts" --width=500 --height=300 --filename=<(echo "$LIST")
            ;;
        "🧹 Cleanup")
            KEEP=$(zenity --scale --title="Cleanup" --text="Cik jaunākos backup saglabāt?" --min-value=2 --max-value=20 --value=5)
            if [ $? -eq 0 ]; then
                oreo-backup cleanup --keep $KEEP 2>&1 | zenity --text-info --title="Cleanup rezultāts" --width=400 --height=200
            fi
            ;;
        "❌ Iziet"|*)
            break
            ;;
    esac
done