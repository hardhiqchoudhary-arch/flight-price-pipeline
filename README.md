# FlightLens: Predictive Airfare Analytics Pipeline

An end-to-end data engineering pipeline that ingests real-time flight prices, transforms and models the data through a multilayer dbt architecture, predicts fare movements using XGBoost, and delivers plainEnglish AI recommendations all orchestrated automatically with Apache Airflow.

## The Problem

Flight prices change hundreds of times a day. Airlines use sophisticated pricing algorithms. Travelers are left guessing , "Should I book now or wait?"

FlightLens answers that question with data.

## Overview

FlightLens is a production style data engineering project built around a real-world problem. It pulls live JFK to LHR flight prices from the Sky Scrapper API, stores them in PostgreSQL, transforms them through a 3-layer dbt pipeline, trains an XGBoost model to predict price direction, and uses the OpenAI API to generate plain-English booking recommendations all scheduled and orchestrated via Apache Airflow.

## Features

### Data Ingestion
- **Real-time Flight Data**: Pulls live prices via Sky Scrapper API (RapidAPI)
- **Historical Tracking**: Stores all ingested data in PostgreSQL for trend analysis
- **Automated Scheduling**: Apache Airflow DAG runs the full pipeline daily at 8am

### Data Transformation
- **3-Layer dbt Architecture**: Staging, Intermediate, and Marts layers
- **Data Quality Tests**: Automated schema tests at each dbt layer
- **Analytics-ready Output**: Final facts table optimized for Power BI consumption

### Machine Learning
- **XGBoost Price Prediction**: Predicts whether fares will go up or down in the next 3 days
- **Feature Engineering**: Day of week, price vs 30-day average, deal flags
- **Model Persistence**: Trained model saved and reloaded for daily inference

### AI Insights
- **Plain-English Recommendations**: OpenAI API converts model output into actionable advice
- **Example Output**: "Fares on JFK to LHR are 31% above the 30-day average. The model predicts prices will drop over the next 3 days. Recommendation: Wait until Tuesday morning to book."

## Tech Stack

- **Data Ingestion**: Python, Sky Scrapper API (RapidAPI)
- **Storage**: PostgreSQL
- **Orchestration**: Apache Airflow
- **Transformation**: dbt (Staging, Intermediate, Marts layers)
- **Machine Learning**: XGBoost
- **AI Insights**: OpenAI API (GPT-3.5)
- **Visualization**: Power BI
- **Version Control**: GitHub

## Getting Started

### Prerequisites
- Python 3.9 or later
- PostgreSQL
- Apache Airflow 2.0 or later
- dbt-core with dbt-postgres adapter
- RapidAPI account (Sky Scrapper API)
- OpenAI API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/hardhiqchoudhary-arch/flight-price-pipeline.git
cd flight-price-pipeline
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Add your API keys and database credentials to .env
```

4. Run the ingestion script
```bash
python scripts/fetch_flights.py
```

5. Run dbt transformations
```bash
dbt run
dbt test
```

6. Train the model
```bash
python scripts/train_model.py
```

7. Generate AI insights
```bash
python scripts/generate_insights.py
```

## Project Status

- [x] Real-time flight data ingestion via Sky Scrapper API
- [x] PostgreSQL database schema for historical price tracking
- [x] dbt 3-layer transformation pipeline
- [x] Automated dbt schema tests for data quality
- [x] Apache Airflow DAG for daily orchestration
- [x] XGBoost price prediction model
- [x] OpenAI API plain-English insight generation
- [ ] Power BI dashboard (in progress)

## Acknowledgments

- Sky Scrapper API via RapidAPI for flight price data
- OpenAI for natural language insight generation
- dbt Labs for the transformation framework
- Apache Airflow community for orchestration tooling

Note: This project is being developed as a portfolio project alongside MS Computer Science studies at George Washington University (January 2026 - Present).

- LinkedIn: [Hardhiq Choudhary](https://www.linkedin.com/in/hardhiq-choudhary)
- Email: hardhiq.choudhary@gwmail.gwu.edu
