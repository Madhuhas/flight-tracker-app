import requests
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def cached_status(flight_code, date):
    time.sleep(0.5)  # Small delay to help prevent 429 errors
    return get_flight_status(flight_code, date)

def get_flight_status(flight_code, date):
    url = f"https://aerodatabox.p.rapidapi.com/flights/number/{flight_code}/{date}"

    headers = {
        "X-RapidAPI-Key": "dc11990ademsh08c7100eda086e6p13cbbdjsn543887d8eb2d",
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 429:
            print(f"[{flight_code}] Rate limit hit: 429")
            return "Too Many Requests"
        if response.status_code != 200:
            print(f"[{flight_code}] Error: {response.status_code}")
            return "Unknown"

        data = response.json()
        for flight in data.get("departures", []) + data.get("arrivals", []):
            return flight.get("status", "Unknown")

        return "Unknown"
    except Exception as e:
        print(f"[{flight_code}] Exception: {e}")
        return "Unknown"
