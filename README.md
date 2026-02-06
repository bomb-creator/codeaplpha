# Weather MCP Agent (Google ADK-style Scaffold)

This repository contains a small, free weather agent that uses an MCP server to
fetch live conditions from the Open-Meteo API and exposes a simple agent loop
that can be wired into a Google ADK tool-calling flow.

## What’s Included
- **MCP weather server**: `app/weather_mcp_server.py` exposes a `get_weather`
  tool backed by the free Open‑Meteo endpoint (no API key required).
- **Agent entrypoint**: `app/agent.py` shows how an ADK-style agent can call the
  MCP tool to answer user weather queries.
- **MCP config**: `mcp_config.json` provides a ready‑to‑use stdio server
  definition.
- **.gitignore**: Added to exclude virtual environment and other artifacts.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the agent CLI directly (it handles server startup internally):
python app/agent.py --city "Seattle"
```

## Changes Made

### Code Updates
1. **Async/await implementation**: Converted `run_agent()` and `main()` functions to async to properly handle async context managers
2. **ClientSession wrapper**: Added `ClientSession` from `mcp.client.session` to wrap the stdio streams for proper tool calling
3. **Session initialization**: Added `await session.initialize()` before calling tools
4. **Timeout increase**: Increased API request timeouts from 20s to 60s to handle slower network conditions
5. **Fixed attribute name**: Changed `response.is_error` to `response.isError` (camelCase) to match actual API
6. **.gitignore**: Created `.gitignore` file with `venv` entry to exclude virtual environments

## Errors Encountered & Fixes

| Error | Root Cause | Solution |
|-------|-----------|----------|
| `TypeError: '_AsyncGeneratorContextManager' does not support context manager protocol` | `stdio_client()` returns an async context manager but was used with regular `with` | Changed to `async with` and made function async |
| `AttributeError: 'MemoryObjectSendStream' has no attribute 'call_tool'` | Raw stream objects don't have `call_tool()` method | Wrapped streams with `ClientSession(read, write)` |
| `McpError: Invalid request parameters` | Client wasn't initialized before use | Added `await session.initialize()` |
| `requests.exceptions.ReadTimeout: HTTPSConnectionPool... Read timed out` | Network was too slow for 20s timeout | Increased timeout to 60s in both geocoding and weather API calls |
| `AttributeError: 'CallToolResult' object has no attribute 'is_error'` | Wrong attribute name (Python naming vs API naming) | Changed to `response.isError` |

## Notes
Open‑Meteo is free for non‑commercial usage without an API key. For production,
review their terms and add caching or rate‑limiting as needed.
