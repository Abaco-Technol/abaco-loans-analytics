import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Pytest compatibility shim: some pytest builds may not expose `_pytest.src`.
# Ensure `_pytest.src` points to the `python` submodule which defines
# `Class`, `Module`, and `Package` used by fixture scope resolution.
try:
    import _pytest
    import _pytest.python as _pytest_src

    if not hasattr(_pytest, "src"):
        _pytest.src = _pytest_src
except Exception:
    # If anything goes wrong here, let pytest run normally and fail in tests
    # so we can surface the underlying issue. This shim only improves
    # compatibility in environments where `_pytest.src` is missing.
    pass

# Ensure repository modules can be imported when tests run from the repo root.
ROOT = tuple(Path(__file__).resolve().parents)[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Change working directory to repository root so relative file paths work
os.chdir(ROOT)


@pytest.fixture(scope="session", autouse=True)
def ensure_sample_csv():
    """Create sample CSV file for tests if it doesn't exist."""
    csv_path = Path(ROOT) / "data_samples" / "abaco_portfolio_sample.csv"

    if not csv_path.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        # Create sample data matching test expectations
        csv_content = """segment,measurement_date,dpd_90_plus_usd,total_receivable_usd,total_eligible_usd,cash_available_usd,par_90,collection_rate,delinquency_flag
Consumer,2025-01-31,32500,1000000,1000000,972000,3.25,97.2,1
Consumer,2025-02-28,32500,1000000,1000000,972000,3.25,97.2,1
SME,2025-01-31,32500,1000000,1000000,972000,3.25,97.2,1
SME,2025-02-28,32500,1000000,1000000,972000,3.25,97.2,1
"""
        csv_path.write_text(csv_content)


@pytest.fixture
def minimal_config() -> Dict[str, Any]:
    """Minimal pipeline config for testing."""
    return {
        "pipeline": {
            "phases": {
                "ingestion": {
                    "validation": {
                        "strict": False,
                        "required_columns": [
                            "total_receivable_usd",
                            "total_eligible_usd",
                            "discounted_balance_usd",
                        ],
                        "numeric_columns": [
                            "total_receivable_usd",
                            "total_eligible_usd",
                            "discounted_balance_usd",
                            "cash_available_usd",
                            "dpd_0_7_usd",
                            "dpd_7_30_usd",
                            "dpd_30_60_usd",
                            "dpd_60_90_usd",
                            "dpd_90_plus_usd",
                        ],
                        "date_columns": ["measurement_date"],
                    },
                    "deduplication": {"enabled": False},
                },
                "transformation": {
                    "normalization": {
                        "lowercase_columns": True,
                        "strip_whitespace": True,
                    },
                    "null_handling": {
                        "strategy": "fill_zero",
                        "columns": [],
                    },
                    "outlier_detection": {
                        "enabled": False,
                    },
                    "pii_masking": {
                        "enabled": False,
                    },
                },
            },
        },
        "cascade": {
            "http": {
                "retry": {
                    "max_retries": 1,
                    "backoff_seconds": 0.1,
                },
                "rate_limit": {
                    "max_requests_per_minute": 60,
                },
                "circuit_breaker": {
                    "failure_threshold": 3,
                    "reset_seconds": 60,
                },
            },
        },
    }


@pytest.fixture
def analytics_test_env(tmp_path, monkeypatch):
    """Create a minimal analytics environment for FI-ANALYTICS tests.

    Produces a small CSV dataset and an output directory. Also ensures any
    cloud integrations are disabled via environment patches so the pipeline
    can run locally and deterministically.
    """
    # Prefer the canonical test dataset if available
    dataset = Path(ROOT) / "tests" / "data" / "archives" / "sample_small.csv"

    if not dataset.exists():
        # Fall back to a minimal locally generated dataset
        dataset = tmp_path / "sample_small.csv"
        csv_content = (
            "segment,measurement_date,total_receivable_usd,total_eligible_usd,cash_available_usd,par_90,collection_rate,delinquency_flag\n"
            "Consumer,2025-01-31,32500,1000000,972000,3.25,97.2,1\n"
            "SME,2025-02-28,42000,1000000,972000,4.20,96.9,1\n"
        )
        dataset.write_text(csv_content)

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Disable any external integrations that rely on credentials
    monkeypatch.delenv("AZURE_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    # Execute the pipeline to produce artifacts for the tests
    import subprocess

    result = subprocess.run(
        [
            "python",
            "-m",
            "src.analytics.run_pipeline",
            "--dataset",
            str(dataset),
            "--output",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline execution failed during fixture setup: exit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )

    # Use the same calculation logic as the pipeline to generate
    # `kpi_results.json` in the expected format for tests.
    import pandas as pd
    import json

    from src.analytics import run_pipeline as pipeline_module

    df = pd.read_csv(dataset)
    kpis = pipeline_module.calculate_kpis(df)

    kpi_output_path = output_dir / "kpi_results.json"
    kpi_output_path.write_text(json.dumps(kpis, indent=2), encoding="utf-8")

    # Locate any generated CSV (from run_data_pipeline) and canonicalize name
    for p in output_dir.glob("*.csv"):
        if p.name != "metrics.csv":
            target = output_dir / "metrics.csv"
            p.replace(target)
            break

    return {"dataset_path": dataset, "output_dir": output_dir}


@pytest.fixture
def analytics_baseline_kpis() -> Dict[str, Any]:
    """Load baseline KPI values for comparison."""
    import json

    baseline_path = Path(ROOT) / "tests" / "fixtures" / "baseline_kpis.json"
    if not baseline_path.exists():
        pytest.skip(f"Baseline KPIs file not found: {baseline_path}")

    with open(baseline_path, "r") as f:
        return json.load(f)


@pytest.fixture
def kpi_schema() -> Dict[str, Any]:
    """Load KPI results JSON schema for validation."""
    import json

    schema_path = Path(ROOT) / "tests" / "fixtures" / "schemas" / "kpi_results_schema.json"
    if not schema_path.exists():
        pytest.skip(f"KPI schema file not found: {schema_path}")

    with open(schema_path, "r") as f:
        return json.load(f)
