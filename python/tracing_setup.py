"""
Tracing setup for Python using Azure Monitor OpenTelemetry.

This module configures distributed tracing for the Abaco Analytics platform,
integrating with Azure Application Insights for observability.

Usage:
    from python.tracing_setup import configure_tracing, get_tracer

    # At application startup
    configure_tracing()

    # In your modules
    tracer = get_tracer(__name__)
    with tracer.start_as_current_span("operation-name"):
        # ... your code here ...
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Global flag to prevent multiple initializations
_tracing_configured = False


def configure_tracing(service_name: Optional[str] = None) -> bool:
    """
    Configure OpenTelemetry tracing with Azure Monitor.

    Args:
        service_name: Optional service name for telemetry. 
                     Defaults to AZURE_APPINSIGHTS_SERVICE_NAME env var or 'abaco-loans-analytics'

    Returns:
        bool: True if tracing was configured successfully, False otherwise
    """
    global _tracing_configured

    if _tracing_configured:
        logger.debug("Tracing already configured, skipping")
        return True

    # Check for Application Insights connection string
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    
    if not connection_string:
        logger.warning(
            "APPLICATIONINSIGHTS_CONNECTION_STRING not set. Tracing disabled. "
            "Set this environment variable to enable Azure Monitor tracing."
        )
        return False

    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from opentelemetry import trace

        # Determine service name
        if service_name is None:
            service_name = os.getenv("AZURE_APPINSIGHTS_SERVICE_NAME", "abaco-loans-analytics")

        # Configure Azure Monitor with the connection string
        configure_azure_monitor(
            connection_string=connection_string,
            # Enable auto-instrumentation for common libraries
            enable_live_metrics=True,
            # Set resource attributes
            resource_attributes={
                "service.name": service_name,
                "service.namespace": "abaco",
                "deployment.environment": os.getenv("PIPELINE_ENV", os.getenv("PYTHON_ENV", "development")),
            }
        )

        _tracing_configured = True
        logger.info("Azure Monitor tracing configured successfully for service: %s", service_name)
        return True

    except ImportError as e:
        logger.warning(
            "Azure Monitor OpenTelemetry packages not installed. Install with: "
            "pip install azure-monitor-opentelemetry. Error: %s", e
        )
        return False
    except Exception as e:
        logger.error("Failed to configure Azure Monitor tracing: %s", e)
        return False


def get_tracer(name: str):
    """
    Get a tracer instance for creating spans.

    Args:
        name: Name of the tracer, typically __name__ of the calling module

    Returns:
        Tracer instance for creating spans, or None if tracing is not available
    """
    try:
        from opentelemetry import trace
        return trace.get_tracer(name)
    except ImportError:
        logger.warning("OpenTelemetry not available. Tracing disabled.")
        return None


# Convenience function for backward compatibility
def traced_function_example():
    """Example of using tracing in a function."""
    tracer = get_tracer(__name__)
    with tracer.start_as_current_span("example-operation"):
        logger.info("This operation is being traced")
        # Your code here
        pass
