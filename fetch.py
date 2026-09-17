# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

from pathlib import Path
import requests

# HKO Open Data API (English Version)
URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"

HERE = Path(__file__).parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

OUT_FILE = DATA / "kowloon_rainfall.json"


def fetch_data():
    headers = {"User-Agent": "pfad-student-assignment2"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    # Save raw English JSON response
    OUT_FILE.write_text(response.text, encoding="utf-8")
    print(f"Successfully downloaded raw HKO weather data to {OUT_FILE}")


if __name__ == "__main__":
    fetch_data()