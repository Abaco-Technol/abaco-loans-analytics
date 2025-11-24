"""Agents focused on cleaning inbound records before analytics pipelines."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


class DataCleaningAgent:
    """Performs non-destructive cleaning of inbound record lists."""

    def clean_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Deep copy to isolate processing from caller-managed data structures
        cleaned_records = deepcopy(records)

        for record in cleaned_records:
            for key, value in list(record.items()):
                if isinstance(value, str):
                    record[key] = value.strip()
                if value is None:
                    record.pop(key)

        return cleaned_records
