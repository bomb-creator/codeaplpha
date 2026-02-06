from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any, Dict

import requests
from mcp.client.stdio import StdioServerParameters, stdio_client

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


@dataclass(frozen=True)
class Location:
    name: str
    latitude: float
    longitude: float
    country: str


def _geocode_city(city: str) -> Location:
    response = requests.get(
        GEOCODE_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=20,
    )
    response.raise_for_status()
    results = response.json().get("results")
    if not results:
        raise ValueError(f"No results for city: {city}")
    match = results[0]
    return Location(
        name=match["name"],
        latitude=match["latitude"],
        longitude=match["longitude"],
        country=match.get("country", "Unknown"),
    )


def _format_weather(location: Location, weather: Dict[str, Any]) -> str:
    current = weather.get("current", {})
    return (
        f"{location.name}, {location.country}\n"
        f"Temperature: {current.get('temperature_2m')}°C "
        f"(feels like {current.get('apparent_temperature')}°C)\n"
        f"Precipitation: {current.get('precipitation')} mm\n"
        f"Wind Speed: {current.get('wind_speed_10m')} km/h\n"
        f"Weather Code: {current.get('weather_code')}\n"
        f"Timezone: {weather.get('location', {}).get('timezone')}"
    )


def run_agent(city: str) -> str:
    location = _geocode_city(city)
    server_params = StdioServerParameters(
        command="python",
        args=["app/weather_mcp_server.py"],
    )
    with stdio_client(server_params) as (read, write):
        response = write.call_tool(
            "get_weather",
            {"latitude": location.latitude, "longitude": location.longitude},
        )
    if response.is_error:
        raise RuntimeError(response.error)
    weather_data = json.loads(response.content[0].text)
    return _format_weather(location, weather_data)


def main() -> None:
    parser = argparse.ArgumentParser(description="MCP weather agent CLI")
    parser.add_argument("--city", required=True, help="City name to look up")
    args = parser.parse_args()
    print(run_agent(args.city))


if __name__ == "__main__":
    main()
