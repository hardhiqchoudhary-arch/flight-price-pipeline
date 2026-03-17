# ✈️ FlightLens: Predictive Airfare Analytics Pipeline

An end-to-end data engineering pipeline that ingests real-time flight prices, transforms and models the data through a multi-layer dbt architecture, predicts fare movements using XGBoost, and delivers plain-English AI recommendations — all orchestrated automatically with Apache Airflow.

---

## 🧠 The Problem

Flight prices change hundreds of times a day. Airlines use sophisticated pricing algorithms. Travelers are left guessing — *"Should I book now or wait?"*

FlightLens answers that question with data.

---

## 🏗️ Architecture
```
Sky Scrapper API (RapidAPI)
        ↓
Python Ingestion Scripts
        ↓
PostgreSQL (Raw Storage)
        ↓
Apache Airflow (Orchestration)
        ↓
dbt (3-Layer Transformation)
  ├── Staging    → clean & standardize
  ├── Intermediate → business logic & enrichment
  └── Marts      → analytics-ready facts table
        ↓
XGBoost (Price Prediction Model)
        ↓
OpenAI API (Plain English Insights)
        ↓
Power BI Dashboard (Visualization)
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data Ingestion | Python, Sky Scrapper API (RapidAPI) |
| Storage | PostgreSQL |
| Orchestration | Apache Airflow |
| Transformation | dbt (staging → intermediate → marts) |
| Machine Learning | XGBoost |
| AI Insights | OpenAI API (GPT-3.5) |
| Visualization | Power BI |
| Version Control | GitHub |

---

## 📁 Project Structure
```
flight-price-pipeline/
│
├── dags/
│   └── flight_pipeline_dag.py    # Airflow DAG — daily pipeline schedule
│
├── scripts/
│   ├── fetch_flights.py          # API ingestion script
│   ├── load_to_db.py             # PostgreSQL loader
│   ├── train_model.py            # XGBoost model training
│   └── generate_insights.py     # OpenAI insight generation
│
├── models/
│   ├── staging/
│   │   ├── stg_flights.sql       # Layer 1: clean raw data
│   │   └── schema.yml            # Data quality tests
│   ├── intermediate/
│   │   └── int_flights_enriched.sql  # Layer 2: business logic
│   └── marts/
│       ├── fct_flights.sql       # Layer 3: Power BI connects here
│       └── schema.yml            # Data quality tests
│
├── data/
│   └── flights_sample.json       # Sample flight data
│
├── dbt_project.yml               # dbt configuration
├── requirements.txt              # Python dependencies
└── .env.example                  # Environment variables template
```

---

## 🤖 AI Insight Example

Instead of just showing numbers, the pipeline generates insights like:

> *"Fares on JFK → LHR are 31% above the 30-day average. The XGBoost model predicts prices will drop over the next 3 days. Recommendation: Wait until Tuesday morning to book."*

---

## 📊 dbt Data Model

| Layer | Model | Purpose |
|---|---|---|
| Staging | `stg_flights` | Clean, standardize, filter raw data |
| Intermediate | `int_flights_enriched` | Add price categories, day of week, price vs average |
| Marts | `fct_flights` | Final table with deal flags for Power BI |

---

## ⚙️ Airflow Pipeline

The DAG runs daily at 8am and executes 4 tasks in order:
```
fetch_flights → load_to_db → run_dbt → test_dbt
```

If any task fails, all downstream tasks stop automatically and retries kick in after 5 minutes.

---

## ✅ Project Status

- [x] Real-time flight data ingestion via Sky Scrapper API
- [x] PostgreSQL database schema for historical price tracking
- [x] dbt 3-layer transformation pipeline
- [x] Automated dbt schema tests for data quality
- [x] Apache Airflow DAG for daily orchestration
- [x] XGBoost price prediction model (up/down in 3 days)
- [x] OpenAI API plain-English insight generation
- [ ] Power BI dashboard (in progress)

---

## 🚀 Getting Started
```bash
# Clone the repo
git clone https://github.com/hardhiqchoudhary-arch/flight-price-pipeline.git
cd flight-price-pipeline

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env

# Run ingestion
python scripts/fetch_flights.py

# Run dbt models
dbt run

# Train model
python scripts/train_model.py

# Generate insights
python scripts/generate_insights.py
```

---

## 👤 Author

**Hardhiq Choudhary**
MS Computer Science — George Washington University
4+ years Data Engineering experience

[LinkedIn](https://www.linkedin.com/in/hardhiq-choudhary) · [GitHub](https://github.com/hardhiqchoudhary-arch)