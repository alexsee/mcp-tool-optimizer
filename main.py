import click


@click.command()
@click.argument("url")
@click.argument("tool_name")
@click.option("--headers", default=None)
async def mcp_tool_optimize(url: str, tool_name: str, headers: dict[str, str] | None = None):
    click.echo("Optimizing MCP tool descriptions...")
    result = await mcp_tool_optimize(url, tool_name, headers)
    click.echo(result)


if __name__ == "__main__":
    mcp_tool_optimize()
