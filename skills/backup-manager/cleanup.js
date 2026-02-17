const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const keepArgIndex = args.indexOf('--keep');

const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : '/home/oreo/backups';
const KEEP_COUNT = keepArgIndex !== -1 ? parseInt(args[keepArgIndex + 1], 10) : 10;

if (!fs.existsSync(BACKUP_DIR)) {
  console.error(`Kļūda: Mape ${BACKUP_DIR} neeksistē.`);
  process.exit(1);
}

// Iegūstam failu sarakstu ar metadatiem
const files = fs.readdirSync(BACKUP_DIR)
  .map(file => {
    const filePath = path.join(BACKUP_DIR, file);
    return {
      name: file,
      path: filePath,
      time: fs.statSync(filePath).mtime.getTime()
    };
  })
  .filter(f => f.name.endsWith('.tar.gz') || f.name.endsWith('.zip')); // Filtrējam backup failus

// Kārtojam pēc laika (jaunākie vispirms)
files.sort((a, b) => b.time - a.time);

console.log(`Atrasti ${files.length} rezerves kopiju faili mapē ${BACKUP_DIR}.`);

if (files.length > KEEP_COUNT) {
  const filesToDelete = files.slice(KEEP_COUNT);
  console.log(`Tiks dzēsti ${filesToDelete.length} vecākie faili (saglabājam ${KEEP_COUNT})...`);

  filesToDelete.forEach(file => {
    try {
      fs.unlinkSync(file.path);
      console.log(`Dzēsts: ${file.name}`);
    } catch (err) {
      console.error(`Kļūda dzēšot ${file.name}:`, err.message);
    }
  });
} else {
  console.log('Failu skaits nepārsniedz limitu. Tīrīšana nav nepieciešama.');
}
