# 📈 Nifty100 Data Foundation

A production-style ETL and Data Quality framework for the Nifty100 dataset. The project ingests core and supplementary datasets, validates data quality, loads normalized data into SQLite, generates analytical reports, creates SQL views, and includes comprehensive automated tests.

---

## 🚀 Features

- ETL pipeline for Nifty100 data
- Data normalization and validation
- SQLite database with 10 tables
- Load audit and validation summaries
- Analytical reports
- SQL views
- Exploratory SQL queries
- 35+ automated unit tests
- Supplementary datasets support

---

## 📂 Project Structure

```text
nifty100-data-foundation
│
├── data
│   ├── core
│   └── supplementry
│
├── db
│   ├── schema.sql
│   └── nifty100.db
│
├── output
│   ├── load_audit.csv
│   ├── validation_failures.csv
│   ├── top_sales.csv
│   ├── top_roe.csv
│   ├── top_cashflow.csv
│   ├── top_dividend.csv
│   ├── sector_distribution.csv
│   └── kpi_summary.csv
│
├── notebooks
│   └── exploratory_queries.sql
│
├── src
│   └── etl
│       ├── loader.py
│       ├── normaliser.py
│       ├── validator.py
│       └── load_to_sqlite.py
│
├── tests
│   ├── test_integrity.py
│   ├── test_loader_columns.py
│   ├── test_normaliser.py
│   ├── test_reports.py
│   ├── test_schema.py
│   ├── test_sqlite.py
│   └── test_views.py
│
└── README.md
```

---

## 🗄 Database Tables

1. companies
2. profitandloss
3. balancesheet
4. cashflow
5. analysis
6. documents
7. prosandcons
8. sectors
9. marketcap
10. stockprices

---

## ⚙️ ETL Components

### loader.py

Loads Excel files into Pandas DataFrames.

### normaliser.py

Performs:

- String trimming
- Uppercase company IDs
- Null handling
- Standardization

### validator.py

Performs:

- Duplicate checks
- Foreign key checks
- Balance sheet equation checks
- OPM consistency checks
- Tax rate validations
- Dividend payout validations
- URL validations
- Year coverage checks

### load_to_sqlite.py

Loads all datasets into SQLite.

---

## 📊 Generated Reports

Located inside:

```text
output/
```

- load_audit.csv
- validation_failures.csv
- top_sales.csv
- top_roe.csv
- top_cashflow.csv
- top_dividend.csv
- sector_distribution.csv
- kpi_summary.csv

---

## 📈 SQL Views

- vw_top_sales
- vw_top_roe
- vw_sector_distribution

Create views:

```bash
python create_views.py
```

---

## 📒 Exploratory Queries

File:

```text
notebooks/exploratory_queries.sql
```

Contains:

- Top sales
- Top ROE
- Top cash flow
- Top dividend
- Highest net profit
- Highest EPS
- Average ROE
- Highest sales growth
- Highest OPM
- Sector distribution

---

## 🧪 Automated Tests

Run all tests:

```bash
pytest tests -v
```

Individual tests:

```bash
pytest tests/test_integrity.py -v 
✅ 6 tests

pytest tests/test_loader_columns.py -v
✅ 8 tests

pytest tests/test_normaliser.py -v
✅ 5 tests

pytest tests/test_reports.py -v
✅ 6 tests

pytest tests/test_schema.py -v
✅ 6 tests (including marketcap and stockprices)

pytest tests/test_sqlite.py -v
✅ 7 tests (including marketcap and stockprices

pytest tests/test_views.py -v
✅ 3 tests

```



## ▶ Running the Project

Create database:

```bash
python test_sqlite.py
```

Create views:

```bash
python create_views.py
```

Generate reports:

```bash
python test_export_reports.py
```

Generate KPI summary:

```bash
python test_kpi_summary.py
```

Generate load audit:

```bash
python load_audit.py
```

Run tests:

```bash
pytest tests -v
```

---

## ✅ Deliverables

- ETL Pipeline
- Data Normalization
- Data Validation
- SQLite Database
- 10 Database Tables
- Analytical Reports
- Validation Summary
- SQL Views
- Exploratory Queries
- Load Audit
- 41 Automated Tests

---

## 🛠 Tech Stack

- Python 3.11
- Pandas
- SQLite3
- OpenPyXL
- Pytest

---

## 👨‍💻 Author

**Shivam Tanwar**

GitHub: https://github.com/Shivam2523

---

# ✅ Project Status

**Completed Successfully 🚀**


# Nifty 100 Analytics Dashboard


A Streamlit-based analytics dashboard for the Nifty 100 companies.

The project provides:

- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports
- Valuation Module

The backend uses SQLite and Pandas, while Plotly is used for interactive visualizations.

## Features

- Interactive Streamlit Dashboard
- 92 Nifty Companies
- Financial Ratio Analysis
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Map
- Annual Report Viewer
- Company Screener
- Valuation Module

src/
│
├── analytics/
│   └── valuation.py
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   └── utils/
│
db/
│
output/
│
README.md


