"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 10: Next Hook  |  20 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s →  5s │  5s │ Next episode intro  — text fades in dark BG
Beat 2 │  5s → 10s │  5s │ Core question       — "The Big Question" glows
Beat 3 │ 10s → 15s │  5s │ Capability doubt    — India box + chip + "?" stamp
Beat 4 │ 15s → 20s │  5s │ Cost of failure     — world dims, RISK stamp, fade
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 20s | No character | English only | Oversimplified

DESIGN INTENT
  Short punchy teaser — each beat is exactly 5 seconds.
  Dark parchment feel that gets progressively dimmer.
  Minimal objects — text and stamps carry the weight.
  No wasted frames — every second has a clear action.

Render:
  Preview : manim -pql scene10.py Scene10
  1080p   : manim -pqh scene10.py Scene10
  4K      : manim -pqk scene10.py Scene10
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────
BG        = "#F5F0E8"
INK       = "#1A1008"
RED       = "#D42B2B"
BLUE      = "#2255AA"
GOLD      = "#C8960C"
CREAM     = "#FFFDF8"
MAP_GREEN = "#C8D8B0"
SUBTLE    = "#9A8F7E"
WHITE     = "#FFFFFF"
ORANGE    = "#E07820"
INDIA_FILL= "#FFD080"
GREEN_COL = "#1A8A2A"
ELECTRIC  = "#00C8FF"
DARK_BG   = "#1A1A2A"
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10

INDIA_C = np.array([0.0, -0.30, 0])   # India box centred slightly below stage


# ─────────────────────────────────────────────────────────────
# TEXT HELPERS
# ─────────────────────────────────────────────────────────────
def T(text, size=34, color=INK, weight=BOLD):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)

def Ts(text, size=22, color=SUBTLE):
    return Text(text, font=FONT, font_size=size, color=color, weight=NORMAL)

