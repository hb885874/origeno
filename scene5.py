"""
Origeno — "Why Taiwan Controls the World's Chips | AI War Explained"
Scene 5: The Risk: What If Taiwan Stops?  |  60 seconds  |  Oversimplified style

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEAT MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beat 1 │  0s → 10s │ 10s │ Hypothetical setup — dark world map, "What if?"
Beat 2 │ 10s → 22s │ 12s │ Supply shock       — Taiwan cut, lines glitch
Beat 3 │ 22s → 38s │ 16s │ Systems failing    — phone/car glitch out
Beat 4 │ 38s → 50s │ 12s │ Industry collapse  — factory flood + glitch
Beat 5 │ 50s → 60s │ 10s │ Global crisis      — world dims to near-black
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 60s | No character | English only | Style: Oversimplified

VISUAL LANGUAGE
  - Background shifts from warm parchment to darker tint as tension builds.
  - Glitch = rapid left/right position jitter + opacity flicker sequence.
  - Red X marks appear over failing icons.
  - World map progressively dims beat by beat.

LAYOUT ZONES
  TOP_Y   =  3.0   stamps / title panels
  STAGE_Y =  0.0   main stage
  NAR_Y   = -3.10  narration strip

Render:
  Preview : manim -pql scene5.py Scene5
  1080p   : manim -pqh scene5.py Scene5
  4K      : manim -pqk scene5.py Scene5
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
ELECTRIC  = "#00C8FF"
DARK_BG   = "#1A1A2A"   # near-black overlay for crisis feel
FONT      = "Georgia"

TOP_Y   =  3.0
STAGE_Y =  0.0
NAR_Y   = -3.10

TW = np.array([5.20, 0.30, 0])   # Taiwan map position


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

def red_x(size=0.55):
    """Bold red X mark drawn from two crossing lines."""
    s = size / 2
    l1 = Line([-s, -s, 0], [s, s, 0], color=RED, stroke_width=8)
    l2 = Line([-s,  s, 0], [s,-s, 0], color=RED, stroke_width=8)
    return VGroup(l1, l2)

def glitch(scene, mob, times=4, dx=0.09, total_t=0.44):
    """
    Rapid jitter + opacity flicker on a single mobject.
    Simulates a digital glitch effect.
    """
    step = total_t / (times * 3)
    ops  = [0.55, 0.90, 0.25, 0.70, 0.15, 0.80, 0.10, 0.60, 0.05, 0.40, 0.02, 0.20]
    dxs  = [dx, -dx*1.8, dx*0.9, -dx*0.6, dx*1.4, -dx*0.4,
             dx*0.7, -dx*1.2, dx*0.5, -dx*0.8, dx*0.3, -dx*0.3]
    for i in range(min(times*3, len(ops))):
        scene.play(
            mob.animate.shift(RIGHT * dxs[i]).set_opacity(ops[i]),
            run_time=step, rate_func=linear
        )


# ─────────────────────────────────────────────────────────────
# PROP BUILDERS
# ─────────────────────────────────────────────────────────────
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

def make_phone():
    body   = RoundedRectangle(corner_radius=0.14, width=0.85, height=1.42,
                               color=INK, fill_color="#2C3E50",
                               fill_opacity=1, stroke_width=3)
    screen = RoundedRectangle(corner_radius=0.08, width=0.65, height=1.05,
                               color="#D6EAF8", fill_color="#D6EAF8",
                               fill_opacity=1, stroke_width=1.5)
    notch  = Rectangle(width=0.22, height=0.07, color=INK,
                        fill_color=INK, fill_opacity=1,
                        stroke_width=0).next_to(screen, UP, buff=0.04)
    btn    = Circle(radius=0.07, color="#888", fill_color="#888",
                     fill_opacity=1, stroke_width=0)\
               .next_to(body, DOWN, buff=-0.17)
    return VGroup(body, screen, notch, btn)

def make_car():
    body = RoundedRectangle(corner_radius=0.20, width=1.95, height=0.63,
                             color=INK, fill_color="#2C3E50",
                             fill_opacity=1, stroke_width=3)
    roof = RoundedRectangle(corner_radius=0.16, width=1.08, height=0.44,
                             color=INK, fill_color="#2C3E50",
                             fill_opacity=1, stroke_width=3)\
             .next_to(body, UP, buff=-0.17)
    wl   = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.28,
                             color="#D6EAF8", fill_color="#D6EAF8",
                             fill_opacity=1, stroke_width=1.5)\
             .move_to(roof.get_center() + LEFT*0.27 + UP*0.03)
    wr   = wl.copy().shift(RIGHT*0.42)
    tl   = Circle(radius=0.22, color=INK, fill_color="#555",
                   fill_opacity=1, stroke_width=3)\
             .move_to(body.get_bottom() + LEFT*0.62)
    tr   = tl.copy().move_to(body.get_bottom() + RIGHT*0.62)
    hl   = Circle(radius=0.09, color=WHITE, fill_color=WHITE,
                   fill_opacity=1, stroke_width=0).move_to(tl.get_center())
    hr   = hl.copy().move_to(tr.get_center())
    return VGroup(body, roof, wl, wr, tl, tr, hl, hr)

def make_small_factory(pos=ORIGIN):
    """Compact factory silhouette for the flood in Beat 4."""
    body  = Rectangle(width=1.10, height=0.90, color=INK,
                        fill_color="#1E2A3A", fill_opacity=1, stroke_width=2.5)\
              .move_to(pos)
    chim1 = Rectangle(width=0.18, height=0.40, color=INK,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=2)\
              .move_to(pos + UP*0.65 + LEFT*0.25)
    chim2 = Rectangle(width=0.14, height=0.30, color=INK,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=2)\
              .move_to(pos + UP*0.55 + RIGHT*0.20)
    base  = Rectangle(width=1.30, height=0.16, color=INK,
                        fill_color="#0E161E", fill_opacity=1, stroke_width=1.5)\
              .move_to(pos + DOWN*0.53)
    win   = Rectangle(width=0.28, height=0.22, color=ELECTRIC,
                        fill_color=ELECTRIC, fill_opacity=0.20,
                        stroke_width=1.5).move_to(pos)
    return VGroup(base, body, chim1, chim2, win)

# Factory scatter positions across map (left half — away from Taiwan dot at x=5.2)
FACTORY_POSITIONS = [
    np.array([-5.20,  1.40, 0]),
    np.array([-3.80, -0.60, 0]),
    np.array([-2.20,  2.00, 0]),
    np.array([ 0.20,  1.60, 0]),
    np.array([ 0.80, -0.80, 0]),
    np.array([ 2.40,  2.20, 0]),
    np.array([ 2.80, -0.40, 0]),
    np.array([ 3.60,  1.20, 0]),
]

def make_supply_lines():
    """
    Radial lines from Taiwan to various world points —
    representing chip supply routes.
    """
    endpoints = [
        np.array([-5.00,  1.50, 0]),
        np.array([-3.50, -0.50, 0]),
        np.array([-1.80,  2.10, 0]),
        np.array([ 0.50,  1.80, 0]),
        np.array([ 1.20, -0.60, 0]),
        np.array([ 3.20,  2.00, 0]),
    ]
    lines = VGroup(*[
        Line(TW, ep, color=GOLD,
              stroke_width=1.8, stroke_opacity=0.65)
        for ep in endpoints
    ])
    return lines


# ═════════════════════════════════════════════════════════════
# MAIN SCENE
# ═════════════════════════════════════════════════════════════
class Scene5(Scene):
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

        # Dark tension overlay — starts transparent, deepens each beat
        tension = Rectangle(width=15.5, height=9.5,
                              fill_color=DARK_BG, fill_opacity=0,
                              stroke_width=0).move_to(ORIGIN)
        self.add(tension)

        # ══════════════════════════════════════════════════════════════
        # BEAT 1  │  0s → 10s  │  Hypothetical setup
        #
        # Map fades in dim. Tension overlay adds slight dark tint.
        # "What if?" ink panel. Slow zoom-in Ken Burns on map.
        #
        # 0.00–0.40  map bg fades in                 0.40s
        # 0.40–1.70  world dots appear (lagged)      1.30s
        # 1.70–1.98  tension overlay darkens         0.28s
        # 1.98–2.26  "What if?" panel slams          0.28s
        # 2.26–3.04  narration writes                0.78s
        # 3.04–4.24  hold                            1.20s
        # 4.24–4.74  narration cross-fades           0.50s
        # 4.74–8.00  hold + slow zoom                3.26s
        # 8.00–10.0  clean exit (panel only)         2.00s
        # ══════════════════════════════════════════════════════════════
        map_bg = Rectangle(width=15.5, height=9.5, fill_color=MAP_GREEN,
                             fill_opacity=0.24, stroke_width=0).move_to(ORIGIN)
        self.play(FadeIn(map_bg, run_time=0.40))

        world = make_world_dots()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in world],
                               lag_ratio=0.003, run_time=1.30))

        # Slight tension tint
        self.play(tension.animate.set_fill(opacity=0.18), run_time=0.28)

        PW1  = 3.8
        st1  = stamp("What if?", color=RED, w=PW1, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st1, from_dir=UP, rt=0.28)

        n1a = nar("Now imagine...")
        n1b = nar("What if Taiwan's chip supply suddenly stops?", color=RED)
        self.play(Write(n1a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n1a, run_time=0.25), FadeIn(n1b, run_time=0.25))

        # Slow Ken Burns zoom-in on world
        self.play(
            world.animate.scale(1.10).shift(LEFT*0.30),
            map_bg.animate.scale(1.10).shift(LEFT*0.30),
            run_time=3.26, rate_func=smooth,
        )

        self.play(FadeOut(st1, run_time=0.55),
                   FadeOut(n1b, run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 2  │  10s → 22s  │  Supply shock
        #
        # Taiwan dot appears in gold → supply lines draw out →
        # "STOPPED" stamp slams → supply lines glitch-cut one by one →
        # Taiwan dot turns red.
        #
        # 0.00–0.50  Taiwan dot + rings appear        0.85s (lagged)
        # 0.85–1.55  supply lines draw out            0.70s
        # 1.55–1.83  STOPPED stamp slams              0.28s
        # 1.83–1.95  stamp wobble                     0.12s
        # 1.95–3.15  lines glitch-cut (one by one)    1.20s
        # 3.15–3.93  narration writes                 0.78s
        # 3.93–5.13  hold                             1.20s
        # 5.13–5.63  narration cross-fades            0.50s
        # 5.63–10.0  hold                             4.37s
        # 10.0–12.0  clean exit                       2.00s
        # ══════════════════════════════════════════════════════════════
        dot_tw = Dot(TW, radius=0.16, color=GOLD, fill_opacity=1)
        rings  = VGroup(*[
            Circle(radius=r, color=GOLD,
                    stroke_opacity=0.60-i*0.18, stroke_width=2.5).move_to(TW)
            for i,r in enumerate([0.16, 0.30, 0.50])
        ])
        self.play(
            FadeIn(dot_tw, scale=0.2, run_time=0.50),
            LaggedStart(*[GrowFromCenter(r) for r in rings],
                         lag_ratio=0.22, run_time=0.85),
        )

        supply_lines = make_supply_lines()
        self.play(LaggedStart(*[Create(ln) for ln in supply_lines],
                               lag_ratio=0.12, run_time=0.70))

        # Tension deepens
        self.play(tension.animate.set_fill(opacity=0.28), run_time=0.20)

        PW2  = 4.4
        st2  = stamp("STOPPED", color=RED, w=PW2, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st2, from_dir=UP, rt=0.28)
        self.play(Rotate(st2, -PI/26, run_time=0.12, rate_func=there_and_back))

        # Lines glitch-cut one by one
        for ln in supply_lines:
            self.play(
                ln.animate.shift(RIGHT*0.08).set_opacity(0.40),
                run_time=0.08, rate_func=linear)
            self.play(
                ln.animate.shift(LEFT*0.16).set_opacity(0.10),
                run_time=0.08, rate_func=linear)
            self.play(
                FadeOut(ln, run_time=0.08))

        # Taiwan dot goes red
        self.play(dot_tw.animate.set_color(RED).scale(1.30),
                   run_time=0.25)
        self.play(rings.animate.scale(2.2).set_stroke(opacity=0),
                   run_time=0.40, rate_func=smooth)

        n2a = nar("Taiwan's chip supply... suddenly stops.")
        n2b = nar("Every supply line. Cut.", color=RED)
        self.play(Write(n2a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n2a, run_time=0.25), FadeIn(n2b, run_time=0.25))
        self.wait(4.37)

        self.play(FadeOut(st2,          run_time=0.55),
                   FadeOut(rings,        run_time=0.55),
                   FadeOut(n2b,          run_time=0.55))
        # Keep dot_tw (red), world, map_bg
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 3  │  22s → 38s  │  Systems failing
        #
        # Map fades to bg. Phone + car appear centre stage.
        # Each icon glitches then gets a red X → fades out.
        # "System Failure" panel.
        #
        # 0.00–0.50  map dims further                0.50s
        # 0.50–0.80  "System Failure" panel          0.30s
        # 0.80–1.40  phone + car fade in             0.60s
        # 1.40–2.28  narration writes                0.78s
        # 2.28–3.48  hold                            1.20s
        # 3.48–3.98  narration cross-fades           0.50s
        # 3.98–4.42  phone glitches (4 steps)        0.44s
        # 4.42–4.72  red X on phone                  0.30s
        # 4.72–5.07  phone + X fade out              0.35s
        # 5.07–5.51  car glitches (4 steps)          0.44s
        # 5.51–5.81  red X on car                    0.30s
        # 5.81–6.16  car + X fade out                0.35s
        # 6.16–14.0  hold                            7.84s
        # 14.0–16.0  clean exit                      2.00s
        # ══════════════════════════════════════════════════════════════
        self.play(
            world.animate.set_opacity(0.12),
            map_bg.animate.set_fill(opacity=0.10),
            tension.animate.set_fill(opacity=0.36),
            run_time=0.50,
        )

        PW3  = 4.8
        tp3  = ink_panel(PW3, 0.72, fill="#FFF0F0", stroke=RED, sw=3.0)\
                 .move_to([0, TOP_Y, 0])
        tt3  = fit_text("System Failure", max_width=PW3-0.40, size=30, color=RED)\
                 .move_to(tp3[1].get_center())
        self.play(GrowFromCenter(tp3, run_time=0.18),
                   Write(tt3, run_time=0.28))

        phone = make_phone().scale(0.92).move_to([-2.20, STAGE_Y + 0.10, 0])
        car   = make_car().scale(0.85).move_to([ 2.20, STAGE_Y - 0.18, 0])
        self.play(FadeIn(phone, run_time=0.35),
                   FadeIn(car,   run_time=0.35))

        n3a = nar("Phones stop. Cars stop.")
        n3b = nar("Entire systems begin to fail.", color=RED)
        self.play(Write(n3a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n3a, run_time=0.25), FadeIn(n3b, run_time=0.25))

        # Phone glitches out
        glitch(self, phone, times=4, dx=0.09, total_t=0.44)
        x_phone = red_x(size=0.60).move_to(phone.get_center())
        self.play(GrowFromCenter(x_phone, run_time=0.30))
        self.play(FadeOut(phone,   run_time=0.18),
                   FadeOut(x_phone, run_time=0.18))

        # Car glitches out
        glitch(self, car, times=4, dx=0.09, total_t=0.44)
        x_car = red_x(size=0.72).move_to(car.get_center())
        self.play(GrowFromCenter(x_car, run_time=0.30))
        self.play(FadeOut(car,   run_time=0.18),
                   FadeOut(x_car, run_time=0.18))

        self.wait(7.84)

        self.play(FadeOut(tp3, run_time=0.55),
                   FadeOut(tt3, run_time=0.55),
                   FadeOut(n3b, run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 4  │  38s → 50s  │  Industry collapse
        #
        # World map comes back faintly. 8 small factory icons flood in
        # across the map. "DOWN" stamp slams. Factories glitch simultaneously
        # then all dim. Zoom-out effect via scaling.
        #
        # 0.00–0.40  world dots restore slightly     0.40s
        # 0.40–1.40  factories flood in (lagged)     1.00s
        # 1.40–1.68  DOWN stamp slams                0.28s
        # 1.68–1.80  stamp wobble                    0.12s
        # 1.80–2.58  narration writes                0.78s
        # 2.58–3.78  hold                            1.20s
        # 3.78–4.28  narration cross-fades           0.50s
        # 4.28–4.72  factories glitch simultaneously 0.44s
        # 4.72–5.22  factories dim                   0.50s
        # 5.22–5.92  zoom-out (scale down)           0.70s
        # 5.92–10.0  hold                            4.08s
        # 10.0–12.0  clean exit                      2.00s
        # ══════════════════════════════════════════════════════════════
        self.play(
            world.animate.set_opacity(0.22),
            map_bg.animate.set_fill(opacity=0.16),
            run_time=0.40,
        )

        factories = VGroup(*[
            make_small_factory(pos=pos).scale(0.72)
            for pos in FACTORY_POSITIONS
        ])
        self.play(LaggedStart(*[GrowFromCenter(f) for f in factories],
                               lag_ratio=0.12, run_time=1.00))

        PW4  = 3.4
        st4  = stamp("DOWN", color=RED, w=PW4, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st4, from_dir=UP, rt=0.28)
        self.play(Rotate(st4, PI/28, run_time=0.12, rate_func=there_and_back))

        n4a = nar("This wouldn't just affect one country...")
        n4b = nar("Industries across the world would collapse.", color=RED)
        self.play(Write(n4a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n4a, run_time=0.25), FadeIn(n4b, run_time=0.25))

        # All factories glitch simultaneously
        for dx, op in [(0.07,0.45),(-0.14,0.80),(0.07,0.25),
                        (-0.08,0.60),(0.10,0.15),(-0.07,0.35)]:
            self.play(factories.animate.shift(RIGHT*dx).set_opacity(op),
                       run_time=0.07, rate_func=linear)

        # Factories dim
        self.play(factories.animate.set_opacity(0.18), run_time=0.50)

        # Zoom out via scaling
        zoom_group = VGroup(world, map_bg, factories, dot_tw)
        self.play(zoom_group.animate.scale(0.82).shift(UP*0.10),
                   run_time=0.70, rate_func=smooth)

        self.wait(4.08)

        self.play(FadeOut(st4,       run_time=0.55),
                   FadeOut(n4b,       run_time=0.55),
                   FadeOut(factories, run_time=0.55))
        self.wait(0.10)

        # ══════════════════════════════════════════════════════════════
        # BEAT 5  │  50s → 60s  │  Global crisis
        #
        # Tension overlay deepens to near-black.
        # World dots flicker and dim. "CRISIS" stamp slams.
        # Final narration. Zoom-out. Fade to black.
        #
        # 0.00–0.70  tension deepens + world dims     0.70s
        # 0.70–0.98  CRISIS stamp slams               0.28s
        # 0.98–1.10  stamp wobble                     0.12s
        # 1.10–1.88  narration writes                 0.78s
        # 1.88–3.08  hold                             1.20s
        # 3.08–3.58  narration cross-fades            0.50s
        # 3.58–5.08  hold                             1.50s
        # 5.08–5.78  final zoom-out                   0.70s
        # 5.78–7.28  fade to black overlay            1.50s
        # ══════════════════════════════════════════════════════════════

        # World flickers down
        for op in [0.08, 0.18, 0.04, 0.14, 0.02]:
            self.play(world.animate.set_opacity(op),
                       run_time=0.10, rate_func=linear)

        # Final dim state
        self.play(
            world.animate.set_opacity(0.06),
            map_bg.animate.set_fill(opacity=0.06),
            tension.animate.set_fill(opacity=0.55),
            run_time=0.20,
        )

        PW5  = 4.0
        st5  = stamp("CRISIS", color=RED, w=PW5, h=0.82)\
                 .move_to([0, TOP_Y, 0])
        slam(self, st5, from_dir=UP, rt=0.28)
        self.play(Rotate(st5, -PI/28, run_time=0.12, rate_func=there_and_back))

        n5a = nar("This wouldn't be a local problem...")
        n5b = nar("It would be a global crisis.", size=40, color=RED)
        self.play(Write(n5a, run_time=0.78))
        self.wait(1.20)
        self.play(FadeOut(n5a, run_time=0.25), FadeIn(n5b, run_time=0.25))
        self.wait(1.50)

        # Final zoom-out
        all_stage = VGroup(world, map_bg, dot_tw, st5)
        self.play(all_stage.animate.scale(0.76).shift(DOWN*0.12),
                   run_time=0.70, rate_func=smooth)

        # Fade to black
        overlay = Rectangle(width=22, height=14,
                              fill_color=BLACK, fill_opacity=0, stroke_width=0)
        self.add(overlay)
        self.play(overlay.animate.set_fill(opacity=1),
                   run_time=1.50, rate_func=smooth)
        self.wait(0.40)