## Run Dashboard

```bash
streamlit run src/dashboard/app.py
```


## Generate Valuation Report

```bash
python src/analytics/valuation.py
```

## Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- OpenPyXL


## Dataset

- 92 Nifty Companies
- Financial Ratios
- Balance Sheet
- Cash Flow
- Market Capitalization
- Sector Information
- Annual Reports






## Take Screenshots

docs/
└── screenshots/
    ├── home.png
    ├── profile.png
    ├── screener.png
    ├── peers.png
    ├── trends.png
    ├── sectors.png
    ├── capital.png
    └── reports.png

# Dashboard Screens

### 1. Home Dashboard

Displays:

- KPI Summary
- Sector Distribution
- Top Companies
- Overall Market Overview

![Home](docs/screenshots/Home/Home1.png)
![Home](docs/screenshots/Home/Home2.png)
![Home](docs/screenshots/Home/Home3.png)

### 2. Company Profile

Displays:

- Company Information
- KPIs
- Revenue & Profit Charts
- ROE / ROCE Trends
- Pros & Cons

![Profile](docs/screenshots/Profile/Profile1.png)
![Profile](docs/screenshots/Profile/Profile2.png)
![Profile](docs/screenshots/Profile/Profile3.png)
![Profile](docs/screenshots/Profile/Profile4.png)
![Profile](docs/screenshots/Profile/Profile5.png)
![Profile](docs/screenshots/Profile/Profile6.png)
![Profile](docs/screenshots/Profile/Profile7.png)
![Profile](docs/screenshots/Profile/Profile8.png)



### 3. Screener

Allows filtering companies using:

- ROE
- Debt/Equity
- Revenue CAGR
- PAT CAGR
- P/E
- Dividend Yield
- CSV Export

![Screener](docs/screenshots/Screener/Screener1.png)
![Screener](docs/screenshots/Screener/Screener2.png)
![Screener](docs/screenshots/Screener/Screener3.png)


### 4. Peer Comparison

Shows:

- Radar Chart
- Peer KPI Comparison
- Industry Benchmark

![Peers](docs/screenshots/Peers/Peers1.png)
![Peers](docs/screenshots/Peers/Peers2.png)
![Peers](docs/screenshots/Peers/Peers3.png)
![Peers](docs/screenshots/Peers/Peers4.png)
![Peers](docs/screenshots/Peers/Peers5.png)


### 5. Trend Analysis

Displays:

- Multi-metric Line Charts
- Historical Trends
- YoY Analysis

![Trends](docs/screenshots/Trends/1.png)
![Trends](docs/screenshots/Trends/2.png)
![Trends](docs/screenshots/Trends/3.png)
![Trends](docs/screenshots/Trends/4.png)

### 6. Sector Analysis

Displays:

- Bubble Chart
- Sector Median KPIs

![Sectors](docs/screenshots/Sectors/1.png)
![Sectors](docs/screenshots/Sectors/2.png)
![Sectors](docs/screenshots/Sectors/3.png)



### 7. Capital Allocation

Displays:

- Treemap
- Capital Allocation Categories

![Capital](docs/screenshots/Capital/1.png)
![Capital](docs/screenshots/Capital/2.png)


### 8. Annual Reports

Displays:

- Annual Report Links
- PDF Access
- Report Availability

![Reports](docs/screenshots/Reports/1.png)
![Reports](docs/screenshots/Reports/2.png)


# Sprint 4 Retrospective

## Dashboard Features Completed

- Built an 8-page interactive Streamlit dashboard.
- Added Company Profile with financial KPIs and charts.
- Implemented an advanced Stock Screener with CSV export.
- Developed Peer Comparison using Radar Charts.
- Added Trend Analysis with multiple financial metrics.
- Created Sector Analysis using Bubble Charts.
- Built Capital Allocation Treemap visualization.
- Integrated Annual Report viewer with BSE report links.

---

## Valuation Module

Implemented a valuation engine that calculates:

- Free Cash Flow Yield
- Sector Median P/E
- PE vs Sector Median
- Fair / Discount / Caution valuation flags

Generated:

- valuation_summary.xlsx
- valuation_flags.csv

---

## Data Quality Improvements

Resolved several data issues during development:

- Fixed market cap merge using company ID and year.
- Corrected SIEMENS financial year mismatch (September reporting).
- Cleaned sector mapping from 94 companies to 92 companies.
- Removed obsolete companies from the sectors table.
- Improved handling of missing financial values.

---

## Performance

- Streamlit caching implemented using `@st.cache_data`.
- Optimized SQLite queries.
- Dashboard pages load within the required response time.
- Plotly charts render interactively.

---

## Challenges Faced

- Financial year mismatches across companies.
- Market Cap integration.
- Missing financial ratios.
- Annual report availability.
- Data consistency across multiple database tables.

---

## Outcome

Sprint 4 successfully delivers a fully functional Nifty 100 Analytics Dashboard with valuation analytics and interactive visualizations.

