from __future__ import annotations

from typing import Any, Dict

import requests
from fastmcp import FastMCP

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

mcp = FastMCP("weather")


def _fetch_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    response = requests.get(
        OPEN_METEO_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
            ],
            "timezone": "auto",
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": payload.get("timezone"),
        },
        "current": payload.get("current", {}),
    }


@mcp.tool()
def get_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """Return current weather conditions using Open-Meteo (free)."""
    return _fetch_weather(latitude, longitude)


if __name__ == "__main__":
    mcp.run()
