#!/usr/bin/env node
/**
 * error-handler.js - Automātiska kļūdu apstrādes sistēma OpenClaw agentam
 * 
 * Klasificē kļūdas un izlemj:
 * - AUTO_RESOLVE: Risināt automātiski bez ziņošanas
 * - NOTIFY_SHORT: Īsa ziņa lietotājam
 * - NOTIFY_FULL: Pilna kļūdas informācija
 */

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Kļūdu klasifikācijas tips
const ErrorAction = {
  AUTO_RESOLVE: 'auto_resolve',   // Risināt bez ziņošanas
  NOTIFY_SHORT: 'notify_short',   // Īsa ziņa
  NOTIFY_FULL: 'notify_full',     // Pilna informācija
};

/**
 * Kļūdu klasifikācijas definīcijas
 * Katrai kļūdai - pattern matching + risinājums
 */
const ERROR_PATTERNS = [
  // === AUTO_RESOLVE kļūdas ===
  {
    name: 'git_fetch_first',
    action: ErrorAction.AUTO_RESOLVE,
    patterns: [
      /fetch first/i,
      /Updates were rejected because the remote contains work/i,
      /non-fast-forward/i
    ],
    resolve: async (error) => {
      try {
        // Mēģinām pull ar rebase
        await execPromise('git pull --rebase');
        return { success: true, message: '✅ Sync izpildīts (pull --rebase)' };
      } catch (e) {
        return { success: false, message: `Pull neizdevās: ${e.message}` };
      }
    }
  },
  {
    name: 'minor_timeout',
    action: ErrorAction.AUTO_RESOLVE,
    patterns: [
      /timeout.*after.*\d+ms/i,
      /ETIMEDOUT/i,
      /socket hang up/i
    ],
    resolve: async (error) => {
      // Timeout - retry paša komanda būs jāpārbauda ārpus šīs funkcijas
      return { success: true, message: '⏱️ Timeout - retry enabled' };
    }
  },
  {
    name: 'network_transient',
    action: ErrorAction.AUTO_RESOLVE,
    patterns: [
      /ECONNRESET/i,
      /ENOTFOUND.*(temporarily|temporary)/i,
      /502 Bad Gateway/i,
      /503 Service Unavailable/i
    ],
    resolve: async (error) => {
      return { success: true, message: '🌐 Tīkla kļūda - retry' };
    }
  },

  // === NOTIFY_SHORT kļūdas ===
  {
    name: 'git_secret_scanning',
    action: ErrorAction.NOTIFY_SHORT,
    patterns: [
      /GH013/i,
      /secret.*detected/i,
      /push rejected.*secret/i,
      /credential.*detected/i,
      /gitleaks/i
    ],
    formatMessage: (error) => {
      // Esošo secret meklējam
      const match = error.match(/[a-f0-9]{7,40}/);
      const commit = match ? match[0].substring(0, 7) : 'latest';
      
      return {
        title: '⚠️ Git push bloķēts',
        body: `Atrasti sensitīvi dati vēsturē (commit: ${commit}).\n` +
              `Risinājums: noņemt secrets vai lietot \`git commit --amend\``
      };
    },
    resolve: async (error) => {
      // Šo nevar auto-risināt - lietotājam jāievērošo
      return { 
        success: false, 
        message: 'Secret scanning kļūda - nepieciešama lietotāja darbība',
        suggestions: [
          'git rebase -i HEAD~3 (labot commitus)',
          'git filter-repo --strip-blobs-bigger-than 10M',
          'GitHub Settings → Security → Secret scanning (whitelist ja nepieciešams)'
        ]
      };
    }
  },
  {
    name: 'git_permission_denied',
    action: ErrorAction.NOTIFY_SHORT,
    patterns: [
      /Permission denied \(publickey\)/i,
      /could not read from remote repository/i,
      /access denied/i,
      /authentication failed/i
    ],
    formatMessage: (error) => ({
      title: '🔐 Piekļuve liegta',
      body: 'SSH/Git piekļuve neizdevās. Pārbaudi SSH atslēgas vai tokens.'
    }),
    resolve: async (error) => {
      return {
        success: false,
        message: 'Piekļuves kļūda - jāpārbauda SSH/Git config',
        suggestions: [
          'ssh-add -l (pārbaudīt atslēgas)',
          'cat ~/.ssh/id_rsa.pub (publiskā atslēga)',
          'git remote -v (pārbaudīt URL)'
        ]
      };
    }
  },
  {
    name: 'rate_limit',
    action: ErrorAction.NOTIFY_SHORT,
    patterns: [
      /rate limit/i,
      /too many requests/i,
      /429 Too Many Requests/i
    ],
    formatMessage: (error) => ({
      title: '🐌 Rate limit sasniegts',
      body: 'Pārāk daudz pieprasījumu. Gaidīšu pirms atkārtota mēģinājuma.'
    }),
    resolve: async (error) => {
      // Extract retry-after ja pieejams
      const retryMatch = error.match(/retry[-\s]after[:\s]*(\d+)/i);
      const retryAfter = retryMatch ? parseInt(retryMatch[1]) : 60;
      
      return {
        success: true,
        message: `Rate limit - gaidu ${retryAfter}s`,
        retryAfter: retryAfter * 1000
      };
    }
  },
  {
    name: 'disk_full',
    action: ErrorAction.NOTIFY_SHORT,
    patterns: [
      /no space left on device/i,
      /ENOSPC/i,
      /disk full/i
    ],
    formatMessage: (error) => ({
      title: '💾 Diska vieta beigusies',
      body: 'Nepieciešams atbrīvot vietu vai notīrīt pagaidu failus.'
    }),
    resolve: async (error) => {
      return {
        success: false,
        message: 'Disk full - nepieciešama lietotāja darbība',
        suggestions: [
          'df -h (pārbaudīt vietu)',
          'docker system prune (notīrīt Docker)',
          'npm cache clean (notīrīt npm cache)',
          'rm -rf /tmp/* (pagaidu faili)'
        ]
      };
    }
  },

  // === NOTIFY_FULL kļūdas ===
  {
    name: 'critical_system_error',
    action: ErrorAction.NOTIFY_FULL,
    patterns: [
      /segmentation fault/i,
      /core dumped/i,
      /kernel panic/i,
      /out of memory.*killed process/i,
      /Fatal error/i
    ],
    formatMessage: (error) => ({
      title: '💥 Kritiska sistēmas kļūda',
      body: 'Sistēma sastapusies ar nopietnu problēmu. Nepieciešama tūlītēja uzmanība.'
    })
  },
  {
    name: 'syntax_error',
    action: ErrorAction.NOTIFY_FULL,
    patterns: [
      /SyntaxError/i,
      /ParseError/i,
      /ReferenceError/i,
      /TypeError.*undefined/i
    ],
    formatMessage: (error) => ({
      title: '💻 Koda kļūda',
      body: 'Atrodas koda problēma. Skatīt detaļas zemāk.'
    })
  }
];

