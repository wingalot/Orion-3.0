const https = require('https');
const process = require('process');

// Parse args
const args = process.argv.slice(2);
const queryIndex = args.indexOf('--query');
const query = queryIndex !== -1 ? args[queryIndex + 1] : null;

if (!query) {
  console.error('Usage: node search.js --query "search term"');
  process.exit(1);
}

// Read API Key from config if not hardcoded (or check env)
const API_KEY = process.env.BRAVE_API_KEY || "BSA05ihIMkD4Na1zjew3q7MqLswohKs"; 

async function main() {
  try {
    const response = await fetch(`https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}&count=1`, {
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': API_KEY
      }
    });

    if (!response.ok) {
        console.error(`Error: ${response.status} ${response.statusText}`);
        process.exit(1);
    }

    const data = await response.json();
    console.log(JSON.stringify(data, null, 2));

  } catch (error) {
    console.error("Network error:", error);
    process.exit(1);
  }
}

main();