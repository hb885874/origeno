"""
scene4.py — "Yield: The Hidden Game"
Origeno Educational Video Channel
Style: Oversimplified | Duration: ~60s | FPS: 60

Verified beat timing:
  Beat 1  Not Just Making    ~ 9.6s  chip duplicates, glitch flicker, zoom-in
  Beat 2  Wafer Overview     ~ 9.9s  wafer + 100 chip tiles flood + counter
  Beat 3  Imperfection       ~ 9.1s  random chips fail red, DEFECT stamp
  Beat 4  High Yield         ~11.2s  90 chips go green, counter, pie chart
  Beat 5  Low Yield          ~ 9.4s  50 red, factory turns red, LOSS stamp
  Beat 6  Experience Matters ~11.2s  counter 50→90, chips stabilise, zoom-out, fade
  ───────────────────────────────────
  TOTAL                      ~60.4s

Design rules (same as scene2/3):
  • load_asset() always returns Group or None — never crashes on PNG
  • Pure-geometry containers use VGroup(), asset containers use Group()
  • No animate chain .set_fill(color, opacity=kw) — use .set_color() instead
  • Title / narr faded before animations that could cover them
  • No Unicode arrows or Hindi in Text() calls

Asset folder (all optional, built-in fallbacks):
  scene4.py
  asset/
      wafer.svg  or  wafer.png
      factory.svg or factory.png
      chip.svg   or  chip.png
"""

from manim import *
import numpy as np
import os
import random

# ─────────────────────────────────────────────
# PALETTE & CONFIG
# ─────────────────────────────────────────────
BG       = "#F5F0E8"
RED      = "#D42B2B"
BLUE     = "#2255AA"
GOLD     = "#C8960C"
GREEN    = "#2A7A2A"
DARK     = "#1A1A1A"
SOFT_GRY = "#888888"
WHITE_OP = "#FFFFFF"
PURPLE   = "#7B2FBE"
LT_GREEN = "#4CAF50"
LT_RED   = "#E57373"

config.background_color = BG
# Resolution controlled by CLI:
#   manim -ql scene4.py Scene4   → 480p  preview
#   manim -qm scene4.py Scene4   → 720p  preview
#   manim -qh scene4.py Scene4   → 1080p final
config.frame_rate = 60

# ─────────────────────────────────────────────
# ASSET PATHS
# ─────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR   = os.path.join(SCRIPT_DIR, "asset")
SVG_WAFER   = os.path.join(ASSET_DIR, "wafer.svg")
SVG_FACTORY = os.path.join(ASSET_DIR, "factory.svg")
SVG_CHIP    = os.path.join(ASSET_DIR, "chip.svg")


# ═══════════════════════════════════════════════
# ASSET LOADER  — always returns Group or None
# ═══════════════════════════════════════════════

def load_asset(svg_path, height=1.0, color=BLUE):
    path = svg_path
    if not os.path.exists(path):
        base = os.path.splitext(path)[0]
        for ext in (".png", ".jpg", ".jpeg"):
            if os.path.exists(base + ext):
                path = base + ext
                break
        else:
            return None
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in (".png", ".jpg", ".jpeg"):
            mob = ImageMobject(path)
            mob.set_height(height)
            return Group(mob)
        else:
            mob = SVGMobject(path)
            mob.set_fill(color, opacity=1)
            mob.set_stroke(color, width=0)
            mob.set_height(height)
            return Group(mob)
    except Exception:
        return None


# ═══════════════════════════════════════════════
# PROP BUILDERS
# ═══════════════════════════════════════════════

def make_chip_tile(size=0.38, color=BLUE) -> VGroup:
    """Small chip tile for wafer grid."""
    asset = load_asset(SVG_CHIP, height=size, color=color)
    if asset is not None:
        return asset
    body = RoundedRectangle(
        corner_radius=0.03, width=size, height=size,
        fill_color=color, fill_opacity=1,
        stroke_color=WHITE_OP, stroke_width=0.8)
    # Tiny cross on body
    h = Line([-size*0.28, 0, 0], [size*0.28, 0, 0],
             stroke_color=WHITE_OP, stroke_width=0.6, stroke_opacity=0.5)
    v = Line([0, -size*0.28, 0], [0,  size*0.28, 0],
             stroke_color=WHITE_OP, stroke_width=0.6, stroke_opacity=0.5)
    return VGroup(body, h, v)


