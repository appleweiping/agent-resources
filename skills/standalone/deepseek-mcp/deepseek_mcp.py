#!/usr/bin/env python3
"""Minimal DeepSeek MCP server for Codex.

Exposes one tool:
  - deepseek_chat: send a prompt to DeepSeek's OpenAI-compatible chat API.

The API key is read from DEEPSEEK_API_KEY. The key is never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


DEFAULT_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEFAULT_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")


def read_message() -> dict[str, Any] | None:
    header_lines: list[bytes] = []
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        header_lines.append(line)

    headers: dict[str, str] = {}
    for raw in header_lines:
        key, _, value = raw.decode("ascii", errors="ignore").partition(":")
        headers[key.lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def write_message(message: dict[str, Any]) -> None:
    body = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def response(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def deepseek_chat(prompt: str, system: str | None, model: str | None, temperature: float, max_tokens: int) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set in the environment that launched Codex.")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{DEFAULT_BASE_URL.rstrip('/')}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek API HTTP {exc.code}: {body[:800]}") from exc
    result = json.loads(raw)
    return result["choices"][0]["message"]["content"]


TOOLS = [
    {
        "name": "deepseek_chat",
        "description": "Ask DeepSeek to perform a bounded text task such as summarization, brainstorming, rewriting, classification, or draft generation. Does not edit files by itself.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The user/task prompt to send to DeepSeek.",
                },
                "system": {
                    "type": "string",
                    "description": "Optional system instruction for DeepSeek.",
                },
                "model": {
                    "type": "string",
                    "description": "DeepSeek model name. Defaults to DEEPSEEK_MODEL or deepseek-chat.",
                },
                "temperature": {
                    "type": "number",
                    "description": "Sampling temperature.",
                    "default": 0.3,
                },
                "max_tokens": {
                    "type": "integer",
                    "description": "Maximum output tokens.",
                    "default": 1200,
                },
            },
            "required": ["prompt"],
            "additionalProperties": False,
        },
    }
]


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        return response(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "deepseek-local", "version": "0.1.0"},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return response(request_id, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name != "deepseek_chat":
            return error_response(request_id, -32601, f"Unknown tool: {name}")
        try:
            content = deepseek_chat(
                prompt=str(arguments["prompt"]),
                system=arguments.get("system"),
                model=arguments.get("model"),
                temperature=float(arguments.get("temperature", 0.3)),
                max_tokens=int(arguments.get("max_tokens", 1200)),
            )
            return response(request_id, {"content": [{"type": "text", "text": content}]})
        except Exception as exc:
            return error_response(request_id, -32000, str(exc))
    return error_response(request_id, -32601, f"Unsupported method: {method}")


def run_stdio() -> None:
    while True:
        message = read_message()
        if message is None:
            break
        result = handle(message)
        if result is not None:
            write_message(result)


def run_cli(prompt: str, system: str | None, model: str | None) -> None:
    print(deepseek_chat(prompt, system=system, model=model, temperature=0.3, max_tokens=1200))


def main() -> None:
    parser = argparse.ArgumentParser(description="DeepSeek MCP server / CLI tester")
    parser.add_argument("--prompt", help="Run a one-shot CLI call instead of MCP stdio mode.")
    parser.add_argument("--system", help="Optional system prompt for --prompt.")
    parser.add_argument("--model", help="Optional DeepSeek model.")
    args = parser.parse_args()
    if args.prompt:
        run_cli(args.prompt, args.system, args.model)
    else:
        run_stdio()


if __name__ == "__main__":
    main()
