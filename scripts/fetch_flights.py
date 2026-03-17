# scripts/fetch_flights.py
# User inputs their own origin and destination

import requests
import json
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "sky-scrapper.p.rapidapi.com"

headers = {
    "x-rapidapi-host": RAPIDAPI_HOST,
    "x-rapidapi-key": RAPIDAPI_KEY
}

DAYS_OUT = [7, 14, 30]

# -----------------------------------------------
# SEARCH AIRPORT ENTITY ID
# -----------------------------------------------
def get_airport_entity(airport_code):
    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"
    querystring = {"query": airport_code, "locale": "en-US"}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    results = data.get("data", [])
    if not results:
        print(f"Could not find airport: {airport_code}")
        return None, None

    # Take first result
    first = results[0]
    sky_id = first.get("skyId")
    entity_id = first.get("entityId")
    name = first.get("presentation", {}).get("title", airport_code)
    print(f"Found: {name} (skyId={sky_id}, entityId={entity_id})")
    return sky_id, entity_id


# -----------------------------------------------
# FETCH FLIGHTS
# -----------------------------------------------
def fetch_flights(origin_sky, destination_sky, origin_entity, destination_entity, days_out):
    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"

    future_date = (datetime.now() + timedelta(days=days_out)).strftime("%Y-%m-%d")
    print(f"\nFetching: {origin_sky} → {destination_sky} on {future_date}")

    querystring = {
        "originSkyId": origin_sky,
        "destinationSkyId": destination_sky,
        "originEntityId": origin_entity,
        "destinationEntityId": destination_entity,
        "date": future_date,
        "cabinClass": "economy",
        "adults": "1",
        "currency": "USD",
        "market": "en-US",
        "countryCode": "US"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json(), future_date


# -----------------------------------------------
# SAVE TO POSTGRESQL
# -----------------------------------------------
def save_to_db(flights, origin, destination, flight_date):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "flight_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()

    saved = 0
    for flight in flights:
        try:
            cursor.execute("""
                INSERT INTO flights (origin, destination, flight_date, price, airline, duration, stops)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                origin,
                destination,
                flight_date,
                flight.get("price"),
                flight.get("airline"),
                flight.get("duration"),
                flight.get("stops", 0)
            ))
            saved += 1
        except Exception as e:
            print(f"Error saving flight: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {saved} flights")


# -----------------------------------------------
# MAIN
# -----------------------------------------------
if __name__ == "__main__":
    print("=== FlightLens: Flight Price Fetcher ===\n")

    # User inputs
    origin_input = input("Enter origin airport code (e.g. JFK, LAX, ORD): ").strip().upper()
    destination_input = input("Enter destination airport code (e.g. LHR, CDG, DXB): ").strip().upper()

    print(f"\nLooking up airports...")
    origin_sky, origin_entity = get_airport_entity(origin_input)
    destination_sky, destination_entity = get_airport_entity(destination_input)

    if not origin_sky or not destination_sky:
        print("Could not find one or both airports. Please check the codes and try again.")
        exit()

    print(f"\nFetching prices for next 7, 14 and 30 days...")
    for days in DAYS_OUT:
        try:
            data, flight_date = fetch_flights(
                origin_sky, destination_sky,
                origin_entity, destination_entity,
                days
            )
            itineraries = data.get("data", {}).get("itineraries", [])
            flights = []
            for item in itineraries:
                legs = item.get("legs", [{}])
                price = item.get("price", {}).get("raw", None)
                airline = legs[0].get("carriers", {}).get("marketing", [{}])[0].get("name", "Unknown")
                duration = legs[0].get("durationInMinutes", 0)
                stops = legs[0].get("stopCount", 0)
                flights.append({
                    "price": price,
                    "airline": airline,
                    "duration": duration,
                    "stops": stops
                })
            save_to_db(flights, origin_input, destination_input, flight_date)
        except Exception as e:
            print(f"Error: {e}")

    print("\nDone! Data saved to database.")
```

**Cmd + S** to save.

---

Now when you run the script it will ask:
```
Enter origin airport code (e.g. JFK, LAX, ORD): JFK
Enter destination airport code (e.g. LHR, CDG, DXB): LHR