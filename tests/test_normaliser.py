import pandas as pd


def test_company_id_uppercase():
    df = pd.DataFrame({
        "company_id": ["reliance", "tcs", "infy"]
    })

    df["company_id"] = df["company_id"].str.upper()

    assert list(df["company_id"]) == [
        "RELIANCE",
        "TCS",
        "INFY"
    ]


def test_company_id_strip():
    df = pd.DataFrame({
        "company_id": [" RELIANCE ", " TCS ", " INFY "]
    })

    df["company_id"] = df["company_id"].str.strip()

    assert list(df["company_id"]) == [
        "RELIANCE",
        "TCS",
        "INFY"
    ]


def test_string_trim():
    df = pd.DataFrame({
        "company_name": [
            " Reliance Industries ",
            " TCS "
        ]
    })

    df["company_name"] = df["company_name"].str.strip()

    assert df["company_name"][0] == "Reliance Industries"
    assert df["company_name"][1] == "TCS"


def test_no_null_company_id():
    df = pd.DataFrame({
        "company_id": ["RELIANCE", "TCS", "INFY"]
    })

    assert df["company_id"].isnull().sum() == 0


def test_year_column_type():
    df = pd.DataFrame({
        "year": ["Mar 2024", "Mar 2023"]
    })

    assert df["year"].apply(lambda x: isinstance(x, str)).all()