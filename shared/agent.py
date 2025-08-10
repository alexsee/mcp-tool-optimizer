import click
from agents import (
    Agent,
    RunContextWrapper,
    TContext,
    Tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.lifecycle import AgentHooksBase
from openai import AsyncOpenAI


def set_openai_client(base_url: str, api_key: str):
    custom_client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    set_default_openai_client(custom_client)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)


class AgentClickHook(AgentHooksBase):
    async def on_tool_start(
        self,
        context: RunContextWrapper[TContext],
        agent: Agent,
        tool: Tool,
    ) -> None:
        click.echo(f"Agent `{agent.name}` is using tool: `{tool.name}`")
