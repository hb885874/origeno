#!/usr/bin/env python3
"""
origeno.py — Origeno Animation Generator  (CLI entry point)
=============================================================
Converts a scene TOML config file into a self-contained Manim .py script.

USAGE
-----
    python origeno.py scene1.toml
    python origeno.py scene1.toml --output outputs/scene1.py
    python origeno.py scene1.toml --validate-only
    python origeno.py --list-primitives

WORKFLOW
--------
1. You write a scene TOML config (manually, or AI-assisted from template)
2. Run: python origeno.py scene1.toml
3. A scene1.py is written to the output location
4. Render: manim -pqh scene1.py Scene1
5. Check the animation
6. Tweak values in scene1.toml, re-run origeno.py, re-render

EXIT CODES
----------
0  — success
1  — config validation error (bad TOML values)
2  — file not found
3  — unknown/unexpected error
"""

import sys
import argparse
from pathlib import Path

# ── CRITICAL: ensure the origeno/ directory is on sys.path ──────────────────
# This must happen before ANY local imports (core, primitives, defaults).
# Without this, running `python origeno.py` from the origeno/ folder on
# Windows (and some Linux setups) fails because '' is not always in sys.path.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="origeno",
        description="Origeno Animation Generator — TOML config → Manim scene.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python origeno.py scene1.toml
  python origeno.py scene1.toml --output outputs/scene1.py
  python origeno.py scene1.toml --validate-only
  python origeno.py --list-primitives
        """
    )
    parser.add_argument(
        "config",
        nargs="?",
        help="Path to the scene .toml config file."
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output path for the generated .py file. "
             "Defaults to the 'output' field in [scene]."
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the config without generating any file."
    )
    parser.add_argument(
        "--list-primitives",
        action="store_true",
        help="List all registered primitives and their parameters."
    )

    args = parser.parse_args()

    # ── Import here so registry is populated before --list-primitives ────────
    import primitives  # noqa: F401 — triggers all @register() decorators
    from core.registry import all_names, get as get_primitive

    # ── --list-primitives ────────────────────────────────────────────────────
    if args.list_primitives:
        names = all_names()
        print(f"\nOrigeno registered primitives ({len(names)}):\n")
        for name in names:
            cls = get_primitive(name)
            print(f"  [{name}]")
            if cls.PARAMS:
                for pname, meta in cls.PARAMS.items():
                    hint  = meta.get("hint", "")
                    tweak = meta.get("tweak", "")
                    defv  = meta.get("default", "")
                    print(f"    {pname:<16} default={defv!r:<12}  # {hint}")
                    if tweak:
                        print(f"    {'':16}              # tweak: {tweak}")
            print()
        return 0

    # ── Require config file for all other operations ──────────────────────────
    if not args.config:
        parser.print_help()
        return 1

    # ── Load + validate ───────────────────────────────────────────────────────
    from core.loader import load, ConfigError

    try:
        config = load(args.config)
    except FileNotFoundError as e:
        print(f"\n❌  {e}", file=sys.stderr)
        return 2
    except ConfigError as e:
        print(f"\n❌  Config error:\n    {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌  Unexpected error loading config:\n    {e}", file=sys.stderr)
        return 3

    scene = config["scene"]
    print(f"\n✓  Config valid: {args.config}")
    print(f"   Scene   : {scene['name']}")
    print(f"   Class   : {scene['class']}")
    print(f"   Duration: {scene['duration']}s")
    print(f"   Beats   : {len(config['beats'])}")

    if args.validate_only:
        print("\n   Validation only — no file generated.")
        return 0

    # ── Assemble ──────────────────────────────────────────────────────────────
    from core.assembler import assemble

    output_path = Path(args.output) if args.output else Path(scene["output"])

    try:
        written = assemble(config, output_path)
    except Exception as e:
        print(f"\n❌  Assembly error:\n    {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 3

    print(f"\n✓  Generated: {written}")

    # Render command hints
    res = config["config"]["resolution"]
    flag_map = {"preview": "-pql", "1080p": "-pqh", "4k": "-pqk"}
    flag = flag_map.get(res, "-pqh")
    print(f"\n▶  Render commands:")
    print(f"   manim {flag} {written} {scene['class']}         # {res}")
    print(f"   manim -pql {written} {scene['class']}           # preview (fast)")
    if res != "4k":
        print(f"   manim -pqk {written} {scene['class']}           # 4K")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())