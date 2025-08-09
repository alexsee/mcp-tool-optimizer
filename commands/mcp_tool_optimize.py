from typing import Any
from agents import Agent, Runner
from agents.mcp.server import MCPServerStreamableHttp
from agents.mcp import create_static_tool_filter


instructions = """
You are an AI Agent Tool developer can you make the description of a tool more precise and clear.
The problem is that the LLM sometimes doesn't translate the queries correctly.
This comes from the fact that the tool description doesn't explain what exactly is allowed and how to use the tool correctly.

How can these issues be avoided by validation i.e. with this tool or external resources or it's just a user mistake? List the main issues and how to avoid them.

Now that the issues and how to avoid them are clear. Please create tool description that addresses these issues. The description is a manual on how to use the tool correctly and what is allowed and what is not.
It should explain how to avoid the issues that were found in the examples. Add that the tool can be invoked multiple times for better validation of the file system state.

Also give few examples if you think they are applicable.

Please provide description which reflects these issues. The new description shouldn't be longer than 100 words.
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
            instructions=instructions,
            mcp_servers=[mcp_server],
            model=model,
        )

        # run agent
        result = await Runner.run(agent, "Optimize the tool with the name " + tool_name)

        await mcp_server.cleanup()
        return result.final_output
