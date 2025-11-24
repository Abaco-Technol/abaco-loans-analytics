import pandas as pd

from streamlit_app.utils.ingestion import DataIngestionEngine


def test_normalize_dataframe_converts_numeric_strings():
    engine = DataIngestionEngine("https://example.com", "anon", {})
    df = pd.DataFrame(
        {
            "customer": ["A", "B"],
            "balance": ["100", "250.50"],
            "limit": ["1000", "2000"],
            "dpd": ["0", "3"],
            "facility_amount": ["5000", "7500"],
        }
    )

    normalized, _ = engine.normalize_dataframe(df, source_name="financial")

    expected = {
        "balance": [100.0, 250.50],
        "limit": [1000.0, 2000.0],
        "dpd": [0.0, 3.0],
        "facility_amount": [5000.0, 7500.0],
    }

    for col, expected_values in expected.items():
        assert pd.api.types.is_numeric_dtype(normalized[col]), f"{col} should be numeric"
        assert list(normalized[col]) == expected_values
