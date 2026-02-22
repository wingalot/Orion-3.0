#!/bin/bash
#
# SAFE-PROCESS-KILL.sh - Droša procesu pārtraukšana
# 
# LIETOŠANA:
#   ./safe-process-kill.sh <process_name> [signal]
#
# PIEMĒRI:
#   ./safe-process-kill.sh felix_auto_executor
#   ./safe-process-kill.sh node -15
#
# DROŠĪBAS PRINCIPI:
#   1. SIGTERM (-15) pirms SIGKILL (-9)
#   2. Exact match (-x) pirms full match (-f)
#   3. || true - lai nebūtu kļūdas, ja procesa nav
#

set -o pipefail

PROCESS_NAME="$1"
SIGNAL="${2:--15}"  # Default: SIGTERM

if [ -z "$PROCESS_NAME" ]; then
    echo "❌ Usage: $0 <process_name> [signal]"
    echo "   Example: $0 felix_auto_executor"
    exit 1
fi

echo "🔍 Checking for process: $PROCESS_NAME"

# 1. Mēģinām exact match ar SIGTERM (polite)
echo "📤 Sending SIGTERM to exact match..."
pkill "$SIGNAL" -x "$PROCESS_NAME" 2>/dev/null || true

# 2. Gaidām mazliet
sleep 1

# 3. Pārbaudām vai vēl dzīvs
if pgrep -x "$PROCESS_NAME" > /dev/null 2>&1; then
    echo "⚠️ Process still running, trying full match..."
    pkill "$SIGNAL" -f "$PROCESS_NAME" 2>/dev/null || true
    sleep 1
fi

# 4. Ja vēl joprojām dzīvs, SIGKILL (force)
if pgrep -x "$PROCESS_NAME" > /dev/null 2>&1; then
    echo "💀 Process resistant, sending SIGKILL..."
    pkill -9 -x "$PROCESS_NAME" 2>/dev/null || true
    sleep 1
fi

# 5. Pārbaudām rezultātu
if pgrep -x "$PROCESS_NAME" > /dev/null 2>&1; then
    echo "❌ Failed to terminate: $PROCESS_NAME"
    exit 1
else
    echo "✅ Process terminated: $PROCESS_NAME"
    exit 0
fi