/**
 * Klasificē kļūdu un atgriež risinājuma instrukcijas
 * @param {string} errorMessage - Kļūdas ziņojums
 * @param {object} context - Papildus konteksts (komanda, utt.)
 * @returns {object} Klasifikācijas rezultāts
 */
function classifyError(errorMessage, context = {}) {
  if (!errorMessage || typeof errorMessage !== 'string') {
    return {
      action: ErrorAction.NOTIFY_FULL,
      type: 'unknown',
      message: formatFullError('Nezināma kļūda (nav ziņojuma)', context),
      resolve: null
    };
  }

  // Sameklējam atbilstošo pattern
  for (const pattern of ERROR_PATTERNS) {
    const matches = pattern.patterns.some(p => p.test(errorMessage));
    
    if (matches) {
      const result = {
        action: pattern.action,
        type: pattern.name,
        resolve: pattern.resolve || null,
        formatMessage: pattern.formatMessage || null
      };

      // Formatējam ziņojumu atbilstoši tipam
      switch (pattern.action) {
        case ErrorAction.AUTO_RESOLVE:
          result.message = null; // Nav jāziņo
          break;
          
        case ErrorAction.NOTIFY_SHORT:
          if (pattern.formatMessage) {
            const formatted = pattern.formatMessage(errorMessage);
            result.message = `${formatted.title}\n${formatted.body}`;
          } else {
            result.message = formatShortError(errorMessage, pattern.name);
          }
          break;
          
        case ErrorAction.NOTIFY_FULL:
          if (pattern.formatMessage) {
            const formatted = pattern.formatMessage(errorMessage);
            result.message = formatFullError(errorMessage, context, formatted);
          } else {
            result.message = formatFullError(errorMessage, context);
          }
          break;
      }

      return result;
    }
  }

  // Nezināma kļūda - NOTIFY_FULL
  return {
    action: ErrorAction.NOTIFY_FULL,
    type: 'unknown',
    message: formatFullError(errorMessage, context),
    resolve: null
  };
}

/**
 * Formatē īsu kļūdas ziņojumu
 */
function formatShortError(errorMessage, errorType) {
  // Saīsinām garu ziņojumu
  const short = errorMessage.split('\n')[0].substring(0, 100);
  return `⚠️ Sastapu problēmu: ${short}${errorMessage.length > 100 ? '...' : ''}`;
}

