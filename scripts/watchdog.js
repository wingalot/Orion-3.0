#!/usr/bin/env node
/**
 * WATCHDOG - Neiznīcināms galvenais cikls
 * Pat ja notiek kļūda, turpinām pēc 5 sekundēm
 */

const { safeExec, safeKill, notifyTelegram } = require('./safe-executor');

const CONFIG = {
  recoveryDelayMs: 5000,
  heartbeatIntervalMs: 60000,
  telegramChatId: '395239117' // Elvis
};

let isRunning = true;
let lastHeartbeat = Date.now();

/**
 * Sūta paziņojumu uz Telegram
 */
async function sendTelegram(message) {
  try {
    // Izmantojam telegram-send skill
    const cmd = `node /home/oreo/.openclaw/workspace/skills/telegram-send/index.js --chat "${CONFIG.telegramChatId}" --message "${message.replace(/"/g, '\\"')}"`;
    await safeExec(cmd, { timeout: 10 });
  } catch (e) {
    console.error('[WATCHDOG] Failed to send Telegram:', e.message);
  }
}

/**
 * Heartbeat - ik pa 60 sekundēm
 */
async function heartbeat() {
  const now = Date.now();
  if (now - lastHeartbeat >= CONFIG.heartbeatIntervalMs) {
    console.log('[WATCHDOG] 🟢 Agent alive');
    await sendTelegram('🟢 Agent alive');
    lastHeartbeat = now;
  }
}

/**
 * Galvenais darbs (placeholders)
 */
async function doWork() {
  // Šeit būtu reālais darbs
  // Piemēram: pārbaudīt cron jobus, sub-aģentus, utt.
  
  // Simulējam darbu
  await new Promise(r => setTimeout(r, 1000));
}

/**
 * NEIZNIĆINĀMAIS galvenais cikls
 */
async function mainLoop() {
  console.log('[WATCHDOG] Starting immortal loop...');
  await sendTelegram('🚀 Watchdog started');
  
  let iteration = 0;
  
  while (isRunning) {
    iteration++;
    
    try {
      // Heartbeat pārbaude
      await heartbeat();
      
      // Galvenais darbs
      await doWork();
      
      // Mazs pauzes
      await new Promise(r => setTimeout(r, 1000));
      
    } catch (error) {
      // KĻŪDA APĶĪLĀTA - nekad neizmetam to tālāk!
      const errorMsg = error.message || 'Unknown error';
      console.error(`[WATCHDOG][Iteration ${iteration}] 💥 CRASH CAUGHT:`, errorMsg);
      
      // Sūtam paziņojumu
      await sendTelegram(`⚠️ Recovered from crash: ${errorMsg.substring(0, 100)}`);
      
      // Gaidām 5 sekundes un turpinām
      console.log(`[WATCHDOG] Recovering in ${CONFIG.recoveryDelayMs}ms...`);
      await new Promise(r => setTimeout(r, CONFIG.recoveryDelayMs));
      
      console.log('[WATCHDOG] Resuming...');
    }
  }
}

/**
 * SIGTERM/SIGINT apstrāde
 */
process.on('SIGTERM', () => {
  console.log('[WATCHDOG] SIGTERM received, graceful shutdown...');
  isRunning = false;
});

process.on('SIGINT', () => {
  console.log('[WATCHDOG] SIGINT received, graceful shutdown...');
  isRunning = false;
});

// Startējam
mainLoop().catch(async (error) => {
  // Pat šeit neļaujam iznīcināt procesu
  console.error('[WATCHDOG] FATAL: Even mainLoop catch failed:', error);
  await sendTelegram('🔥 Watchdog fatal error (should never happen)');
  process.exit(1);
});
