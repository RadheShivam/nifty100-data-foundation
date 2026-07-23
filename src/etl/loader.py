import pandas as pd
from pathlib import Path

BASE_PATH = Path("data")


def load_companies():
    return pd.read_excel(BASE_PATH / "core" / "companies.xlsx", skiprows=1, header=0)


def load_profitandloss():
    df = pd.read_excel(BASE_PATH / "core" / "profitandloss.xlsx", skiprows=1)

    # Recalculate OPM Percentage
    df["opm_percentage"] = (df["operating_profit"] / df["sales"] * 100).round(2)

    return df


def load_balancesheet():
    return pd.read_excel(BASE_PATH / "core" / "balancesheet.xlsx", skiprows=1)


def load_cashflow():
    return pd.read_excel(BASE_PATH / "core" / "cashflow.xlsx", skiprows=1)


def load_analysis():
    return pd.read_excel(BASE_PATH / "core" / "analysis.xlsx", skiprows=1)


def load_documents():
    return pd.read_excel(BASE_PATH / "core" / "documents.xlsx", skiprows=1)


def load_prosandcons():
    return pd.read_excel(BASE_PATH / "core" / "prosandcons.xlsx", skiprows=1)


def load_market_cap():
    return pd.read_excel(BASE_PATH / "supplementry" / "market_cap.xlsx", skiprows=1)


def load_peer_groups():
    return pd.read_excel(BASE_PATH / "supplementry" / "peer_groups.xlsx")


def load_sectors():
    return pd.read_excel(BASE_PATH / "supplementry" / "sectors.xlsx")


def load_stock_prices():
    return pd.read_excel(BASE_PATH / "supplementry" / "stock_prices.xlsx", skiprows=1)
