"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 9: Closing  |  50 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 10s │ 10s │ Core idea recap    — chip + network lines
Beat 2 │ 10s → 20s │ 10s │ Power concentrated — world map, lines converge
Beat 3 │ 20s → 28s │  8s │ Taiwan             — gold glow, world dims
Beat 4 │ 28s → 40s │ 12s │ Future uncertain   — flicker + zoom-out
Beat 5 │ 40s → 50s │ 10s │ Final question     — India box + fade to black
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 50s | No character | English only | Style: Oversimplified

KEY VISUAL MOTIF
  This is the recap / closing scene. Each beat callbacks to earlier:
  B1 -> Scene 2 (chip)
  B2 -> Scene 3 (world map + convergence)
  B3 -> Scene 3/5 (Taiwan gold)
  B4 -> Scene 5 (uncertainty)
  B5 -> Scene 7/8 (India opportunity)

LAYOUT ZONES
  TOP_Y   =  3.0
  STAGE_Y =  0.0
  NAR_Y   = -3.10
  TW      = [5.20, 0.30]  — Taiwan world-map position
  INDIA_C = [2.40, -0.55] — India world-map position

Render:
  Preview : manim -pql scene9.py Scene9
  1080p   : manim -pqh scene9.py Scene9
  4K      : manim -pqk scene9.py Scene9
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
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10

TW      = np.array([5.20,  0.30, 0])
INDIA_C = np.array([2.40, -0.55, 0])


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


def make_network_lines(centre=ORIGIN, n=10):
    """
    Radial lines from a centre point outward — represent network/AI connections.
    Lengths vary for organic feel.
    """
    np.random.seed(3)
    lines = VGroup()
    for a in np.linspace(0, TAU, n, endpoint=False):
        length = np.random.uniform(1.40, 2.80)
        start  = centre + 0.75*np.array([np.cos(a), np.sin(a), 0])
        end    = centre + length*np.array([np.cos(a), np.sin(a), 0])
        lines.add(Line(start, end, color=ELECTRIC,
                        stroke_width=1.5, stroke_opacity=0.55))
    return lines


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
    return VGroup(*[Dot([x,y,0], radius=0.028, color=BLUE, fill_opacity=0.38)
                    for x,y in pts])


def make_convergence_arcs(target=TW):
    """
    6 arcs from spread world positions converging toward Taiwan — 
    visualises global power concentrated in one point.
    """
    sources = [
        np.array([-5.20,  1.80, 0]),
        np.array([-3.80, -0.60, 0]),
        np.array([-1.00,  2.20, 0]),
        np.array([ 0.60,  1.60, 0]),
        np.array([ 0.80, -0.80, 0]),
        np.array([ 3.20,  2.00, 0]),
    ]
    arcs = VGroup()
    for i, src in enumerate(sources):
        angle = -0.55 if src[0] < target[0] else 0.55
        arc   = ArcBetweenPoints(
            src, target + LEFT*0.20,
            angle=angle, color=GOLD,
            stroke_width=1.8, stroke_opacity=0.65
        ).add_tip(tip_length=0.18)
        arcs.add(arc)
    return arcs


def make_taiwan_marker():
    dot   = Dot(TW, radius=0.16, color=GOLD, fill_opacity=1)
    rings = VGroup(*[
        Circle(radius=r, color=GOLD,
                stroke_opacity=0.60-i*0.18, stroke_width=2.5).move_to(TW)
        for i, r in enumerate([0.16, 0.30, 0.50])
    ])
    return dot, rings


def make_india_box():
    box = RoundedRectangle(corner_radius=0.15, width=1.60, height=1.90,
                            color=ORANGE, fill_color=INDIA_FILL,
                            fill_opacity=0.80, stroke_width=3.0)\
            .move_to(INDIA_C)
    lbl = T("India", size=24, color=ORANGE).move_to(INDIA_C)
    return VGroup(box, lbl)


