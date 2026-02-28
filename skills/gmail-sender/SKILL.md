---
name: gmail-sender
description: Send emails via Gmail SMTP and manage Google Contacts. Supports email sending with App Passwords, contact listing/search via Google People API, and contact updates. Latvian text fully supported with RFC 2047 encoding.
---

# Gmail Sender & Contacts

Send emails via Gmail SMTP and manage Google Contacts via People API.

## Features

- ✅ **Email Sending** - Via Gmail SMTP with App Passwords
- ✅ **Contact Management** - List, search, and update Google Contacts
- ✅ **Latvian Language** - Full support with RFC 2047 encoding
- ✅ **HTML Emails** - Rich formatting support

---

## Prerequisites

### For Email Sending (SMTP)
1. Gmail account with 2FA enabled
2. Gmail App Password (NOT your regular password)
   - Generate at: https://myaccount.google.com/apppasswords

### For Contact Management (Google API)
1. Google Cloud Console project
2. Gmail API and People API enabled
3. OAuth 2.0 credentials (Desktop App)
4. `credentials.json` and `token.json` files

---

## Configuration

### Email Sending (`.env`)
```bash
GMAIL_USER=your-email@gmail.com
GMAIL_PASS=your-app-password
```

### Contact Management
Place in skill root directory:
- `credentials.json` - OAuth client credentials from Google Cloud Console
- `token.json` - Generated after first OAuth authorization

**First-time setup:**
```bash
node auth.js
# Follow the URL, authorize, paste the code back
```

---

## Usage

### 📧 Send Email

```bash
# Basic
node scripts/send.js --to "recipient@example.com" --subject "Subject" --message "Body"

# HTML content
node scripts/send.js --to "recipient@example.com" --subject "Subject" --message "<h1>HTML</h1>" --html

# Multiple recipients
node scripts/send.js --to "a@example.com,b@example.com" --subject "Subject" --message "Body"
```

### 👥 List/Search Contacts

```bash
# List all contacts (369 total)
node contacts.js --query "ALL"

# Search by name
node contacts.js --query "Elvis"

# Search partial match
node contacts.js --query "EG"
```

### 📝 Update Contact

```bash
# Add email to existing contact
node update-contact.js --query "Vārds" --email "new@example.com"
```

---

## API Reference

### contacts.js

| Option | Description | Example |
|--------|-------------|---------|
| `--query` | Search string or "ALL" | `--query "John"`, `--query "ALL"` |

**Output format:**
```
- Name: John Doe
  Email: john@example.com
  Phone: +371 12345678
```

### update-contact.js

| Option | Description | Example |
|--------|-------------|---------|
| `--query` | Contact name to find | `--query "John Doe"` |
| `--email` | New email to add | `--email "new@example.com"` |

---

## File Structure

```
gmail-sender/
├── scripts/
│   └── send.js          # Email sending (SMTP)
├── contacts.js          # Contact search/list (Google API)
├── update-contact.js    # Contact update (Google API)
├── auth.js              # OAuth authorization
├── credentials.json     # Google OAuth credentials
├── token.json           # OAuth access token
└── .env                 # SMTP credentials
```

---

## Notes

- **Email limits:** ~500 emails/day for Gmail personal accounts
- **Latvian text:** Subject lines auto-encoded with RFC 2047
- **App Passwords:** 16-character codes, not your Gmail password
- **OAuth tokens:** `token.json` auto-refreshes, keep it secure

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Invalid login` | Check App Password in `.env` |
| `Token expired` | Run `node auth.js` again |
| `API disabled` | Enable Gmail + People API in Google Cloud Console |
| `No contacts found` | Check that account has contacts at https://contacts.google.com |

---

*Atjaunots: 2026-02-28*
