import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError


class AzureBlobKPIExporter:
    """Publishes KPI payloads to Azure Blob Storage with traceable metadata."""

    def __init__(
        self,
        *,
        container_name: str,
        account_url: Optional[str] = None,
        connection_string: Optional[str] = None,
        credential: Optional[Any] = None,
        blob_service_client: Optional[BlobServiceClient] = None,
    ):
        if blob_service_client is not None:
            self.blob_service_client = blob_service_client
        else:
            if not connection_string and not account_url:
                raise ValueError("Either connection_string or account_url must be provided.")
            if connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            else:
                self.blob_service_client = BlobServiceClient(
                    account_url=account_url, credential=credential or DefaultAzureCredential()
                )
        self.container_name = container_name

    def upload_metrics(self, metrics: Dict[str, float], blob_name: Optional[str] = None) -> str:
        if not metrics:
            raise ValueError("Metrics payload cannot be empty.")

        container_client = self.blob_service_client.get_container_client(self.container_name)
        try:
            container_client.create_container()
        except ResourceExistsError:
            pass

        timestamp = datetime.now(timezone.utc)
        blob_path = blob_name or f"kpi-dashboard-{timestamp.strftime('%Y%m%dT%H%M%SZ')}.json"
        payload = {
            "generated_at": timestamp.isoformat(),
            "metrics": metrics,
        }

        container_client.upload_blob(
            name=blob_path,
            data=json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            overwrite=True,
            content_settings=ContentSettings(content_type="application/json"),
        )
        return f"{self.container_name}/{blob_path}"
