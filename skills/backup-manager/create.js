const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Konfigurācija un argumentu apstrāde
const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const sourceArgIndex = args.indexOf('--source');

// Noklusētie ceļi
const DEFAULT_BACKUP_DIR = process.env.BACKUP_DIR || '/home/elvis/backups';
const DEFAULT_SOURCE_DIR = process.env.WORKSPACE_DIR || '/home/elvis/.openclaw/workspace';

const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : DEFAULT_BACKUP_DIR;
const SOURCE_DIR = sourceArgIndex !== -1 ? args[sourceArgIndex + 1] : DEFAULT_SOURCE_DIR;

// Pārbauda vai avots eksistē
if (!fs.existsSync(SOURCE_DIR)) {
  console.error(`Kļūda: Avota mape ${SOURCE_DIR} neeksistē.`);
  process.exit(1);
}

// Izveido backup mapi, ja tā neeksistē
if (!fs.existsSync(BACKUP_DIR)) {
  console.log(`Izveido backup mapi: ${BACKUP_DIR}`);
  fs.mkdirSync(BACKUP_DIR, { recursive: true });
}

// Ģenerē faila nosaukumu ar laika zīmogu
const now = new Date();
const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
const filename = `backup-${timestamp}.tar.gz`;
const backupPath = path.join(BACKUP_DIR, filename);

console.log(`Veido backup no: ${SOURCE_DIR}`);
console.log(`Saglabā uz: ${backupPath}`);

try {
  // Izmanto 'tar' komandu
  // -c: create, -z: gzip, -f: file, -C: change dir
  // Mēs ejam uz avota mapi un arhivējam visu tās saturu (.), lai struktūra būtu pareiza
  execSync(`tar -czf "${backupPath}" -C "${SOURCE_DIR}" .`, { stdio: 'inherit' });
  console.log(`Backup veiksmīgi izveidots: ${filename}`);
  
  // Automātiska veco kopiju tīrīšana
  const cleanupScript = path.join(__dirname, 'cleanup.js');
  if (fs.existsSync(cleanupScript)) {
    console.log('Izpilda automātisko tīrīšanu...');
    execSync(`node "${cleanupScript}" --dir "${BACKUP_DIR}"`, { stdio: 'inherit' });
  }

} catch (err) {
  console.error('Kļūda backup veidošanas laikā:', err.message);
  process.exit(1);
}
