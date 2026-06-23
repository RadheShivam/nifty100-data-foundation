DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS profitandloss;
DROP TABLE IF EXISTS balancesheet;
DROP TABLE IF EXISTS cashflow;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS prosandcons;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS marketcap;
DROP TABLE IF EXISTS stockprices;

CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

CREATE TABLE profitandloss (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL
);

CREATE TABLE balancesheet (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL
);

CREATE TABLE cashflow (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL
);

CREATE TABLE analysis (
    id INTEGER,
    company_id TEXT,
    compounded_sales_growth REAL,
    compounded_profit_growth REAL,
    stock_price_cagr REAL,
    roe REAL
);

CREATE TABLE documents (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    annual_report TEXT
);

CREATE TABLE prosandcons (
    id INTEGER,
    company_id TEXT,
    pros TEXT,
    cons TEXT
);

CREATE TABLE sectors (
    id INTEGER,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT
);

CREATE TABLE marketcap (
    id INTEGER,
    company_id TEXT,
    year TEXT,
    market_cap_crore REAL,
    enterprise_value_crore REAL,
    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL
);

CREATE TABLE stockprices (
    id INTEGER,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL
);