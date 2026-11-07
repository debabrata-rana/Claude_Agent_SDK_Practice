# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

A minimal FastAPI wrapper that exposes a Claude Agent SDK agent over HTTP. It's a sub-project of the parent learning repo (see `../CLAUDE.md` and `../README.md`) and has its own dependencies, Docker image, and `.env`.

## Commands

Run from this directory (`claude-agent-api/`):

```bash
docker compose build     # build the image (Python 3.12 + Node 22 + Claude Code CLI)
docker compose up        # serve on http://localhost:8000
```

To run without Docker, install the pinned deps and start uvicorn. The Dockerfile installs `@anthropic-ai/claude-code` globally via npm, so do the same locally if the SDK can't find the CLI:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

There are no tests or linters. To check it manually, use Swagger UI at `http://localhost:8000/docs` or send a POST:

```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"prompt": "Sample Python code for Azure Cosmos DB from MS Learn"}'
```

A GET to `/chat` returns 405. The route only accepts POST.

## Architecture

Everything lives in `app.py`. There is one endpoint, `POST /chat`, which takes `{"prompt": str}` and returns `{"response": str, "tools_used": [str]}`.

- **Config:** at import time `load_dotenv()` reads `.env`, then `ANTHROPIC_API_KEY` is copied into `ANTHROPIC_API_KEY`, which the SDK reads. `CLAUDE_MODEL` picks the model.
- **Agent call:** each request runs a fresh `claude_agent_sdk.query()`. No session or conversation state is kept between requests. Options are built inline and use:
  - the remote Microsoft Learn MCP server (`https://learn.microsoft.com/api/mcp`, HTTP transport) under the name `MSLearnMCPServer`. Its tools are allowed through the wildcard `mcp__MSLearnMCPServer__*`. Renaming the server key means updating this prefix as well.
  - built-in tools `Read`, `Edit`, `Glob`, `WebSearch`, `WebFetch`. No `permission_mode` or `cwd` is set, so file tools act on the server process's working directory (`/app` in the container).
- **Response assembly:** text blocks from each `AssistantMessage` are concatenated. Blocks that have a `name` attribute (tool-use blocks) go into `tools_used`. If the final `ResultMessage.result` is non-empty, it **replaces** the accumulated text rather than being appended.
- **Container:** `COPY . .` copies the whole directory into the image, and there is no `.dockerignore`, so the local `.env` ends up in the image as well as being passed via `env_file` in `docker-compose.yml`.

## Versions

`requirements.txt` pins `claude-agent-sdk==0.2.129`. Check that version's API before using newer `ClaudeAgentOptions` fields.