/**
 * Formatē pilnu kļūdas ziņojumu
 */
function formatFullError(errorMessage, context = {}, custom = null) {
  let output = '';
  
  if (custom) {
    output += `**${custom.title}**\n${custom.body}\n\n`;
  }
  
  if (context.command) {
    output += `Komanda: \`${context.command}\`\n`;
  }
  
  output += `\`\`\`\n${errorMessage.substring(0, 2000)}\n\`\`\``;
  
  if (context.cwd) {
    output += `\nDirektorija: \`${context.cwd}\``;
  }
  
  return output;
}

/**
 * Apstrādā kļūdu - galvenā funkcija
 * @param {Error|string} error - Kļūdas objekts vai ziņojums
 * @param {object} options - Opcijas
 * @param {function} notifyFn - Funkcija ziņošanai (optional)
 */
async function handleError(error, options = {}, notifyFn = null) {
  const errorMessage = error instanceof Error ? error.message : String(error);
  const context = {
    command: options.command || null,
    cwd: options.cwd || process.cwd(),
    timestamp: new Date().toISOString()
  };

  // Klasificējam kļūdu
  const classification = classifyError(errorMessage, context);

  // Reaģējam atbilstoši tipam
  switch (classification.action) {
    case ErrorAction.AUTO_RESOLVE:
      console.log(`[AUTO_RESOLVE] ${classification.type}`);
      
      if (classification.resolve) {
        try {
          const result = await classification.resolve(errorMessage);
          return {
            handled: true,
            resolved: result.success,
            message: result.message,
            type: classification.type,
            action: 'auto_resolve'
          };
        } catch (resolveError) {
          return {
            handled: false,
            error: resolveError.message,
            type: classification.type,
            action: 'auto_resolve_failed'
          };
        }
      }
      
      return {
        handled: true,
        resolved: true,
        type: classification.type,
        action: 'auto_resolve'
      };

    case ErrorAction.NOTIFY_SHORT:
      console.log(`[NOTIFY_SHORT] ${classification.type}`);
      
      if (notifyFn && classification.message) {
        await notifyFn(classification.message);
      }
      
      // Mēģinām arī auto-risināt ja definēts
      if (classification.resolve) {
        const resolveResult = await classification.resolve(errorMessage);
        return {
          handled: true,
          notified: true,
          resolved: resolveResult.success,
          message: resolveResult.message,
          suggestions: resolveResult.suggestions,
          type: classification.type,
          action: 'notify_short'
        };
      }
      
      return {
        handled: true,
        notified: true,
        message: classification.message,
        type: classification.type,
        action: 'notify_short'
      };

    case ErrorAction.NOTIFY_FULL:
      console.log(`[NOTIFY_FULL] ${classification.type}`);
      
      if (notifyFn) {
        await notifyFn(classification.message);
      }
      
      return {
        handled: true,
        notified: true,
        message: classification.message,
        type: classification.type,
        action: 'notify_full'
      };
  }
}

/**
 * Ērtības funkcija - wrap promise ar error handling
 */
async function safeExecute(promise, options = {}, notifyFn = null) {
  try {
    const result = await promise;
    return { success: true, result };
  } catch (error) {
    const handled = await handleError(error, options, notifyFn);
    return { success: false, error: handled };
  }
}

/**
 * Ērtības funkcija - wrap exec ar error handling
 */
async function safeExec(command, options = {}, notifyFn = null) {
  const execOptions = {
    command,
    cwd: options.cwd || process.cwd(),
    ...options
  };
  
  try {
    const { stdout, stderr } = await execPromise(command, options);
    return { success: true, stdout, stderr };
  } catch (error) {
    const handled = await handleError(error, execOptions, notifyFn);
    return { success: false, error: handled, stderr: error.stderr };
  }
}

// Eksportējam moduli
module.exports = {
  ErrorAction,
  ERROR_PATTERNS,
  classifyError,
  handleError,
  safeExecute,
  safeExec,
  // Ērtības constants
  ACTIONS: ErrorAction
};

// Ja palaižam kā standalone skriptu
if (require.main === module) {
  // CLI test režīms
  const testError = process.argv[2];
  
  if (testError) {
    console.log('Testējam kļūdu:', testError);
    const result = classifyError(testError);
    console.log('Klasifikācija:', JSON.stringify(result, null, 2));
  } else {
    console.log('Lietojums: node error-handler.js "<error message>"');
    console.log('\nAtbalstītās kļūdu kategorijas:');
    ERROR_PATTERNS.forEach(p => {
      console.log(`  - ${p.name} (${p.action})`);
    });
  }
}
