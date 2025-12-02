"""Utility exports for Streamlit features with lazy loading."""

from importlib import import_module
from typing import TYPE_CHECKING, Any, Callable, Dict, List

__all__ = ["FeatureEngineer"]

if TYPE_CHECKING:  # pragma: no cover - used for type checkers only
    from .feature_engineering import FeatureEngineer  # noqa: F401


_LAZY_LOADERS: Dict[str, Callable[[], Any]] = {
    "FeatureEngineer": lambda: getattr(
        import_module(".feature_engineering", __name__), "FeatureEngineer"
    ),
}


def __getattr__(name: str) -> Any:
    """Lazily import heavy dependencies when requested."""
    try:
        loader = _LAZY_LOADERS[name]
    except KeyError as err:
        raise AttributeError(f"module 'streamlit_app.utils' has no attribute {name!r}") from err

    value = loader()
    globals()[name] = value
    return value


def __dir__() -> List[str]:
    """Expose lazy attributes through introspection utilities."""
    return sorted(set(__all__) | set(globals().keys()))
