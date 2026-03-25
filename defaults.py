"""
defaults.py — Origeno brand defaults
=====================================
Single source of truth for all brand constants, palette values, and
tool-level defaults. Any value here can be overridden by a scene's
[config] block in the TOML. Never import Manim here — this is pure data.

If the brand changes (new palette, new BG colour), change it here only.
"""

# ── Background & palette ────────────────────────────────────────────────────
BACKGROUND   = "#F5F0E8"   # warm paper

PALETTE = {
    "RED"  : "#D42B2B",
    "BLUE" : "#2255AA",
    "GOLD" : "#C8960C",
    "GREEN": "#2A7A2A",
    "WHITE": "#EEEBE3",
    "DARK" : "#1C1A14",
    "DIM"  : "#888070",
    "GRID" : "#C8C0A8",
    "CYAN" : "#00BFFF",
}

# ── Render / timing ─────────────────────────────────────────────────────────
FPS         = 30
RESOLUTION  = "1080p"   # choices: "preview" | "1080p" | "4k"

RESOLUTION_FLAGS = {
    "preview": "-pql",
    "1080p"  : "-pqh",
    "4k"     : "-pqk",
}

# ── Font ────────────────────────────────────────────────────────────────────
FONT = "Georgia"

# ── Camera / safe frame ─────────────────────────────────────────────────────
# Manim default frame: x ∈ [−7.1, +7.1], y ∈ [−4.0, +4.0]
FRAME_W = 14.2
FRAME_H = 8.0

# ── Character ───────────────────────────────────────────────────────────────
CHARACTER_DEFAULT_COLOR    = "BLUE"
CHARACTER_DEFAULT_POSITION = "right"

# ── Transition defaults ──────────────────────────────────────────────────────
# Used when a beat does not specify transition
DEFAULT_TRANSITION = "fade"
