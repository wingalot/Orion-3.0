const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const keepArgIndex = args.indexOf('--keep');

// Definē mainīgos no argumentiem vai noklusējuma
const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : '/home/elvis/backups';
const KEEP_COUNT = keepArgIndex !== -1 ? parseInt(args[keepArgIndex + 1], 10) : 10;

// Pārbauda vai backup mape eksistē
if (!fs.existsSync(BACKUP_DIR)) {
  console.error(`Kļūda: Mape ${BACKUP_DIR} neeksistē.`);
  // Ja backup mape neeksistē, skripts vienkārši beidz darbību bez kļūdas (jo nav ko tīrīt)
  process.exit(0);
}

// Iegūst failu sarakstu ar metadatiem
try {
  const files = fs.readdirSync(BACKUP_DIR)
    .filter(file => file.startsWith('backup-') && (file.endsWith('.tar.gz') || file.endsWith('.zip'))) // Filtrē tikai backup failus ar konkrēto nosaukuma formātu
    .map(file => {
      const filePath = path.join(BACKUP_DIR, file);
      try {
        const stats = fs.statSync(filePath);
        return {
          name: file,
          path: filePath,
          time: stats.mtime.getTime()
        };
      } catch (err) {
        console.error(`Kļūda iegūstot informāciju par ${file}:`, err.message);
        return null;
      }
    })
    .filter(f => f !== null) // Noņem failus, kuriem neizdevās iegūt info
    .sort((a, b) => b.time - a.time); // Kārto dilstoši pēc laika (jaunākie vispirms)

  console.log(`Atrasti ${files.length} rezerves kopiju faili mapē ${BACKUP_DIR}.`);

  if (files.length > KEEP_COUNT) {
    const filesToDelete = files.slice(KEEP_COUNT);
    console.log(`Pārsniegts limits (${KEEP_COUNT}). Tiks dzēsti ${filesToDelete.length} vecākie faili...`);

    filesToDelete.forEach(file => {
      try {
        fs.unlinkSync(file.path);
        console.log(`Dzēsts vecais fails: ${file.name}`);
      } catch (err) {
        console.error(`Kļūda dzēšot ${file.name}:`, err.message);
      }
    });
  } else {
    console.log(`Failu skaits (${files.length}) nepārsniedz limitu (${KEEP_COUNT}). Tīrīšana nav nepieciešama.`);
  }

} catch (err) {
  console.error('Kļūda tīrīšanas procesā:', err.message);
  process.exit(1);
}
