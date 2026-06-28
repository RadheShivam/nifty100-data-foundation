from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)


# ----------------------------
# Generic CAGR Tests
# ----------------------------

def test_cagr_normal():
    value, flag = calculate_cagr(100, 200, 5)
    assert round(value, 2) == 14.87
    assert flag is None


def test_cagr_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 5)
    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_cagr_turnaround():
    value, flag = calculate_cagr(-100, 50, 5)
    assert value is None
    assert flag == "TURNAROUND"


def test_cagr_both_negative():
    value, flag = calculate_cagr(-100, -50, 5)
    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_cagr_zero_base():
    value, flag = calculate_cagr(0, 100, 5)
    assert value is None
    assert flag == "ZERO_BASE"


def test_cagr_insufficient():
    value, flag = calculate_cagr(100, 200, 0)
    assert value is None
    assert flag == "INSUFFICIENT"


# ----------------------------
# Wrapper Tests
# ----------------------------

def test_revenue_cagr():
    value, flag = revenue_cagr(100, 200, 5)
    assert round(value, 2) == 14.87
    assert flag is None


def test_pat_cagr():
    value, flag = pat_cagr(50, 100, 5)
    assert round(value, 2) == 14.87
    assert flag is None


def test_eps_cagr():
    value, flag = eps_cagr(10, 20, 5)
    assert round(value, 2) == 14.87
    assert flag is None


# ----------------------------
# Extra Edge Case
# ----------------------------

def test_cagr_one_year():
    value, flag = calculate_cagr(100, 120, 1)
    assert round(value, 2) == 20.00
    assert flag is None