#!/usr/bin/env node
/**
 * SAFE EXECUTOR - Crash-proof command wrapper
 * Neļauj nevienai komandai iznīcināt galveno cilpu
 */

const { exec } = require('child_process');
const util = require('util');

const execAsync = util.promisify(exec);

// Konfigurācija
const CONFIG = {
  defaultTimeout: 30,
  retryAttempts: 1,
  retryDelayMs: 1000
};

/**
 * Droša komandas izpilde ar kļūdu apķīlāšanu
 * @param {string} command - Komanda
 * @param {object} options - Opcijas
 * @returns {Promise<{success: boolean, output: string, error: string|null}>}
 */
async function safeExec(command, options = {}) {
  const timeout = options.timeout || CONFIG.defaultTimeout;
  const logPrefix = options.logPrefix || '[SAFE-EXEC]';
  
  console.log(`${logPrefix} Starting: ${command.substring(0, 80)}...`);
  
  try {
    const { stdout, stderr } = await execAsync(command, {
      timeout: timeout * 1000,
      killSignal: 'SIGTERM',
      maxBuffer: 10 * 1024 * 1024 // 10MB buffer
    });
    
    console.log(`${logPrefix} ✅ Success`);
    return {
      success: true,
      output: stdout || '',
      error: stderr || null,
      exitCode: 0
    };
    
  } catch (error) {
    // Kļūda apķīlāta - NEIZMETAM to tālāk!
    const errorMsg = error.message || 'Unknown error';
    const exitCode = error.code || error.exitCode || -1;
    
    console.error(`${logPrefix} ❌ Failed (code ${exitCode}): ${errorMsg.substring(0, 200)}`);
    
    return {
      success: false,
      output: error.stdout || '',
      error: errorMsg,
      exitCode: exitCode,
      signal: error.signal || null
    };
  }
}

/**
 * Komandas izpilde ar mēģinājumu atkārtošanu
 */
async function safeExecWithRetry(command, options = {}) {
  const attempts = options.attempts || CONFIG.retryAttempts;
  
  for (let i = 0; i < attempts; i++) {
    const result = await safeExec(command, {
      ...options,
      logPrefix: `[SAFE-EXEC][Attempt ${i + 1}/${attempts}]`
    });
    
    if (result.success) {
      return result;
    }
    
    if (i < attempts - 1) {
      console.log(`[SAFE-EXEC] Waiting ${CONFIG.retryDelayMs}ms before retry...`);
      await new Promise(r => setTimeout(r, CONFIG.retryDelayMs));
    }
  }
  
  return {
    success: false,
    error: `All ${attempts} attempts failed`,
    exitCode: -1
  };
}

/**
 * Procesa noslepkavošana ar SIGTERM (nevis SIGKILL)
 * Drošs veids kā pārtraukt procesu bez sistēmas sabrukšanas
 */
async function safeKill(processName, options = {}) {
  // ⚠️ LIETOT -15 (SIGTERM) nevis -9 (SIGKILL)
  // -x = exact match, nevis -f (full match)
  // || true = neatgriež kļūdu, ja process nav atrasts
  
  const exactMatch = options.exact !== false; // default: true
  const signal = options.signal || '-15'; // SIGTERM (polite)
  
  let killCmd;
  if (exactMatch) {
    // Drošākais - exact match
    killCmd = `pkill ${signal} -x "${processName}" || true`;
  } else {
    // Fallback - full command match
    killCmd = `pkill ${signal} -f "${processName}" || true`;
  }
  
  console.log(`[SAFE-KILL] Terminating: ${processName} (${signal})`);
  
  const result = await safeExec(killCmd, { timeout: 5 });
  
  if (result.success) {
    console.log(`[SAFE-KILL] ✅ Termination signal sent`);
  } else {
    console.log(`[SAFE-KILL] ⚠️ Process may not exist or already terminated`);
  }
  
  return result;
}

/**
 * Telegram paziņojuma sūtīšana par kļūdu
 */
async function notifyTelegram(message, options = {}) {
  // Šo izsauc ārējais sistēmas līmenis
  // Šeit tikai logojam
  const emoji = options.severity === 'error' ? '❌' : 
                options.severity === 'warning' ? '⚠️' : 'ℹ️';
  
  console.log(`[NOTIFY] ${emoji} ${message}`);
  
  // Atgriežam objektu, ko var izmantot ārpusē
  return {
    notified: true,
    message: `${emoji} ${message}`,
    timestamp: new Date().toISOString()
  };
}

// Eksportējam funkcijas
module.exports = {
  safeExec,
  safeExecWithRetry,
  safeKill,
  notifyTelegram,
  CONFIG
};

// Ja izpildām tieši
if (require.main === module) {
  console.log('Safe Executor module loaded.');
  console.log('Usage: const { safeExec, safeKill } = require("./safe-executor");');
}