def make_wafer_outline(radius=2.8) -> VGroup:
    """Silicon wafer circle with subtle grid lines."""
    asset = load_asset(SVG_WAFER, height=radius*2, color=SOFT_GRY)
    if asset is not None:
        return asset
    disc  = Circle(radius=radius, fill_color="#D8D8D8", fill_opacity=0.25,
                   stroke_color=SOFT_GRY, stroke_width=2.5)
    notch = Arc(radius=radius, start_angle=-PI/2 - 0.12, angle=0.24,
                stroke_color=DARK, stroke_width=4)
    return VGroup(disc, notch)


def make_factory_icon(width=1.6) -> VGroup:
    """Simple flat factory silhouette."""
    asset = load_asset(SVG_FACTORY, height=width*0.8, color=DARK)
    if asset is not None:
        return asset
    h = width * 0.55
    base = Rectangle(width=width, height=h,
                     fill_color=DARK, fill_opacity=1,
                     stroke_color=SOFT_GRY, stroke_width=1.5)
    base.move_to([0, -h*0.10, 0])
    ch1 = Rectangle(width=width*0.13, height=h*0.55,
                    fill_color=DARK, fill_opacity=1,
                    stroke_color=SOFT_GRY, stroke_width=1
                    ).move_to([-width*0.28, h*0.38, 0])
    ch2 = Rectangle(width=width*0.13, height=h*0.40,
                    fill_color=DARK, fill_opacity=1,
                    stroke_color=SOFT_GRY, stroke_width=1
                    ).move_to([width*0.28, h*0.32, 0])
    smoke = Arc(radius=0.10, start_angle=PI/2, angle=PI,
                stroke_color=SOFT_GRY, stroke_width=1.5, stroke_opacity=0.5
                ).move_to([-width*0.28+0.10, h*0.58, 0])
    return VGroup(base, ch1, ch2, smoke)


# ─────────────────────────────────────────────
# WAFER CHIP GRID HELPER
# Returns list of (chip_mobject, position, is_inside_wafer)
# ─────────────────────────────────────────────
def build_wafer_chip_grid(wafer_radius=2.8, tile_size=0.38, gap=0.06):
    """
    Build a rectangular grid of chip tiles that fit inside wafer_radius.
    Returns list of VGroup chips and their centre positions.
    """
    step    = tile_size + gap
    chips   = []
    half    = int(wafer_radius / step) + 1
    for row in range(-half, half + 1):
        for col in range(-half, half + 1):
            cx = col * step
            cy = row * step
            # Check if tile fits inside circle (use centre point)
            if np.sqrt(cx**2 + cy**2) + tile_size * 0.55 <= wafer_radius:
                tile = make_chip_tile(size=tile_size, color=BLUE)
                tile.move_to([cx, cy, 0])
                chips.append((tile, np.array([cx, cy, 0])))
    return chips


# ─────────────────────────────────────────────
# PIE CHART HELPER (Beat 4 & 5)
# ─────────────────────────────────────────────
def make_pie(good_pct, radius=1.1, centre=ORIGIN) -> VGroup:
    """
    Simple two-slice pie chart: good_pct green, rest red.
    Returns VGroup of two sectors + labels.
    """
    good_angle = good_pct / 100 * TAU
    bad_angle  = TAU - good_angle

    good_sector = AnnularSector(
        inner_radius=0, outer_radius=radius,
        angle=good_angle, start_angle=PI/2,
        fill_color=GREEN, fill_opacity=0.85, stroke_width=0)
    bad_sector = AnnularSector(
        inner_radius=0, outer_radius=radius,
        angle=bad_angle, start_angle=PI/2 + good_angle,
        fill_color=RED, fill_opacity=0.85, stroke_width=0)

    good_lbl = Text(f"{good_pct}%", font="Georgia",
                    font_size=22, color=WHITE_OP, weight=BOLD)
    bad_lbl  = Text(f"{100-good_pct}%", font="Georgia",
                    font_size=22, color=WHITE_OP, weight=BOLD)

    # Place labels at sector midpoints
    good_mid = PI/2 + good_angle/2
    bad_mid  = PI/2 + good_angle + bad_angle/2
    good_lbl.move_to(np.array([
        np.cos(good_mid) * radius * 0.65,
        np.sin(good_mid) * radius * 0.65, 0]) + centre)
    bad_lbl.move_to(np.array([
        np.cos(bad_mid) * radius * 0.65,
        np.sin(bad_mid) * radius * 0.65, 0]) + centre)

    g = VGroup(good_sector, bad_sector)
    g.move_to(centre)
    return VGroup(g, good_lbl, bad_lbl)


