# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

A learning/reference repo for the Claude Agent SDK (`claude_agent_sdk` Python package). Each top-level script is a standalone example of one SDK feature; `claude-agent-api/` wraps the same pattern in a FastAPI service. Not a production application.

## Setup and Running

`.env` at the project root (also a copy in `claude-agent-api/`):
```
ANTHROPIC_API_KEY="sk-ant-..."
CLAUDE_MODEL="claude-sonnet-4-6"
```

```bash
pip install claude-agent-sdk python-dotenv
python claude_agent_sdk_use.py          # Read/Edit/Glob review of utils.py (acceptEdits — modifies utils.py)
python claude_agent_sdk_multi_tool.py   # remote Microsoft Learn MCP server + WebSearch/WebFetch
python subagents.py                     # two AgentDefinitions orchestrated via the Agent tool
python claude_skills.py                 # loads the project skill .claude/skills/marketing-review
```

Run scripts from the repo root: `claude_skills.py` passes `cwd=os.getcwd()` with `setting_sources=["project"]`, so the skill is only found when cwd contains `.claude/skills/`. The SDK drives the Claude Code CLI, so Node + `@anthropic-ai/claude-code` must be installed (the Dockerfile installs both).

No build step, tests, or linter exist.

## Shared Script Pattern

Every script (and `claude-agent-api/app.py`) follows the same skeleton:
1. `load_dotenv()`, then `os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")`.
2. `async for message in query(prompt=..., options=ClaudeAgentOptions(model=claude_model, ...))` inside `asyncio.run(main())`.
3. Branch on `AssistantMessage` (print `block.text`; blocks with `.name` are tool uses) and `ResultMessage` (`.subtype`, `.result`).

Feature-specific `ClaudeAgentOptions` usage:
- **MCP:** `mcp_servers={"MSLearnMCPServer": {"type": "http", "url": ...}}`; its tools are allowed via the `mcp__MSLearnMCPServer__*` wildcard, so renaming the server key requires updating the prefix.
- **Subagents:** `agents={name: AgentDefinition(...)}` plus `allowed_tools=["Agent"]` so the main agent can delegate.
- **Skills:** `skills=["marketing-review"]` + `setting_sources=["project"]`; the skill content (brand guidelines, checklist, LinkedIn template) lives in `.claude/skills/marketing-review/`.

`utils.py` is just the target for the code-review demo, not a shared library.

## claude-agent-api/

FastAPI app exposing `POST /chat` (`{"prompt": str}` → `{"response": str, "tools_used": [str]}`) using the MS Learn MCP setup. Run with `docker compose build && docker compose up` from inside that directory; Swagger at `http://localhost:8000/docs`. It has its own `CLAUDE.md` with details, and pins `claude-agent-sdk==0.2.129` in `requirements.txt` — check that version's API before using newer `ClaudeAgentOptions` fields there.

## Models

Model comes from `CLAUDE_MODEL`. Default to `claude-sonnet-4-6`; other IDs in use: `claude-opus-4-7`, `claude-haiku-4-5-20251001`.
