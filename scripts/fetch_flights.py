import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "sky-scrapper.p.rapidapi.com"

headers = {
    "x-rapidapi-host": RAPIDAPI_HOST,
    "x-rapidapi-key": RAPIDAPI_KEY
}

def fetch_flights(origin_sky_id, destination_sky_id, origin_entity_id, destination_entity_id):
    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"
    
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    print(f"Searching flights: {origin_sky_id} → {destination_sky_id} on {future_date}")
    
    querystring = {
        "originSkyId": origin_sky_id,
        "destinationSkyId": destination_sky_id,
        "originEntityId": origin_entity_id,
        "destinationEntityId": destination_entity_id,
        "date": future_date,
        "cabinClass": "economy",
        "adults": "1",
        "currency": "USD",
        "market": "en-US",
        "countryCode": "US"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(json.dumps(data, indent=2))

# New York → London
fetch_flights("JFK", "LHR", "95565058", "95565050")