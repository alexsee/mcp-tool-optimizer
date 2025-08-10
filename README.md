# MCP Tool Optimizer

Small CLI to optimize Model Context Protocol (MCP) tool descriptions using an LLM. It connects to an MCP server, exercises the selected tool with sample inputs, and generates a concise, clearer description that LLMs can follow reliably.

## Requirements

- Python 3.12+
- An accessible MCP server URL and the target tool name
- An OpenAI-compatible API endpoint for the model (OpenAI, vLLM, Ollama, etc.)
	- Configure via `--model-base-url` and `OPENAI_API_KEY` when required

Defaults are aimed at a local Ollama-style endpoint (`http://localhost:11434/v1/`) with a compatible model name. You can point to OpenAI with `https://api.openai.com/v1/` and set `OPENAI_API_KEY`.

## Install

You can use uv (recommended if you have it) or plain pip.

### Using uv

```bash
# From the repo root
uv sync
```


## Usage

Run the CLI directly from the repo (works with uv or pip):

```bash
# Generic
OPENAI_API_KEY=your_key \
uv run python main.py <MCP_SERVER_URL> <TOOL_NAME> \
	--headers '<optional JSON map>' \
	--model '<model-id>' \
	--model-base-url '<openai-compatible-base-url>'
```

Examples:

```bash
# Local LLM via Ollama-compatible API
uv run python main.py http://localhost:3000 my_tool \
	--model 'llama3.1:8b-instruct-q4_K_M' \
	--model-base-url 'http://localhost:11434/v1/'

# OpenAI API
export OPENAI_API_KEY=sk-...
uv run python main.py https://your-mcp-server.example.com my_tool \
	--model 'gpt-4o-mini' \
	--model-base-url 'https://api.openai.com/v1/'
```


## Options

- `url` (positional): MCP server URL (e.g., `http://localhost:3000`).
- `tool_name` (positional): The exact MCP tool name to optimize.
- `--headers` (optional): String containing a JSON object with HTTP headers (e.g., `'{"Authorization":"Bearer ..."}'`).
- `--model` (optional): Chat model ID (default may point to a local model).
- `--model-base-url` (optional): OpenAI-compatible base URL (default `http://localhost:11434/v1/`).

Environment:

- `OPENAI_API_KEY`: Used if your selected endpoint requires an API key.

## How it works (high level)

The command spins up an MCP HTTP client, filters to the specified tool, and runs a small agent loop that:

- Probes the tool with example inputs
- Learns constraints from responses
- Emits a rewritten description (<=100 words) suited for LLM planners

## Development

```bash
# Install dev tools
uv sync --group dev

# Lint and format
uv run ruff check
uv run ruff format
```

Pre-commit hooks are configured in `pyproject.toml` for local linting if you enable them in your environment.
