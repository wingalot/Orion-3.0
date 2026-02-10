const fs = require('fs');
const { google } = require('googleapis');
const path = require('path');

// Constants
const TOKEN_PATH = path.join(__dirname, 'token.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');

// Parse arguments
const args = process.argv.slice(2);
let query = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--query') {
    query = args[i + 1];
    i++;
  }
}

if (!query) {
  console.error('Usage: node contacts.js --query "Name"');
  process.exit(1);
}

// Load credentials and authorize
fs.readFile(CREDENTIALS_PATH, (err, content) => {
  if (err) return console.log('Error loading client secret file:', err);
  authorize(JSON.parse(content), searchContacts);
});

function authorize(credentials, callback) {
  const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) return console.log('Error retrieving access token:', err);
    oAuth2Client.setCredentials(JSON.parse(token));
    callback(oAuth2Client);
  });
}

/**
 * Lists contacts matching the query.
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 */
async function searchContacts(auth) {
  const service = google.people({ version: 'v1', auth });

  // 1. Try searchContacts first (better search)
  try {
    const res = await service.people.searchContacts({
      query: query,
      readMask: 'names,emailAddresses,phoneNumbers',
    });

    if (res.data.results && res.data.results.length > 0) {
      console.log(`Found ${res.data.results.length} result(s) via search:`);
      res.data.results.forEach((r) => {
        const person = r.person;
        const names = person.names ? person.names.map(n => n.displayName).join(', ') : 'No Name';
        const emails = person.emailAddresses ? person.emailAddresses.map(e => e.value).join(', ') : 'No Email';
        const phones = person.phoneNumbers ? person.phoneNumbers.map(p => p.value).join(', ') : 'No Phone';
        console.log(`- Name: ${names}`);
        console.log(`  Email: ${emails}`);
        console.log(`  Phone: ${phones}`);
        console.log('---');
      });
      return; // Exit if search found something
    }
  } catch (e) {
    // console.log('Search failed/empty, falling back to local list:', e.message);
  }

  // 2. Fallback: list all connections and filter locally
  try {
    let connections = [];
    let nextPageToken = undefined;

    do {
      const res = await service.people.connections.list({
        resourceName: 'people/me',
        pageSize: 100,
        personFields: 'names,emailAddresses,phoneNumbers',
        pageToken: nextPageToken,
      });
      
      if (res.data.connections) {
        connections = connections.concat(res.data.connections);
      }
      nextPageToken = res.data.nextPageToken;
    } while (nextPageToken);

    if (!connections || connections.length === 0) {
      console.log('No contacts found.');
      return;
    }

    if (query === 'ALL') {
      console.log(`Listing all ${connections.length} contact(s):`);
      connections.forEach((person) => {
        const names = person.names ? person.names.map(n => n.displayName).join(', ') : 'No Name';
        const emails = person.emailAddresses ? person.emailAddresses.map(e => e.value).join(', ') : 'No Email';
        const phones = person.phoneNumbers ? person.phoneNumbers.map(p => p.value).join(', ') : 'No Phone';

        console.log(`- Name: ${names}`);
        console.log(`  Email: ${emails}`);
        console.log(`  Phone: ${phones}`);
        console.log('---');
      });
      return;
    }

    const lowerQuery = query.toLowerCase();
    const filtered = connections.filter(person => {
      const names = person.names ? person.names.map(n => n.displayName).join(' ') : '';
      const emails = person.emailAddresses ? person.emailAddresses.map(e => e.value).join(' ') : '';
      return names.toLowerCase().includes(lowerQuery) || emails.toLowerCase().includes(lowerQuery);
    });

    if (filtered.length === 0) {
      console.log(`No contacts found matching "${query}".`);
      return;
    }

    console.log(`Found ${filtered.length} contact(s) via list:`);
    filtered.forEach((person) => {
      const names = person.names ? person.names.map(n => n.displayName).join(', ') : 'No Name';
      const emails = person.emailAddresses ? person.emailAddresses.map(e => e.value).join(', ') : 'No Email';
      const phones = person.phoneNumbers ? person.phoneNumbers.map(p => p.value).join(', ') : 'No Phone';

      console.log(`- Name: ${names}`);
      console.log(`  Email: ${emails}`);
      console.log(`  Phone: ${phones}`);
      console.log('---');
    });

  } catch (error) {
    console.error('The API returned an error: ' + error);
  }
}
