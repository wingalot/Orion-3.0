const fs = require('fs');
const {google} = require('googleapis');
const path = require('path');

const TOKEN_PATH = path.join(__dirname, 'token.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');

// Get arguments from command line
const args = process.argv.slice(2);
let to, subject, message;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--to') to = args[i + 1];
  if (args[i] === '--subject') subject = args[i + 1];
  if (args[i] === '--message') message = args[i + 1];
}

if (!to || !subject || !message) {
  console.error('Usage: node send.js --to <email> --subject <subject> --message <message>');
  process.exit(1);
}

// Append signature
message += '\n\nOr3o Core, Personīgais asistents';

fs.readFile(CREDENTIALS_PATH, (err, content) => {
  if (err) return console.log('Error loading client secret file:', err);
  authorize(JSON.parse(content), sendEmail);
});

function authorize(credentials, callback) {
  const {client_secret, client_id, redirect_uris} = credentials.installed || credentials.web;
  const oAuth2Client = new google.auth.OAuth2(
      client_id, client_secret, redirect_uris[0]);

  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) return console.log('Token not found');
    oAuth2Client.setCredentials(JSON.parse(token));
    callback(oAuth2Client);
  });
}

function sendEmail(auth) {
  const gmail = google.gmail({version: 'v1', auth});
  
  const str = [
    `To: ${to}`,
    `Subject: ${subject}`,
    'Content-Type: text/plain; charset=utf-8',
    'MIME-Version: 1.0',
    '',
    message
  ].join('\n');

  const encodedMessage = Buffer.from(str)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  gmail.users.messages.send({
    userId: 'me',
    requestBody: {
      raw: encodedMessage,
    },
  }, (err, res) => {
    if (err) return console.log('The API returned an error: ' + err);
    console.log('Email sent successfully. ID:', res.data.id);
  });
}