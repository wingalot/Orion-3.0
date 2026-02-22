---
name: datetime
description: Get current date, time, and day of week. Use when the user asks for current time, date, day of week, or when you need to verify today's date. Formats output in Latvian by default.
---

# Datetime Skill

Provides current date and time information with Latvian localization.

## Usage

### Get current timestamp (ISO 8601)
```bash
./scripts/now.sh
```

### Get formatted date/time in Latvian
```bash
./scripts/now.sh --format "full"     # Sestdiena, 2026. gada 22. februāris, 18:03
./scripts/now.sh --format "date"     # 2026. gada 22. februāris
./scripts/now.sh --format "time"     # 18:03
./scripts/now.sh --format "day"      # Svētdiena
```

### Get raw components
```bash
./scripts/now.sh --json
```

## When to Use

- User asks "What time is it?" / "Cik pulkstens?"
- User asks "What day is today?" / "Kāda šodien diena?"
- User asks for current date
- You need to verify today's date before making statements about it
- Scheduling reminders or cron jobs

## Timezone

Uses Europe/Riga (GMT+2) by default. Set TZ env var to override.
