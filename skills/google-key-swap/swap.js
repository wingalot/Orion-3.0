import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import https from 'https';

// --- Configuration ---
const CONFIG_PATH = path.resolve(process.env.HOME || '/home/elvis', '.openclaw/openclaw.json');

// --- Helpers ---

// Simple Google API check (Generative AI list models)
async function validateApiKey(apiKey) {
  return new Promise((resolve, reject) => {
    const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`;
    
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const parsed = JSON.parse(data);
            if (parsed.models && parsed.models.length > 0) {
              resolve(true); // Valid key
            } else {
              reject(new Error('API returned 200 but no models found (unlikely).'));
            }
          } catch (e) {
            reject(new Error('Failed to parse Google API response.'));
          }
        } else {
          try {
             const err = JSON.parse(data);
             reject(new Error(`API Error ${res.statusCode}: ${err.error?.message || 'Unknown error'}`));
          } catch (e) {
             reject(new Error(`API Error ${res.statusCode}`));
          }
        }
      });
    }).on('error', (err) => {
      reject(new Error(`Network error: ${err.message}`));
    });
  });
}

// Main logic
async function main() {
  const newKey = process.argv[2];

  if (!newKey) {
    console.error('Usage: node skills/google-key-swap/swap.js <NEW_API_KEY>');
    process.exit(1);
  }

  console.log('🔍 Validating new API key...');
  
  try {
    await validateApiKey(newKey);
    console.log('✅ New API key is valid!');
  } catch (err) {
    console.error(`❌ Validation failed: ${err.message}`);
    console.error('⚠️  Safety switch activated: Keeping original key. No changes made.');
    process.exit(1);
  }

  // If validation passes, read and update config
  console.log('Reading openclaw.json...');
  let configRaw;
  try {
    configRaw = fs.readFileSync(CONFIG_PATH, 'utf8');
  } catch (err) {
    console.error(`❌ Failed to read config at ${CONFIG_PATH}: ${err.message}`);
    process.exit(1);
  }

  let config;
  try {
    config = JSON.parse(configRaw);
  } catch (err) {
     console.error('❌ Failed to parse openclaw.json');
     process.exit(1);
  }

  // Backup logic (optional, but good practice) - skipped for brevity as we have the validation check
  
  // Update the key
  if (!config.env) config.env = {};
  if (!config.env.vars) config.env.vars = {};
  
  const oldKey = config.env.vars.GOOGLE_API_KEY_google_default;
  if (oldKey === newKey) {
    console.log('ℹ️  New key is identical to the current key. No update needed.');
    process.exit(0);
  }

  config.env.vars.GOOGLE_API_KEY_google_default = newKey;

  // Write back
  console.log('💾 Writing updated config...');
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));

  // Restart Gateway
  console.log('🔄 Restarting OpenClaw Gateway to apply changes...');
  try {
    // We use the CLI because the script runs outside the main process context mostly
    execSync('openclaw gateway restart', { stdio: 'inherit' });
    console.log('✅ Restart command issued.');
  } catch (err) {
    console.error('⚠️  Failed to restart gateway automatically. Please run "openclaw gateway restart" manually.');
  }
}

main();
