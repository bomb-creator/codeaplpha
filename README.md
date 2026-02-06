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

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# In one terminal, run the MCP server:
python app/weather_mcp_server.py

# In another terminal, run the agent CLI:
python app/agent.py --city "Seattle"
```

## Notes
Open‑Meteo is free for non‑commercial usage without an API key. For production,
review their terms and add caching or rate‑limiting as needed.
