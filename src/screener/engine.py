import sqlite3
import pandas as pd
import yaml
from pathlib import Path

class ScreenerEngine:

    def __init__(
        self,
        db_path=None,
        config_path=None,
        config=None
    ):
        

        

        project_root = Path(__file__).resolve().parents[2]

        self.db_path = db_path or str(project_root / "db" / "nifty100.db")
        self.config_path = config_path or str(project_root / "config" / "screener_config.yaml")

        
        if config is None:
            self.config = self.load_config()
        else:
            self.config = config

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


        

        # -----------------------
        # Keep latest year per company
        # -----------------------

        df["year_num"] = (
            df["year"]
            .str.extract(r"(\d{4})")
            .astype(int)
        )

        df = (
            df.sort_values("year_num")
            .groupby("company_id", as_index=False)
            .tail(1)
            .drop(columns='year_num')
        )


        
        # -----------------------
        # ROE
        # -----------------------
        df = self.apply_min_filter(
            df,
            "roe_min",
            "return_on_equity_pct"
        )

        # -----------------------
        # Debt to Equity
        # Skip Financials
        # -----------------------
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

        # -----------------------
        # Free Cash Flow
        # -----------------------
        df = self.apply_min_filter(
            df,
            "fcf_min",
            "free_cash_flow_cr"
        )

        
        # -----------------------
        # Revenue CAGR 5-Year
        # -----------------------
        df = self.apply_min_filter(
            df,
            "revenue_cagr_5yr_min",
            "revenue_cagr_5yr"
        )




        print(df[[

            "company_id",
            "year",
            "revenue_cagr_3yr"
        ]].head(20))
        # -----------------------
        # Revenue CAGR 3-Year
        # -----------------------

        df = self.apply_min_filter(
            df,
            "revenue_cagr_3yr_min",
            "revenue_cagr_3yr"
        )

        print("After Revenue CAGR 3-Year:", len(df))

        # -----------------------
        # PAT CAGR 5-Year
        # -----------------------
        df = self.apply_min_filter(
            df,
            "pat_cagr_5yr_min",
            "pat_cagr_5yr"
        )

        

    



        # -----------------------
        # Operating Profit Margin
        # -----------------------
        df = self.apply_min_filter(
            df,
            "opm_min",
            "operating_profit_margin_pct"
        )

        # -----------------------
        # Interest Coverage
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
        # Asset Turnover
        # -----------------------
        df = self.apply_min_filter(
            df,
            "asset_turnover_min",
            "asset_turnover"
        )

        # -----------------------
        # EPS CAGR 5-Year
        # -----------------------
        df = self.apply_min_filter(
            df,
            "eps_cagr_5yr_min",
            "eps_cagr_5yr"
        )

        # -----------------------
        # Net Profit
        # -----------------------
        df = self.apply_min_filter(
            df,
            "net_profit_min",
            "net_profit"
        )

        # -----------------------
        # Sales
        # -----------------------
        df = self.apply_min_filter(
            df,
            "sales_min",
            "sales"
        )

        
        # ----------------------
        # P/E Ratio
        # -----------------------
        df = self.apply_max_filter(
            df,
            "pe_max",
            "pe_ratio"
        )

        
        print(df[
            [
                "company_id",
                "pe_ratio",
                "pb_ratio",
                "dividend_yield_pct"
            ]
        ].sort_values("pe_ratio"))


        # -----------------------
        # P/B Ratio
        # -----------------------
        df = self.apply_max_filter(
            df,
            "pb_max",
            "pb_ratio"
        )

        

        

        # -----------------------
        # Dividend Yield
        # -----------------------
        df = self.apply_min_filter(
            df,
            "dividend_yield_min",
            "dividend_yield_pct"
        )

        

        df = self.apply_max_filter(
            df,
            "dividend_payout_max",
            "dividend_payout"
        )

        
        

        # -----------------------
        # Dividend Payout
        # -----------------------

        df = self.apply_max_filter(
            df,
            "dividend_payout_max",
            "dividend_payout"
        )

        # -----------------------
        # Market Capitalization
        # -----------------------
        df = self.apply_min_filter(
            df,
            "market_cap_min",
            "market_cap_crore"
        )

       


        # -----------------------
        # Remove duplicate company-year records
        # -----------------------

        df = df.drop_duplicates(
            subset=["company_id", "year"]
        )      

        # -----------------------
        # Sort by Composite Quality Score
        # ----------------------
        df = df.sort_values(
            by="composite_quality_score",
            ascending=False
        ).reset_index(drop=True)

        return df

# -----------------------------------
# Main
# -----------------------------------

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