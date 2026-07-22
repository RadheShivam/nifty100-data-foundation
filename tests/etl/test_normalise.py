import pytest
import pandas as pd
import numpy as np

from src.etl.normaliser import normalize_year


# ==========================
# Valid integer years
# ==========================

def test_integer_year():
    assert normalize_year(2024) == 2024


def test_integer_float():
    assert normalize_year(2024.0) == 2024


def test_string_year():
    assert normalize_year("2024") == 2024


def test_old_year():
    assert normalize_year(1999) == 1999


def test_zero_year():
    assert normalize_year(0) == 0


# ==========================
# Missing values
# ==========================

def test_none():
    assert normalize_year(None) is None


def test_nan():
    assert normalize_year(float("nan")) is None


def test_pd_na():
    assert normalize_year(pd.NA) is None


def test_numpy_nan():
    assert normalize_year(np.nan) is None


# ==========================
# Negative values
# ==========================

def test_negative_year():
    assert normalize_year(-2024) == -2024


# ==========================
# Float values
# ==========================

def test_float_decimal():
    assert normalize_year(2024.9) == 2024


def test_small_float():
    assert normalize_year(1.2) == 1


# ==========================
# String values
# ==========================

def test_spaces():
    assert normalize_year(" 2024 ") == 2024


def test_leading_zero():
    assert normalize_year("02024") == 2024


# ==========================
# Invalid values
# ==========================

def test_invalid_string():
    with pytest.raises(ValueError):
        normalize_year("ABC")


def test_empty_string():
    with pytest.raises(ValueError):
        normalize_year("")


def test_special_characters():
    with pytest.raises(ValueError):
        normalize_year("@@@@")


def test_boolean_true():
    assert normalize_year(True) == 1


def test_boolean_false():
    assert normalize_year(False) == 0


def test_large_year():
    assert normalize_year(999999) == 999999