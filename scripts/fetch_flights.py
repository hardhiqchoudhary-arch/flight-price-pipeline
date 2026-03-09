import requests
import json
from dotenv import load_dotenv
import os

# Load API keys from .env file
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

def fetch_flights(origin, destination):
    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlightsComplete"
    
    querystring = {
        "originSkyId": origin,
        "destinationSkyId": destination,
        "originEntityId": "27537542",
        "destinationEntityId": "27544008",
        "cabinClass": "economy",
        "adults": "1",
        "currency": "USD",
        "market": "en-US",
        "countryCode": "US"
    }
    
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(json.dumps(data, indent=2))

# Test with New York to London
fetch_flights("NYCA", "LOND")