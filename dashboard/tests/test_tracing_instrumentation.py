import sys
import types
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from dashboard import tracing_setup


def test_enable_auto_instrumentation_httpx_new(monkeypatch):
    """If the package exposes HTTPXClientInstrumentor, enable_auto_instrumentation should not raise."""
    m = types.ModuleType("opentelemetry.instrumentation.httpx")

    class HTTPXClientInstrumentor:
        def instrument(self):
            return None

    m.HTTPXClientInstrumentor = HTTPXClientInstrumentor
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.httpx", m)

    # Should run without raising
    tracing_setup.enable_auto_instrumentation()


def test_enable_auto_instrumentation_httpx_old(monkeypatch):
    """If the package exposes legacy HttpxInstrumentor, enable_auto_instrumentation should not raise."""
    m = types.ModuleType("opentelemetry.instrumentation.httpx")

    class HttpxInstrumentor:
        def instrument(self):
            return None

    m.HttpxInstrumentor = HttpxInstrumentor
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.httpx", m)

    # Should run without raising
    tracing_setup.enable_auto_instrumentation()


def test_init_tracing_preserves_existing_provider(monkeypatch):
    """If a TracerProvider is already installed, init_tracing should reuse it rather than override.

    The Opentelemetry API can refuse to override the global provider, so instead of trying
    to set a global provider we monkeypatch `trace.get_tracer_provider` to return a
    TracerProvider instance and assert `init_tracing` uses it.
    """
    existing = TracerProvider()

    # Ensure init_tracing observes an existing provider and does not attempt to override
    monkeypatch.setattr(trace, "get_tracer_provider", lambda: existing)

    ret = tracing_setup.init_tracing()
    assert ret is existing
    assert trace.get_tracer_provider() is existing
