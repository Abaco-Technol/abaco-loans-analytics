"""Utility package for feature engineering and helpers used by the Streamlit app."""

from importlib import import_module
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Mapping, Tuple

if TYPE_CHECKING:  # pragma: no cover
    from .feature_engineering import FeatureEngineer  # noqa: F401


def _load_feature_engineer() -> Any:
    module = import_module(".feature_engineering", __name__)
    return module.FeatureEngineer


_ATTR_LOADERS: Mapping[str, Callable[[], Any]] = MappingProxyType(
    {
        "FeatureEngineer": _load_feature_engineer,
    }
)

_EXPORTED_UTILS: Tuple[str, ...] = tuple(_ATTR_LOADERS)

__all__: Iterable[str] = ("available_utils", *_EXPORTED_UTILS)


def available_utils() -> Tuple[str, ...]:
    return _EXPORTED_UTILS


def __getattr__(name: str) -> Any:
    loader = _ATTR_LOADERS.get(name)
    if loader is None:
        raise AttributeError(f"module 'streamlit_app.utils' has no attribute {name!r}")

    value = loader()
    globals()[name] = value
    return value


def __dir__() -> List[str]:
    return sorted(set(__all__) | set(globals().keys()))
