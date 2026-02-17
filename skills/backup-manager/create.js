const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const nameArgIndex = args.indexOf('--name');

const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : '/home/oreo/backups';
const SOURCE_DIR = '/home/oreo/.openclaw/workspace';

// Izveidojam backup mapes nosaukumu ar timestamp
const now = new Date();
const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
const BACKUP_NAME = nameArgIndex !== -1 ? args[nameArgIndex + 1] : `oreo-backup-${timestamp}`;
const BACKUP_FILE = path.join(BACKUP_DIR, `${BACKUP_NAME}.tar.gz`);

// Pārbaudām vai backup mape eksistē
if (!fs.existsSync(BACKUP_DIR)) {
  console.log(`Mape ${BACKUP_DIR} neeksistē. Izveidoju...`);
  try {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  } catch (err) {
    console.error(`Kļūda izveidojot mapi ${BACKUP_DIR}:`, err.message);
    process.exit(1);
  }
}

// Pārbaudām vai source mape eksistē
if (!fs.existsSync(SOURCE_DIR)) {
  console.error(`Kļūda: Source mape ${SOURCE_DIR} neeksistē.`);
  process.exit(1);
}

console.log(`Backup avots: ${SOURCE_DIR}`);
console.log(`Backup mērķis: ${BACKUP_FILE}`);

try {
  // Izveidojam tar.gz arhīvu
  console.log('Notiek backup izveide...');
  
  // Pārejām uz vecāku mapi, lai arhīvā būtu "workspace" mape
  const parentDir = path.dirname(SOURCE_DIR);
  const dirName = path.basename(SOURCE_DIR);
  
  execSync(`tar -czf "${BACKUP_FILE}" -C "${parentDir}" "${dirName}"`, { 
    stdio: 'inherit',
    timeout: 60000 // 1 minūtes timeout
  });
  
  // Iegūstam faila izmēru
  const stats = fs.statSync(BACKUP_FILE);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  
  console.log('✅ Backup veiksmīgi izveidots!');
  console.log(`📁 Fails: ${BACKUP_FILE}`);
  console.log(`📊 Izmērs: ${sizeMB} MB`);
  console.log(`🕐 Laiks: ${now.toLocaleString('lv-LV')}`);
  
} catch (err) {
  console.error('❌ Kļūda backup izveidē:', err.message);
  process.exit(1);
}
