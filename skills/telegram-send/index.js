const fs = require('fs');
const path = require('path');

// 1. Konfigurācijas definīcijas
const CONFIG_FILE = path.resolve(__dirname, '../../config/telegram.json');

// 2. Palīgfunkcijas
function loadConfig() {
    if (!fs.existsSync(CONFIG_FILE)) {
        return null;
    }
    const data = fs.readFileSync(CONFIG_FILE, 'utf8');
    try {
        return JSON.parse(data);
    } catch (e) {
        return null;
    }
}

async function sendMessage(botToken, chatId, text, parseMode) {
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
    const params = {
        chat_id: chatId,
        text: text
    };
    if (parseMode && parseMode !== 'None') {
        params.parse_mode = parseMode;
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        const data = await response.json();
        if (data.ok) {
            return {
                status: 'success',
                message_id: data.result.message_id
            };
        } else {
            return {
                status: 'error',
                error: `Telegram API error: ${data.description}`
            };
        }
    } catch (e) {
        return {
            status: 'error',
            error: `Network error: ${e.message}`
        };
    }
}

// 3. Ievades parsēšana
const args = process.argv.slice(2);
const channelId = args[0];
const message = args[1];
const parseMode = args[2] || 'HTML';

// 4. Validācija (Deterministiska)
const errors = [];
if (!channelId || !/^-?[0-9]+$/.test(channelId)) {
    errors.push(`Kļūda: 'channel_id' jābūt skaitliskam. Saņemts: ${channelId}`);
}
if (!message || message.length < 1) {
    errors.push("Kļūda: 'message' nevar būt tukšs.");
}

if (errors.length > 0) {
    console.log(JSON.stringify({ status: 'error', error: errors.join(', ') }));
    process.exit(1);
}

// 5. Izpilde
const config = loadConfig();
if (!config || !config.bot_token) {
    console.log(JSON.stringify({ status: 'error', error: 'Konfigurācija (config/telegram.json) trūkst vai nav bot_token.' }));
    process.exit(1);
}

sendMessage(config.bot_token, channelId, message, parseMode).then(result => {
    console.log(JSON.stringify(result));
    process.exit(result.status === 'success' ? 0 : 1);
});
