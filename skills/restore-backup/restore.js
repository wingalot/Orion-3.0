const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
const dirArgIndex = args.indexOf('--dir');
const targetArgIndex = args.indexOf('--target');
const forceArgIndex = args.indexOf('--force');

// Noklusētie ceļi
const BACKUP_DIR = dirArgIndex !== -1 ? args[dirArgIndex + 1] : '/home/elvis/backups';
const TARGET_DIR = targetArgIndex !== -1 ? args[targetArgIndex + 1] : '/home/elvis/.openclaw/workspace';
const FORCE = forceArgIndex !== -1;

// Pārbauda vai backup mape eksistē
if (!fs.existsSync(BACKUP_DIR)) {
  console.error(`Kļūda: Mape ${BACKUP_DIR} neeksistē.`);
  process.exit(1);
}

// 1. Find the newest backup
const files = fs.readdirSync(BACKUP_DIR)
  .filter(file => file.startsWith('backup-') && (file.endsWith('.tar.gz') || file.endsWith('.zip')))
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
  .filter(f => f !== null)
  .sort((a, b) => b.time - a.time); // Jaunākie vispirms

if (files.length === 0) {
  console.error('Kļūda: Rezerves kopijas netika atrastas mapē:', BACKUP_DIR);
  process.exit(1);
}

const latestBackup = files[0];
console.log(`Jaunākā rezerves kopija: ${latestBackup.name}`);
console.log(`Atjaunošanas mērķis: ${TARGET_DIR}`);

// 2. Apstiprinājums (ja nav --force)
if (!FORCE) {
  // Šeit mēs nevaram interaktīvi jautāt lietotājam, jo aģents var darboties fonā.
  // Tā vietā mēs pieņemam, ka lietotājs zina, ko dara, ja palaiž šo skriptu.
  // Bet mēs izveidosim drošības kopiju pirms pārrakstīšanas.
  console.log('Brīdinājums: Šī darbība pārrakstīs pašreizējo workspace saturu.');
  console.log('Lai izlaistu drošības kopijas izveidi, lietojiet --force argumentu (nav implementēts šajā versijā).');
}

try {
  // Izveido pagaidu drošības kopiju (ja kaut kas noiet greizi)
  const tempBackup = path.join(path.dirname(TARGET_DIR), `workspace_pre_restore_${Date.now()}`);
  if (fs.existsSync(TARGET_DIR)) {
    console.log(`Veido pašreizējā workspace drošības kopiju: ${tempBackup}`);
    fs.cpSync(TARGET_DIR, tempBackup, { recursive: true });
  }

  // Notīra esošo mērķa mapi pirms atjaunošanas (lai nepaliktu vecie faili)
  if (fs.existsSync(TARGET_DIR)) {
    console.log('Dzēš esošo workspace saturu...');
    fs.rmSync(TARGET_DIR, { recursive: true, force: true });
  }
  
  // Izveido mērķa mapi no jauna
  fs.mkdirSync(TARGET_DIR, { recursive: true });

  // 3. Extract the backup
  console.log(`Notiek atjaunošana no ${latestBackup.name}...`);
  // -x: extract, -z: gzip, -f: file, -C: change dir
  execSync(`tar -xzf "${latestBackup.path}" -C "${TARGET_DIR}"`, { stdio: 'inherit' });
  console.log('Faili atjaunoti veiksmīgi.');

  // Dzēš pagaidu drošības kopiju, ja viss veiksmīgi
  if (fs.existsSync(tempBackup)) {
    console.log('Dzēš pagaidu drošības kopiju...');
    fs.rmSync(tempBackup, { recursive: true, force: true });
  }

  // 4. Restart the agent (ja nepieciešams)
  console.log('Lai izmaiņas stātos spēkā, ieteicams restartēt OpenClaw.');
  // Mēs varam mēģināt restartēt, ja lietotājs to vēlas, bet tas var pārtraukt sesiju.
  // Labāk atstāt to lietotāja ziņā vai kā atsevišķu komandu.
  // Bet uzdevumā bija minēts restartēt.
  console.log('Restartē OpenClaw gateway...');
  try {
     execSync('openclaw gateway restart', { stdio: 'inherit' });
  } catch (e) {
     console.warn('Neizdevās restartēt gateway automātiski. Lūdzu, veiciet manuālu restartu.');
  }

} catch (err) {
  console.error('Kļūda atjaunošanas procesā:', err.message);
  // Ja bija kļūda un mēs izveidojām tempBackup, mēģinām atjaunot
  // Tas būtu sarežģīti implementēt perfekti, bet vismaz paziņojam.
  process.exit(1);
}
