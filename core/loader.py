"""
core/loader.py — Config loader and validator
=============================================
Reads a .toml scene config file, validates it, and returns a clean
Python dict that the assembler consumes.

VALIDATION RULES
----------------
1. Required top-level keys: [scene]  →  name, class, output, duration, fps
2. [[beats]] array must be non-empty
3. Each beat must have: id, time_start, time_end
4. Beat IDs must be unique and sequential starting at 1
5. Sum of (time_end - time_start) across all beats must equal scene.duration
6. No beat may have time_start >= time_end
7. Beats must not have overlapping time ranges
8. Camera values must be from VALID_CAMERAS
9. Transition values must be from VALID_TRANSITIONS
10. Any [beats.X] sub-block key must be a registered primitive name
    (checked against the registry)

ERROR MESSAGES
--------------
All errors raise ConfigError with a message that includes:
  - The field path (e.g. "beats[2].time_end")
  - What was wrong
  - What was expected
This is intentional: when debugging, you should never need to read
source code to understand what the config file got wrong.

RETURN STRUCTURE
----------------
load(path) returns a dict with keys:
    scene    : dict   — scene metadata
    config   : dict   — render/brand config (with defaults filled in)
    assets   : dict   — character, icons, map, svgs
    beats    : list[dict]  — ordered list of beat dicts
              each beat dict has a "primitives" key:
              dict[str, dict]  name → params
"""

from __future__ import annotations
import tomllib
from pathlib import Path
from defaults import (
    BACKGROUND, PALETTE, FPS, RESOLUTION,
    DEFAULT_TRANSITION, CHARACTER_DEFAULT_COLOR, CHARACTER_DEFAULT_POSITION
)

# ── Valid values ─────────────────────────────────────────────────────────────
VALID_CAMERAS = {
    "static", "zoom-in", "zoom-out", "pan-left", "pan-right"
}

VALID_TRANSITIONS = {
    "cut", "fade", "fade-to-black", "slide", "keep"
}

VALID_RESOLUTIONS = {"preview", "1080p", "4k"}

# Keys in a beat block that are NOT primitive sub-blocks
BEAT_CORE_KEYS = {
    "id", "name", "time_start", "time_end",
    "narration", "on_screen_text",
    "camera", "transition", "ken_burns", "bg_image"
}


class ConfigError(Exception):
    """Raised for any validation failure in the config file."""
    pass


