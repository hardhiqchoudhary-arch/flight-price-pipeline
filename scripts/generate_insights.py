import os
import psycopg2
import pickle
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_latest_flights():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "flight_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )
    query = """
        SELECT
            route,
            airline,
            flight_date,
            price_usd,
            avg_route_price,
            price_vs_avg,
            deal_flag,
            stop_type,
            duration_hours,
            days_until_departure,
            duration_minutes,
            stops,
            EXTRACT(DOW FROM flight_date) as day_of_week_num,
            flight_month,
            price_rank
        FROM fct_flights
        ORDER BY ingested_at DESC
        LIMIT 10
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_prediction(df):
    with open('models/price_predictor.pkl', 'rb') as f:
        model = pickle.load(f)
    features = [
        'duration_minutes',
        'stops',
        'day_of_week_num',
        'flight_month',
        'days_until_departure',
        'avg_route_price',
        'price_vs_avg',
        'price_rank'
    ]
    prediction = model.predict(df[features].head(1))[0]
    return "go UP" if prediction == 1 else "go DOWN"

def generate_insight(df, prediction):
    route = df['route'].iloc[0]
    avg_price = df['avg_route_price'].iloc[0]
    current_price = df['price_usd'].iloc[0]
    deal_flag = df['deal_flag'].iloc[0]
    days_out = df['days_until_departure'].iloc[0]
    airline = df['airline'].iloc[0]

    prompt = f"""
    You are a flight price analyst. Based on the data below, give a short,
    clear recommendation to a traveler in 2-3 sentences. Be direct and helpful.

    Route: {route}
    Airline: {airline}
    Current Price: ${current_price}
    30-day Average Price: ${avg_price:.2f}
    Price Assessment: {deal_flag}
    Days Until Departure: {days_out}
    ML Model Prediction: Prices expected to {prediction} in next 3 days

    Give a recommendation: should the traveler book now or wait?
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful flight price analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("=== FlightLens: AI Insight Generator ===\n")
    df = load_latest_flights()
    prediction = get_prediction(df)
    insight = generate_insight(df, prediction)
    print(f"Route: {df['route'].iloc[0]}")
    print(f"Current Price: ${df['price_usd'].iloc[0]}")
    print(f"ML Prediction: Prices will {prediction}")
    print(f"\nAI Insight:\n{insight}")
