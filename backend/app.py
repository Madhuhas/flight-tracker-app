from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os

app = Flask(__name__)
CORS(app)

def load_status_cache():
    if os.path.exists("status_cache.json"):
        with open("status_cache.json", "r") as f:
            return json.load(f)
    return {}

def load_flight_data():
    df = pd.read_excel("flights.xlsx", engine="openpyxl")
    df.columns = [col.strip().replace('\n', ' ') for col in df.columns]

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

    iata_map = {
        "Alaska Airlines": "AS",
        "Southwest Airlines": "WN",
        "American Airlines": "AA",
        "Delta Airlines": "DL",
        "United Airlines": "UA",
        "Frontier Airlines": "F9",
        "Allegiant Airlines": "G4"
    }

    status_cache = load_status_cache()
    flights = []

    for _, row in df.iterrows():
        airline = row["Airline"]
        iata = iata_map.get(airline, "")
        flight_number = str(row["FlightNumber"]).strip()
        flight_code = iata + flight_number
        date_str = row["Date"].strftime("%Y-%m-%d")

        cache_key = f"{flight_code}_{date_str}"
        status = status_cache.get(cache_key, "Unknown")

        row_dict = row.to_dict()
        row_dict["Status"] = status
        flights.append(row_dict)

    return flights

@app.route("/api/flights")
def get_flights():
    return jsonify(load_flight_data())

if __name__ == "__main__":
    app.run(debug=True)
