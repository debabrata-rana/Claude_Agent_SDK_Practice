# Claude Agent SDK Practice

This repository is a learning and reference project for the Anthropic Claude Agent SDK. It demonstrates multiple ways to use Claude agent workflows in Python, including:

- direct SDK queries
- repo-aware file review and editing
- tool usage with MCP servers
- multi-agent collaboration
- skills-based prompting
- FastAPI exposure of an agent endpoint

This project is designed for experimentation and education rather than production deployment.

## Project purpose

The repo shows how to integrate the Claude Agent SDK with:

- local files and project folders
- external MCP servers such as Microsoft Learn
- multiple specialized agents working together
- developer skills for content refinement or review tasks
- a web API that accepts user prompts and returns agent responses

## Repository structure

- `claude_agent_sdk_use.py`  
  Basic async example using `query()` to review and fix code in a local project file.

- `claude_agent_sdk_multi_tool.py`  
  Example that connects to the Microsoft Learn MCP server and uses agent tools like `WebSearch`, `WebFetch`, and MCP tool calls.

- `subagents.py`  
  Example that defines multiple agents and invokes them in sequence for a marketing workflow.

- `claude_skills.py`  
  Example that loads a project skill (`marketing-review`) and uses it to improve a LinkedIn announcement.

- `utils.py`  
  Small helper module that acts as the target for code-review / fix tasks.

- `claude-agent-api/`  
  FastAPI app that exposes a `/chat` endpoint and forwards prompts to Claude Agent SDK through the Microsoft Learn MCP server.

## Required setup

Create a `.env` file in the project root with:

```env
ANTHROPIC_API_KEY="sk-ant-..."
CLAUDE_MODEL="claude-sonnet-4-6"
```

Then install the Python dependencies:

```bash
pip install claude-agent-sdk python-dotenv
```

## Running the examples

### 1) Local code-review workflow

```bash
python claude_agent_sdk_use.py
```

This script:

- loads environment variables
- sets `ANTHROPIC_API_KEY` from `ANTHROPIC_API_KEY` in `.env` file
- calls `query()` with a prompt asking the agent to inspect `utils.py` for crash-causing bugs
- limits the allowed tools to `Read`, `Edit`, and `Glob`
- uses `permission_mode="acceptEdits"`

### 2) Microsoft Learn MCP workflow

```bash
python claude_agent_sdk_multi_tool.py
```

This script connects to the Microsoft Learn MCP endpoint:

```python
"https://learn.microsoft.com/api/mcp"
```

It uses tools such as:

- `mcp__MSLearnMCPServer__*`
- `WebSearch`
- `WebFetch`
- `Read`
- `Edit`
- `Glob`

This demonstrates how to use external MCP documentation tools in a real-world assistant flow.

### 3) Multi-agent workflow

```bash
python subagents.py
```

This script creates two named agents:

- `market-researcher`
- `content-creator`

The prompt asks the system to first determine the target audience for an AI-powered fitness smartwatch, then generate a LinkedIn announcement using the content-focused agent.

### 4) Skill-based workflow

```bash
python claude_skills.py
```

This example registers `skills=["marketing-review"]` and asks the agent to improve a marketing message.

## FastAPI sample app

The `claude-agent-api` directory contains a minimal API app that exposes Claude to an HTTP client.

### Files

- `claude-agent-api/app.py`  
  FastAPI application with `/chat` endpoint

- `claude-agent-api/Dockerfile`  
  Docker image definition

- `claude-agent-api/docker-compose.yml`  
  Container orchestration for the API

- `claude-agent-api/requirements.txt`  
  Dependencies for the app container

### Running the API with Docker

From inside the `claude-agent-api` directory:

```bash
docker compose build
docker compose up
```

Then access:

- Swagger UI: `http://localhost:8000/docs`
- Chat endpoint: `http://localhost:8000/chat`

### API request format

`POST /chat`

Request body:

```json
{
  "prompt": "Give me a Python example for Azure Cosmos DB using the Microsoft Learn MCP server."
}
```

Example response payload:

```json
{
  "response": "...",
  "tools_used": ["mcp__MSLearnMCPServer__*", "WebFetch"]
}
```

The endpoint is implemented as a POST-only route. A direct GET request to `/chat` will be rejected by FastAPI with a method-not-allowed response.

## Notes

- The project is focused on learning and experimentation with the Claude Agent SDK.
- It demonstrates direct tool calls, skill usage, agent collaboration, and external MCP access.
- The API sample is intended as a lightweight integration example, not a production deployment.

## Example model usage

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Review this repo for issues.",
    options=ClaudeAgentOptions(
        model="claude-sonnet-4-6",
        allowed_tools=["Read", "Edit", "Glob"],
    ),
):
    print(message)
```

This pattern is used throughout the repo to connect agent prompts to the Claude model and available tools.
