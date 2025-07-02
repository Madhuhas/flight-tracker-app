import pandas as pd
import requests
import json
import time

# IATA code lookup
IATA_MAP = {
    "Alaska Airlines": "AS",
    "Southwest Airlines": "WN",
    "American Airlines": "AA",
    "Delta Airlines": "DL",
    "United Airlines": "UA",
    "Frontier Airlines": "F9",
    "Allegiant Airlines": "G4"
}

API_KEY = "dc11990ademsh08c7100eda086e6p13cbbdjsn543887d8eb2d"
API_HOST = "aerodatabox.p.rapidapi.com"

def get_status(flight_code, date):
    url = f"https://{API_HOST}/flights/number/{flight_code}/{date}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 429:
            print(f"[{flight_code}] ⛔ Rate limit hit")
            return "Too Many Requests"
        if res.status_code != 200:
            print(f"[{flight_code}] ❌ Error: {res.status_code}")
            return "Unknown"

        data = res.json()
        for flight in data.get("arrivals", []) + data.get("departures", []):
            return flight.get("status", "Unknown")
        return "Unknown"

    except Exception as e:
        print(f"[{flight_code}] ❗ Exception: {e}")
        return "Unknown"

def update_status_cache():
    df = pd.read_excel("flights.xlsx", engine="openpyxl")
    df.columns = [col.strip().replace("\n", " ") for col in df.columns]
    df.rename(columns={
        "First and Last Name": "Name",
        "Phone Number": "Phone",
        "Check-Out Date": "Date",
        "Check-Out Time": "Time",
        "Arriving Airlines Name": "Airline",
        "Flight Number": "FlightNumber",
        "Number Of Passenger": "PassengerCount",
        "Arrival Airport": "ArrivalAirport"
    }, inplace=True)

    df["Time"] = df["Time"].apply(lambda t: t.strftime("%I:%M %p") if not pd.isnull(t) else "")

    status_map = {}
    for _, row in df.iterrows():
        airline = row["Airline"]
        iata = IATA_MAP.get(airline, "")
        flight_number = str(row["FlightNumber"]).strip()
        flight_code = iata + flight_number
        date_str = row["Date"].strftime("%Y-%m-%d")

        key = f"{flight_code}_{date_str}"
        status = get_status(flight_code, date_str)
        status_map[key] = status
        time.sleep(1)  # polite delay

    with open("status_cache.json", "w") as f:
        json.dump(status_map, f, indent=2)
    print("✅ Status cache updated.")

if __name__ == "__main__":
    update_status_cache()
