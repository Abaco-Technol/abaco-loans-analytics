import pandas as pd
from pandas.api import types as ptypes

from streamlit_ingestion import coerce_numeric_columns


REQUIRED_NUMERIC_COLUMNS = {
    "loan_amount",
    "appraised_value",
    "borrower_income",
    "monthly_debt",
    "interest_rate",
    "principal_balance",
}


def test_required_numeric_columns_coerced_when_blank():
    df = pd.DataFrame({"loan_amount": ["", " "]})

    coerced = coerce_numeric_columns(df, REQUIRED_NUMERIC_COLUMNS)

    assert ptypes.is_numeric_dtype(coerced["loan_amount"])
    assert coerced["loan_amount"].isna().all()


def test_optional_object_columns_only_coerced_when_numeric_values_present():
    df = pd.DataFrame({"notes": ["abc", ""], "other_metric": ["10", ""]})

    coerced = coerce_numeric_columns(df, REQUIRED_NUMERIC_COLUMNS)

    assert coerced["notes"].dtype == object
    assert ptypes.is_numeric_dtype(coerced["other_metric"])
