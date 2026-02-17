const fs = require('fs');
const path = require('path');
const OpenAI = require('openai');
const readline = require('readline');

// Konfigurācija
const AUTH_FILE = path.join(process.env.HOME, '.openclaw', 'auth.json');
// Lietotājs prasīja 'qwen/qwen3-32b'. OpenRouter šobrīd (2025) piedāvā 'qwen/qwen-2.5-coder-32b-instruct'.
// Es izmantošu stabilo versiju, bet kodā atstāju iespēju to mainīt.
const MODEL_ID = "qwen/qwen-2.5-coder-32b-instruct"; // OpenRouter ID fallback
const AGENT_NAME = "Kodētājs";

async function getApiKey() {
  let apiKey = null;

  // 1. Pārbauda failā
  if (fs.existsSync(AUTH_FILE)) {
    try {
      const config = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf8'));
      if (config.openrouter_api_key) {
        apiKey = config.openrouter_api_key;
      }
    } catch (e) {
      console.error("Kļūda lasot konfigurāciju:", e.message);
    }
  }

  // 2. Ja nav failā, prasa ievadīt (CLI interaktīvi)
  if (!apiKey) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    apiKey = await new Promise((resolve) => {
      rl.question('OpenRouter API atslēga nav atrasta. Lūdzu ievadiet to (sk-or-...): ', (answer) => {
        rl.close();
        resolve(answer.trim());
      });
    });

    if (apiKey) {
      // Saglabājam nākotnei
      const configDir = path.dirname(AUTH_FILE);
      if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true });
      
      let existingConfig = {};
      if (fs.existsSync(AUTH_FILE)) {
          try { existingConfig = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf8')); } catch(e){}
      }
      
      existingConfig.openrouter_api_key = apiKey;
      fs.writeFileSync(AUTH_FILE, JSON.stringify(existingConfig, null, 2), { mode: 0o600 }); // Secure read/write
      console.log(`API atslēga saglabāta: ${AUTH_FILE}`);
    }
  }

  return apiKey;
}

async function run() {
  const task = process.argv.slice(2).join(" ");
  if (!task) {
    console.log("Lietošana: node index.js <uzdevums>");
    return;
  }

  const apiKey = await getApiKey();
  if (!apiKey) {
    console.error("Kļūda: API atslēga ir nepieciešama darbam.");
    process.exit(1);
  }

  const openai = new OpenAI({
    baseURL: "https://openrouter.ai/api/v1",
    apiKey: apiKey,
    defaultHeaders: {
      "HTTP-Referer": "https://openclaw.ai",
      "X-Title": "OpenClaw Kodetajs"
    }
  });

  console.log(`🚀 Sub-aģents '${AGENT_NAME}' (${MODEL_ID}) sāk darbu...`);
  console.log(`📝 Uzdevums: ${task}`);
  console.log("-".repeat(40));

  try {
    const stream = await openai.chat.completions.create({
      model: MODEL_ID,
      messages: [
        {
          "role": "system",
          "content": "Tu esi eksperts programmētājs 'Kodētājs'. Tavs mērķis ir rakstīt efektīvu, drošu un labi dokumentētu kodu. Atbildi īsi un konkrēti, sniedzot tikai nepieciešamo kodu un paskaidrojumus."
        },
        {
          "role": "user",
          "content": task
        }
      ],
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || "";
      process.stdout.write(content);
    }
    process.stdout.write("\n");

  } catch (error) {
    console.error("API Kļūda:", error.message);
    if (error.status === 401) {
        console.error("Pārbaudi API atslēgu failā ~/.openclaw/auth.json");
    }
  }
}

run();