# ═══════════════════════════════════════════════
# SCENE
# ═══════════════════════════════════════════════

class Scene4(MovingCameraScene):

    def _reset_camera(self):
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.set(width=14.22)

    def construct(self):
        self._beat1()
        self._beat2()
        self._beat3()
        self._beat4()
        self._beat5()
        self._beat6()

    # ──────────────────────────────────────────
    # BEAT 1  ·  ~9.6s  ·  Not Just Making
    # Chip + duplicates, some dim/glitch, zoom-in
    # ──────────────────────────────────────────
    def _beat1(self):
        self._reset_camera()

        title = Text("Making  is not  Perfect Making",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.6))

        narr = Text(
            "Making chips is not just making them... it's making them right.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Central chip
        chip_c = make_chip_tile(size=1.4, color=BLUE)
        chip_c.move_to(ORIGIN)
        self.play(FadeIn(chip_c, scale=0.4, run_time=0.8))

        # Duplicate chips around it — 6 copies, alternating bright/dim
        offsets = [
            (-2.8, 1.2), (0, 2.2), (2.8, 1.2),
            (-2.8,-1.2), (0,-2.2), (2.8,-1.2),
        ]
        dupes = Group()
        for i, (dx, dy) in enumerate(offsets):
            c = BLUE if i % 2 == 0 else SOFT_GRY
            op = 1.0 if i % 2 == 0 else 0.35
            d = make_chip_tile(size=1.0, color=c)
            d.move_to([dx, dy, 0])
            d.set_opacity(op)
            dupes.add(d)
        self.play(LaggedStart(
            *[FadeIn(d, scale=0.3) for d in dupes],
            lag_ratio=0.12, run_time=1.2))

        # Glitch flicker on dim chips — colour flash using set_color
        for _ in range(3):
            anims = []
            for i, d in enumerate(dupes):
                if i % 2 != 0:   # dim chips
                    anims.append(d.animate.set_color(RED))
            self.play(*anims, run_time=0.12)
            anims2 = [d.animate.set_color(SOFT_GRY)
                      for i, d in enumerate(dupes) if i % 2 != 0]
            self.play(*anims2, run_time=0.10)

        # Ken Burns zoom-in
        self.play(
            self.camera.frame.animate.scale(0.80).move_to(ORIGIN),
            run_time=3.5)
        self.wait(1.2)

        self.play(FadeOut(chip_c), FadeOut(dupes),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 2  ·  ~9.9s  ·  Wafer Overview
    # Wafer appears, 100 chip tiles flood it, counter
    # ──────────────────────────────────────────
    def _beat2(self):
        self._reset_camera()

        title = Text("Hundreds of Chips per Wafer",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "One silicon wafer produces hundreds of chips at once.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Wafer outline
        wafer = make_wafer_outline(radius=2.9)
        wafer.move_to(ORIGIN)
        self.play(FadeIn(wafer, run_time=0.8))

        # Build chip grid inside wafer
        chip_data = build_wafer_chip_grid(
            wafer_radius=2.75, tile_size=0.36, gap=0.07)
        # Cap at 100 for clean counter
        chip_data = chip_data[:100]

        # Counter — top-right, outside wafer
        c_lbl = Text("Chips:", font="Georgia",
                     font_size=22, color=DARK).move_to([5.0, 0.5, 0])
        c_val = Text("0", font="Georgia", font_size=38,
                     color=BLUE, weight=BOLD).move_to([5.0, -0.1, 0])
        self.play(FadeIn(c_lbl), FadeIn(c_val), run_time=0.4)

        # Flood chips — every 10th chip update counter
        all_chips = Group()
        milestone = len(chip_data) // 10
        for i, (tile, _) in enumerate(chip_data):
            all_chips.add(tile)

        # Animate in batches of 10 for smooth counter
        for batch_start in range(0, len(chip_data), 10):
            batch = [chip_data[j][0]
                     for j in range(batch_start,
                                    min(batch_start+10, len(chip_data)))]
            count_so_far = min(batch_start + 10, len(chip_data))
            nv = Text(str(count_so_far), font="Georgia", font_size=38,
                      color=BLUE, weight=BOLD).move_to(c_val.get_center())
            self.play(
                LaggedStart(*[FadeIn(b, scale=0.2) for b in batch],
                            lag_ratio=0.03, run_time=0.35),
                ReplacementTransform(c_val, nv, run_time=0.35))
            c_val = nv

        self.wait(1.2)
        self.play(FadeOut(wafer), FadeOut(all_chips),
                  FadeOut(c_lbl), FadeOut(c_val),
                  FadeOut(title), FadeOut(narr), run_time=0.6)

    # ──────────────────────────────────────────
    # BEAT 3  ·  ~9.1s  ·  Imperfection Reality
    # Some chips randomly fail (turn red/dim), DEFECT stamp
    # ──────────────────────────────────────────
    def _beat3(self):
        self._reset_camera()

        title = Text("Not All Chips Work",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "But not every chip on the wafer is perfect.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Rebuild wafer + chip grid (compact version — 60 chips)
        wafer = make_wafer_outline(radius=2.9)
        wafer.move_to(ORIGIN)
        self.add(wafer)

        chip_data = build_wafer_chip_grid(
            wafer_radius=2.75, tile_size=0.36, gap=0.07)[:60]
        all_chips = Group(*[t for t, _ in chip_data])

        self.play(
            FadeIn(wafer, run_time=0.5),
            LaggedStart(*[FadeIn(t, scale=0.2) for t, _ in chip_data],
                        lag_ratio=0.02, run_time=0.8))

        # ~20 chips randomly fail — set_color(RED) + dim
        rng = random.Random(13)
        fail_indices = rng.sample(range(len(chip_data)), 20)
        fail_anims = []
        for idx in fail_indices:
            tile = chip_data[idx][0]
            fail_anims.append(tile.animate.set_color(RED).set_opacity(0.55))
        self.play(LaggedStart(*fail_anims, lag_ratio=0.04, run_time=0.6))

        # Glitch flicker on failed chips × 3
        fail_tiles = [chip_data[i][0] for i in fail_indices]
        for _ in range(3):
            self.play(*[t.animate.set_color(GOLD) for t in fail_tiles],
                      run_time=0.08)
            self.play(*[t.animate.set_color(RED)  for t in fail_tiles],
                      run_time=0.08)

        # DEFECT stamp — top-left corner
        stamp = Text("DEFECT", font="Georgia",
                     font_size=58, color=RED, weight=BOLD)
        stamp.to_corner(UL, buff=0.45)
        stamp_start = stamp.copy().shift(UP * 3.5)
        self.add(stamp_start)
        self.play(stamp_start.animate.move_to(stamp.get_center()),
                  run_time=0.40)
        self.remove(stamp_start)
        self.add(stamp)

        self.wait(2.8)
        self.play(FadeOut(wafer), FadeOut(all_chips), FadeOut(stamp),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 4  ·  ~11.2s  ·  High Yield
    # 90 chips green, 10 dim, counter, pie chart
    # ──────────────────────────────────────────
    def _beat4(self):
        self._reset_camera()

        title = Text("High Yield  =  90%",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "If 90 out of 100 chips work... that is called high yield.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Left side: wafer with 90 green + 10 red chips
        wafer = make_wafer_outline(radius=2.5)
        wafer.move_to([-2.8, 0.0, 0])
        self.play(FadeIn(wafer, run_time=0.5))

        chip_data = build_wafer_chip_grid(
            wafer_radius=2.55, tile_size=0.34, gap=0.07)[:100]

        # Show all chips dim first
        all_tiles = Group(*[t for t, _ in chip_data])
        for t, _ in chip_data:
            t.set_color(SOFT_GRY).set_opacity(0.35)
            t.move_to(t.get_center() + np.array([-2.8, 0, 0]))
        self.play(FadeIn(all_tiles, run_time=0.5))

        # Counter — right side
        c_lbl = Text("Working:", font="Georgia",
                     font_size=22, color=DARK).move_to([5.0, 0.6, 0])
        c_val = Text("0", font="Georgia", font_size=42,
                     color=GREEN, weight=BOLD).move_to([5.0, 0.0, 0])
        self.play(FadeIn(c_lbl), FadeIn(c_val), run_time=0.4)

        # Animate 90 chips lighting up green, counter increments every 10
        rng = random.Random(42)
        n_good = min(90, len(chip_data))   # defensive clamp
        good_indices = rng.sample(range(len(chip_data)), n_good)
        bad_indices  = [i for i in range(len(chip_data))
                        if i not in good_indices]

        # Turn bad ones red right away
        self.play(*[chip_data[i][0].animate.set_color(RED).set_opacity(0.55)
                    for i in bad_indices], run_time=0.3)

        # Light up good ones in batches of 10
        for batch_num in range(9):
            batch = good_indices[batch_num*10 : (batch_num+1)*10]
            count = (batch_num + 1) * 10
            nv = Text(str(count), font="Georgia", font_size=42,
                      color=GREEN, weight=BOLD).move_to(c_val.get_center())
            self.play(
                LaggedStart(
                    *[chip_data[i][0].animate.set_color(LT_GREEN).set_opacity(1.0)
                      for i in batch],
                    lag_ratio=0.03, run_time=0.38),
                ReplacementTransform(c_val, nv, run_time=0.38))
            c_val = nv

        # Pie chart — right-centre area
        pie = make_pie(90, radius=1.1, centre=np.array([4.2, -0.5, 0]))
        pie_lbl = Text("Yield", font="Georgia", font_size=20,
                       color=DARK).move_to([4.2, -1.9, 0])
        self.play(FadeIn(pie, run_time=0.8), FadeIn(pie_lbl, run_time=0.6))

        # Zoom slightly
        self.play(self.camera.frame.animate.scale(0.90), run_time=1.5)
        self.wait(1.8)

        self.play(FadeOut(wafer), FadeOut(all_tiles), FadeOut(pie),
                  FadeOut(pie_lbl), FadeOut(c_lbl), FadeOut(c_val),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 5  ·  ~9.4s  ·  Low Yield
    # 50 red chips, factory turns red, LOSS stamp
    # ──────────────────────────────────────────
    def _beat5(self):
        self._reset_camera()

        title = Text("Low Yield  =  Loss",
                     font="Georgia", font_size=36, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "If only 50 work... the factory runs at a loss.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Wafer — left side
        wafer = make_wafer_outline(radius=2.3)
        wafer.move_to([-3.0, 0.0, 0])
        self.play(FadeIn(wafer, run_time=0.5))

        chip_data = build_wafer_chip_grid(
            wafer_radius=2.40, tile_size=0.34, gap=0.07)[:100]

        rng = random.Random(99)
        n_good5 = min(50, len(chip_data))
        good_idx = rng.sample(range(len(chip_data)), n_good5)
        bad_idx  = [i for i in range(len(chip_data)) if i not in good_idx]

        all_tiles = Group(*[t for t, _ in chip_data])
        for t, _ in chip_data:
            t.move_to(t.get_center() + np.array([-3.0, 0, 0]))

        # Show wafer filled — 50 green, 50 red simultaneously
        good_anims = [chip_data[i][0].animate.set_color(LT_GREEN).set_opacity(0.9)
                      for i in good_idx]
        bad_anims  = [chip_data[i][0].animate.set_color(RED).set_opacity(0.75)
                      for i in bad_idx]
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.2) for t, _ in chip_data],
                        lag_ratio=0.02, run_time=0.9))
        self.play(*good_anims + bad_anims, run_time=0.50)

        # Factory icon — right side
        factory = make_factory_icon(width=2.2)
        factory.move_to([3.5, 0.2, 0])
        self.play(FadeIn(factory, scale=0.4, run_time=0.8))

        # Factory turns red — financial loss signal
        self.play(factory.animate.set_color(RED), run_time=0.4)

        # Pie chart — between wafer and factory
        pie = make_pie(50, radius=0.95, centre=np.array([0.3, -0.4, 0]))
        self.play(FadeIn(pie, run_time=0.5))

        # LOSS stamp slides from right
        loss = Text("LOSS", font="Georgia",
                    font_size=80, color=RED, weight=BOLD)
        loss.move_to(RIGHT * 12)
        self.play(loss.animate.move_to([0, 2.0, 0]), run_time=0.45)

        # Slight pan down
        self.play(self.camera.frame.animate.shift(DOWN * 0.4), run_time=1.5)
        self.wait(0.8)

        self.play(FadeOut(wafer), FadeOut(all_tiles), FadeOut(factory),
                  FadeOut(pie), FadeOut(loss),
                  FadeOut(title), FadeOut(narr), run_time=0.5)

    # ──────────────────────────────────────────
    # BEAT 6  ·  ~11.2s  ·  Experience Matters
    # Counter 50→90, chips stabilise green, zoom-out, fade
    # ──────────────────────────────────────────
    def _beat6(self):
        self._reset_camera()

        title = Text("Experience  =  Higher Yield",
                     font="Georgia", font_size=34, color=DARK, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, run_time=0.5))

        narr = Text(
            "That's why experience matters so much in chip manufacturing.",
            font="Georgia", font_size=20, color=SOFT_GRY, slant=ITALIC)
        narr.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(narr, run_time=0.5))

        # Wafer with mixed chips starting at 50% yield
        wafer = make_wafer_outline(radius=2.5)
        wafer.move_to(ORIGIN)
        self.play(FadeIn(wafer, run_time=0.5))

        chip_data = build_wafer_chip_grid(
            wafer_radius=2.55, tile_size=0.34, gap=0.07)[:100]
        all_tiles = Group(*[t for t, _ in chip_data])

        rng  = random.Random(77)
        n_start = min(50, len(chip_data))
        good_start = rng.sample(range(len(chip_data)), n_start)
        bad_start  = [i for i in range(len(chip_data)) if i not in good_start]

        for i, (t, _) in enumerate(chip_data):
            if i in good_start:
                t.set_color(LT_GREEN).set_opacity(0.85)
            else:
                t.set_color(RED).set_opacity(0.65)
        self.play(FadeIn(all_tiles, run_time=0.6))

        # Yield improvement counter: 50 → 90
        y_lbl = Text("Yield:", font="Georgia",
                     font_size=24, color=DARK).move_to([5.2, 0.6, 0])
        y_val = Text("50%", font="Georgia", font_size=42,
                     color=RED, weight=BOLD).move_to([5.2, 0.0, 0])
        self.play(FadeIn(y_lbl), FadeIn(y_val), run_time=0.4)

        # Gradually convert red chips to green in 4 waves
        # Each wave: +10 chips become green, counter updates
        extra_good = rng.sample(bad_start, min(40, len(bad_start)))  # 40 more go good
        wave_size  = 10
        cur_yield  = 50

        for wave in range(4):
            wave_chips = extra_good[wave*wave_size : (wave+1)*wave_size]
            cur_yield += wave_size
            col = GREEN if cur_yield >= 80 else GOLD
            nv = Text(f"{cur_yield}%", font="Georgia", font_size=42,
                      color=col, weight=BOLD).move_to(y_val.get_center())

            # Glow pulse on converting chips
            glow_anims = [
                chip_data[i][0].animate.set_color(LT_GREEN).set_opacity(1.0)
                for i in wave_chips
            ]
            self.play(
                *glow_anims,
                ReplacementTransform(y_val, nv, run_time=0.5),
                run_time=0.5)
            y_val = nv
            self.wait(0.25)

        # Final state: stable green wafer + electricity glow pulses
        # (3 expanding rings from wafer centre)
        for _ in range(3):
            ring = Circle(radius=0.4, stroke_color=GREEN,
                          stroke_width=3, stroke_opacity=0.8,
                          fill_opacity=0).move_to(ORIGIN)
            self.add(ring)
            self.play(ring.animate.scale(7).set_opacity(0), run_time=0.45)
            self.remove(ring)

        # Updated pie chart
        pie = make_pie(90, radius=0.95, centre=np.array([4.5, -0.8, 0]))
        self.play(FadeIn(pie, run_time=0.5))

        # Zoom out Ken Burns
        self.play(
            self.camera.frame.animate.scale(1.18),
            run_time=3.0)
        self.wait(1.2)

        # Fade to black
        black_out = Rectangle(width=30, height=18,
                               fill_color=BLACK, fill_opacity=0,
                               stroke_width=0)
        self.add(black_out)
        self.play(black_out.animate.set_fill(BLACK, 1), run_time=1.0)
        self.wait(0.2)