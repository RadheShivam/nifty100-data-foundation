import pandas as pd


def display_value(value, decimals=2, suffix=""):
    """
    Display numbers safely.
    Returns 'N/A' for None or NaN.
    """

    if pd.isna(value):
        return "N/A"

    return f"{value:.{decimals}f}{suffix}"
