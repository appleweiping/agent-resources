#!/usr/bin/env node
// Minimal DeepSeek MCP server for Codex.

const DEFAULT_MODEL = process.env.DEEPSEEK_MODEL || "deepseek-chat";
const DEFAULT_BASE_URL = process.env.DEEPSEEK_BASE_URL || "https://api.deepseek.com";

function normalizeModel(model) {
  if (!model) return DEFAULT_MODEL;
  const name = String(model).trim();
  const aliases = {
    v4pro: "deepseek-v4-pro",
    "v4-pro": "deepseek-v4-pro",
    pro: "deepseek-v4-pro",
    v4flash: "deepseek-v4-flash",
    "v4-flash": "deepseek-v4-flash",
    flash: "deepseek-v4-flash",
  };
  return aliases[name.toLowerCase()] || name;
}

function writeMessage(message) {
  const body = Buffer.from(JSON.stringify(message), "utf8");
  process.stdout.write(`Content-Length: ${body.length}\r\n\r\n`);
  process.stdout.write(body);
}

let buffer = Buffer.alloc(0);

function tryReadMessages() {
  while (true) {
    const sep = buffer.indexOf("\r\n\r\n");
    if (sep === -1) return;
    const header = buffer.slice(0, sep).toString("ascii");
    const match = /content-length:\s*(\d+)/i.exec(header);
    if (!match) {
      throw new Error("Missing Content-Length header");
    }
    const length = Number(match[1]);
    const start = sep + 4;
    const end = start + length;
    if (buffer.length < end) return;
    const body = buffer.slice(start, end).toString("utf8");
    buffer = buffer.slice(end);
    handle(JSON.parse(body));
  }
}

function response(id, result) {
  return { jsonrpc: "2.0", id, result };
}

function errorResponse(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}

async function deepseekChat({ prompt, system, model, temperature = 0.3, max_tokens = 1200 }) {
  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    throw new Error("DEEPSEEK_API_KEY is not set in the environment that launched Codex.");
  }

  const messages = [];
  if (system) messages.push({ role: "system", content: String(system) });
  messages.push({ role: "user", content: String(prompt) });

  const res = await fetch(`${DEFAULT_BASE_URL.replace(/\/$/, "")}/chat/completions`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: normalizeModel(model),
      messages,
      temperature,
      max_tokens,
    }),
  });

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`DeepSeek API HTTP ${res.status}: ${text.slice(0, 800)}`);
  }
  const data = JSON.parse(text);
  return data.choices?.[0]?.message?.content ?? "";
}

const tools = [
  {
    name: "deepseek_chat",
    description:
      "Ask DeepSeek to perform a bounded text task such as summarization, brainstorming, rewriting, classification, or draft generation. Does not edit files by itself.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "The user/task prompt to send to DeepSeek." },
        system: { type: "string", description: "Optional system instruction for DeepSeek." },
        model: { type: "string", description: "DeepSeek model name. Defaults to DEEPSEEK_MODEL or deepseek-chat." },
        temperature: { type: "number", description: "Sampling temperature.", default: 0.3 },
        max_tokens: { type: "integer", description: "Maximum output tokens.", default: 1200 },
      },
      required: ["prompt"],
      additionalProperties: false,
    },
  },
];

async function handle(message) {
  const { id, method, params = {} } = message;
  try {
    if (method === "initialize") {
      writeMessage(
        response(id, {
          protocolVersion: "2024-11-05",
          capabilities: { tools: {} },
          serverInfo: { name: "deepseek-local", version: "0.1.0" },
        }),
      );
      return;
    }
    if (method === "notifications/initialized") return;
    if (method === "tools/list") {
      writeMessage(response(id, { tools }));
      return;
    }
    if (method === "tools/call") {
      if (params.name !== "deepseek_chat") {
        writeMessage(errorResponse(id, -32601, `Unknown tool: ${params.name}`));
        return;
      }
      const text = await deepseekChat(params.arguments || {});
      writeMessage(response(id, { content: [{ type: "text", text }] }));
      return;
    }
    writeMessage(errorResponse(id, -32601, `Unsupported method: ${method}`));
  } catch (error) {
    writeMessage(errorResponse(id, -32000, error instanceof Error ? error.message : String(error)));
  }
}

async function runCli() {
  const idx = process.argv.indexOf("--prompt");
  if (idx !== -1) {
    const prompt = process.argv[idx + 1];
    const modelIdx = process.argv.indexOf("--model");
    const systemIdx = process.argv.indexOf("--system");
    const out = await deepseekChat({
      prompt,
      model: modelIdx !== -1 ? process.argv[modelIdx + 1] : undefined,
      system: systemIdx !== -1 ? process.argv[systemIdx + 1] : undefined,
    });
    console.log(out);
    return true;
  }
  return false;
}

if (!(await runCli())) {
  process.stdin.on("data", (chunk) => {
    buffer = Buffer.concat([buffer, chunk]);
    tryReadMessages();
  });
}
