const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : '/home/elvis/backups';
const TARGET_DIR = '/home/elvis/.openclaw'; // Mērķa mape, kurā atrodas 'workspace'

if (!fs.existsSync(BACKUP_DIR)) {
  console.error(`Kļūda: Mape ${BACKUP_DIR} neeksistē.`);
  process.exit(1);
}

// 1. Find the newest backup
const files = fs.readdirSync(BACKUP_DIR)
  .map(file => {
    const filePath = path.join(BACKUP_DIR, file);
    return {
      name: file,
      path: filePath,
      time: fs.statSync(filePath).mtime.getTime()
    };
  })
  .filter(f => f.name.includes('backup') && (f.name.endsWith('.tar.gz') || f.name.endsWith('.zip')))
  .sort((a, b) => b.time - a.time);

if (files.length === 0) {
  console.error('Kļūda: Rezerves kopijas netika atrastas.');
  process.exit(1);
}

const latestBackup = files[0];
console.log(`Jaunākā rezerves kopija: ${latestBackup.name}`);
console.log(`Atjaunošanas mērķis: ${TARGET_DIR}/workspace`);

try {
  // 2. Extract the backup
  // Pieņemam, ka arhīvā ir 'workspace' mape
  console.log('Notiek atjaunošana...');
  execSync(`tar -xzf "${latestBackup.path}" -C "${TARGET_DIR}"`, { stdio: 'inherit' });
  console.log('Faili atjaunoti veiksmīgi.');

  // 3. Restart the agent
  console.log('Tiek restartēts OpenClaw serviss...');
  execSync('openclaw gateway restart', { stdio: 'inherit' });

} catch (err) {
  console.error('Kļūda atjaunošanas procesā:', err.message);
  process.exit(1);
}
