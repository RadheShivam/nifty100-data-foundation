# 📈 Nifty100 Financial Intelligence Platform

## Overview

The **Nifty100 Financial Intelligence Platform** is a production-style financial data analytics application that processes and analyzes financial data of Nifty 100 companies. It provides an end-to-end solution for data ingestion, validation, storage, analysis, visualization, and reporting.

The platform integrates an ETL pipeline, SQLite database, FastAPI backend, and Streamlit dashboard to enable users to explore company financial statements, compare sector performance, screen stocks based on financial metrics, analyze valuation, and generate interactive reports.

The project follows software engineering best practices, including modular architecture, automated testing, documentation, performance optimization, and code quality validation.

---

# 🚀 Features

## ETL Pipeline

- Reads raw financial datasets from Excel files
- Cleans and normalizes financial information
- Validates data integrity before loading
- Generates audit logs and validation summaries

## SQLite Database

- Stores normalized financial data
- Maintains relationships between companies and financial statements
- Uses optimized indexes for faster queries

## Financial Analytics

- Revenue Growth Analysis
- Profit Growth Analysis
- ROE & ROCE Analysis
- Capital Allocation Analysis
- Sector Comparison
- Financial Ratio Analysis
- CAGR Calculations

## FastAPI Backend

- RESTful API endpoints
- Interactive Swagger UI
- JSON responses
- Company and sector data services

## Streamlit Dashboard

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports

## Reporting

- KPI Reports
- Validation Reports
- Load Audit Reports
- Performance Reports
- Integration Reports

## Testing

- Unit Testing
- Integration Testing
- API Testing
- Dashboard Testing
- Data Quality Testing

---

# 🏗 Project Architecture

```text
                  Raw Excel Files
                         │
                         ▼
                  ETL Pipeline
                         │
                         ▼
                  Data Validation
                         │
                         ▼
                  SQLite Database
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
          FastAPI API         Streamlit Dashboard
              │                     │
              └──────────┬──────────┘
                         ▼
          Financial Intelligence Platform
```

---

# 📂 Project Structure

```text
nifty100-data-foundation/
│
├── config/
├── data/
├── db/
├── docs/
│   ├── analyst_guide.pdf
│   ├── acceptance_checklist.pdf
│   ├── openapi.json
│   └── screenshots/
│
├── notebooks/
├── output/
├── reports/
├── scripts/
├── sql/
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   └── etl/
│
├── tests/
├── README.md
├── requirements.txt
├── pytest.ini
└── .gitignore
```

---

# 💻 Technology Stack

- Python 3.11
- SQLite
- FastAPI
- Uvicorn
- Streamlit
- Plotly
- Pandas
- NumPy
- OpenPyXL
- SQLAlchemy
- Scikit-Learn
- Pytest
- Black
- Ruff

---

# ⚙ Installation

```bash
git clone https://github.com/RadheShivam/nifty100-data-foundation.git

cd nifty100-data-foundation

python -m venv venv

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

# 📊 Database Setup

```bash
python create_database.py

python etl_pipeline.py

python verify_companies.py
```

---

# 🚀 Running the FastAPI Server

```bash
uvicorn src.api.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 📈 Running the Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py
```

### Dashboard Pages

- 🏠 Home
- 🏢 Company Profile
- 🔍 Stock Screener
- 📊 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📑 Reports

---

# 🧪 Running Tests

Run all tests:

```bash
pytest
```

Generate HTML report:

```bash
pytest --html=reports/pytest_report.html
```

---

# 📑 Documentation

The project includes the following documentation:

- README.md
- Analyst Guide
- Acceptance Checklist
- OpenAPI Documentation
- API Documentation
- Release Notes
- Code Quality Report
- Integration Test Report
- Performance Notes
- Final Validation Report

---

# 📊 Reports

Generated reports include:

- Load Audit Report
- KPI Summary
- Validation Report
- Financial Ratio Reports
- HTML Test Report
- Performance Report

---

# 📸 Dashboard Screenshots

Store screenshots inside:

```text
docs/screenshots/
```

Suggested screenshots:

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Reports

---

# 📈 Key Achievements

- ✅ Developed a complete ETL pipeline
- ✅ Built a normalized SQLite database
- ✅ Created REST APIs using FastAPI
- ✅ Developed an interactive Streamlit dashboard
- ✅ Implemented financial analytics and KPI calculations
- ✅ Optimized database performance using indexes
- ✅ Added automated testing and validation
- ✅ Produced comprehensive project documentation

---

# 🔮 Future Improvements

- User Authentication
- Portfolio Management
- Watchlist Functionality
- Real-time Stock Data Integration
- PostgreSQL / MySQL Support
- Docker Containerization
- GitHub Actions CI/CD
- Cloud Deployment

---

# 👨‍💻 Author

## Shivam Kumar Mehta

**Bachelor of Technology (Computer Science & Engineering)**  
Lovely Professional University

**Data Analyst**

### Connect with Me

- **GitHub:** https://github.com/RadheShivam
- **LinkedIn:** https://www.linkedin.com/in/shivam-kumar-mehta-77a631251/

---

# 📄 License

This project is licensed under the **MIT License**.

---

⭐ **If you found this project useful, consider giving it a star on GitHub!**