#!/usr/bin/env node
/**
 * telegram-error-handler.js - Error handler integrācija ar Telegram
 * 
 * Lietojums:
 *   const { handleWithTelegram } = require('./telegram-error-handler');
 *   
 *   try {
 *     await git.push();
 *   } catch (error) {
 *     await handleWithTelegram(error, { command: 'git push' });
 *   }
 */

const { handleError, safeExec } = require('./error-handler');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Telegram message limits
const MAX_MESSAGE_LENGTH = 4096;

/**
 * Nosūta ziņu uz Telegram caur OpenClaw gateway
 */
async function sendTelegram(message, options = {}) {
  // Saīsinām ja pārāk garš
  const safeMessage = message.length > MAX_MESSAGE_LENGTH 
    ? message.substring(0, MAX_MESSAGE_LENGTH - 100) + '\n\n...[saīsināts]'
    : message;

  try {
    // Mēģinām caur OpenClaw CLI
    const escaped = safeMessage.replace(/"/g, '\\"');
    await execPromise(`openclaw message send "${escaped}"`, { 
      timeout: 10000 
    });
    return { success: true };
  } catch (e) {
    // Fallback - console
    console.log('[TELEGRAM]', safeMessage);
    return { success: false, error: e.message };
  }
}

/**
 * Apstrādā kļūdu ar Telegram ziņošanu
 * AUTOMĀTISKI izslēdz pilnas kļūdas ziņas - tikai klasificētās
 */
async function handleWithTelegram(error, options = {}) {
  const notifyFn = async (message) => {
    // NOFULL: Neziņojam tehniskās detaļas
    // Tikai jau formatēto īso/ vidējo ziņu
    await sendTelegram(message, { silent: options.silent });
  };

  const result = await handleError(error, options, notifyFn);

  // Papildus logging
  if (result.action === 'auto_resolve' && result.resolved) {
    // Vieglā ziņa par veiksmīgu auto-resolve
    if (options.verbose) {
      await sendTelegram(`✅ ${result.message || 'Problēma automātiski novērsta'}`);
    }
  }

  return result;
}

/**
 * Droša git komandu izpilde ar error handling
 */
async function safeGit(command, options = {}) {
  const fullCommand = `git ${command}`;
  const result = await safeExec(fullCommand, {
    ...options,
    command: fullCommand
  }, async (msg) => {
    await sendTelegram(msg);
  });
  
  return result;
}

module.exports = {
  handleWithTelegram,
  safeGit,
  sendTelegram
};
