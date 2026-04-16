import pandas as pd
import numpy as np
import psycopg2
import pickle
import os
from dotenv import load_dotenv
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

load_dotenv()

def load_data():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "flight_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )
    query = """
        SELECT
            price_usd,
            duration_minutes,
            stops,
            EXTRACT(DOW FROM flight_date) as day_of_week_num,
            flight_month,
            days_until_departure,
            avg_route_price,
            price_vs_avg,
            price_rank
        FROM fct_flights
        ORDER BY flight_date ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"Loaded {len(df)} records from database")
    return df

def build_features(df):
    df['price_shifted'] = df['price_usd'].shift(-3)
    df['target'] = (df['price_shifted'] > df['price_usd']).astype(int)
    df = df.dropna()
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
    X = df[features]
    y = df['target']
    print(f"Target distribution:\n{y.value_counts()}")
    return X, y

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.2%}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    return model

def save_model(model):
    os.makedirs('models', exist_ok=True)
    with open('models/price_predictor.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("\nModel saved to models/price_predictor.pkl")

if __name__ == "__main__":
    print("=== FlightLens: XGBoost Price Predictor ===\n")
    df = load_data()
    X, y = build_features(df)
    model = train_model(X, y)
    save_model(model)
