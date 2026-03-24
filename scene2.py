"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 2: What Exactly Is a Chip?  |  60 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 10s │ 10s │ Question hook          — chip zooms in
Beat 2 │ 10s → 22s │ 12s │ Small but powerful     — glow + chip-traces
Beat 3 │ 22s → 36s │ 14s │ Inside the chip        — transistor flood + counter
Beat 4 │ 36s → 50s │ 14s │ Electricity control    — signal paths pan right
Beat 5 │ 50s → 60s │ 10s │ Real-world impact      — grid → phone + AI glow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 60s | No character | English only | Style: Oversimplified

LAYOUT ZONES
  TOP_Y   =  3.0   title panels / stamps
  STAGE_Y =  0.0   main stage (centred — no floor needed, no character)
  NAR_Y   = -3.10  narration strip

Render:
  Preview : manim -pql scene2.py Scene2
  1080p   : manim -pqh scene2.py Scene2
  4K      : manim -pqk scene2.py Scene2
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
# PALETTE  (identical to Scene 1)
# ─────────────────────────────────────────────────────────────
BG       = "#F5F0E8"
INK      = "#1A1008"
RED      = "#D42B2B"
BLUE     = "#2255AA"
GOLD     = "#C8960C"
CREAM    = "#FFFDF8"
SUBTLE   = "#9A8F7E"
WHITE    = "#FFFFFF"
ELECTRIC = "#00C8FF"
GREEN    = "#2A7A2A"
FONT     = "Georgia"

TOP_Y  =  3.0
NAR_Y  = -3.10
STAGE_Y = 0.0


# ─────────────────────────────────────────────────────────────
# TEXT HELPERS
# ─────────────────────────────────────────────────────────────
def T(text, size=34, color=INK, weight=BOLD):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)

def Ts(text, size=22, color=SUBTLE):
    return Text(text, font=FONT, font_size=size, color=color, weight=NORMAL)

def nar(text, size=32, color=INK):
    """Narration — always at NAR_Y, never overlaps stage."""
    return T(text, size=size, color=color, weight=NORMAL).move_to([0, NAR_Y, 0])

def fit_text(text, max_width, size=28, color=INK, weight=BOLD):
    mob = T(text, size=size, color=color, weight=weight)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


# ─────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────
def ink_panel(w, h, fill=CREAM, stroke=INK, sw=2.5):
    shadow = RoundedRectangle(
        corner_radius=0.14, width=w+0.10, height=h+0.10,
        color=INK, fill_color=INK, fill_opacity=0.10, stroke_width=0
    ).shift(DR * 0.08)
    box = RoundedRectangle(
        corner_radius=0.14, width=w, height=h,
        color=stroke, fill_color=fill, fill_opacity=1, stroke_width=sw
    )
    return VGroup(shadow, box)

def stamp(text, color=RED, w=3.4, h=0.80):
    outer = Rectangle(width=w,       height=h,
                       color=color,  fill_color=color,
                       fill_opacity=0.10, stroke_width=4.5)
    inner = Rectangle(width=w-0.16,  height=h-0.16,
                       color=color,  fill_opacity=0, stroke_width=1.8)
    lbl   = fit_text(text, max_width=w-0.30, size=38, color=color)
    return VGroup(outer, inner, lbl)

def slam(scene, mob, from_dir=UP, rt=0.28):
    mob.shift(from_dir * 4.0)
    scene.add(mob)
    scene.play(mob.animate.shift(-from_dir * 4.0),
                run_time=rt, rate_func=rush_from)


