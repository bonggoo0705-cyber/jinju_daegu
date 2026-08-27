"""Collect current weather from Open-Meteo and append it to a CSV file."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


API_URL = "https://api.open-meteo.com/v1/forecast"
CSV_PATH = Path(__file__).parent / "data" / "weather.csv"
TIMEZONE = "Asia/Seoul"
KST = timezone(timedelta(hours=9), name="KST")

LOCATIONS = (
    {"location": "진주", "latitude": 35.1796, "longitude": 128.1076},
    {"location": "대구", "latitude": 35.8714, "longitude": 128.6014},
)

FIELDNAMES = (
    "collected_at",
    "location",
    "latitude",
    "longitude",
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation",
    "weather_code",
    "weather_description",
)

WEATHER_DESCRIPTIONS = {
    0: "맑음",
    1: "대체로 맑음",
    2: "부분적으로 흐림",
    3: "흐림",
    45: "안개",
    48: "착빙 안개",
    51: "약한 이슬비",
    53: "보통 이슬비",
    55: "강한 이슬비",
    56: "약한 결빙 이슬비",
    57: "강한 결빙 이슬비",
    61: "약한 비",
    63: "보통 비",
    65: "강한 비",
    66: "약한 결빙비",
    67: "강한 결빙비",
    71: "약한 눈",
    73: "보통 눈",
    75: "강한 눈",
    77: "싸락눈",
    80: "약한 소나기",
    81: "보통 소나기",
    82: "강한 소나기",
    85: "약한 눈 소나기",
    86: "강한 눈 소나기",
    95: "뇌우",
    96: "약한 우박 동반 뇌우",
    99: "강한 우박 동반 뇌우",
}


def fetch_weather(latitude: float, longitude: float) -> dict:
    params = urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,apparent_temperature,"
                "precipitation,weather_code"
            ),
            "timezone": TIMEZONE,
        }
    )
    with urlopen(f"{API_URL}?{params}", timeout=30) as response:
        return json.load(response)["current"]


def collect() -> list[dict]:
    collected_at = datetime.now(KST).isoformat(timespec="seconds")
    rows = []
    for place in LOCATIONS:
        current = fetch_weather(place["latitude"], place["longitude"])
        code = current["weather_code"]
        rows.append(
            {
                "collected_at": collected_at,
                "location": place["location"],
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "temperature_2m": current["temperature_2m"],
                "relative_humidity_2m": current["relative_humidity_2m"],
                "apparent_temperature": current["apparent_temperature"],
                "precipitation": current["precipitation"],
                "weather_code": code,
                "weather_description": WEATHER_DESCRIPTIONS.get(code, "알 수 없음"),
            }
        )
    return rows


def append_rows(rows: list[dict]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with CSV_PATH.open("a", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    records = collect()
    append_rows(records)
    print(f"{len(records)}개 지역의 날씨 데이터를 {CSV_PATH}에 저장했습니다.")
