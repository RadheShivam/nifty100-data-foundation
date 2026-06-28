from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    net_debt,
    asset_turnover,
)


def test_debt_to_equity_normal():
    assert debt_to_equity(200, 100, 300) == 0.5


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 300) == 0


def test_high_leverage_flag_true():
    assert high_leverage_flag(6.2, "IT") is True


def test_high_leverage_flag_financials():
    assert high_leverage_flag(6.2, "Financials") is False


def test_interest_coverage_ratio_normal():
    assert interest_coverage_ratio(200, 50, 25) == (
        10.0,
        None,
        False,
    )


def test_interest_coverage_ratio_debt_free():
    assert interest_coverage_ratio(100, 20, 0) == (
        None,
        "Debt Free",
        False,
    )


def test_interest_coverage_ratio_warning():
    assert interest_coverage_ratio(10, 5, 20) == (
        0.75,
        None,
        True,
    )


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0