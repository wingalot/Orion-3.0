const fs = require('fs');
const path = require('path');

// 1. Konfigurācijas definīcijas
const CONFIG_DIR = path.resolve(__dirname, '../../config');
const CHANNELS_FILE = path.join(CONFIG_DIR, 'channels.json');

// 2. Palīgfunkcijas
function ensureConfigDir() {
    if (!fs.existsSync(CONFIG_DIR)) {
        fs.mkdirSync(CONFIG_DIR, { recursive: true });
    }
}

function loadChannels() {
    if (!fs.existsSync(CHANNELS_FILE)) {
        return [];
    }
    const data = fs.readFileSync(CHANNELS_FILE, 'utf8');
    try {
        return JSON.parse(data);
    } catch (e) {
        return [];
    }
}

function saveChannels(channels) {
    fs.writeFileSync(CHANNELS_FILE, JSON.stringify(channels, null, 2));
}

// 3. Ievades parsēšana
const args = process.argv.slice(2);
const channelId = args[0];
const channelName = args[1];
const inviteLink = args[2] || null;

// 4. Validācija (Deterministiska)
const errors = [];
if (!channelId || !/^-?[0-9]+$/.test(channelId)) {
    errors.push(`Kļūda: 'channelId' ir obligāts un tam jābūt ciparu virknei. Saņemts: ${channelId}`);
}
if (!channelName || channelName.length < 3) {
    errors.push("Kļūda: 'name' ir obligāts un tam jābūt vismaz 3 simboliem.");
}
if (inviteLink && !/^https:\/\/t\.me\/.*$/.test(inviteLink)) {
    errors.push("Kļūda: 'invite_link' jābūt 'https://t.me/...' formātā.");
}

// 5. Kļūdu apstrāde
if (errors.length > 0) {
    console.log(JSON.stringify({ status: 'error', messages: errors }));
    process.exit(1);
}

// 6. Izpilde
ensureConfigDir();
let channels = loadChannels();

// Pārbaudīt dublikātu
const existingIndex = channels.findIndex(c => c.id === channelId);
if (existingIndex > -1) {
    // Atjaunināt esošu
    channels[existingIndex] = { id: channelId, name: channelName, link: inviteLink, updated_at: new Date().toISOString() };
    saveChannels(channels);
    console.log(JSON.stringify({ status: 'success', message: `Kanāls ${channelId} atjaunināts.` }));
} else {
    // Pievienot jaunu
    channels.push({ id: channelId, name: channelName, link: inviteLink, created_at: new Date().toISOString() });
    saveChannels(channels);
    console.log(JSON.stringify({ status: 'success', message: `Kanāls ${channelId} pievienots.` }));
}
