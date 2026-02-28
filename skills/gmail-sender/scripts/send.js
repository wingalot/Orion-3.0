#!/usr/bin/env node
/**
 * Gmail Sender Script
 * Usage: node send.js --to "email@example.com" --subject "Subject" --message "Body" [--html]
 */

const nodemailer = require('nodemailer');
const path = require('path');

// Load .env from skill directory
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

// Parse arguments
const args = process.argv.slice(2);
const options = {};

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
    options[key] = value;
    if (value !== true) i++;
  }
}

// RFC 2047 encoding for non-ASCII subject lines
function encodeSubject(subject) {
  // Check if subject contains non-ASCII characters
  if (/[^\x00-\x7F]/.test(subject)) {
    // Encode using RFC 2047: =?charset?encoding?encoded-text?=
    const encoded = Buffer.from(subject, 'utf-8').toString('base64');
    return `=?UTF-8?B?${encoded}?=`;
  }
  return subject;
}

async function sendEmail() {
  const { to, subject, message, html } = options;

  if (!to || !subject || !message) {
    console.error('❌ Trūkst obligātie parametri: --to, --subject, --message');
    console.log('Lietošana: node send.js --to "email@example.com" --subject "Virsraksts" --message "Teksts"');
    process.exit(1);
  }

  if (!process.env.GMAIL_USER || !process.env.GMAIL_PASS) {
    console.error('❌ Nav konfigurēti GMAIL_USER un GMAIL_PASS .env failā');
    process.exit(1);
  }

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.GMAIL_USER,
      pass: process.env.GMAIL_PASS
    }
  });

  try {
    const info = await transporter.sendMail({
      from: `"${process.env.GMAIL_USER}" <${process.env.GMAIL_USER}>`,
      to: to,
      subject: encodeSubject(subject),
      text: html ? undefined : message,
      html: html ? message : undefined
    });

    console.log('✅ E-pasts nosūtīts:', info.messageId);
    console.log('   Saņēmējs:', to);
    console.log('   Virsraksts:', subject);
  } catch (error) {
    console.error('❌ Kļūda sūtot e-pastu:', error.message);
    process.exit(1);
  }
}

sendEmail();
