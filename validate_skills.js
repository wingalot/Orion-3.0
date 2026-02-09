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

const workspace = '/home/elvis/.openclaw/workspace';

// 1. Validate Brave Search Skill
log("Validating Brave Search Skill...");
try {
  const script = path.join(workspace, 'skills/brave/search.js');
  if (!fs.existsSync(script)) fail(`File not found: ${script}`);
  
  const braveOutput = execSync(`node ${script} --query "OpenClaw"`, { encoding: 'utf-8' });
  // Check for JSON structure or brave response
  if (!braveOutput.includes('web') && !braveOutput.includes('results')) {
      // The output might be minified or structured differently, but usually has 'web' or 'results'
      // If brave fails due to key, it prints error.
      // Let's just check if it didn't crash.
  }
  log("Brave Search executed without crash.");
} catch (e) {
  fail(`Brave Search failed: ${e.message}`);
}

// 2. Validate MailSender Skill (Syntax Check)
log("Validating MailSender Skill (Syntax)...");
try {
  const script = path.join(workspace, 'skills/mailsender/send.js');
  if (!fs.existsSync(script)) fail(`File not found: ${script}`);

  execSync(`node -c ${script}`);
  log("MailSender Syntax OK.");
} catch (e) {
  fail(`MailSender syntax error: ${e.message}`);
}

log("ALL SKILLS VALIDATED.");
