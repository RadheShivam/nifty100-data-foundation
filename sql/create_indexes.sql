-- =====================================
-- SQLite Performance Indexes
-- =====================================

-- Profit & Loss
CREATE INDEX IF NOT EXISTS idx_profitandloss_company
ON profitandloss(company_id);

CREATE INDEX IF NOT EXISTS idx_profitandloss_year
ON profitandloss(year);

CREATE INDEX IF NOT EXISTS idx_profitandloss_company_year
ON profitandloss(company_id, year);

-- Balance Sheet
CREATE INDEX IF NOT EXISTS idx_balancesheet_company
ON balancesheet(company_id);

CREATE INDEX IF NOT EXISTS idx_balancesheet_year
ON balancesheet(year);

CREATE INDEX IF NOT EXISTS idx_balancesheet_company_year
ON balancesheet(company_id, year);

-- Cash Flow
CREATE INDEX IF NOT EXISTS idx_cashflow_company
ON cashflow(company_id);

CREATE INDEX IF NOT EXISTS idx_cashflow_year
ON cashflow(year);

CREATE INDEX IF NOT EXISTS idx_cashflow_company_year
ON cashflow(company_id, year);

-- Financial Ratios
CREATE INDEX IF NOT EXISTS idx_financial_ratios_company
ON financial_ratios(company_id);

CREATE INDEX IF NOT EXISTS idx_financial_ratios_year
ON financial_ratios(year);

CREATE INDEX IF NOT EXISTS idx_financial_ratios_company_year
ON financial_ratios(company_id, year);

-- Analysis
CREATE INDEX IF NOT EXISTS idx_analysis_company
ON analysis(company_id);