# ─────────────────────────────────────────────────────────────
# PROP BUILDERS
# ─────────────────────────────────────────────────────────────
def make_chip(sc=1.0):
    base = Square(side_length=1.40*sc, color=INK, fill_color="#1C2833",
                   fill_opacity=1, stroke_width=4)
    die  = Square(side_length=0.90*sc, color=GOLD, fill_color="#2C3E50",
                   fill_opacity=1, stroke_width=2.5)
    grid = VGroup(*[
        Line([v*sc, -0.45*sc, 0], [v*sc,  0.45*sc, 0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30, 0.30, 4)
    ] + [
        Line([-0.45*sc, v*sc, 0], [0.45*sc, v*sc, 0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30, 0.30, 4)
    ])
    core = Square(side_length=0.26*sc, color=RED, fill_color=RED,
                   fill_opacity=1, stroke_width=0)
    pins = VGroup(*[
        Rectangle(width=0.08*sc, height=0.20*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([-0.48*sc + i*0.24*sc, sg*0.80*sc, 0])
        for i in range(5) for sg in [1, -1]
    ] + [
        Rectangle(width=0.20*sc, height=0.08*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([sg*0.80*sc, -0.48*sc + i*0.24*sc, 0])
        for i in range(5) for sg in [1, -1]
    ])
    return VGroup(base, pins, die, grid, core)


def make_phone():
    body   = RoundedRectangle(corner_radius=0.18, width=1.10, height=1.90,
                               color=INK, fill_color="#2C3E50",
                               fill_opacity=1, stroke_width=3.5)
    screen = RoundedRectangle(corner_radius=0.10, width=0.85, height=1.42,
                               color="#D6EAF8", fill_color="#D6EAF8",
                               fill_opacity=1, stroke_width=1.5)
    notch  = Rectangle(width=0.26, height=0.09, color=INK,
                        fill_color=INK, fill_opacity=1, stroke_width=0)\
               .next_to(screen, UP, buff=0.05)
    btn    = Circle(radius=0.08, color="#888", fill_color="#888",
                     fill_opacity=1, stroke_width=0)\
               .next_to(body, DOWN, buff=-0.18)
    return VGroup(body, screen, notch, btn)


def make_lightning(start, end, steps=8, seed=0):
    np.random.seed(seed)
    pts = [np.array(start)]
    for i in range(1, steps):
        t    = i / steps
        mid  = np.array(start) * (1-t) + np.array(end) * t
        d    = np.array(end) - np.array(start)
        perp = np.array([-d[1], d[0], 0])
        n    = np.linalg.norm(perp)
        if n > 1e-4: perp /= n
        pts.append(mid + perp * (np.random.rand() - 0.5) * 0.26)
    pts.append(np.array(end))
    bolt = VMobject(stroke_color=ELECTRIC, stroke_width=3.8, stroke_opacity=0.95)
    bolt.set_points_as_corners(pts)
    return bolt


# ─────────────────────────────────────────────────────────────
# TRANSISTOR GRID  (Beat 3 flood)
# ─────────────────────────────────────────────────────────────
def make_transistor_grid(rows=14, cols=20, spacing=0.38):
    """
    Dense grid of tiny transistor symbols.
    Each symbol: small rectangle (gate) + two short lines (source/drain).
    Spread across the full stage area.
    """
    np.random.seed(7)
    group = VGroup()
    total_w = cols * spacing
    total_h = rows * spacing
    ox = -total_w / 2
    oy = -total_h / 2 + 0.3   # slight upward shift, centred on stage

    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing + np.random.uniform(-0.06, 0.06)
            y = oy + r * spacing + np.random.uniform(-0.06, 0.06)
            # Gate rectangle
            gate = Rectangle(width=0.12, height=0.20, color=BLUE,
                               fill_color="#1A2A4A", fill_opacity=1,
                               stroke_width=1.2).move_to([x, y, 0])
            # Source line (left)
            src  = Line([x-0.14, y, 0], [x-0.06, y, 0],
                         color=GOLD, stroke_width=1.0)
            # Drain line (right)
            drn  = Line([x+0.06, y, 0], [x+0.14, y, 0],
                         color=GOLD, stroke_width=1.0)
            group.add(VGroup(gate, src, drn))
    return group


# ─────────────────────────────────────────────────────────────
# SIGNAL PATH  (Beat 4 — electricity flowing through grid)
# ─────────────────────────────────────────────────────────────
def make_signal_paths(n_paths=6):
    """
    Horizontal L-shaped paths that simulate electrical signals
    flowing left-to-right through the transistor grid area.
    """
    np.random.seed(3)
    paths = VGroup()
    for i in range(n_paths):
        y_start = -2.0 + i * 0.70
        # Random waypoints creating an L-shaped route
        x0, x1, x2 = -6.0, np.random.uniform(-2.0, 0.0), 6.5
        y1 = y_start + np.random.choice([-0.35, 0.35])
        pts = [
            np.array([x0,  y_start, 0]),
            np.array([x1,  y_start, 0]),
            np.array([x1,  y1,      0]),
            np.array([x2,  y1,      0]),
        ]
        path = VMobject(stroke_color=ELECTRIC,
                         stroke_width=2.2, stroke_opacity=0.80)
        path.set_points_as_corners(pts)
        paths.add(path)
    return paths


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene2(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Permanent fixtures ───────────────────────────────────────
        paper = VGroup(*[
            Line(LEFT*7.8, RIGHT*7.8, color=INK,
                  stroke_width=0.25, stroke_opacity=0.05).shift(UP*y)
            for y in np.arange(-4.6, 4.8, 0.46)
        ])
        nar_line = Line(LEFT*6.8, RIGHT*6.8, color=INK,
                         stroke_width=1.0, stroke_opacity=0.14)\
                     .move_to([0, -2.15, 0])
        self.add(paper, nar_line)

        # ══════════════════════════════════════════════════════════════
        # BEAT 1  │  0s → 10s  │  Question hook — chip zooms in
        #
        # Chip starts small at centre, zooms up to fill stage.
        # "What is a CHIP?" stamp slams from top.
        # Narration holds on screen — no quick swap.
        #
        # 0.00–0.80  chip fades in small              0.80s
        # 0.80–1.80  chip scales up (Ken Burns zoom)  1.00s
        # 1.80–2.08  stamp slams from top             0.28s
        # 2.08–2.20  stamp wobble                     0.12s
        # 2.20–2.98  narration writes in              0.78s
        # 2.98–8.00  hold                             5.02s
        # 8.00–10.0  narration fades (clean exit)     2.00s
        # ══════════════════════════════════════════════════════════════
        chip = make_chip(sc=1.0).scale(0.60).move_to([0, STAGE_Y, 0])
        self.play(FadeIn(chip, run_time=0.80))
        self.play(chip.animate.scale(2.60), run_time=1.00, rate_func=smooth)

        PW1  = 5.8
        st1  = stamp("What is a CHIP?", color=RED, w=PW1, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st1, from_dir=UP, rt=0.28)
        self.play(Rotate(st1, PI/28, run_time=0.12, rate_func=there_and_back))

        n1 = nar("What is a chip?", size=36, color=INK)
        self.play(Write(n1, run_time=0.78))
        self.wait(5.02)
        self.play(FadeOut(n1, run_time=0.50),
                   FadeOut(st1, run_time=0.50))
        self.wait(0.10)   # clean gap before B2

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  10s → 22s  │  Small but powerful — glow + traces
        #
        # Chip shrinks to working size. Circuit traces extend from edges.
        # ShowPassingFlash runs twice for energy feel.
        # "Tiny but Powerful" panel appears.
        #
        # 0.00–0.70  chip scales down to stage size   0.70s
        # 0.70–1.10  "Tiny but Powerful" panel        0.40s
        # 1.10–1.80  traces draw out                  0.70s
        # 1.80–2.50  electricity flash pass 1         0.70s
        # 2.50–2.72  centre glow burst                0.22s
        # 2.72–3.10  electricity flash pass 2         0.38s
        # 3.10–3.88  narration line 1 writes          0.78s
        # 3.88–5.08  hold                             1.20s  ← readable hold
        # 5.08–5.58  narration cross-fades            0.50s
        # 5.58–9.50  hold                             3.92s
        # 9.50–12.0  clean exit                       2.50s
        # ══════════════════════════════════════════════════════════════
        self.play(chip.animate.scale(1/2.60 * 1.40), run_time=0.70,
                   rate_func=smooth)
        # chip is now at sc≈1.35 — comfortable stage size

        PW2    = 5.2
        tp2    = ink_panel(PW2, 0.72).move_to([0, TOP_Y, 0])
        tt2    = fit_text("Tiny but Powerful", max_width=PW2-0.40, size=32)\
                   .move_to(tp2[1].get_center())
        self.play(GrowFromCenter(tp2, run_time=0.25),
                   Write(tt2, run_time=0.40))

        # Circuit traces from chip edges
        chip_c = chip.get_center()
        trace_data = [
            (chip_c + LEFT*0.96+UP*0.25,    chip_c + LEFT*2.30+UP*0.70),
            (chip_c + LEFT*0.96+DOWN*0.25,  chip_c + LEFT*2.30+DOWN*0.70),
            (chip_c + RIGHT*0.96+UP*0.25,   chip_c + RIGHT*2.30+UP*0.70),
            (chip_c + RIGHT*0.96+DOWN*0.25, chip_c + RIGHT*2.30+DOWN*0.70),
            (chip_c + UP*0.96,              chip_c + UP*2.10),
            (chip_c + DOWN*0.96,            chip_c + DOWN*1.80),
        ]
        traces = VGroup(*[
            Line(a, b, color=GOLD, stroke_width=1.8, stroke_opacity=0.50)
            for a, b in trace_data
        ])
        self.play(Create(traces, run_time=0.70))

        bolts = [make_lightning(a, b, seed=i*7) for i, (a, b) in enumerate(trace_data)]
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 5.0),
                    time_width=0.55, run_time=0.70) for bolt in bolts])

        # Centre glow burst
        glow = Circle(radius=0.18, color=ELECTRIC, fill_color=ELECTRIC,
                       fill_opacity=0.60, stroke_width=0).move_to(chip_c)
        self.add(glow)
        self.play(glow.animate.scale(5.0).set_opacity(0),
                   run_time=0.22, rate_func=smooth)
        self.remove(glow)

        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 3.5),
                    time_width=0.45, run_time=0.38) for bolt in bolts])

        n2a = nar("A tiny piece...")
        n2b = nar("...but incredibly powerful.", color=RED)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(3.92)

        # Clean exit — fade traces + panel + narration, keep chip
        self.play(
            FadeOut(tp2,    run_time=0.60),
            FadeOut(tt2,    run_time=0.60),
            FadeOut(traces, run_time=0.60),
            FadeOut(n2b,    run_time=0.60),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  22s → 36s  │  Inside the chip — transistor flood
        #
        # Chip zooms in (Ken Burns) then cross-fades to transistor grid.
        # Transistor dots flood in with lag. Spinning counter hits 1B.
        # "Billions of Transistors" stamp slams.
        #
        # 0.00–0.70  chip zooms in (Ken Burns)        0.70s
        # 0.70–1.10  chip fades → transistor grid     0.40s
        # 1.10–1.90  grid floods in (lagged dots)     0.80s
        # 1.90–2.18  stamp slams                      0.28s
        # 2.18–2.30  stamp wobble                     0.12s
        # 2.30–4.80  counter spins 0 → 1,000,000,000 2.50s
        # 4.80–5.58  narration writes                 0.78s
        # 5.58–6.78  hold                             1.20s  ← readable
        # 6.78–7.28  narration cross-fades            0.50s
        # 7.28–12.0  hold                             4.72s
        # 12.0–14.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        self.play(chip.animate.scale(1.55), run_time=0.70, rate_func=smooth)
        t_grid = make_transistor_grid(rows=14, cols=20, spacing=0.38)
        self.play(FadeOut(chip, run_time=0.40),
                   FadeIn(t_grid, run_time=0.40))

        # Flood transistors in with stagger
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.4) for t in t_grid],
                         lag_ratio=0.004, run_time=0.80)
        )

        # Stamp
        PW3  = 5.4
        st3  = stamp("Billions of Transistors", color=BLUE, w=PW3, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st3, from_dir=UP, rt=0.28)
        self.play(Rotate(st3, -PI/30, run_time=0.12, rate_func=there_and_back))

        # Spinning counter — right side, doesn't overlap grid too much
        counter_val = ValueTracker(0)
        counter_bg  = ink_panel(4.0, 0.90, fill=CREAM, stroke=BLUE, sw=2.5)\
                        .move_to([0, -1.55, 0])
        self.play(GrowFromCenter(counter_bg, run_time=0.30))

        def counter_label():
            v   = int(counter_val.get_value())
            txt = f"{v:,}"
            return T(txt, size=34, color=BLUE).move_to([0, -1.55, 0])

        counter_lbl = always_redraw(counter_label)
        self.add(counter_lbl)
        self.play(
            counter_val.animate.set_value(1_000_000_000),
            run_time=2.50, rate_func=rush_from,
        )

        n3a = nar("Inside it... are billions of transistors.")
        n3b = nar("One billion switches. In your pocket.", color=RED)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))
        self.wait(4.72)

        # Clean exit
        self.remove(counter_lbl)
        self.play(
            FadeOut(st3,         run_time=0.60),
            FadeOut(counter_bg,  run_time=0.60),
            FadeOut(n3b,         run_time=0.60),
        )
        # Keep t_grid visible going into Beat 4
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  36s → 50s  │  Electricity control — signal paths
        #
        # Signal paths appear over the transistor grid and animate
        # left-to-right (pan-right camera feel via group shift).
        # "Control Electricity" panel. Each path flashes with
        # ShowPassingFlash in sequence.
        #
        # 0.00–0.50  "Control Electricity" panel      0.50s
        # 0.50–1.20  signal paths create              0.70s
        # 1.20–5.20  4 rounds of passing flash        4.00s  (1s each)
        # 5.20–5.98  narration writes                 0.78s
        # 5.98–7.18  hold                             1.20s  ← readable
        # 7.18–7.68  narration cross-fades            0.50s
        # 7.68–12.0  hold                             4.32s
        # 12.0–14.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        PW4  = 5.4
        tp4  = ink_panel(PW4, 0.72).move_to([0, TOP_Y, 0])
        tt4  = fit_text("They Control Electricity", max_width=PW4-0.40, size=30)\
                 .move_to(tp4[1].get_center())
        self.play(GrowFromCenter(tp4, run_time=0.28),
                   Write(tt4, run_time=0.40))

        sig_paths = make_signal_paths(n_paths=6)
        self.play(Create(sig_paths, run_time=0.70))

        # 4 rounds of passing flashes — alternating colors
        for rnd in range(4):
            col    = ELECTRIC if rnd % 2 == 0 else GREEN
            width  = 3.8 if rnd % 2 == 0 else 2.8
            self.play(*[
                ShowPassingFlash(
                    path.copy().set_stroke(col, width),
                    time_width=0.40, run_time=1.00
                )
                for path in sig_paths
            ])

        n4a = nar("These transistors... control electricity.")
        n4b = nar("On. Off. On. Off. Billions of times per second.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))
        self.wait(4.32)

        # Clean exit — fade grid, paths, panel
        self.play(
            FadeOut(t_grid,    run_time=0.70),
            FadeOut(sig_paths, run_time=0.70),
            FadeOut(tp4,       run_time=0.70),
            FadeOut(tt4,       run_time=0.70),
            FadeOut(n4b,       run_time=0.70),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  50s → 60s  │  Real-world impact — phone + AI glow
        #
        # Phone grows from centre. Chip icon appears inside screen.
        # AI node network lights up on the screen surface.
        # "This is Intelligence" stamp. Zoom-out then fade to black.
        #
        # 0.00–0.70  phone grows from centre          0.70s
        # 0.70–1.10  chip icon appears on screen      0.40s
        # 1.10–1.80  AI nodes pulse on screen         0.70s
        # 1.80–2.08  stamp slams                      0.28s
        # 2.08–2.20  stamp wobble                     0.12s
        # 2.20–2.98  narration line 1 writes          0.78s
        # 2.98–4.18  hold                             1.20s  ← readable
        # 4.18–4.68  narration cross-fades            0.50s
        # 4.68–7.00  hold                             2.32s
        # 7.00–7.70  zoom out (scale everything down) 0.70s
        # 7.70–9.20  fade to black overlay            1.50s
        # ══════════════════════════════════════════════════════════════
        phone = make_phone().scale(1.30).move_to([0, STAGE_Y + 0.10, 0])
        self.play(GrowFromCenter(phone, run_time=0.70))

        # Small chip on the screen
        screen_chip = make_chip(sc=0.28)\
                        .move_to(phone[1].get_center() + DOWN*0.10)
        self.play(GrowFromCenter(screen_chip, run_time=0.40))

        # AI glow nodes — small dots pulsing over the screen
        np.random.seed(21)
        sc_rect   = phone[1]  # screen RoundedRectangle
        node_pos  = [
            sc_rect.get_center() + UP*0.52 + LEFT*0.22,
            sc_rect.get_center() + UP*0.52 + RIGHT*0.22,
            sc_rect.get_center() + UP*0.15,
            sc_rect.get_center() + DOWN*0.28 + LEFT*0.28,
            sc_rect.get_center() + DOWN*0.28 + RIGHT*0.28,
        ]
        node_mobs = VGroup(*[
            VGroup(
                Circle(radius=0.06, color=ELECTRIC, fill_color=ELECTRIC,
                        fill_opacity=1, stroke_width=0),
                Circle(radius=0.13, color=ELECTRIC, fill_color=ELECTRIC,
                        fill_opacity=0.22, stroke_width=0),
            ).move_to(p) for p in node_pos
        ])
        # Connection lines between nodes
        node_lines = VGroup(
            Line(node_pos[0], node_pos[2], color=ELECTRIC,
                  stroke_width=1.2, stroke_opacity=0.55),
            Line(node_pos[1], node_pos[2], color=ELECTRIC,
                  stroke_width=1.2, stroke_opacity=0.55),
            Line(node_pos[2], node_pos[3], color=ELECTRIC,
                  stroke_width=1.2, stroke_opacity=0.55),
            Line(node_pos[2], node_pos[4], color=ELECTRIC,
                  stroke_width=1.2, stroke_opacity=0.55),
            Line(node_pos[3], node_pos[4], color=ELECTRIC,
                  stroke_width=1.2, stroke_opacity=0.55),
        )
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in node_mobs],
                         lag_ratio=0.12, run_time=0.45),
            Create(node_lines, run_time=0.50),
        )
        # Pulse nodes
        self.play(
            node_mobs.animate.scale(1.18),
            run_time=0.25, rate_func=there_and_back,
        )

        # Stamp
        PW5  = 5.6
        st5  = stamp("This is Intelligence", color=BLUE, w=PW5, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, PI/32, run_time=0.12, rate_func=there_and_back))

        n5a = nar("And that's what makes your phone smart...")
        n5b = nar("Your AI runs on chips.", size=38, color=RED)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))
        self.wait(2.32)

        # Zoom out — scale all stage objects down together
        stage_group = VGroup(phone, screen_chip, node_mobs, node_lines, st5)
        self.play(
            stage_group.animate.scale(0.72).shift(DOWN * 0.20),
            run_time=0.70, rate_func=smooth,
        )
        self.wait(0.10)

        # Fade to black via overlay
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)