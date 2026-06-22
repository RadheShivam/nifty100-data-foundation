import pandas as pd

def load_companies():
    file_path = "data/core/companies.xlsx"

    df = pd.read_excel(file_path, skiprows=1)

    return df



def load_companies():
    file_path = "data/core/companies.xlsx"
    df = pd.read_excel(file_path)
    return df


def load_profitandloss():
    file_path = "data/core/profitandloss.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1
    )

    return df


def load_companies():
    file_path = "data/core/companies.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1,
        header=0
    )

    return df


def load_balancesheet():
    file_path = "data/core/balancesheet.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1
    )

    return df


def load_cashflow():
    file_path = "data/core/cashflow.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1
    )

    return df



def load_analysis():
    file_path = "data/core/analysis.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1
    )

    return df


def load_documents():
    file_path = "data/core/documents.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1
    )

    return df



def load_prosandcons():
    file_path = "data/core/prosandcons.xlsx"

    df = pd.read_excel(
        file_path,
        skiprows=1
    )

    return df


def load_market_cap():
    return pd.read_excel(
        "data/supplementry/market_cap.xlsx",
        skiprows=1
    )


def load_peer_groups():
    return pd.read_excel(
        "data/supplementry/peer_groups.xlsx",
        skiprows=1
    )


def load_sectors():
    return pd.read_excel(
        "data/supplementry/sectors.xlsx"
    )


def load_stock_prices():
    return pd.read_excel(
        "data/supplementry/stock_prices.xlsx",
        skiprows=1
    )