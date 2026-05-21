# DeepSeek MCP for Codex

This is a small local MCP server that lets Codex call DeepSeek as an optional tool without changing Codex's main model.

## Tool

- `deepseek_chat`: sends a bounded prompt to DeepSeek and returns text.

Good uses:

- summarization
- rewriting
- brainstorming
- classification
- cheap batch drafting

Not recommended:

- autonomous file editing
- security-sensitive reasoning
- tasks requiring Codex tool access

## Environment

The server reads:

- `DEEPSEEK_API_KEY` - required
- `DEEPSEEK_MODEL` - optional, defaults to `deepseek-chat`
- `DEEPSEEK_BASE_URL` - optional, defaults to `https://api.deepseek.com`

Do not put the API key in `config.toml`.

## Test

```powershell
& "C:\Users\admin\AppData\Local\OpenAI\Codex\bin\node.exe" D:\Skill\deepseek-mcp\deepseek_mcp.mjs --prompt "Say hello in one sentence."
```

## Codex Config

Add this to `C:\Users\admin\.codex\config.toml`:

```toml
[features]
rmcp_client = true

[mcp_servers.deepseek]
command = "C:\\Users\\admin\\AppData\\Local\\OpenAI\\Codex\\bin\\node.exe"
args = ["D:\\Skill\\deepseek-mcp\\deepseek_mcp.mjs"]
env_vars = ["DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "DEEPSEEK_BASE_URL"]
startup_timeout_sec = 10
tool_timeout_sec = 120
```

Restart Codex after editing the config.
