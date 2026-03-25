# Origeno Animation Generator

## Table of Contents
1. [What This Tool Is](#1-what-this-tool-is)
2. [How It Was Designed — The Full Story](#2-how-it-was-designed--the-full-story)
3. [File Structure](#3-file-structure)
4. [The Workflow](#4-the-workflow)
5. [Config File Reference (TOML Schema)](#5-config-file-reference-toml-schema)
6. [Primitive Reference](#6-primitive-reference)
7. [Running the Tool](#7-running-the-tool)
8. [Rendering with Manim](#8-rendering-with-manim)
9. [Adding a New Primitive](#9-adding-a-new-primitive)
10. [Debugging Guide](#10-debugging-guide)
11. [Architecture Deep-Dive](#11-architecture-deep-dive)
12. [Design Decisions and Why](#12-design-decisions-and-why)
13. [Known Limitations and Future Work](#13-known-limitations-and-future-work)
14. [Glossary](#14-glossary)

---

## 1. What This Tool Is

Origeno is a local command-line tool that converts a structured TOML
config file into a self-contained Manim Python animation script.

It is built for the YouTube channel **Origeno** (hindi/english explainer
videos, "Oversimplified" visual style). The owner writes scene config
files, runs the tool, and renders the output with Manim. No manual
Python writing is needed for standard scenes.

### What it does NOT do
- It does not use any AI/LLM at runtime. It is a deterministic
  code generator.
- It does not render video itself. It produces a `.py` file that
  Manim renders.
- It does not read the scene planning template directly. The template
  is a human-readable planning document; the owner (or AI assistant)
  translates it into a TOML config.

### The one-line description for AI tools
> Origeno reads a TOML scene config, instantiates registered Manim
> primitive classes for each beat, and assembles a self-contained
> `scene.py` that can be rendered with `manim -pqh scene.py ClassName`.

---

## 2. How It Was Designed — The Full Story

Understanding the design history prevents future contributors from
re-opening closed questions.

### The problem
The channel owner writes 8-12 Manim Python scripts per video. Each
script reuses the same animation patterns (stamp, counter, chart, map,
character) but with different content. Writing these by hand is slow
and error-prone. The repetition was the signal to build a generator.

### Why not AI-generated code at runtime?
Three reasons were considered and rejected:
1. **Non-determinism** — the same config should always produce the
   same `.py`. AI output varies.
2. **Offline use** — the tool must work with no internet connection
   (on-set, on a flight, etc.)
3. **Debuggability** — when a render breaks, the `.py` must be fully
   traceable to the config, not to a model's output.

The decision: purely deterministic, rule-based code generation.

### Why TOML, not YAML or JSON?
- TOML `[[beats]]` array syntax maps perfectly to the beat table
  in the scene planning template.
- TOML is not indentation-sensitive (unlike YAML), so copy-paste
  errors don't silently produce wrong structure.
- `[beats.stamp]` sub-blocks are explicit and readable.
- Python 3.11+ includes `tomllib` in stdlib — no extra dependency.

### Why a primitive registry, not if/elif chains?
The primitive library grows organically video by video. If the
assembler had `if primitive == "stamp": ... elif primitive == "counter":`
then every new primitive would require editing the assembler. With
`@register("name")` decorators and a registry lookup, the assembler
never changes — only a new file is added. This is the core scalability
mechanism.

### Why is scene.py machine-generated and never hand-edited?
Because the config file is the source of truth. If scene.py could be
edited, the config and the script would diverge and neither would be
trustworthy. The rule is absolute: **tweak the config, regenerate,
re-render**.

### Why does scene.py inline all brand constants?
So it is fully self-contained. You can copy scene.py to any Manim
project, any machine, any folder and render it with no dependency on
the origeno/ tool being present on PYTHONPATH.

### The scene planning template
The owner writes scenes using a 5-section planning template:

```
Section 1 — Scene header   (name, duration, class, output file)
Section 2 — Beat table     (timing breakdown, narration triggers)
Section 3 — Per-beat detail (narration, visuals, animation primitives)
Section 4 — Assets         (character, icons, map, SVGs)
Section 5 — Global config  (background, palette, resolution, FPS)
```

This template is a **human document only**. It is not parsed by the
tool. The owner (or an AI assistant) translates it into the TOML
config. The reason: the template is optimised for creative planning;
the TOML is optimised for machine consumption. Mixing the two would
make both worse.

---

## 3. File Structure

```
origeno/
│
├── origeno.py              ← CLI entry point. Run this.
├── defaults.py             ← Brand constants and global defaults.
│                             Single source of truth for palette,
│                             background, FPS, resolution.
│
├── core/
│   ├── __init__.py
│   ├── loader.py           ← Reads + validates TOML config.
│   │                         Returns clean dict. Raises ConfigError
│   │                         with descriptive messages on failure.
│   ├── registry.py         ← @register() decorator and get() lookup.
│   │                         The scalability mechanism.
│   └── assembler.py        ← Writes scene.py from config dict.
│                             Calls primitive.render() for each beat.
│
├── primitives/
│   ├── __init__.py         ← Imports all primitive modules so their
│   │                         @register() decorators fire at startup.
│   ├── base.py             ← BasePrimitive. All primitives inherit this.
│   │                         Defines render(), get(), color(), var().
│   ├── stamp.py            ← Text slams in from a direction.
│   ├── counter.py          ← Number counts up/down with ValueTracker.
│   ├── chart.py            ← Bar chart or pie chart from data array.
│   ├── character.py        ← Stick-figure scientist, various actions.
│   ├── map.py              ← World dot-map with highlights and arcs.
│   ├── prop.py             ← Named icon props (chip, globe, phone…).
│   ├── flood.py            ← N copies of an object flood the screen.
│   ├── electricity.py      ← Travelling dot along traces or path.
│   └── glitch.py           ← Rapid scale+colour flash effect.
│
├── scene1.toml             ← Example config (The Hidden Dependency).
│                             Use this as a reference when writing
│                             new configs.
│
└── README.md               ← This file.
```

### What each file is responsible for

| File | Reads | Writes | Raises |
|---|---|---|---|
| `origeno.py` | CLI args | stdout messages | SystemExit |
| `core/loader.py` | `.toml` file | config dict | `ConfigError` |
| `core/registry.py` | — | `_REGISTRY` dict | `KeyError` |
| `core/assembler.py` | config dict | `scene.py` | `Exception` |
| `primitives/*.py` | `cfg` dict | Python code string | `None` |
| `defaults.py` | — | — | — |

---

## 4. The Workflow

```
Scene planning template  (you write this, creative document)
         │
         │  you (or AI) translate manually
         ▼
    scene1.toml           (structured config, machine-readable)
         │
         │  python origeno.py scene1.toml
         ▼
    scene1.py             (auto-generated Manim script, never edit)
         │
         │  manim -pqh scene1.py Scene1
         ▼
    animation clip (.mp4)
         │
         │  review — not happy?
         └──────────────────────► edit scene1.toml → repeat
```

### The tweak loop in practice

1. Render the scene at preview quality first:
   ```
   manim -pql scene1.py Scene1
   ```
2. Find something to fix (timing, colour, size).
3. Open `scene1.toml`, find the relevant parameter, change the value.
   The inline comments tell you what each tweak does:
   ```toml
   run_time = 0.6   # tweak: 0.3=snappy  1.2=slow dramatic
   ```
4. Regenerate:
   ```
   python origeno.py scene1.toml
   ```
5. Re-render and check.
6. When happy, render full quality:
   ```
   manim -pqh scene1.py Scene1
   ```

---

## 5. Config File Reference (TOML Schema)

A config file has four top-level blocks. Only `[scene]` and `[[beats]]`
are required.

### [scene]  ← required

```toml
[scene]
name     = "The Hidden Dependency"   # Human-readable scene name
class    = "Scene1"                  # Manim class name (used in render cmd)
output   = "scene1.py"              # Output filename
duration = 45                        # Total scene duration in seconds
fps      = 30                        # Frames per second
style    = "oversimplified"          # Informational only, not used by tool
```

All fields are required. `class` must be a valid Python identifier.

### [config]  ← optional

```toml
[config]
background = "#F5F0E8"    # Background colour hex. Default: "#F5F0E8"
resolution = "1080p"      # "preview" | "1080p" | "4k". Default: "1080p"

[config.palette]
RED   = "#D42B2B"         # Override any palette colour.
BLUE  = "#2255AA"         # Omitted keys use defaults from defaults.py.
GOLD  = "#C8960C"
GREEN = "#2A7A2A"
```

If `[config]` is omitted entirely, all Origeno brand defaults are used.
You only need this block when overriding something.

### [assets]  ← optional

```toml
[assets]
character  = "scientist"  # Character type. Only "scientist" currently.
char_color = "blue"       # Colour key for the character.
char_pos   = "right"      # Starting position: "left" | "center" | "right"
icons      = ["chip", "globe"]   # Props used in this scene.
map        = "world-dots"        # Map type (or omit if no map).
svg_files  = []                  # Paths to external SVG files.
```

### [[beats]]  ← required, one block per beat

The `[[beats]]` double-bracket syntax means it's an array — repeat
the block for each beat. Beats are processed in the order they appear
in the file (sorted by `time_start` as a safety measure).

```toml
[[beats]]
id             = 1              # Unique integer. Must start at 1.
name           = "Hook"         # Human label for this beat.
time_start     = 0              # Beat start in seconds.
time_end       = 8              # Beat end in seconds.
narration      = "..."          # Voiceover line (written as comment in .py)
on_screen_text = "ZERO CHIPS"   # Text shown on screen (if no stamp primitive)
camera         = "static"       # "static"|"zoom-in"|"zoom-out"|"pan-left"|"pan-right"
transition     = "keep"         # "cut"|"fade"|"fade-to-black"|"slide"|"keep"
ken_burns      = "zoom-in"      # Optional: "zoom-in"|"zoom-out"|"pan-left"|"pan-right"
bg_image       = "bg.png"       # Optional: background image filename
```

**Duration validation**: The tool sums `(time_end - time_start)` across
all beats and checks it equals `scene.duration`. A tolerance of 0.5s
is allowed for float rounding. If the sum is wrong, the tool errors
with the exact discrepancy.

#### Beat primitive sub-blocks

Below each `[[beats]]` block, add `[beats.X]` sub-blocks for each
primitive you want in that beat. Only declare what you need — undeclared
primitives are simply absent.

```toml
[[beats]]
id = 1
...

  [beats.stamp]        ← stamp primitive for beat 1
  text = "ZERO"
  ...

  [beats.prop]         ← prop primitive for beat 1
  name = "chip"
  ...
```

Chart data is a special case — it uses its own array syntax:

```toml
  [beats.chart]
  type = "pie"

    [[beats.chart.data]]   ← first data point
    label = "Taiwan"
    value = 92

    [[beats.chart.data]]   ← second data point
    label = "Others"
    value = 8
```

---

## 6. Primitive Reference

Each primitive maps to a `[beats.X]` sub-block in the config.
All fields have defaults — you only need to specify what you're
changing from the default.

---

### stamp
**What it does**: Bold text slams onto screen from a direction with
a bounce impact. Classic overlay titles: "ZERO CHIPS", "SUBSCRIBE".

```toml
[beats.stamp]
text         = "ZERO CHIPS"
color        = "RED"        # RED | BLUE | GOLD | GREEN | WHITE | hex
from_dir     = "TOP"        # TOP | BOTTOM | LEFT | RIGHT | CENTER
run_time     = 0.6          # tweak: 0.3=snappy  1.2=slow dramatic
bounce_count = 3            # tweak: 0=no bounce  3=medium  6+=comedic
font_size    = 52           # tweak: larger = more emphasis
position     = "center"     # center | top | bottom | left | right
```

---

### counter
**What it does**: Number animates from `start` to `end` using a
ValueTracker. For data reveals: "92%", "$3.2B", "1.4 Billion".

```toml
[beats.counter]
start     = 0
end       = 92
label     = "%"       # appended after number
prefix    = ""        # prepended before number (e.g. "$")
duration  = 2.5       # tweak: slower = more suspense
color     = "RED"
position  = "center"  # center | top | bottom | left | right
font_size = 88        # tweak: bigger = number IS the message
decimals  = 0         # decimal places shown during count
```

---

### chart
**What it does**: Bar chart or pie chart, grows in from zero.

```toml
[beats.chart]
type         = "pie"           # bar | pie
grow_time    = 1.8             # tweak: slower = more suspense per element
position     = "right"         # center | left | right
color_scheme = "highlight_first"  # default | mono | highlight_first

  [[beats.chart.data]]
  label = "Taiwan"
  value = 92

  [[beats.chart.data]]
  label = "Others"
  value = 8
```

**Color schemes**:
- `default` — cycles RED, BLUE, GOLD, GREEN
- `mono` — all bars/slices the same grey
- `highlight_first` — first element RED, rest grey (draws eye to lead value)

---

### character
**What it does**: Origeno scientist stick-figure performs an action.
Built from Manim geometric primitives — no image files needed.

```toml
[beats.character]
action   = "walks-in"   # walks-in | points-at | holds-prop | shocked | wink | static
position = "right"      # left | center | right
color    = "BLUE"       # BLUE=protagonist  RED=antagonist
target   = "map"        # for points-at: descriptive only (no auto-lookup)
run_time = 0.8          # tweak: walk-in speed
```

**Actions**:
- `walks-in` — enters from off-screen edge toward position
- `points-at` — walks in, then extends arm toward target side
- `holds-prop` — walks in with arms down (prop added separately)
- `shocked` — fades in, jumps back with arms up
- `wink` — quick scale pulse (comedic beat)
- `static` — fades in, no movement

---

### map
**What it does**: World dot-map schematic with optional country
highlight and trade-route arc.

```toml
[beats.map]
type            = "world-dots"  # only option currently
highlight       = "Taiwan"      # country to circle (see KNOWN_REGIONS)
arc_from        = "USA"         # arc start (see KNOWN_REGIONS)
arc_to          = "Taiwan"      # arc end
dot_color       = "GRID"
highlight_color = "RED"
arc_color       = "GOLD"
```

**Known regions** (usable in `highlight`, `arc_from`, `arc_to`):
USA, Canada, Mexico, Brazil, UK, France, Germany, Russia, China,
India, Japan, Taiwan, South Korea, Australia, South Africa, Egypt,
Saudi Arabia.

To add a region: open `primitives/map.py`, add to `KNOWN_REGIONS`
dict with `(x, y)` in Manim frame coordinates
(x ∈ [−7.1, +7.1], y ∈ [−4.0, +4.0]).

---

### prop
**What it does**: Renders a named icon built from Manim shapes.
No external SVG needed for built-ins. Supports external SVG via
`svg_path`.

```toml
[beats.prop]
name     = "chip"     # chip | globe | phone | factory
position = "center"   # center | left | right | top | bottom
scale    = 1.0        # tweak: 1.5=dominant  0.5=supporting
color    = "BLUE"
svg_path = ""         # optional: path to .svg overrides built-in
```

**Built-in props**: chip (square with grid lines), globe (circle with
lat/long lines), phone (rounded rectangle), factory (silhouette with
chimneys).

To add a new built-in: add a `_<name>_code(v, color, scale, pos)` 
function to `primitives/prop.py` and register it in `BUILT_IN_PROPS`.

---

### flood
**What it does**: N copies of an object appear across the screen in
a LaggedStart wave. "Factories everywhere", "phones everywhere" effect.

```toml
[beats.flood]
object      = "chip"   # prop name or short text
count       = 20       # tweak: more = overwhelming
spread_time = 2.0      # tweak: slower = tension builds
color       = "BLUE"
```

---

### electricity
**What it does**: Animated dot travels along a circuit trace or
straight path. Data flow, signal propagation, power transmission.

```toml
[beats.electricity]
mode      = "chip-traces"  # chip-traces | path
color     = "CYAN"
run_time  = 1.5            # tweak: faster = urgent signal
path_from = "left"         # for mode=path
path_to   = "right"        # for mode=path
```

---

### glitch
**What it does**: Rapid scale+colour flash on the last object added
to the scene. Data corruption, system error effect.

```toml
[beats.glitch]
target   = "title"   # descriptive label — no auto-lookup, applied to last object
duration = 0.4       # tweak: 0.15=violent  0.8=slow degradation
repeats  = 3         # tweak: 1=jolt  5+=full corruption
color    = "RED"     # RED=error  CYAN=digital corruption
```

**Important**: glitch is applied to the last object added to
`all_objects`. Place it after the primitive whose object you want
to glitch, within the same beat.

---

## 7. Running the Tool

### Requirements
- Python 3.11+ (for `tomllib` in stdlib)
- Manim Community Edition (for rendering — not needed to generate)

### Basic usage

```bash
# Generate scene.py from config
python origeno.py scene1.toml

# Specify output path explicitly
python origeno.py scene1.toml --output outputs/scene1.py

# Validate config without generating (check for errors first)
python origeno.py scene1.toml --validate-only

# List all registered primitives with their parameters
python origeno.py --list-primitives
```

### Exit codes
- `0` — success
- `1` — config validation error (bad TOML values, missing fields,
        timing mismatch)
- `2` — file not found
- `3` — unexpected error (bug in tool)

### What the output looks like

```
✓  Config valid: scene1.toml
   Scene   : The Hidden Dependency
   Class   : Scene1
   Duration: 45s
   Beats   : 4

✓  Generated: scene1.py

▶  Render commands:
   manim -pqh scene1.py Scene1         # 1080p
   manim -pql scene1.py Scene1         # preview (fast)
   manim -pqk scene1.py Scene1         # 4K
```

---

## 8. Rendering with Manim

The generated `scene.py` is a standard Manim script. Render with:

```bash
# Preview (fast, low quality — use during iteration)
manim -pql scene1.py Scene1

# 1080p (default for final)
manim -pqh scene1.py Scene1

# 4K
manim -pqk scene1.py Scene1

# Render specific beats by using --from_animation and --upto_animation
# (Manim feature — useful for checking a single beat)
```

**Output location**: Manim writes to `media/videos/scene1/` by default.
The exact path is printed after rendering.

**Frame rate**: Set in `[scene] fps` in the config. Default 30.

---

## 9. Adding a New Primitive

This is the primary extension point. Follow these steps exactly.

### Step 1 — Create the primitive file

```python
# primitives/timeline.py
"""
primitives/timeline.py — Timeline primitive
============================================
[one paragraph describing what it does and when to use it]

TOML BLOCK
----------
[beats.timeline]
events    = [...]     # list of event labels
duration  = 3.0       # total animation time
color     = "BLUE"
position  = "center"
"""

from primitives.base import BasePrimitive
from core.registry import register


@register("timeline")         # ← the key used in TOML [beats.timeline]
class Timeline(BasePrimitive):

    PARAMS = {
        "duration": {
            "type"   : "float",
            "default": 3.0,
            "range"  : (0.5, 8.0),
            "hint"   : "Total animation duration.",
            "tweak"  : "Slower = each event lands with more weight.",
        },
        # ... define all parameters
    }

    def render(self) -> str:
        duration = self.get("duration", 3.0)
        v = self.var("timeline")   # unique variable prefix e.g. "_b2_timeline"

        return f"""# Timeline
# ... your Manim code here ...
# Use {v}_something for variable names to avoid name collisions
# between beats. self.var() generates "_b<beatid>_<suffix>".
"""
```

### Step 2 — Import it in primitives/__init__.py

```python
# At the bottom of the existing import block:
from primitives import timeline
```

### Step 3 — Use it in a config

```toml
[beats.timeline]
duration = 3.0
```

### Step 4 — Nothing else

The registry picks it up automatically. The assembler needs no changes.
The loader validates against the registry automatically. Existing configs
are not affected.

### Rules for render() method

1. **Return a string** of Python code, not a list of lines.
2. **Write at column 0**. The assembler adds the 8-space indent.
3. **Use `self.var("suffix")`** for all variable names to avoid
   collisions between beats (e.g. two stamps in different beats both
   name their variable `_b1_stamp` vs `_b2_stamp`).
4. **Use `self.get("key", default)`** not `self.cfg.get("key")` so
   PARAMS defaults are respected.
5. **Use `self.color("RED")`** not the hex string directly, so palette
   overrides work.
6. **Add to `all_objects`** at the end: `all_objects.add({v})`
7. **Write a docstring** at the top of the file explaining the TOML
   block format — future you will thank you.

---

## 10. Debugging Guide

### "Config validation error"

The loader always includes the field path and what was wrong. Read the
full error message — it tells you exactly which field to fix.

Common causes:
- `time_start / time_end` don't sum to `scene.duration` → check all
  beats, recalculate
- `camera` value not in valid set → check spelling, use lowercase
- `[beats.somename]` block where `somename` is not a registered primitive
  → check `python origeno.py --list-primitives` for valid names
- Missing `id`, `time_start`, or `time_end` in a beat

### "Unknown primitive 'X'"

You used `[beats.X]` in a config but `X` is not registered. Either:
- Typo in the block name → fix the config
- New primitive not yet built → create `primitives/X.py` following
  the guide in Section 9

### "scene.py renders but animation looks wrong"

1. Identify which beat/primitive is wrong.
2. Open `scene.py`, find the beat comment block:
   `# BEAT N — Beat Name`
3. Read the generated code for that primitive.
4. Trace back to the primitive's `render()` method in
   `primitives/<name>.py`.
5. Fix the `render()` method, regenerate, re-render.

### "Variable name collision — 'X' already defined"

This means two primitives in the same beat used the same variable name.
All primitives must use `self.var("suffix")` which generates
`_b<beatid>_<suffix>`. If two primitives of the same type appear in
one beat (unusual), the second call will collide. Fix: add a more
specific suffix in `var()`.

### "FadeOut removes the background dots"

The transition code in `assembler.py` explicitly excludes `_bg`
from FadeOut:
```python
FadeOut(VGroup(*[m for m in self.mobjects if m is not _bg]))
```
If the background is still disappearing, check that `circuit_bg()`
assigns its result to `_bg` and that the primitive's `render()` is
not replacing `_bg` with something else.

### "Manim crash: name 'X' is not defined"

This is a bug in a primitive's `render()` output. The generated code
references a variable that doesn't exist. Common causes:
- Using a variable name from a helper (`C_RED`, `FONT`, etc.) that
  is not inlined in the header — check `assembler._write_header()`
- Using a Manim class that is not in `from manim import *`
  (e.g. `ArcBetweenPoints` — check Manim CE docs for the exact name)

---

## 11. Architecture Deep-Dive

### Data flow (detailed)

```
origeno.py
    │  argparse
    ▼
primitives/__init__.py
    │  imports all primitive modules
    │  @register() decorators fire → _REGISTRY populated
    ▼
core/loader.py  load(path)
    │  tomllib.load() → raw dict
    │  _validate() → ConfigError if invalid
    │  _normalise() → fills defaults, extracts primitive sub-blocks
    │  returns: { scene, config, assets, beats }
    │  beats[i]["primitives"] = { "stamp": {...}, "counter": {...} }
    ▼
core/assembler.py  assemble(config, output_path)
    │  _write_header()       → imports, brand constants, helpers
    │  _write_class_open()   → class ClassName(MovingCameraScene):
    │                          T_BEAT_N timing constants
    │  _write_construct_open() → def construct(self):
    │  _write_circuit_bg()   → _bg = circuit_bg(self)
    │  for each beat:
    │      _write_beat()
    │          _write_camera_in()
    │          _write_ken_burns()
    │          for each primitive in beat["primitives"]:
    │              cls = registry.get(name)
    │              obj = cls(prim_config, full_config, beat)
    │              code = obj.render()
    │              → lines.append(indented code)
    │          self.wait(T_BEAT_N)
    │          _write_transition()
    │  _write_outro()
    │  _write_footer()
    ▼
scene.py  (written to disk)
```

### Registry internals

`_REGISTRY` is a module-level dict in `core/registry.py`. It is
populated when `primitives/__init__.py` is imported (which happens
at the top of `origeno.py`). The `@register("name")` decorator is
a closure that captures `name` and stores `cls` in `_REGISTRY[name]`.

The loader calls `core.registry.all_names()` during validation to
check that `[beats.X]` blocks are known. This means: if a primitive
file exists but is not imported in `primitives/__init__.py`, it will
not be in the registry and configs using it will fail validation.

### BasePrimitive.var()

Every primitive calls `self.var("something")` to generate variable
names. This produces `_b{beat_id}_{suffix}` e.g. `_b1_stamp`,
`_b2_stamp`. This prevents collisions when the same primitive type
appears in multiple beats (which is normal — stamps appear in
nearly every beat).

### The all_objects VGroup

The assembler initialises `all_objects = VGroup()` at the start of
`construct()`. Every primitive's `render()` output ends with:
```python
all_objects.add({v})
```
This lets the assembler (and glitch primitive) reference "everything
on screen" without tracking individual objects. The final fade uses
`self.mobjects` directly to catch anything not added to `all_objects`.

### Transition logic

| Transition | What happens |
|---|---|
| `keep` | Nothing — objects persist into next beat |
| `fade` | FadeOut all non-bg objects, restore camera |
| `cut` | Remove all non-bg objects instantly |
| `fade-to-black` | Handled in `_write_outro()` — final beat only |
| `slide` | Currently same as fade — future: slide direction |

---

## 12. Design Decisions and Why

### Decision: one TOML file per scene (not per video)
Each scene has its own config. A video with 9 scenes has 9 TOML files.
This keeps configs small and focused, makes iteration fast (only
re-run the scene you changed), and allows scenes to be reordered or
reused across videos.

### Decision: time_start + time_end (not duration per beat)
The validator sums `(time_end - time_start)` and checks it equals
`scene.duration`. This catches timing errors that a pure `duration`
field would miss (e.g. beats with gaps or overlaps).

### Decision: primitive params have inline tweak comments
Every timing/feel parameter in the example config has a comment like:
```toml
run_time = 0.6   # tweak: 0.3=snappy  1.2=slow dramatic
```
This is intentional UX design. The owner tweaks configs often, and
should not need to open source code to understand what a value does.
The PARAMS dict in each primitive class is the source for these
comments — future tooling could auto-generate them.

### Decision: character is built from Manim primitives, not SVG
External SVG files add a dependency: the file must exist at render
time, at the right path, on the right machine. The stick-figure
character needs no assets. New machines, new collaborators, new
render environments — all work immediately.

### Decision: map is schematic, not geographic
A real map projection would require a coordinate dataset (~1000 points
minimum) and a projection library. The dot-map is a schematic that
is visually recognisable without being geographically precise. For
the channel's educational style, this is sufficient. If a real map
is needed, the map primitive can be upgraded — the interface does not
change.

---

## 13. Known Limitations and Future Work

### Current limitations

**Character actions are basic**: The stick-figure has limited
expressiveness. "points-at" uses a simple arm extension. Full
walk-cycle animation would require more complex keyframing.
This is a known trade-off — the current implementation is reliable
and offline.

**Map is schematic only**: `world-dots` is a hand-crafted dot grid,
not a real cartographic projection. Countries are approximate. To
upgrade: replace `_world_dot_positions()` in `map.py` with a
Robinson-projection point set derived from Natural Earth data.

**Glitch targets last object only**: The glitch primitive cannot
target a specific named object from a previous beat. The workaround
is to use `transition = "keep"` and place the glitch in the next beat
immediately after the object is introduced.

**No audio sync**: The tool does not know about the voiceover audio.
`narration` fields are written as comments in `scene.py` for
reference, but timing is the owner's responsibility.

**slide transition is a stub**: Currently `slide` behaves like `fade`.
Implementing directional slide requires knowing the slide direction —
add a `transition_dir` field to beats and update `_write_transition()`
in `assembler.py`.

### Natural growth areas (add when needed, not before)

- **race_track** primitive — nodes racing along horizontal lanes
  (already used in clip_01 manually)
- **text_reveal** primitive — letter-by-letter text appearance
- **network_graph** primitive — nodes connected by edges, for
  supply chain / dependency diagrams
- **timeline** primitive — horizontal time axis with events
- **split_screen** beat-level feature — two primitives side by side
- **bg_image** support — the field exists in the schema but the
  assembler currently ignores it; add loading logic in
  `_write_construct_open()`
- **auto-config from template** — a separate tool that reads the
  5-section scene planning template and outputs a starter TOML.
  Deliberately not built yet; the owner prefers AI-assisted manual
  translation for now.

---

## 14. Glossary

| Term | Meaning |
|---|---|
| **Scene** | One continuous animation clip, 30-60 seconds. Maps to one TOML file and one Manim class. |
| **Beat** | A timed segment within a scene. Has a start time, end time, narration line, and zero or more primitives. |
| **Primitive** | A reusable animation building block (stamp, counter, chart, etc.). Implemented as a Python class in `primitives/`. |
| **Config file** | A TOML file describing one scene. This is the source of truth. |
| **scene.py** | The Manim Python script generated from the config. Never edited by hand. |
| **Registry** | The `_REGISTRY` dict in `core/registry.py`. Maps primitive names to classes. |
| **PARAMS** | A dict defined on each primitive class documenting its configurable parameters, defaults, and tweak hints. |
| **Tweak loop** | The iterative workflow: edit config → regenerate → re-render → review → repeat. |
| **Brand constants** | Colour palette, font, background defined in `defaults.py` and inlined into every `scene.py`. |
| **Scene planning template** | The 5-section human document (Sections 1-5) the owner writes before creating the TOML. Not parsed by the tool. |
| **all_objects** | A `VGroup` initialised in `construct()` that accumulates every on-screen object. Used for bulk FadeOut transitions. |
| **var()** | `BasePrimitive.var(suffix)` — generates `_b{beatid}_{suffix}` to avoid variable name collisions between beats. |
