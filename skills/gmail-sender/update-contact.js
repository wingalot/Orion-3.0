const fs = require('fs');
const { google } = require('googleapis');
const path = require('path');

// Constants
const TOKEN_PATH = path.join(__dirname, 'token.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');

// Parse arguments
const args = process.argv.slice(2);
let query = '';
let email = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--query') {
    query = args[i + 1];
    i++;
  } else if (args[i] === '--email') {
    email = args[i + 1];
    i++;
  }
}

if (!query || !email) {
  console.error('Usage: node update-contact.js --query "Name" --email "new@email.com"');
  process.exit(1);
}

// Load credentials and authorize
fs.readFile(CREDENTIALS_PATH, (err, content) => {
  if (err) return console.log('Error loading client secret file:', err);
  authorize(JSON.parse(content), updateContact);
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

async function updateContact(auth) {
  const service = google.people({ version: 'v1', auth });

  try {
    // 1. Search for the contact first
    let targetPerson = null;

    // Try searchContacts first
    const searchRes = await service.people.searchContacts({
      query: query,
      readMask: 'names,emailAddresses,phoneNumbers,metadata',
    });

    if (searchRes.data.results && searchRes.data.results.length > 0) {
      // Filter strictly by name if possible, or take first best match
      const exactMatches = searchRes.data.results.filter(r => {
         const name = r.person.names ? r.person.names[0].displayName : '';
         return name.toLowerCase().includes(query.toLowerCase());
      });

      if (exactMatches.length === 1) {
        targetPerson = exactMatches[0].person;
      } else if (exactMatches.length > 1) {
        console.log(`Found multiple contacts matching "${query}". Please be more specific.`);
        exactMatches.forEach(m => console.log(`- ${m.person.names[0].displayName}`));
        return;
      }
    }

    // Fallback to listing all if search failed or yielded nothing
    if (!targetPerson) {
      let connections = [];
      let nextPageToken = undefined;
      do {
        const res = await service.people.connections.list({
          resourceName: 'people/me',
          pageSize: 100,
          personFields: 'names,emailAddresses,phoneNumbers,metadata',
          pageToken: nextPageToken,
        });
        if (res.data.connections) connections = connections.concat(res.data.connections);
        nextPageToken = res.data.nextPageToken;
      } while (nextPageToken);

      const matches = connections.filter(p => {
        const name = p.names ? p.names[0].displayName : '';
        return name.toLowerCase().includes(query.toLowerCase());
      });

      if (matches.length === 1) {
        targetPerson = matches[0];
      } else if (matches.length > 1) {
        console.log(`Found multiple contacts matching "${query}". Please be more specific.`);
        matches.forEach(m => console.log(`- ${m.names ? m.names[0].displayName : 'No Name'}`));
        return;
      }
    }

    if (!targetPerson) {
      console.log(`No contact found for "${query}".`);
      return;
    }

    // 2. Prepare update
    console.log(`Updating contact: ${targetPerson.names[0].displayName}`);
    
    // Existing emails
    const existingEmails = targetPerson.emailAddresses || [];
    
    // Check if email already exists
    if (existingEmails.some(e => e.value === email)) {
        console.log(`Email ${email} already exists for this contact.`);
        return;
    }

    const newEmails = [...existingEmails, { value: email, type: 'home' }];

    // 3. Update via updateContact (using resourceName)
    // We need to fetch the full person first to get the etag if we don't have it reliably from search
    // But search/list usually returns etag in metadata.
    
    const resourceName = targetPerson.resourceName;
    const etag = targetPerson.etag;

    const updateRes = await service.people.updateContact({
      resourceName: resourceName,
      updatePersonFields: 'emailAddresses',
      requestBody: {
        etag: etag,
        emailAddresses: newEmails
      }
    });

    console.log('Successfully updated contact!');
    console.log('New emails:', updateRes.data.emailAddresses.map(e => e.value).join(', '));

  } catch (error) {
    console.error('The API returned an error: ' + error);
  }
}
