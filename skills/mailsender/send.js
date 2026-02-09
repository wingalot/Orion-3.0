const process = require('process');

// Parse args
const args = process.argv.slice(2);
const toIndex = args.indexOf('--to');
const subjectIndex = args.indexOf('--subject');
const textIndex = args.indexOf('--text');

const to = toIndex !== -1 ? args[toIndex + 1] : null;
const subject = subjectIndex !== -1 ? args[subjectIndex + 1] : null;
const text = textIndex !== -1 ? args[textIndex + 1] : null;

if (!to || !subject || !text) {
  console.error('Usage: node send.js --to <email> --subject <subject> --text <text>');
  process.exit(1);
}

const API_KEY = "mlsn.b27e5c989cd50b53ba59e36034e2dc89d5ce60dcf735b1265e747c4d3139116d";
const SENDER_EMAIL = "MS_CGFKs6@test-ywj2lpn7531g7oqz.mlsender.net";

async function main() {
  try {
    const response = await fetch("https://api.mailersend.com/v1/email", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "X-Requested-With": "XMLHttpRequest"
      },
      body: JSON.stringify({
        from: {
          email: SENDER_EMAIL,
          name: "Orions (OpenClaw)"
        },
        to: [
          {
            email: to,
            name: "Elvis Brencis" 
          }
        ],
        subject: subject,
        text: text,
        html: `<p>${text}</p>` // Simple HTML fallback
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Error sending email: ${response.status} ${response.statusText}`);
      console.error("Details:", errorText);
      process.exit(1);
    }

    // MailerSend returns 202 Accepted on success with valid JSON or empty body
    // If it returns JSON, we can log the ID, otherwise just success.
    const responseText = await response.text();
    console.log("Email sent successfully!");
    if (responseText) {
        console.log("Response:", responseText);
    }

  } catch (error) {
    console.error("Network error:", error);
    process.exit(1);
  }
}

main();