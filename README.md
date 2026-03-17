# ✈️ Flight Price Intelligence Pipeline

An end-to-end data engineering pipeline that ingests real-time flight prices, models historical trends, predicts fare movements using ML, and delivers plain-English recommendations through an AI layer — all visualized in a live Power BI dashboard.

---

## 🧠 The Problem

Flight prices change hundreds of times a day. Airlines use sophisticated pricing algorithms. Travelers are left guessing — *"Should I buy now or wait?"*

This pipeline answers that question with data.

---

## 🏗️ Architecture

```
Sky Scrapper API
      ↓
 Python (Ingestion)
      ↓
 PostgreSQL (Raw Storage)
      ↓
 Apache Airflow (Orchestration)
      ↓
 dbt (Data Modeling & Transformation)
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
|-------|------|
| Data Ingestion | Python, Sky Scrapper API (RapidAPI) |
| Storage | PostgreSQL |
| Orchestration | Apache Airflow |
| Transformation | dbt |
| Machine Learning | XGBoost |
| AI Insights | OpenAI API |
| Visualization | Power BI |
| Version Control | GitHub |

---

## ✅ Current Progress

- [x] Real-time flight data ingestion via Sky Scrapper API
- [x] PostgreSQL database schema designed for historical price tracking
- [x] End-to-end data load verified (JFK → LHR and more routes)
- [x] Project version-controlled on GitHub
- [ ] Apache Airflow DAGs — automated pipeline scheduling
- [ ] dbt models — raw data cleaned and transformed
- [ ] XGBoost model — price prediction (up or down in 3 days)
- [ ] OpenAI API integration — plain English fare insights
- [ ] Power BI dashboard — live, business-ready reporting

---

## 🤖 What the AI Layer Will Do

Instead of just showing a number, the system will generate insights like:

> *"Fares on JFK → LHR are 31% above the 30-day average. Prices on this route historically drop mid-week. Recommendation: Wait until Tuesday morning."*

---

## 📁 Project Structure

```
flight_pipeline/
│
├── dags/               # Airflow DAGs for pipeline orchestration
├── scripts/            # Python ingestion and utility scripts
├── models/             # dbt models for data transformation
├── data/               # Sample data and schemas
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL
- Apache Airflow
- dbt
- RapidAPI account (Sky Scrapper API)

### Setup

```bash
# Clone the repo
git clone https://github.com/hardhiqchoudhary-arch/flight-price-pipeline.git
cd flight-price-pipeline

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys and DB credentials to .env

# Run ingestion script
python scripts/fetch_flights.py
```

---

## 📊 Sample Data

The pipeline currently tracks routes including:
- JFK → LHR (New York to London)
- More routes being added

Each record captures: route, airline, departure time, price, currency, and ingestion timestamp.

---

## 👤 Author

**Hardhiq Choudhary**
MS Computer Science — George Washington University
4+ years Data Engineering experience

https://www.linkedin.com/in/hardhiq-choudhary/
https://hardhiqchoudhary-arch.github.io/

---

## 📌 Status

🔨 **Active Development** — updates pushed regularly as each layer is completed.
