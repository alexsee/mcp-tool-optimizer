from typing import Any

from agents import Agent, Runner
from agents.mcp import create_static_tool_filter
from agents.mcp.server import MCPServerStreamableHttp

from lib.agent import AgentClickHook


def get_instructions(tool_name: str) -> str:
    return f"""
You are an AI Agent Tool developer that can make the description of a tool more precise and clear.
The problem is that the LLM sometimes doesn't translate the queries correctly.
This comes from the fact that the tool description doesn't explain what exactly is allowed and how to use the tool correctly.

Your task is to create a proper tool description that LLMs can use to understand the tool's functionality and limitations.
Given the tool description, think of possible example tool calls and produce those that are likely to be correctly executed.
Think of parameter values that are reasonable, make sense, and are likely tool calls that people use in the real world.
Use the tool's input schema as a guide for crafting your queries.

You have access to the `{tool_name}` tool so you can experiment with different inputs and see how the tool responds.
Repeat calling the tool with different inputs to explore its behavior.

## Structure of the description
- The description is a manual on how to use the tool correctly and what is allowed and what is not.
- It should explain how to avoid the issues that were found in the examples.
- Add that the tool can be invoked multiple times for better validation of the file system state.
- Also give few examples if you think they are applicable.
- The new description shouldn't be longer than 100 words.

## Output
- Please create tool description that an LLM can understand.
- Only return the description of the tool.
"""


async def mcp_tool_optimize(
    url: str,
    tool_name: str,
    headers: dict[str, str] | None = None,
    model: str | None = None,
) -> Any:
    """Optimize MCP tool descriptions.

    Args:
        url (str): The URL of the MCP server.
        tool_name (str): The name of the tool to optimize.
        headers (dict[str, str] | None): Headers to include in the request.

    Return:
        Any: The optimized tool description.
    """
    # define mcp server
    async with MCPServerStreamableHttp(
        params={
            "url": url,
            "headers": headers,
        },
        tool_filter=create_static_tool_filter(allowed_tool_names=[tool_name]),
    ) as mcp_server:
        await mcp_server.connect()

        # define agent
        agent = Agent(
            name="MCP Tool Optimizer",
            instructions=get_instructions(tool_name),
            mcp_servers=[mcp_server],
            model=model,
            hooks=AgentClickHook(),
        )

        # run agent
        result = await Runner.run(agent, "Optimize the tool with the name " + tool_name)

        await mcp_server.cleanup()
        return result.final_output
