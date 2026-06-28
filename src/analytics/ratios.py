# Net Profit Margin

def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (NPM)

    Formula:
        (Net Profit / Sales) * 100

    Returns:
        float : Net Profit Margin
        None  : If sales is 0 or None
    """

    if sales is None or sales == 0:
        return None

    return (net_profit / sales) * 100


# Operating Profit Margin

def operating_profit_margin(operating_profit, sales, opm_percentage=None):
    """
    Operating Profit Margin (OPM)

    Formula:
        (Operating Profit / Sales) * 100

    If opm_percentage is provided,
    checks whether the calculated OPM matches
    within 1%.

    Returns:
        (calculated_opm, is_match)
    """

    if sales is None or sales == 0:
        return None, None

    calculated_opm = (operating_profit / sales) * 100

    if opm_percentage is None:
        return calculated_opm, None

    is_match = abs(calculated_opm - opm_percentage) <= 1

    return calculated_opm, is_match


# Return on Equity

def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
        (Net Profit / (Equity Capital + Reserves)) * 100

    Returns:
        float : ROE
        None  : If Equity + Reserves <= 0
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


# Return on Capital Employed

def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
    broad_sector=None
):
    """
    Return on Capital Employed (ROCE)

    Formula:
        (EBIT /
        (Equity Capital + Reserves + Borrowings))
        * 100

    Financial companies use
    sector-relative benchmark.

    Returns:
        (roce, benchmark_type)
    """

    capital_employed = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital_employed <= 0:
        return None, None

    roce = (
        ebit / capital_employed
    ) * 100

    if broad_sector == "Financials":
        return roce, "sector-relative"

    return roce, "absolute"


# Return on Assets

def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
        (Net Profit / Total Assets) * 100

    Returns:
        float : ROA
        None  : If Total Assets <= 0
    """

    if total_assets is None or total_assets <= 0:
        return None

    return (net_profit / total_assets) * 100


# Debt-to-Equity Ratio


def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt-to-Equity Ratio

    Formula:
        Borrowings / (Equity Capital + Reserves)

    Returns:
        float : Debt-to-Equity Ratio
        0     : If borrowings = 0
        None  : If equity <= 0
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity


# High Leverage Flag

def high_leverage_flag(debt_to_equity_ratio, broad_sector):
    """
    High Leverage Flag

    Rule:
    - If D/E > 5 and company is NOT in Financials,
      return True.
    - Otherwise return False.
    """

    if debt_to_equity_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_to_equity_ratio > 5

# Interest Coverage Ratio (ICR)

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio (ICR)

    Formula:
        (Operating Profit + Other Income) / Interest

    Returns:
        tuple:
            (
                icr,
                icr_label,
                warning_flag
            )

    icr_label:
        "Debt Free" if interest == 0

    warning_flag:
        True if ICR < 1.5
    """

    if interest == 0:
        return None, "Debt Free", False

    icr = (
        operating_profit + other_income
    ) / interest

    warning_flag = icr < 1.5

    return icr, None, warning_flag


# Net Debt


def net_debt(borrowings, investments):
    """
    Net Debt

    Formula:
        Borrowings - Investments

    Investments are treated as liquid assets.
    Negative net debt is allowed.
    """

    return borrowings - investments


# Asset Turnover

def asset_turnover(sales, total_assets):
    """
    Asset Turnover

    Formula:
        Sales / Total Assets

    Returns:
        float : Asset Turnover
        None  : If total_assets <= 0
    """

    if total_assets is None or total_assets <= 0:
        return None

    return sales / total_assets