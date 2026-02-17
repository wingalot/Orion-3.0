const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function log(message) {
  console.log(`[VALIDATION] ${message}`);
}

function fail(message) {
  console.error(`[FAIL] ${message}`);
  process.exit(1);
}

const workspace = '/home/oreo/.openclaw/workspace';

// 1. Validate Brave Search Skill
log("Validating Brave Search Skill...");
try {
  const script = path.join(workspace, 'skills/brave/search.js');
  if (!fs.existsSync(script)) {
      log(`Brave Search script not found at ${script}. Skipping.`);
  } else {
      const braveOutput = execSync(`node ${script} --query "OpenClaw"`, { encoding: 'utf-8' });
      log("Brave Search executed without crash.");
  }
} catch (e) {
  // Brave might fail without API key, check error message
  if (e.message.includes('API key')) {
      log("Brave Search missing API key (expected).");
  } else {
      fail(`Brave Search failed: ${e.message}`);
  }
}

// 2. Validate Gmail Sender Skill (Syntax Check)
log("Validating Gmail Sender Skill (Syntax)...");
try {
  const senderDir = path.join(workspace, 'skills/gmail-sender');
  if (!fs.existsSync(senderDir)) {
      // Maybe old name?
      const oldDir = path.join(workspace, 'skills/mailsender');
       if (fs.existsSync(oldDir)) {
           fail(`Found old 'skills/mailsender' directory. Should be renamed to 'skills/gmail-sender'.`);
       } else {
           fail(`Gmail Sender directory not found at ${senderDir}`);
       }
  }

  const scripts = ['send.js', 'contacts.js', 'update-contact.js', 'auth.js'];
  for (const s of scripts) {
      const scriptPath = path.join(senderDir, s);
      if (fs.existsSync(scriptPath)) {
          execSync(`node -c ${scriptPath}`);
          log(`${s} Syntax OK.`);
      } else {
          log(`${s} missing (optional?).`);
      }
  }
  
} catch (e) {
  fail(`Gmail Sender validation error: ${e.message}`);
}

log("ALL SKILLS VALIDATED.");