def make_india_glow_rings():
    return VGroup(*[
        Circle(radius=r, color=GREEN_COL,
                stroke_opacity=0.52-i*0.15, stroke_width=2.0)\
          .move_to(INDIA_C)
        for i, r in enumerate([1.10, 1.40, 1.75])
    ])


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
class Scene9(Scene):
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
        # BEAT 1  │  0s → 10s  │  Core idea recap
        #
        # Chip fades in centre. Network lines radiate outward.
        # ShowPassingFlash on traces. "Everything Starts with Chips" panel.
        # Ken Burns zoom-in.
        #
        # 0.00–0.70  chip fades in                   0.70s
        # 0.70–1.40  chip scales up (Ken Burns)      0.70s
        # 1.40–2.10  network lines create (lagged)   0.70s
        # 2.10–2.80  passing flash on traces         0.70s
        # 2.80–3.08  top panel slams                 0.28s
        # 3.08–3.86  narration writes                0.78s
        # 3.86–5.06  hold                            1.20s
        # 5.06–5.56  narration cross-fades           0.50s
        # 5.56–8.56  hold                            3.00s
        # 8.56–10.0  clean exit (chip + lines stay)  1.44s
        # ══════════════════════════════════════════════════════════════
        chip = make_chip(sc=1.0).scale(0.70).move_to(ORIGIN)
        self.play(FadeIn(chip, run_time=0.70))
        self.play(chip.animate.scale(1.55), run_time=0.70, rate_func=smooth)

        net_lines = make_network_lines(centre=ORIGIN, n=10)
        self.play(LaggedStart(*[Create(ln) for ln in net_lines],
                               lag_ratio=0.07, run_time=0.70))

        # Passing flash on network lines
        self.play(*[
            ShowPassingFlash(ln.copy().set_stroke(ELECTRIC, 3.5),
                              time_width=0.50, run_time=0.70)
            for ln in net_lines
        ])

        PW1 = 5.8
        tp1 = ink_panel(PW1, 0.72).move_to([0, TOP_Y, 0])
        tt1 = fit_text("Everything Starts with Chips",
                        max_width=PW1-0.40, size=28)\
                .move_to(tp1[1].get_center())
        slam(self, tp1, from_dir=UP, rt=0.28)
        self.add(tt1)
        self.play(FadeIn(tt1, run_time=0.18))

        n1a = nar("In the world of AI... everything begins with chips.")
        n1b = nar("Every device. Every model. Every breakthrough.", color=GOLD)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))
        self.wait(3.00)

        self.play(
            FadeOut(tp1,       run_time=0.50),
            FadeOut(tt1,       run_time=0.50),
            FadeOut(n1b,       run_time=0.50),
            FadeOut(net_lines, run_time=0.50),
            FadeOut(chip,      run_time=0.50),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  10s → 20s  │  Power concentrated
        #
        # World map appears. 6 convergence arcs draw toward Taiwan point.
        # "Power Concentrated" panel. Slow pan-right.
        #
        # 0.00–0.40  map bg fades in                 0.40s
        # 0.40–1.70  world dots appear               1.30s
        # 1.70–2.40  convergence arcs draw (lagged)  0.70s
        # 2.40–2.68  top panel slams                 0.28s
        # 2.68–3.46  narration writes                0.78s
        # 3.46–4.66  hold                            1.20s
        # 4.66–5.16  narration cross-fades           0.50s
        # 5.16–8.16  hold + slow pan-right           3.00s
        # 8.16–10.0  clean exit (world + arcs stay)  1.84s
        # ══════════════════════════════════════════════════════════════
        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.26, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.003, run_time=1.30))

        conv_arcs = make_convergence_arcs(target=TW)
        self.play(LaggedStart(*[Create(a) for a in conv_arcs],
                               lag_ratio=0.12, run_time=0.70))

        PW2 = 5.2
        tp2 = ink_panel(PW2, 0.72).move_to([0, TOP_Y, 0])
        tt2 = fit_text("Power Concentrated", max_width=PW2-0.40, size=30)\
                .move_to(tp2[1].get_center())
        slam(self, tp2, from_dir=UP, rt=0.28)
        self.add(tt2)
        self.play(FadeIn(tt2, run_time=0.18))

        n2a = nar("And right now... that power is concentrated in one place.")
        n2b = nar("One island. One chokepoint.", color=RED)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))

        # Slow pan-right (shift left)
        self.play(
            world.animate.shift(LEFT*0.30),
            map_bg.animate.shift(LEFT*0.30),
            conv_arcs.animate.shift(LEFT*0.30),
            run_time=3.00, rate_func=smooth,
        )

        self.play(
            FadeOut(tp2, run_time=0.50),
            FadeOut(tt2, run_time=0.50),
            FadeOut(n2b, run_time=0.50),
        )
        # Keep: world, map_bg, conv_arcs
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  20s → 28s  │  Taiwan
        #
        # World + arcs dim. Taiwan dot appears GOLD + rings pulse.
        # "TAIWAN" large stamp in gold. Zoom-in on Taiwan.
        # Short beat — single punchy narration line.
        #
        # 0.00–0.50  world dims + arcs fade          0.50s
        # 0.50–1.35  Taiwan dot + rings              0.85s
        # 1.35–1.63  TAIWAN stamp slams              0.28s
        # 1.63–1.75  stamp wobble                    0.12s
        # 1.75–2.53  narration writes                0.78s
        # 2.53–5.03  hold                            2.50s
        # 5.03–6.53  zoom-in on Taiwan              1.50s
        # 6.53–8.00  hold                            1.47s
        # ══════════════════════════════════════════════════════════════
        self.play(
            world.animate.set_opacity(0.12),
            map_bg.animate.set_fill(opacity=0.10),
            conv_arcs.animate.set_opacity(0.20),
            run_time=0.50,
        )

        dot_tw, tw_rings = make_taiwan_marker()
        self.play(
            FadeIn(dot_tw, scale=0.2, run_time=0.50),
            LaggedStart(*[GrowFromCenter(r) for r in tw_rings],
                         lag_ratio=0.22, run_time=0.85),
        )

        PW3 = 4.2
        st3 = stamp("TAIWAN", color=GOLD, w=PW3, h=0.88)\
                .move_to([0, TOP_Y, 0])
        slam(self, st3, from_dir=UP, rt=0.28)
        self.play(Rotate(st3, PI/28, run_time=0.12, rate_func=there_and_back))

        n3 = nar("Taiwan.", size=48, color=GOLD)
        self.play(Write(n3, run_time=0.78))
        self.wait(2.50)

        # Zoom-in toward Taiwan
        self.play(
            world.animate.scale(1.15).shift(LEFT*0.80+DOWN*0.15),
            map_bg.animate.scale(1.15).shift(LEFT*0.80+DOWN*0.15),
            dot_tw.animate.scale(1.20),
            tw_rings.animate.scale(1.20),
            run_time=1.50, rate_func=smooth,
        )
        # Fade n3 and st3 BEFORE Beat 4 builds — prevents overlap
        self.play(
            FadeOut(n3,  run_time=0.40),
            FadeOut(st3, run_time=0.40),
        )
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  28s → 40s  │  Future uncertain
        #
        # Taiwan dot flickers (glitch). World fades back in partially.
        # "?" gold stamp slams. Zoom-out.
        #
        # 0.00–0.60  Taiwan dot flickers             0.60s  (6 steps)
        # 0.60–0.90  world fades back partially      0.30s
        # 0.90–1.18  "?" stamp slams                 0.28s
        # 1.18–1.30  stamp wobble                    0.12s
        # 1.30–2.08  narration writes                0.78s
        # 2.08–3.28  hold                            1.20s
        # 3.28–3.78  narration cross-fades           0.50s
        # 3.78–4.48  zoom-out                        0.70s
        # 4.48–10.0  hold                            5.52s
        # 10.0–12.0  clean exit                      2.00s
        # ══════════════════════════════════════════════════════════════
        # Taiwan flicker
        for op in [0.40, 0.90, 0.20, 0.80, 0.15, 1.00]:
            self.play(dot_tw.animate.set_opacity(op),
                       tw_rings.animate.set_stroke(opacity=op*0.60),
                       run_time=0.10, rate_func=linear)

        self.play(
            world.animate.set_opacity(0.25),
            map_bg.animate.set_fill(opacity=0.18),
            run_time=0.30,
        )

        PW4 = 2.2
        st4 = stamp("?", color=GOLD, w=PW4, h=0.88)\
                .move_to([-3.20, TOP_Y, 0])
        slam(self, st4, from_dir=UP, rt=0.28)
        self.play(Rotate(st4, -PI/22, run_time=0.12, rate_func=there_and_back))

        n4a = nar("But the future... is still uncertain.")
        n4b = nar("The balance of power can shift.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))

        # Zoom-out
        b4_stage = VGroup(world, map_bg, dot_tw, tw_rings, conv_arcs)
        self.play(b4_stage.animate.scale(0.88).shift(UP*0.10),
                   run_time=0.70, rate_func=smooth)
        self.wait(5.52)

        self.play(
            FadeOut(st4,       run_time=0.55),
            FadeOut(conv_arcs, run_time=0.55),
            FadeOut(n4b,       run_time=0.55),
        )
        # Keep: world, map_bg, dot_tw (dim), tw_rings (dim)
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  40s → 50s  │  Final question
        #
        # India box appears on map. Green glow rings pulse softly.
        # "?" green stamp slams. "Can India Rise?" panel.
        # Electric pulse lines from India outward.
        # Final zoom-in. Fade to black.
        #
        # 0.00–0.55  India box grows                 0.55s
        # 0.55–1.40  green glow rings appear         0.85s
        # 1.40–1.68  "?" green stamp slams           0.28s
        # 1.68–1.80  stamp wobble                    0.12s
        # 1.80–2.10  "Can India Rise?" panel         0.30s
        # 2.10–2.88  narration writes                0.78s
        # 2.88–4.08  hold                            1.20s
        # 4.08–4.58  narration cross-fades           0.50s
        # 4.58–5.08  zoom-in on India                0.50s
        # 5.08–7.08  hold                            2.00s
        # 7.08–8.58  fade to black                   1.50s
        # ══════════════════════════════════════════════════════════════
        india      = make_india_box()
        india_glow = make_india_glow_rings()

        self.play(GrowFromCenter(india, run_time=0.55))
        self.play(LaggedStart(*[GrowFromCenter(r) for r in india_glow],
                               lag_ratio=0.22, run_time=0.85))

        PW5a = 2.2
        st5  = stamp("?", color=GREEN_COL, w=PW5a, h=0.88)\
                 .move_to([-3.50, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, PI/22, run_time=0.12, rate_func=there_and_back))

        PW5b = 4.6
        tp5  = ink_panel(PW5b, 0.72, fill="#E8FFE8", stroke=GREEN_COL, sw=2.5)\
                 .move_to([1.80, TOP_Y, 0])
        tt5  = fit_text("Can India Rise?", max_width=PW5b-0.40, size=30,
                         color=GREEN_COL)\
                 .move_to(tp5[1].get_center())
        self.play(GrowFromCenter(tp5, run_time=0.18),
                   Write(tt5, run_time=0.25))

        n5a = nar("The real question is... can India rise in this race?")
        n5b = nar("The answer will shape the future.", color=GREEN_COL)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))

        # Zoom-in toward India
        self.play(
            india.animate.scale(1.15),
            india_glow.animate.scale(1.15),
            run_time=0.50, rate_func=smooth,
        )
        self.wait(2.00)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)