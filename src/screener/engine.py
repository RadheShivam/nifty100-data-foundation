import sqlite3
import pandas as pd
import yaml


class ScreenerEngine:

    def __init__(
        self,
        db_path="db/nifty100.db",
        config_path="config/screener_config.yaml"
    ):

        self.db_path = db_path
        self.config_path = config_path

        self.config = self.load_config()
        self.df = self.load_financial_ratios()

    # -----------------------------------
    # Load YAML Configuration
    # -----------------------------------

    def load_config(self):

        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    # -----------------------------------
    # Load Financial Data
    # -----------------------------------

    def load_financial_ratios(self):

        conn = sqlite3.connect(self.db_path)

        query = """

        SELECT
            f.*,

            s.broad_sector,

            p.sales,
            p.net_profit,
            p.eps,
            p.dividend_payout,

            m.market_cap_crore,
            m.pe_ratio,
            m.pb_ratio,
            m.dividend_yield_pct

        FROM financial_ratios f

        LEFT JOIN sectors s
            ON f.company_id = s.company_id

        LEFT JOIN profitandloss p
            ON f.company_id = p.company_id
            AND f.year = p.year

        LEFT JOIN market_cap m
            ON f.company_id = m.company_id
            AND CAST(substr(f.year, -4) AS INTEGER) = m.year
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    # -----------------------------------
    # Generic Minimum Filter
    # -----------------------------------

    def apply_min_filter(self, df, config_key, column):

        value = self.config.get(config_key)

        if value is not None:
            df = df[
                df[column] >= value
            ]

        return df

    # -----------------------------------
    # Generic Maximum Filter
    # -----------------------------------

    def apply_max_filter(self, df, config_key, column):

        value = self.config.get(config_key)

        if value is not None:
            df = df[
                df[column] <= value
            ]

        return df

    # -----------------------------------
    # Apply All Filters
    # -----------------------------------

    def apply_filters(self):

        df = self.df.copy()

        # ROE
        df = self.apply_min_filter(
            df,
            "roe_min",
            "return_on_equity_pct"
        )

        # Debt to Equity
        de_max = self.config.get("de_max")

        if de_max is not None:

            financials = df[
                df["broad_sector"] == "Financials"
            ]

            others = df[
                df["broad_sector"] != "Financials"
            ]

            others = others[
                others["debt_to_equity"] <= de_max
            ]

            df = pd.concat(
                [financials, others],
                ignore_index=True
            )

        # Free Cash Flow
        df = self.apply_min_filter(
            df,
            "fcf_min",
            "free_cash_flow_cr"
        )

        # Revenue CAGR 5-Year
        df = self.apply_min_filter(
            df,
            "revenue_cagr_5yr_min",
            "revenue_cagr_5yr"
        )

        # PAT CAGR 5-Year
        df = self.apply_min_filter(
            df,
            "pat_cagr_5yr_min",
            "pat_cagr_5yr"
        )

        # Operating Profit Margin
        df = self.apply_min_filter(
            df,
            "opm_min",
            "operating_profit_margin_pct"
        )

        # -----------------------s
        # Interest Coverage Filter
        # Debt Free = Infinity
        # -----------------------

        icr_min = self.config.get("interest_coverage_min")

        if icr_min is not None:

            df = df[
                (df["interest_coverage"] >= icr_min)
                |
                (df["interest_coverage"].isna())
            ]

        # -----------------------
        # Asset Turnover Filter
        # -----------------------

        df = self.apply_min_filter(
            df,
            "asset_turnover_min",
            "asset_turnover"
        )

        # -----------------------
        # EPS CAGR 5-Year Filter
        # -----------------------

        df = self.apply_min_filter(
            df,
            "eps_cagr_5yr_min",
            "eps_cagr_5yr"
        )

        # -----------------------
        # Net Profit Filter
        # -----------------------

        df = self.apply_min_filter(
            df,
            "net_profit_min",
            "net_profit"
        )

        # -----------------------
        # Sales Filter
        # -----------------------

        df = self.apply_min_filter(
            df,
            "sales_min",
            "sales"
        )

        # -----------------------
        # Sort by Composite Quality Score
        # -----------------------
        df = df.sort_values(
            by="composite_quality_score",
            ascending=False
        ).reset_index(drop=True)


        # P/E Ratio
        df = self.apply_max_filter(
            df,
            "pe_max",
            "pe_ratio"
        )

        # P/B Ratio
        df = self.apply_max_filter(
            df,
            "pb_max",
            "pb_ratio"
        )

        # Dividend Yield
        df = self.apply_min_filter(
            df,
            "dividend_yield_min",
            "dividend_yield_pct"
        )

        # Market Capitalization
        df = self.apply_min_filter(
            df,
            "market_cap_min",
            "market_cap_crore"
        )

        return df


        


# -----------------------------------
# Main
# -----------------------------------

if __name__ == "__main__":

    engine = ScreenerEngine()

    filtered = engine.apply_filters()

    print(filtered.columns.tolist())

    print()

    print(filtered.head())

    print()

    print("Rows:", len(filtered))