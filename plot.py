# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import json
from pathlib import Path
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "kowloon_rainfall.json"
OUT_DIR = HERE / "out"
OUT_DIR.mkdir(exist_ok=True)

# Main weather stations in Kowloon region
KOWLOON_STATIONS = [
    "Kowloon City",
    "Wong Tai Sin",
    "Kwun Tong",
    "Sham Shui Po",
    "Yau Tsim Mong",
]


def main():
    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}. Please run fetch.py first.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract rainfall section from API data
    rainfall_data = data.get("rainfall", {}).get("data", [])

    stations = []
    rainfall_values = []

    # Filter for Kowloon stations
    for place in rainfall_data:
        station_name = place.get("place", "")
        if any(ks.lower() in station_name.lower() for ks in KOWLOON_STATIONS):
            val = place.get("max", 0)
            stations.append(station_name)
            rainfall_values.append(val)

    # Fallback: take first 5 stations if Kowloon names differ
    if not stations:
        for place in rainfall_data[:5]:
            stations.append(place.get("place", "Station"))
            rainfall_values.append(place.get("max", 0))

    # Plotting chart
    plt.figure(figsize=(9, 5))
    bars = plt.bar(stations, rainfall_values, color="#3498db", edgecolor="#2980b9")

    # Pure English Title & Axis Labels
    plt.title("Kowloon Hourly Rainfall (mm)")
    plt.xlabel("Kowloon Weather Station")
    plt.ylabel("Rainfall (mm)")
    plt.ylim(0, max(rainfall_values) + 5 if rainfall_values else 10)
    plt.xticks(rotation=20, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Display numeric values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.1,
            f"{height} mm",
            ha="center",
            va="bottom",
        )

    out_path = OUT_DIR / "plot.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"Chart saved successfully to {out_path}")


if __name__ == "__main__":
    main()