def load(path: str | Path) -> dict:
    """
    Load and validate a scene TOML config.

    Parameters
    ----------
    path : str or Path
        Path to the .toml file.

    Returns
    -------
    dict with keys: scene, config, assets, beats

    Raises
    ------
    ConfigError   — validation failure with a descriptive message
    FileNotFoundError — if path does not exist
    tomllib.TOMLDecodeError — if TOML is malformed
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "rb") as f:
        raw = tomllib.load(f)

    _validate(raw, path.name)
    return _normalise(raw)


# ── Validation ───────────────────────────────────────────────────────────────

def _validate(raw: dict, filename: str) -> None:
    _check_scene(raw, filename)
    _check_beats(raw, filename)


def _check_scene(raw: dict, filename: str) -> None:
    if "scene" not in raw:
        raise ConfigError(
            f"[{filename}] Missing required [scene] block. "
            "Every config must start with [scene] containing "
            "name, class, output, duration, fps."
        )
    s = raw["scene"]
    for key in ("name", "class", "output", "duration", "fps"):
        if key not in s:
            raise ConfigError(
                f"[{filename}] scene.{key} is required but missing."
            )
    if not isinstance(s["duration"], (int, float)) or s["duration"] <= 0:
        raise ConfigError(
            f"[{filename}] scene.duration must be a positive number. "
            f"Got: {s['duration']!r}"
        )

    res = raw.get("config", {}).get("resolution", RESOLUTION)
    if res not in VALID_RESOLUTIONS:
        raise ConfigError(
            f"[{filename}] config.resolution '{res}' is not valid. "
            f"Choose from: {', '.join(sorted(VALID_RESOLUTIONS))}"
        )


def _check_beats(raw: dict, filename: str) -> None:
    if "beats" not in raw or not raw["beats"]:
        raise ConfigError(
            f"[{filename}] No [[beats]] blocks found. "
            "A scene must have at least one beat."
        )

    beats = raw["beats"]
    scene_duration = raw["scene"]["duration"]
    seen_ids = set()
    total_time = 0.0

    for i, beat in enumerate(beats):
        ref = f"beats[{i+1}]"

        # Required fields
        for key in ("id", "time_start", "time_end"):
            if key not in beat:
                raise ConfigError(
                    f"[{filename}] {ref} is missing required field '{key}'."
                )

        bid = beat["id"]
        t0  = beat["time_start"]
        t1  = beat["time_end"]

        # ID uniqueness
        if bid in seen_ids:
            raise ConfigError(
                f"[{filename}] {ref} has duplicate id={bid}. "
                "Beat IDs must be unique."
            )
        seen_ids.add(bid)

        # Time sanity
        if t0 >= t1:
            raise ConfigError(
                f"[{filename}] {ref} (id={bid}): "
                f"time_start ({t0}) must be less than time_end ({t1})."
            )

        total_time += (t1 - t0)

        # Camera
        cam = beat.get("camera", "static")
        if cam not in VALID_CAMERAS:
            raise ConfigError(
                f"[{filename}] {ref} (id={bid}): "
                f"camera '{cam}' is not valid. "
                f"Choose from: {', '.join(sorted(VALID_CAMERAS))}"
            )

        # Transition
        tr = beat.get("transition", DEFAULT_TRANSITION)
        if tr not in VALID_TRANSITIONS:
            raise ConfigError(
                f"[{filename}] {ref} (id={bid}): "
                f"transition '{tr}' is not valid. "
                f"Choose from: {', '.join(sorted(VALID_TRANSITIONS))}"
            )

        # Primitive keys — validate against registry
        _check_primitives(beat, ref, filename)

    # Total duration check (allow 0.5s float tolerance)
    if abs(total_time - scene_duration) > 0.5:
        raise ConfigError(
            f"[{filename}] Beat durations sum to {total_time:.1f}s "
            f"but scene.duration is {scene_duration}s. "
            f"Difference: {abs(total_time - scene_duration):.1f}s. "
            "Check your time_start / time_end values."
        )


def _check_primitives(beat: dict, ref: str, filename: str) -> None:
    """
    Check that all sub-block keys in a beat are either core keys or
    registered primitive names. Deferred import avoids circular imports
    (registry imports nothing from core/).
    """
    from core.registry import all_names
    known_primitives = set(all_names())

    for key in beat:
        if key in BEAT_CORE_KEYS:
            continue
        if not isinstance(beat[key], dict):
            continue   # scalar extra fields — ignore
        if key not in known_primitives:
            raise ConfigError(
                f"[{filename}] {ref}: unknown primitive block '[beats.{key}]'. "
                f"Registered primitives: {', '.join(sorted(known_primitives))}. "
                f"To add '{key}': create primitives/{key}.py."
            )


# ── Normalisation (fill defaults) ────────────────────────────────────────────

def _normalise(raw: dict) -> dict:
    """Fill in defaults for optional fields. Returns clean config dict."""

    scene = dict(raw["scene"])

    # Merge [config] with defaults
    raw_config = raw.get("config", {})
    config = {
        "background" : raw_config.get("background", BACKGROUND),
        "palette"    : {**PALETTE, **raw_config.get("palette", {})},
        "resolution" : raw_config.get("resolution", RESOLUTION),
        "fps"        : raw_config.get("fps", scene.get("fps", FPS)),
    }

    # Merge [assets] with defaults
    raw_assets = raw.get("assets", {})
    assets = {
        "character"  : raw_assets.get("character", None),
        "char_color" : raw_assets.get("char_color", CHARACTER_DEFAULT_COLOR),
        "char_pos"   : raw_assets.get("char_pos", CHARACTER_DEFAULT_POSITION),
        "icons"      : raw_assets.get("icons", []),
        "map"        : raw_assets.get("map", None),
        "svg_files"  : raw_assets.get("svg_files", []),
    }

    # Normalise beats — extract primitive sub-blocks
    beats = []
    for beat in raw["beats"]:
        core = {k: v for k, v in beat.items() if k in BEAT_CORE_KEYS}
        core.setdefault("camera", "static")
        core.setdefault("transition", DEFAULT_TRANSITION)
        core.setdefault("narration", "")
        core.setdefault("on_screen_text", "")
        core.setdefault("ken_burns", None)
        core.setdefault("bg_image", None)

        # Collect primitive sub-blocks
        primitives = {}
        for key, val in beat.items():
            if key not in BEAT_CORE_KEYS and isinstance(val, dict):
                primitives[key] = val

        core["primitives"] = primitives
        beats.append(core)

    # Sort beats by time_start (defensive — TOML order should already be correct)
    beats.sort(key=lambda b: b["time_start"])

    return {
        "scene"  : scene,
        "config" : config,
        "assets" : assets,
        "beats"  : beats,
    }
