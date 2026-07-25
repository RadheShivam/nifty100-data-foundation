
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    net_debt,
    asset_turnover,
)

from src.analytics.cagr import (
    calculate_cagr,
)

# =====================================================
# Net Profit Margin
# =====================================================


def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None


# =====================================================
# Operating Profit Margin
# =====================================================


def test_operating_profit_margin():
    opm, match = operating_profit_margin(300, 1000)

    assert opm == 30
    assert match is None


def test_operating_profit_margin_match():
    opm, match = operating_profit_margin(300, 1000, 30)

    assert match is True


# =====================================================
# Return on Equity
# =====================================================


def test_return_on_equity():
    assert return_on_equity(200, 500, 500) == 20


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -500, 100) is None


# =====================================================
# Return on Capital Employed
# =====================================================


def test_roce():
    roce, benchmark = return_on_capital_employed(300, 500, 500, 500)

    assert roce == 20
    assert benchmark == "absolute"


# =====================================================
# Debt to Equity
# =====================================================


def test_debt_to_equity():
    assert debt_to_equity(500, 500, 500) == 0.5


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 500, 500) == 0


# =====================================================
# High Leverage
# =====================================================


def test_high_leverage():
    assert high_leverage_flag(6, "IT") is True


# =====================================================
# Interest Coverage Ratio
# =====================================================


def test_interest_coverage():
    icr, label, warning = interest_coverage_ratio(500, 100, 100)

    assert icr == 6
    assert warning is False


def test_interest_zero():
    icr, label, warning = interest_coverage_ratio(500, 100, 0)

    assert icr is None
    assert label == "Debt Free"


# =====================================================
# Net Debt
# =====================================================


def test_net_debt():
    assert net_debt(1000, 400) == 600


# =====================================================
# Asset Turnover
# =====================================================


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None


# =====================================================
# CAGR
# =====================================================


def test_calculate_cagr():
    cagr, flag = calculate_cagr(100, 200, 5)

    assert round(cagr, 2) == 14.87
    assert flag is None


def test_calculate_cagr_zero_base():
    cagr, flag = calculate_cagr(0, 200, 5)

    assert cagr is None
    assert flag == "ZERO_BASE"


def test_calculate_cagr_decline_to_loss():
    cagr, flag = calculate_cagr(100, -50, 5)

    assert cagr is None
    assert flag == "DECLINE_TO_LOSS"


def test_calculate_cagr_turnaround():
    cagr, flag = calculate_cagr(-100, 50, 5)

    assert cagr is None
    assert flag == "TURNAROUND"


def test_calculate_cagr_insufficient():
    cagr, flag = calculate_cagr(100, 200, 0)

    assert cagr is None
    assert flag == "INSUFFICIENT"
