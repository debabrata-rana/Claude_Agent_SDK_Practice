# pip install claude-agent-sdk

# import statements
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
claude_model = os.getenv("CLAUDE_MODEL")


async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
        options=ClaudeAgentOptions(
            model=claude_model,
            max_tokens=1024,
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
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
