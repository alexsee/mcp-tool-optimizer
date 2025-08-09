import asyncio
from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
import click
from openai import AsyncOpenAI

from commands.mcp_tool_optimize import mcp_tool_optimize
from functools import wraps


def use_ollama():
    custom_client = AsyncOpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")
    set_default_openai_client(custom_client)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


def sync(func):
    """Decorator that wraps coroutine with asyncio.run."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.command()
@click.argument("url")
@click.argument("tool_name")
@click.option("--headers", default=None)
@click.option("--model", default="qwen3:30b-a3b-instruct-2507-q4_k_m")
@sync
async def mcp_tool_optimize_cmd(
    url: str,
    tool_name: str,
    headers: dict[str, str] | None = None,
    model: str = "qwen3:30b-a3b-instruct-2507-q4_k_m",
):
    click.echo("Optimizing MCP tool descriptions...")
    use_ollama()

    result = await mcp_tool_optimize(url, tool_name, headers, model)

    click.echo("=============================")
    click.echo("Optimized tool description:")
    click.echo(result)
    click.echo("=============================")


if __name__ == "__main__":
    mcp_tool_optimize_cmd()
