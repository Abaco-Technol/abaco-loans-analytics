
# --- Step 1: Set up a clean branch for the fix ---
echo "INFO: Setting up a clean branch..."
# Ensure we are on the main branch and it's up-to-date
git checkout main
git pull
# Create a new, clean branch for this specific fix
git checkout -b fix/gx-api-update

# --- Step 2: Atomically write the corrected file content ---
echo "INFO: Applying fix to data_validation_gx.py..."
cat << 'EOF' > src/pipeline/data_validation_gx.py
# src/pipeline/data_validation_gx.py

import great_expectations as gx
from great_expectations.data_context import EphemeralDataContext
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_or_create_datasource(context: EphemeralDataContext, datasource_name: str):
    """Gets a datasource or creates it if it does not exist using the modern API."""
    try:
        datasource = context.get_datasource(datasource_name)
    except ValueError:
        logger.info(f"Datasource '{datasource_name}' not found, creating it.")
        datasource = context.sources.add_pandas(name=datasource_name)
    return datasource

def create_validator_for_dataframe(
    context: EphemeralDataContext, df: pd.DataFrame, datasource_name: str, asset_name: str
):
    """Creates a Great Expectations validator for a given Pandas DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a Pandas DataFrame.")

    datasource = get_or_create_datasource(context, datasource_name)

    # Modern way to add a dataframe as an asset and build a batch request
    pandas_asset = datasource.add_dataframe_asset(name=asset_name, dataframe=df)
    batch_request = pandas_asset.build_batch_request()

    validator = context.get_validator(
        batch_request=batch_request,
        create_expectation_suite_with_name=f"{asset_name}_suite",
    )
    return validator

def validate_data(df: pd.DataFrame, expectations: dict, datasource_name: str, asset_name: str):
    """
    Validates a DataFrame against a set of Great Expectations.
    """
    context = gx.get_context(project_root_dir=None, mode="ephemeral")
    validator = create_validator_for_dataframe(
        context, df, datasource_name, asset_name
    )

    for expectation in expectations:
        expectation_type = expectation.pop("type")
        try:
            getattr(validator, expectation_type)(**expectation)
        except Exception as e:
            logger.error(f"Failed to apply expectation {expectation_type}: {e}")

    validation_result = validator.validate()
    if not validation_result["success"]:
        logger.warning("Data validation failed!")
        logger.warning(validation_result)
    else:
        logger.info("Data validation successful!")

    return validation_result
