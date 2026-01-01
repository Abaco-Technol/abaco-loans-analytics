"""
Unified output integrations for Figma, Azure, Supabase, Meta, Notion, and other platforms.

This module provides a factory pattern for creating and managing output handlers
for scheduled batch exports (daily/hourly) and real-time KPI/analytics syncs.
"""

from python.integrations.figma_client import FigmaClient
from python.integrations.azure_outputs import AzureStorageClient, AzureDashboardClient
from python.integrations.supabase_client import SupabaseOutputClient
from python.integrations.meta_client import MetaOutputClient
from python.integrations.notion_client import NotionOutputClient

__all__ = [
    "FigmaClient",
    "AzureStorageClient",
    "AzureDashboardClient",
    "SupabaseOutputClient",
    "MetaOutputClient",
    "NotionOutputClient",
]
