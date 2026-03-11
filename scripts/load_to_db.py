import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database="flight_db",
    user="postgres",
    password=os.getenv("DB_PASSWORD")
)
cursor = conn.cursor()

with open("data/flights_sample.json", "r") as f:
    data = json.load(f)

for flight in data["flights"]:
    cursor.execute("""
        INSERT INTO flights (origin, destination, flight_date, price, airline, duration, stops)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        flight["origin"],
        flight["destination"],
        flight["flight_date"],
        flight["price"],
        flight["airline"],
        flight["duration"],
        flight["stops"]
    ))

conn.commit()
print(f"Saved {len(data['flights'])} flights to database!")

cursor.close()
conn.close()
EOF