#!/bin/bash
# now.sh - Get current date/time with Latvian formatting

# Default timezone
TZ="${TZ:-Europe/Riga}"
export TZ

# Parse arguments
FORMAT="${1:---format}"
VALUE="${2:-full}"

if [[ "$1" == "--json" ]]; then
    # JSON output
    date '{
    "iso": "%Y-%m-%dT%H:%M:%S%z",
    "date": "%Y-%m-%d",
    "time": "%H:%M",
    "time_full": "%H:%M:%S",
    "year": "%Y",
    "month": "%m",
    "day": "%d",
    "weekday_en": "%A",
    "weekday_lv": "",
    "timezone": "'"$TZ"'"
}'
    exit 0
fi

# Latvian weekday names (1=Monday, 7=Sunday)
WEEKDAY_NUM=$(date +%u)
WEEKDAY_LV=""

case "$WEEKDAY_NUM" in
    1) WEEKDAY_LV="Pirmdiena" ;;
    2) WEEKDAY_LV="Otrdiena" ;;
    3) WEEKDAY_LV="Trešdiena" ;;
    4) WEEKDAY_LV="Ceturtdiena" ;;
    5) WEEKDAY_LV="Piektdiena" ;;
    6) WEEKDAY_LV="Sestdiena" ;;
    7) WEEKDAY_LV="Svētdiena" ;;
esac

# Latvian month names
MONTH_NUM=$(date +%m)
MONTH_LV=""
case "$MONTH_NUM" in
    01) MONTH_LV="janvāris" ;;
    02) MONTH_LV="februāris" ;;
    03) MONTH_LV="marts" ;;
    04) MONTH_LV="aprīlis" ;;
    05) MONTH_LV="maijs" ;;
    06) MONTH_LV="jūnijs" ;;
    07) MONTH_LV="jūlijs" ;;
    08) MONTH_LV="augusts" ;;
    09) MONTH_LV="septembris" ;;
    10) MONTH_LV="oktobris" ;;
    11) MONTH_LV="novembris" ;;
    12) MONTH_LV="decembris" ;;
esac

YEAR=$(date +%Y)
DAY=$(date +%d)
TIME=$(date +%H:%M)

# Output based on format
case "$VALUE" in
    "full")
        echo "$WEEKDAY_LV, $YEAR. gada $DAY. $MONTH_LV, $TIME"
        ;;
    "date")
        echo "$YEAR. gada $DAY. $MONTH_LV"
        ;;
    "time")
        echo "$TIME"
        ;;
    "day")
        echo "$WEEKDAY_LV"
        ;;
    *)
        echo "$WEEKDAY_LV, $YEAR. gada $DAY. $MONTH_LV, $TIME"
        ;;
esac
