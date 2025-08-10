from os import environ

import click

from commands.mcp_tool_optimize import mcp_tool_optimize
from lib.agent import set_openai_client
from lib.click import sync


@click.command()
@click.argument("url")
@click.argument("tool_name")
@click.option("--headers", default=None)
@click.option("--model", default="qwen3:30b-a3b-instruct-2507-q4_k_m")
@click.option("--model-base-url", default="http://localhost:11434/v1/")
@sync
async def mcp_tool_optimize_cmd(
    url: str,
    tool_name: str,
    headers: dict[str, str] | None = None,
    model: str = "gpt-oss:20b",
    model_base_url: str = "http://localhost:11434/v1/",
):
    click.echo("Optimizing MCP tool descriptions...")
    set_openai_client(model_base_url, environ.get("OPENAI_API_KEY", ""))

    result = await mcp_tool_optimize(url, tool_name, headers, model)

    click.echo("=============================")
    click.echo("Optimized tool description:")
    click.echo(result)
    click.echo("=============================")


if __name__ == "__main__":
    mcp_tool_optimize_cmd()
