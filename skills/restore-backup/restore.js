const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const forceArg = args.includes('--force');

const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : '/home/oreo/backups';
const TARGET_DIR = '/home/oreo/.openclaw';
const WORKSPACE_DIR = path.join(TARGET_DIR, 'workspace');

// Pārbaudām vai backup mape eksistē
if (!fs.existsSync(BACKUP_DIR)) {
  console.error(`❌ Kļūda: Mape ${BACKUP_DIR} neeksistē.`);
  process.exit(1);
}

// Atrodam visus backup failus
const files = fs.readdirSync(BACKUP_DIR)
  .map(file => {
    const filePath = path.join(BACKUP_DIR, file);
    const stats = fs.statSync(filePath);
    return {
      name: file,
      path: filePath,
      size: stats.size,
      time: stats.mtime,
      sizeMB: (stats.size / (1024 * 1024)).toFixed(2)
    };
  })
  .filter(f => f.name.endsWith('.tar.gz') || f.name.endsWith('.zip'))
  .sort((a, b) => b.time - a.time);

if (files.length === 0) {
  console.error('❌ Kļūda: Rezerves kopijas netika atrastas.');
  process.exit(1);
}

// Parādām backup sarakstu
console.log('\n📦 Pieejamās rezerves kopijas:');
console.log('=' .repeat(70));
files.forEach((file, index) => {
  const date = file.time.toLocaleString('lv-LV');
  console.log(`${index + 1}. ${file.name}`);
  console.log(`   📅 ${date} | 📊 ${file.sizeMB} MB`);
});
console.log('=' .repeat(70));

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Funkcija atjaunošanai
function restoreBackup(backupFile) {
  console.log(`\n⚠️  Brīdinājums!`);
  console.log(`Atjaunošana pārrakstīs visu pašreizējo workspace saturu!`);
  console.log(`Mērķis: ${WORKSPACE_DIR}`);
  console.log(`Avots: ${backupFile.path}`);
  
  if (!forceArg) {
    console.log('\nVai vēlaties turpināt? (jā/nē): ');
  } else {
    performRestore(backupFile);
  }
}

function performRestore(backupFile) {
  try {
    // 1. Izveidojam pagaidu backup pašreizējā stāvokļa (ja nav --force)
    if (!forceArg) {
      const tempBackup = path.join(BACKUP_DIR, `pre-restore-backup-${Date.now()}.tar.gz`);
      console.log('\n💾 Izveidoju pagaidu backup pašreizējā stāvokļa...');
      const parentDir = path.dirname(WORKSPACE_DIR);
      const dirName = path.basename(WORKSPACE_DIR);
      execSync(`tar -czf "${tempBackup}" -C "${parentDir}" "${dirName}"`, { 
        stdio: 'pipe',
        timeout: 60000
      });
      console.log('✅ Pagaidu backup izveidots');
    }

    // 2. Izdzēšam esošo workspace
    console.log('\n🗑️  Dzēšu esošo workspace...');
    if (fs.existsSync(WORKSPACE_DIR)) {
      fs.rmSync(WORKSPACE_DIR, { recursive: true, force: true });
    }

    // 3. Izvelkam backup
    console.log('📦 Atjaunoju failus no backup...');
    execSync(`tar -xzf "${backupFile.path}" -C "${TARGET_DIR}"`, { 
      stdio: 'inherit',
      timeout: 120000
    });

    console.log('\n✅ Atjaunošana veiksmīga!');
    console.log(`📁 Workspace atjaunots no: ${backupFile.name}`);
    console.log(`🕐 Backup datums: ${backupFile.time.toLocaleString('lv-LV')}`);
    
    // 4. Restartējam OpenClaw
    console.log('\n🔄 Restartēju OpenClaw servisu...');
    execSync('openclaw gateway restart', { stdio: 'inherit' });

  } catch (err) {
    console.error('\n❌ Kļūda atjaunošanas procesā:', err.message);
    console.error('Lūdzu pārbaudiet vai backup fails nav bojāts.');
    process.exit(1);
  }
}

// Ja ir --force, izmantojam jaunāko backup
if (forceArg) {
  restoreBackup(files[0]);
} else {
  // Vaicājam lietotājam izvēlēties backup
  rl.question('\nIevadiet backup numuru (1-' + files.length + ') vai "q" iziet: ', (answer) => {
    if (answer.toLowerCase() === 'q') {
      console.log('Atcelts.');
      rl.close();
      process.exit(0);
    }

    const choice = parseInt(answer, 10);
    if (isNaN(choice) || choice < 1 || choice > files.length) {
      console.error('❌ Nederīga izvēle.');
      rl.close();
      process.exit(1);
    }

    const selectedBackup = files[choice - 1];
    
    rl.question(`Vai tiešām vēlaties atjaunot no "${selectedBackup.name}"? (jā/nē): `, (confirm) => {
      rl.close();
      
      if (confirm.toLowerCase() === 'jā' || confirm.toLowerCase() === 'ja') {
        performRestore(selectedBackup);
      } else {
        console.log('Atcelts.');
        process.exit(0);
      }
    });
  });
}
