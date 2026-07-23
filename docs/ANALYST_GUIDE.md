# Nifty100 Financial Intelligence Platform

## Analyst Guide

### Project Overview

The Nifty100 Financial Intelligence Platform is a data analytics application that provides financial insights for Nifty100 companies.

The platform consists of:

- ETL Pipeline
- SQLite Database
- FastAPI REST API
- Streamlit Dashboard
- KPI Analytics
- Financial Ratio Calculations

---

## Project Structure

```
src/
│
├── api/
├── dashboard/
├── analytics/
├── etl/
└── utils/

db/
docs/
tests/
output/
```

---

## Running the Project

### 1. Start FastAPI

```bash
uvicorn src.api.main:app --reload
```

Runs on:

```
http://127.0.0.1:8000
```

---

### 2. Start Streamlit

```bash
streamlit run src/dashboard/app.py
```

Runs on:

```
http://localhost:8501
```

---

## Dashboard Pages

- Home
- Company Profile
- Screener
- Peers
- Trends
- Sectors
- Capital Allocation
- Reports

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

Health Endpoint

```
/api/v1/health
```

---

## Testing

Run all tests:

```bash
pytest
```

Generate HTML report:

```bash
pytest --html=reports/pytest_report.html
```

---

## Performance

- Dashboard loads within target performance.
- API supports concurrent requests.
- SQLite indexes added for optimized queries.

---

## Technologies Used

- Python
- SQLite
- FastAPI
- Streamlit
- Pandas
- NumPy
- Plotly
- Pytest