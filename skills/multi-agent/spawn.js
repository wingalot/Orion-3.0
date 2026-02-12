const { spawn } = require('child_process');
// NOTE: This is a CLI wrapper. The actual spawning happens via the OpenClaw runtime tool `sessions_spawn`.
// This script is just a placeholder to invoke the tool via user prompt or similar,
// OR it could use the `openclaw sessions spawn` CLI command if one exists (which it does via `openclaw exec`).
// But the core tool `sessions_spawn` is the preferred way inside a session.

console.log("To spawn a sub-agent session, use the tool `sessions_spawn` directly in your prompt.");
console.log("Example: `sessions_spawn(task='Research this topic', label='researcher')`");