def nar(text, size=32, color=INK):
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
        Line([v*sc,-0.45*sc,0],[v*sc,0.45*sc,0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30,0.30,4)
    ] + [
        Line([-0.45*sc,v*sc,0],[0.45*sc,v*sc,0],
              color=GOLD, stroke_width=0.7, stroke_opacity=0.50)
        for v in np.linspace(-0.30,0.30,4)
    ])
    core = Square(side_length=0.26*sc, color=RED, fill_color=RED,
                   fill_opacity=1, stroke_width=0)
    pins = VGroup(*[
        Rectangle(width=0.08*sc, height=0.20*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([-0.48*sc+i*0.24*sc, sg*0.80*sc, 0])
        for i in range(5) for sg in [1,-1]
    ] + [
        Rectangle(width=0.20*sc, height=0.08*sc, color=GOLD,
                    fill_color=GOLD, fill_opacity=1, stroke_width=0)
        .move_to([sg*0.80*sc,-0.48*sc+i*0.24*sc, 0])
        for i in range(5) for sg in [1,-1]
    ])
    return VGroup(base, pins, die, grid, core)


def make_india_box():
    box = RoundedRectangle(corner_radius=0.16, width=2.00, height=2.40,
                            color=ORANGE, fill_color=INDIA_FILL,
                            fill_opacity=0.55, stroke_width=3.0)\
            .move_to(INDIA_C)
    lbl = T("India", size=28, color=ORANGE).move_to(INDIA_C)
    return VGroup(box, lbl)


def make_chip_traces(centre):
    """Short circuit traces from chip edges."""
    data = [
        (centre+LEFT*0.76+UP*0.22,   centre+LEFT*1.80+UP*0.60),
        (centre+LEFT*0.76+DOWN*0.22, centre+LEFT*1.80+DOWN*0.60),
        (centre+RIGHT*0.76+UP*0.22,  centre+RIGHT*1.80+UP*0.60),
        (centre+RIGHT*0.76+DOWN*0.22,centre+RIGHT*1.80+DOWN*0.60),
        (centre+UP*0.76,             centre+UP*1.70),
    ]
    return VGroup(*[
        Line(a, b, color=GOLD, stroke_width=1.6, stroke_opacity=0.55)
        for a, b in data
    ]), data


def make_world_dots():
    np.random.seed(42)
    pts = []
    for _ in range(90):  pts.append((np.random.uniform(-6.5,-3.2), np.random.uniform(0.3, 2.5)))
    for _ in range(55):  pts.append((np.random.uniform(-5.3,-3.6), np.random.uniform(-2.5,0.2)))
    for _ in range(55):  pts.append((np.random.uniform(-0.7, 1.7), np.random.uniform(1.1, 2.6)))
    for _ in range(70):  pts.append((np.random.uniform(-0.4, 2.0), np.random.uniform(-2.3,1.0)))
    for _ in range(155): pts.append((np.random.uniform( 2.0, 6.6), np.random.uniform(-0.3,2.8)))
    for _ in range(40):  pts.append((np.random.uniform( 4.2, 6.3), np.random.uniform(-2.8,-0.5)))
    np.random.shuffle(pts)
    return VGroup(*[Dot([x,y,0], radius=0.028, color=BLUE, fill_opacity=0.28)
                    for x,y in pts])


def make_lightning(start, end, steps=8, seed=0):
    np.random.seed(seed)
    pts = [np.array(start)]
    for i in range(1, steps):
        t    = i/steps
        mid  = np.array(start)*(1-t)+np.array(end)*t
        d    = np.array(end)-np.array(start)
        perp = np.array([-d[1],d[0],0])
        n    = np.linalg.norm(perp)
        if n>1e-4: perp/=n
        pts.append(mid+perp*(np.random.rand()-0.5)*0.26)
    pts.append(np.array(end))
    bolt = VMobject(stroke_color=ELECTRIC, stroke_width=3.8, stroke_opacity=0.95)
    bolt.set_points_as_corners(pts)
    return bolt


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene10(Scene):
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

        # Dark tension overlay — starts light, deepens by Beat 4
        tension = Rectangle(width=15.5, height=9.5,
                              fill_color=DARK_BG, fill_opacity=0.10,
                              stroke_width=0).move_to(ORIGIN)
        self.add(tension)

        # ══════════════════════════════════════════════════════════════
        # BEAT 1  │  0s → 5s  │  Next episode intro
        #
        # "Next Episode" large panel fades in centre.
        # Sub-label below. Narration writes. Slight zoom-in.
        #
        # 0.00–0.50  "Next Episode" panel fades in   0.50s
        # 0.50–1.28  narration writes                0.78s
        # 1.28–2.48  hold                            1.20s
        # 2.48–2.98  narration cross-fades           0.50s
        # 2.98–5.00  hold + slight scale up          2.02s
        # ══════════════════════════════════════════════════════════════
        PW1  = 6.2
        tp1  = ink_panel(PW1, 1.10).move_to([0, 0.60, 0])
        tt1a = fit_text("Next Episode", max_width=PW1-0.40, size=44)\
                 .move_to(tp1[1].get_center() + UP*0.18)
        tt1b = Ts("Coming up...", size=24, color=SUBTLE)\
                 .move_to(tp1[1].get_center() + DOWN*0.22)
        self.play(
            GrowFromCenter(tp1,  run_time=0.30),
            FadeIn(tt1a,         run_time=0.35),
            FadeIn(tt1b,         run_time=0.35),
        )

        n1a = nar("In the next episode...")
        n1b = nar("We go deeper.", color=GOLD)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))

        # Slight Ken Burns scale up
        self.play(tp1.animate.scale(1.06),
                   tt1a.animate.scale(1.06),
                   tt1b.animate.scale(1.06),
                   run_time=2.02, rate_func=smooth)

        # ── B1 exit — keep tp1 + text visible, just fade narration
        self.play(FadeOut(n1b, run_time=0.25))
        self.wait(0.05)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  5s → 10s  │  Core question
        #
        # "Next Episode" panel shifts up. "The Big Question" panel
        # grows below it with a gold border glow.
        # Electric pulse lines radiate briefly.
        #
        # 0.00–0.40  tp1 slides up to TOP_Y            0.40s
        # 0.40–0.75  "The Big Question" panel grows    0.35s
        # 0.75–1.53  narration writes                  0.78s
        # 1.53–2.73  hold                              1.20s
        # 2.73–3.23  narration cross-fades             0.50s
        # 3.23–5.00  hold                              1.77s
        # ══════════════════════════════════════════════════════════════
        self.play(
            tp1.animate.move_to([0, TOP_Y, 0]),
            tt1a.animate.move_to([0, TOP_Y, 0]),
            tt1b.animate.move_to([0, TOP_Y + 0.22, 0]),
            run_time=0.40, rate_func=smooth,
        )
        # Reposition text properly inside panel
        tt1a.move_to(tp1[1].get_center())
        tt1b.set_opacity(0)   # hide sub-label now it's in the top bar

        PW2  = 5.8
        tp2  = ink_panel(PW2, 0.90, fill="#FFFBE6", stroke=GOLD, sw=3.5)\
                 .move_to([0, 2.00, 0])
        tt2  = fit_text("The Big Question", max_width=PW2-0.40, size=38, color=GOLD)\
                 .move_to(tp2[1].get_center())

        self.play(GrowFromCenter(tp2, run_time=0.22),
                   Write(tt2, run_time=0.30))

        # Subtle gold glow pulse on panel border
        self.play(tp2[1].animate.set_stroke(color=GOLD, width=5.5),
                   run_time=0.20, rate_func=there_and_back)

        n2a = nar("We'll explore the question...")
        n2b = nar("That decides India's future.", color=GOLD)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(1.77)

        self.play(FadeOut(n2b, run_time=0.25))
        self.wait(0.05)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │   10s → 15s  │  Capability doubt
        #
        # "The Big Question" panel stays. India box fades in.
        # Chip appears on India box. Chip traces flash.
        # "?" gold stamp slams RIGHT side.
        # "Can India Build Chips?" narration.
        #
        # 0.00–0.40  India box fades in               0.40s
        # 0.40–0.75  chip grows on India box          0.35s
        # 0.75–1.10  chip traces appear               0.35s
        # 1.10–1.45  passing flash on traces          0.35s
        # 1.45–1.73  "?" stamp slams right            0.28s
        # 1.73–2.51  narration writes                 0.78s
        # 2.51–3.71  hold                             1.20s
        # 3.71–4.21  narration cross-fades            0.50s
        # 4.21–5.00  hold                             0.79s
        # ══════════════════════════════════════════════════════════════
        # India box on LEFT side — clear of tp2 (y=2.00) and chip (right side)
        india = make_india_box()
        india.move_to([-3.20, -0.10, 0])
        self.play(FadeIn(india, run_time=0.40))

        # Chip on RIGHT side — mirrors India box on left
        chip_pos = np.array([3.20, -0.10, 0])
        chip = make_chip(sc=0.55).move_to(chip_pos)
        self.play(GrowFromCenter(chip, run_time=0.35))

        traces, trace_data = make_chip_traces(chip_pos)
        self.play(Create(traces, run_time=0.35))

        bolts = [make_lightning(a, b, seed=i*7) for i,(a,b) in enumerate(trace_data)]
        self.play(*[ShowPassingFlash(bolt.copy().set_stroke(ELECTRIC, 4.0),
                    time_width=0.50, run_time=0.35) for bolt in bolts])

        PW3 = 2.2
        st3 = stamp("?", color=GOLD, w=PW3, h=0.88)\
                .move_to([5.20, 2.00, 0])   # right of tp2, same row
        slam(self, st3, from_dir=RIGHT, rt=0.28)
        self.play(Rotate(st3, PI/24, run_time=0.10, rate_func=there_and_back))

        n3a = nar("Can India build its own chips?")
        n3b = nar("The answer will change everything.", color=GOLD)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))
        self.wait(0.79)

        self.play(FadeOut(n3b, run_time=0.25))
        self.wait(0.05)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  15s → 20s  │  Cost of failure
        #
        # World dots appear dim. Tension darkens.
        # "RISK" red stamp slams LEFT side.
        # India box + chip flicker (glitch).
        # "What's the Cost?" narration. Zoom-out. Fade to black.
        #
        # 0.00–0.35  world dots fade in (dim)          0.35s
        # 0.35–0.55  tension overlay deepens           0.20s
        # 0.55–0.83  RISK stamp slams left             0.28s
        # 0.83–0.95  stamp wobble                      0.12s
        # 0.95–1.73  narration writes                  0.78s
        # 1.73–2.93  hold                              1.20s
        # 2.93–3.43  narration cross-fades             0.50s
        # 3.43–3.87  india + chip flicker              0.44s
        # 3.87–4.57  zoom-out (scale down)             0.70s
        # 4.57–5.07  wait before overlay               0.50s — cut short by fade
        # Then fade to black: overlay animates over ~1.50s (extends past 20s slightly)
        # ══════════════════════════════════════════════════════════════
        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.002, run_time=0.35))

        self.play(tension.animate.set_fill(opacity=0.38), run_time=0.20)

        PW4 = 3.0
        st4 = stamp("RISK", color=RED, w=PW4, h=0.82)\
                .move_to([-5.20, 2.00, 0])   # left of tp2, same row
        slam(self, st4, from_dir=LEFT, rt=0.28)
        self.play(Rotate(st4, -PI/26, run_time=0.12, rate_func=there_and_back))

        n4a = nar("And if not... what will it cost?")
        n4b = nar("This is the question India must answer.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))

        # Glitch india + chip, then fade them out — Beat 4 is world + RISK only
        glitch_grp = VGroup(india, chip, traces)
        for dx, op in [(0.08,0.45),(-0.16,0.85),(0.08,0.25),
                        (-0.09,0.70),(0.10,0.15),(-0.07,0.00)]:
            self.play(glitch_grp.animate.shift(RIGHT*dx).set_opacity(op),
                       run_time=0.07, rate_func=linear)
        # Also clear Beat 3 panels and "?" stamp — only world + RISK remain
        self.play(
            FadeOut(tp2,  run_time=0.25),
            FadeOut(tt2,  run_time=0.25),
            FadeOut(st3,  run_time=0.25),
            FadeOut(tp1,  run_time=0.25),
            FadeOut(tt1a, run_time=0.25),
        )

        # Zoom-out — only world dots + RISK stamp remain on screen
        all_stage = VGroup(world, st4)
        self.play(all_stage.animate.scale(0.85).shift(DOWN*0.10),
                   run_time=0.70, rate_func=smooth)

        self.wait(0.30)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.30)