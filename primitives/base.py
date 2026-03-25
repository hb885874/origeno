"""
primitives/base.py — BasePrimitive base class
==============================================
Every primitive in Origeno inherits from this class.

CONTRACT
--------
Subclasses MUST implement:
    render() -> str
        Returns a string of Python/Manim code.
        The code will be inserted inside construct(), already indented
        to 8 spaces by the assembler. Do NOT add 8 spaces of your own
        — write the code as if it starts at column 0 and the assembler
        will handle indentation.

Subclasses SHOULD define:
    PARAMS : dict
        Metadata about every configurable parameter.
        Used for documentation, validation hints, and future tooling.

        Format:
        PARAMS = {
            "param_name": {
                "type"    : "str" | "float" | "int" | "bool" | "list",
                "default" : <default value>,
                "range"   : (min, max) | None,    # for numeric types
                "options" : [list of valid strings] | None,
                "hint"    : "one-line description of visual effect",
                "tweak"   : "what changing this value does visually",
            },
        }

HELPERS AVAILABLE TO ALL PRIMITIVES
------------------------------------
self.cfg         — the primitive's own config dict (from TOML)
self.scene_cfg   — the full scene config dict (palette, assets, etc.)
self.beat        — the beat dict this primitive belongs to
self.palette     — colour palette dict (e.g. self.palette["RED"])
self.color(name) — resolve a colour name to hex string

self.get(key, default=None)
    Safe getter for self.cfg with fallback to PARAMS default.
    Always use this instead of self.cfg.get() so PARAMS defaults
    are respected even when the user omits a field.
"""

from __future__ import annotations
from defaults import PALETTE


class BasePrimitive:
    """
    Abstract base for all Origeno animation primitives.

    Parameters passed by assembler
    --------------------------------
    cfg       : dict  — the [beats.primitivename] sub-block from TOML
    scene_cfg : dict  — full config dict from loader.load()
    beat      : dict  — the parent beat dict
    """

    # Subclasses define this to document their parameters
    PARAMS: dict = {}

    def __init__(self, cfg: dict, scene_cfg: dict, beat: dict) -> None:
        self.cfg       = cfg
        self.scene_cfg = scene_cfg
        self.beat      = beat
        self.palette   = scene_cfg.get("config", {}).get("palette", PALETTE)

    def render(self) -> str:
        """
        Return Manim Python code as a string.
        Code is inserted inside construct() by the assembler.
        Write at column 0; assembler handles indentation.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement render()"
        )

    def get(self, key: str, default=None):
        """
        Get a config value, falling back to PARAMS default, then
        the supplied default.
        """
        if key in self.cfg:
            return self.cfg[key]
        if key in self.PARAMS and "default" in self.PARAMS[key]:
            return self.PARAMS[key]["default"]
        return default

    def color(self, name: str | None) -> str:
        """
        Resolve a colour name (e.g. "RED", "BLUE") to a hex string.
        Accepts hex strings directly (pass-through).
        Falls back to C_WHITE if name is None or unrecognised.
        """
        if name is None:
            return self.palette.get("WHITE", "#EEEBE3")
        if name.startswith("#"):
            return name
        return self.palette.get(name.upper(), self.palette.get("WHITE", "#EEEBE3"))

    def beat_id(self) -> int:
        return self.beat.get("id", 0)

    def var(self, suffix: str) -> str:
        """
        Generate a unique variable name scoped to this beat.
        Avoids name collisions between beats in the same construct().

        e.g. self.var("stamp") → "_b1_stamp"
        """
        return f"_b{self.beat_id()}_{suffix}"
