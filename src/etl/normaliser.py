import pandas as pd


def normalize_year(year):
    """
    Convert year to integer.
    """
    if pd.isna(year):
        return None

    return int(year)


def normalize_ticker(ticker):
    """
    Convert ticker to uppercase and remove spaces.
    """
    if pd.isna(ticker):
        return None

    return str(ticker).strip().upper()


def normalize_sector(sector):
    """
    Standardize sector names.
    """
    if pd.isna(sector):
        return None

    return str(sector).strip().title()


def clean_nulls(df):
    """
    Replace blank strings with None.
    """
    return df.replace(r'^\s*$', None, regex=True)