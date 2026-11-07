# pip install claude-agent-sdk

# import statements
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
import os
from dotenv import load_dotenv
import asyncio
from typing import Any

load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
claude_model = os.getenv("CLAUDE_MODEL")


async def main():

    async for message in query(
        prompt="Give me python code snippet for Microsoft Foundry SDK Client Creation using the MSLearn MCP Server",
        options=ClaudeAgentOptions(
            model=claude_model,
            mcp_servers={"MSLearnMCPServer": {
                "type": "http",
                "url": "https://learn.microsoft.com/api/mcp"
            }},
            allowed_tools=["mcp__MSLearnMCPServer__*", "Read",
                           "Edit", "Glob", "WebSearch", "WebFetch"]
        ),
    ):

        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)

                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")

        elif isinstance(message, ResultMessage):
            print(f"\nCompleted: {message.subtype}")

asyncio.run(main())
