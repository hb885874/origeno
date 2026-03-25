"""
core/registry.py — Primitive registry
=======================================
The registry is the scalability mechanism of Origeno.

HOW IT WORKS
------------
Every primitive class in primitives/ decorates itself with @register("name").
That decorator stores the class in _REGISTRY under that key.

When the assembler sees [beats.stamp] in a config it calls:
    cls = get("stamp")        →  Stamp class
    obj = cls(beat_config)
    code = obj.render()       →  Python code string

ADDING A NEW PRIMITIVE
----------------------
1. Create primitives/myprimitive.py
2. Inherit from BasePrimitive
3. Decorate the class with @register("myprimitive")
4. Import it in primitives/__init__.py

That's it. Nothing else changes. Existing configs are unaffected because
the tool only instantiates primitives that are declared in the config.

REGISTRY STRUCTURE
------------------
_REGISTRY : dict[str, type[BasePrimitive]]
    key   = the TOML block name  e.g. "stamp", "counter", "chart"
    value = the class itself (not an instance)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from primitives.base import BasePrimitive

_REGISTRY: dict[str, type] = {}


def register(name: str):
    """
    Class decorator. Usage:

        @register("stamp")
        class Stamp(BasePrimitive): ...
    """
    def decorator(cls):
        if name in _REGISTRY:
            raise ValueError(
                f"[Registry] Duplicate primitive name '{name}'. "
                f"Already registered by {_REGISTRY[name].__module__}."
            )
        _REGISTRY[name] = cls
        return cls
    return decorator


def get(name: str) -> type:
    """
    Look up a primitive class by its TOML block name.
    Raises KeyError with a helpful message if not found.
    """
    if name not in _REGISTRY:
        known = ", ".join(sorted(_REGISTRY.keys()))
        raise KeyError(
            f"[Registry] Unknown primitive '{name}'. "
            f"Known primitives: {known}\n"
            f"To add '{name}': create primitives/{name}.py, "
            f"inherit BasePrimitive, decorate with @register('{name}'), "
            f"import in primitives/__init__.py"
        )
    return _REGISTRY[name]


def all_names() -> list[str]:
    """Return sorted list of all registered primitive names."""
    return sorted(_REGISTRY.keys())
