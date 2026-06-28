from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


def test_free_cash_flow_positive():
    assert free_cash_flow(500, -200) == 300


def test_free_cash_flow_negative():
    assert free_cash_flow(100, -300) == -200


def test_cfo_quality_high():
    assert cfo_quality_score(200, 100) == (2.0, "High Quality")


def test_cfo_quality_moderate():
    assert cfo_quality_score(80, 100) == (0.8, "Moderate")


def test_cfo_quality_accrual():
    assert cfo_quality_score(20, 100) == (0.2, "Accrual Risk")


def test_cfo_quality_zero_pat():
    assert cfo_quality_score(100, 0) == (None, None)


def test_capex_asset_light():
    assert capex_intensity(-20, 1000) == (2.0, "Asset Light")


def test_capex_moderate():
    assert capex_intensity(-50, 1000) == (5.0, "Moderate")


def test_capex_capital_intensive():
    assert capex_intensity(-120, 1000) == (12.0, "Capital Intensive")


def test_fcf_conversion():
    assert fcf_conversion_rate(300, 600) == 50.0


def test_fcf_conversion_zero():
    assert fcf_conversion_rate(100, 0) is None


def test_reinvestor():
    assert capital_allocation_pattern(500, -200, -100) == (
        "+", "-", "-", "Reinvestor"
    )


def test_shareholder_returns():
    assert capital_allocation_pattern(
        500, -200, -100, "High Quality"
    ) == (
        "+", "-", "-", "Shareholder Returns"
    )


def test_distress_signal():
    assert capital_allocation_pattern(-100, 50, 100) == (
        "-", "+", "+", "Distress Signal"
    )


def test_growth_funded_by_debt():
    assert capital_allocation_pattern(-100, -50, 100) == (
        "-", "-", "+", "Growth Funded by Debt"
    )


def test_cash_accumulator():
    assert capital_allocation_pattern(100, 50, 50) == (
        "+", "+", "+", "Cash Accumulator"
    )


def test_pre_revenue():
    assert capital_allocation_pattern(-100, -50, -10) == (
        "-", "-", "-", "Pre-Revenue"
    )


def test_mixed():
    assert capital_allocation_pattern(100, -50, 50) == (
        "+", "-", "+", "Mixed"
    )