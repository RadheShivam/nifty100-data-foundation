# CAGR function

import math


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR.

    CAGR = ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
        (cagr, flag)

    Possible flags:
        None
        DECLINE_TO_LOSS
        TURNAROUND
        BOTH_NEGATIVE
        ZERO_BASE
        INSUFFICIENT
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = (
        (end_value / start_value) ** (1 / years) - 1
    ) * 100

    return cagr, None


# Wrapper Functions


def revenue_cagr(start_sales, end_sales, years):
    """
    Revenue CAGR
    """
    return calculate_cagr(start_sales, end_sales, years)


def pat_cagr(start_profit, end_profit, years):
    """
    Profit After Tax CAGR
    """
    return calculate_cagr(start_profit, end_profit, years)


def eps_cagr(start_eps, end_eps, years):
    """
    Earnings Per Share CAGR
    """
    return calculate_cagr(start_eps, end_eps, years)