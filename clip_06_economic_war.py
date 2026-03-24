"""
clip_06_economic_war.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Economic War — Naukriyan aur Taaqat"
Scenes: holographic_globe, job_wipeout, control_orb
Duration: ~75 seconds  (6:45 – 8:00)
RENDER: manim -pqh clip_06_economic_war.py EconomicWar
"""

from manim import *
import numpy as np, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from brand import *

# ╔══════════════════════════════════════╗
# ║              INPUTS                 ║
# ║  Edit these before each render      ║
# ╚══════════════════════════════════════╝
GDP_TARGET      = 13          # trillion
GDP_LABEL       = "$13 Trillion"
GDP_SOURCE      = "Source: McKinsey Global Institute, 2023"
JOBS_MILLIONS   = 300
JOBS_LABEL      = "300 Million Jobs"
JOBS_SOURCE     = "Source: Goldman Sachs, 2023"
CONTROL_Q       = "Who controls it?"

# Wealth stream destinations (relative to globe centre)
# Three dominant AI nations receive streams
STREAM_TARGETS = [
    {"label": "USA",    "angle": 25,  "color": C_USER},
    {"label": "China",  "angle": 155, "color": C_HOT1},
    {"label": "EU",     "angle": 70,  "color": C_INFRA},
]

# Job silhouette grid
JOB_COLS  = 20
JOB_ROWS  = 8
JOB_DOT_R = 0.10

# Timing
T_GLOBE_BUILD   = 1.4
T_GLOBE_ROTATE  = 3.0
T_STREAM_LAG    = 0.22
T_COUNT_UP      = 3.5
T_GLOBE_HOLD    = 2.0
T_WIPE_DUR      = 4.0    # full red-wave wipe across jobs
T_JOBS_HOLD     = 1.8
T_ORB_PULSE     = 1.2
T_HAND_REACH    = 1.8
T_CONTROL_HOLD  = 3.2
T_OUTRO         = 1.2
# ╚══════════════════════════════════════╝


# ── Geometry helpers ──────────────────────────────────────────────────────────

def lat_lon_arc(lat_deg, lon_range, r, n_pts=60, color=C_INFRA, opacity=0.28):
    """
    Single latitude arc at lat_deg degrees, spanning lon_range=(lon0, lon1).
    Projected onto a flat 2D circle of radius r (simple orthographic).
    Returns a VMobject polyline.
    """
    lat  = lat_deg * DEGREES
    lons = np.linspace(lon_range[0], lon_range[1], n_pts) * DEGREES
    pts  = []
    for lon in lons:
        x = r * np.cos(lat) * np.sin(lon)
        y = r * np.sin(lat)
        pts.append([x, y, 0])
    vm = VMobject(color=color, stroke_width=0.7, stroke_opacity=opacity)
    vm.set_points_as_corners(pts)
    return vm


def lon_arc(lon_deg, lat_range, r, n_pts=60, color=C_INFRA, opacity=0.28):
    """Single longitude arc."""
    lon  = lon_deg * DEGREES
    lats = np.linspace(lat_range[0], lat_range[1], n_pts) * DEGREES
    pts  = []
    for lat in lats:
        x = r * np.cos(lat) * np.sin(lon)
        y = r * np.sin(lat)
        pts.append([x, y, 0])
    vm = VMobject(color=color, stroke_width=0.7, stroke_opacity=opacity)
    vm.set_points_as_corners(pts)
    return vm


def wireframe_globe(r=1.55, color=C_INFRA, n_lat=7, n_lon=12):
    """
    Orthographic wireframe globe — latitude + longitude arcs.
    Only the front hemisphere is drawn (visible half).
    """
    arcs = VGroup()
    # Latitude lines
    for lat in np.linspace(-75, 75, n_lat):
        arcs.add(lat_lon_arc(lat, (-180, 180), r, color=color))
    # Longitude lines
    for lon in np.linspace(-180, 180, n_lon, endpoint=False):
        arcs.add(lon_arc(lon, (-90, 90), r, color=color))
    # Outer circle
    outer = Circle(radius=r, color=color,
                   stroke_width=1.8, stroke_opacity=0.65, fill_opacity=0)
    arcs.add(outer)
    return arcs


def wealth_stream(start, end, color=C_STAT, n_particles=8):
    """
    Returns a VGroup of dots that will travel start→end via MoveAlongPath.
    Caller animates them with LaggedStart.
    """
    particles = VGroup()
    path      = Line(start, end)
    for _ in range(n_particles):
        d = Dot(radius=0.07, color=color, fill_opacity=0.85)
        d.move_to(start)
        particles.add(d)
    return particles, path


def person_silhouette(color, r=JOB_DOT_R):
    """Tiny person: filled circle head + small rect body."""
    head = Circle(radius=r * 0.55,
                  fill_color=color, fill_opacity=1, stroke_width=0)
    head.move_to(UP * r * 0.9)
    body = Rectangle(width=r * 0.8, height=r * 1.1,
                     fill_color=color, fill_opacity=1, stroke_width=0)
    body.move_to(DOWN * r * 0.05)
    return VGroup(head, body)


def circuit_replacement(color=C_GPT, size=0.22):
    """
    Tiny circuit pattern to replace a person silhouette.
    A small square with two stub lines — like a chip pad.
    """
    sq  = Square(side_length=size * 0.7,
                 fill_color=C_DARK, fill_opacity=1,
                 stroke_color=color, stroke_width=0.9)
    l1  = Line(LEFT * size * 0.35, LEFT * size * 0.62,
               color=color, stroke_width=0.8)
    l2  = Line(RIGHT * size * 0.35, RIGHT * size * 0.62,
               color=color, stroke_width=0.8)
    l3  = Line(UP * size * 0.35, UP * size * 0.55,
               color=color, stroke_width=0.8)
    return VGroup(sq, l1, l2, l3)


def reaching_hand(direction, color, length=1.8, tip_r=0.18):
    """
    A stylised reaching arm: tapered line + small filled circle at tip.
    direction: unit vector (numpy array) pointing toward the orb.
    Tip starts at origin + direction * length, base farther away.
    """
    base = -direction * length * 1.05
    tip  = direction * 0.32
    arm  = Line(base, tip, color=color, stroke_width=4.5,
                stroke_opacity=0.75)
    hand = Circle(radius=tip_r, fill_color=color,
                  fill_opacity=0.55, stroke_width=0)
    hand.move_to(tip)
    return VGroup(arm, hand)


# ── Main scene ────────────────────────────────────────────────────────────────

class EconomicWar(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (6:45 – 7:25)  ~40s
        # HOLOGRAPHIC GLOBE
        #
        # Jarvis-style: wireframe Earth materialises arc-by-arc with
        # LaggedStart. Globe slowly rotates (achieved by redrawing arcs
        # at shifted longitude offsets each frame — approximated by
        # three sequential redraws at +15° shifts). Scan line sweeps
        # across globe face. Three golden wealth streams shoot outward
        # from globe surface toward USA / China / EU labels.
        # $13T counter ticks up with ValueTracker + always_redraw.
        # Holographic scan lines overlay the globe for Jarvis feel.
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("Economic Power")
        self.play(FadeIn(sec1), run_time=0.4)

        GLOBE_C = UP * 0.55
        GLOBE_R = 1.65

        # ── Globe materialises ──
        globe = wireframe_globe(r=GLOBE_R, color=C_INFRA, n_lat=7, n_lon=12)
        globe.move_to(GLOBE_C)

        # Holographic scan lines — horizontal cyan lines across globe
        scan_lines = VGroup(*[
            Line(LEFT * GLOBE_R, RIGHT * GLOBE_R,
                 color=C_INFRA, stroke_width=0.5, stroke_opacity=0.12)
            .move_to(GLOBE_C + UP * y)
            for y in np.linspace(-GLOBE_R + 0.1, GLOBE_R - 0.1, 22)
        ])

        # Globe outer glow ring
        glow = Circle(radius=GLOBE_R * 1.08,
                      color=C_INFRA, stroke_width=6,
                      stroke_opacity=0.08, fill_opacity=0)
        glow.move_to(GLOBE_C)

        self.play(
            LaggedStart(*[Create(arc) for arc in globe],
                        lag_ratio=0.035),
            FadeIn(glow),
            run_time=T_GLOBE_BUILD
        )
        self.play(
            LaggedStart(*[FadeIn(sl) for sl in scan_lines],
                        lag_ratio=0.025),
            run_time=0.6
        )

        # Jarvis sweep: a bright horizontal line sweeps top→bottom
        jarvis_sweep = Line(
            GLOBE_C + LEFT * GLOBE_R + UP * GLOBE_R,
            GLOBE_C + RIGHT * GLOBE_R + UP * GLOBE_R,
            color=C_INFRA, stroke_width=1.8, stroke_opacity=0.7
        )
        self.add(jarvis_sweep)
        self.play(
            jarvis_sweep.animate
                .move_to(GLOBE_C + DOWN * GLOBE_R),
            run_time=1.1, rate_func=linear
        )
        self.remove(jarvis_sweep)

        # Simulated rotation: three LaggedStart redraws of arcs
        # Each redraw shifts longitude by +20° giving illusion of spin
        for lon_shift in [20, 20]:
            globe2 = wireframe_globe(
                r=GLOBE_R, color=C_INFRA, n_lat=7, n_lon=12
            )
            # Shift all longitude arcs by rotating points
            for mob in globe2:
                mob.rotate(lon_shift * DEGREES, axis=UP,
                           about_point=GLOBE_C)
            globe2.move_to(GLOBE_C)
            self.play(
                ReplacementTransform(globe, globe2),
                run_time=0.9, rate_func=smooth
            )
            globe = globe2

        self.wait(0.3)

        # ── Wealth streams shoot from globe surface ──
        nation_labels = []
        for st in STREAM_TARGETS:
            ang = st["angle"] * DEGREES
            col = st["color"]
            # Stream origin: globe surface at angle
            origin = GLOBE_C + GLOBE_R * np.array([np.cos(ang), np.sin(ang), 0])
            # Destination: label position outside globe
            dest   = GLOBE_C + (GLOBE_R + 1.55) * np.array([
                np.cos(ang), np.sin(ang), 0
            ])
            # Clamp dest to safe frame
            dest[0] = np.clip(dest[0], -5.8, 5.8)
            dest[1] = np.clip(dest[1], -3.2, 3.2)

            # Nation label
            n_lbl = TAG(st["label"], color=col, size=16)
            n_lbl.move_to(dest)
            nation_labels.append(n_lbl)

            # Particles stream outward with LaggedStart
            particles, path = wealth_stream(origin, dest, color=C_STAT, n_particles=6)
            self.add(*particles)
            self.play(
                LaggedStart(
                    *[MoveAlongPath(p, path, run_time=0.55, rate_func=smooth)
                      for p in particles],
                    lag_ratio=0.12
                ),
                FadeIn(n_lbl, shift=np.array([np.cos(ang), np.sin(ang), 0]) * 0.2),
                run_time=0.65
            )
            for p in particles:
                self.remove(p)

        self.wait(0.4)

        # ── $13T counter ticks up ──
        # always_redraw counter — gold, large, below globe
        tracker = ValueTracker(0)
        counter = always_redraw(
            lambda: STAT(
                f"${tracker.get_value():.1f}T",
                color=C_STAT
            ).move_to(DOWN * 1.55)
        )
        self.add(counter)
        count_up(self, tracker, GDP_TARGET, run_t=T_COUNT_UP)

        self.wait(0.5)

        # GDP label below counter
        gdp_sub = TAG("added to global economy — next 10 years",
                      color=C_DIM, size=15).move_to(DOWN * 2.25)
        self.play(FadeIn(gdp_sub, shift=UP * 0.1), run_time=0.5)

        src1 = SRC(GDP_SOURCE)
        self.play(FadeIn(src1), run_time=0.4)
        self.wait(T_GLOBE_HOLD)

        # Camera punch-in on counter
        self.play(
            self.camera.frame.animate.scale(0.72).move_to(DOWN * 1.6),
            run_time=0.55
        )
        self.wait(0.9)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Full clear
        self.remove(counter)
        globe_group = VGroup(
            globe, scan_lines, glow,
            gdp_sub, src1,
            *nation_labels
        )
        self.play(
            FadeOut(globe_group),
            FadeOut(sec1),
            run_time=0.7
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (7:25 – 7:48)  ~23s
        # SPIRAL WIPEOUT
        #
        # 300 human dots are placed on an Archimedean spiral winding
        # outward from centre. A red expanding ring sweeps outward —
        # as it passes each dot, that dot fades to dim (erased).
        # A live counter counts DOWN from 300 as dots are erased.
        # Brief text labels appear at key moments.
        # ══════════════════════════════════════════════════════════════════

        sec2 = corner_lbl("Jobs at Risk")
        self.play(FadeIn(sec2), run_time=0.4)

        # Brief intro label
        intro_lbl = TAG("300 million jobs — at risk", color=C_HOT1, size=20)
        intro_lbl.move_to(UP * 3.1)
        self.play(FadeIn(intro_lbl, shift=DOWN * 0.1), run_time=0.5)

        # Build spiral dot positions
        # Archimedean spiral: r = a * theta, theta from 0 to N_TURNS * 2pi
        N_DOTS   = 280          # visual representation of 300M
        N_TURNS  = 5.5
        A_SPIRAL = 0.42         # controls spacing between arms
        MAX_R    = A_SPIRAL * N_TURNS * TAU  # ~14.5 — scale down to fit screen
        SCALE_S  = 2.55 / MAX_R             # fits spiral in radius 2.55

        rng      = np.random.default_rng(17)
        thetas   = np.linspace(0.35, N_TURNS * TAU, N_DOTS)
        radii    = A_SPIRAL * thetas * SCALE_S

        # Sort by radius so we can erase outward
        spiral_dots   = []
        spiral_radii  = []
        for theta, r_val in zip(thetas, radii):
            jitter = rng.uniform(-0.04, 0.04, 2)
            x = r_val * np.cos(theta) + jitter[0]
            y = r_val * np.sin(theta) + jitter[1]
            col = C_USER if rng.random() > 0.25 else C_DIM
            dot = Dot(radius=0.068, color=col, fill_opacity=0.85)
            dot.move_to(RIGHT * x + UP * y)
            spiral_dots.append(dot)
            spiral_radii.append(r_val)

        # Dots appear with fast LaggedStart — winding outward
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.2) for d in spiral_dots],
                lag_ratio=0.008
            ),
            run_time=1.6
        )
        self.wait(0.4)

        # Live DOWN counter — always_redraw at top-right
        erase_tracker = ValueTracker(300)
        erase_counter = always_redraw(
            lambda: VGroup(
                STAT(f"{int(erase_tracker.get_value())}M",
                     color=C_HOT1).scale(0.62).move_to(RIGHT * 4.8 + UP * 2.6),
            )
        )
        counter_lbl = TAG("jobs at risk", color=C_DIM, size=14)
        counter_lbl.move_to(RIGHT * 4.8 + UP * 2.1)
        self.add(erase_counter, counter_lbl)

        # Red expanding ring erases dots in radius order
        # Group dots into 12 radius bands
        N_BANDS   = 14
        max_r_val = max(spiral_radii)
        bands     = [[] for _ in range(N_BANDS)]
        for dot, r_val in zip(spiral_dots, spiral_radii):
            band_idx = min(int(N_BANDS * r_val / max_r_val), N_BANDS - 1)
            bands[band_idx].append(dot)

        # Red ring starts at centre
        erase_ring = Circle(radius=0.05,
                            color=C_HOT1, stroke_width=2.2,
                            stroke_opacity=0.8, fill_opacity=0)
        self.add(erase_ring)

        dots_per_band  = N_DOTS / N_BANDS
        count_per_band = 300 / N_BANDS

        for i, band in enumerate(bands):
            target_r = max_r_val * (i + 1) / N_BANDS * SCALE_S
            self.play(
                erase_ring.animate.become(
                    Circle(radius=target_r,
                           color=C_HOT1, stroke_width=2.2,
                           stroke_opacity=0.75, fill_opacity=0)
                ),
                erase_tracker.animate.set_value(
                    300 - count_per_band * (i + 1)
                ),
                *[dot.animate.set_color(C_DIM).set_opacity(0.15)
                  for dot in band],
                run_time=0.22, rate_func=linear
            )

        self.remove(erase_ring)
        self.wait(0.5)

        # Stat slams in — centre, dark backing
        stat_bg   = Rectangle(width=4.8, height=1.1,
                              fill_color=C_BG, fill_opacity=0.88,
                              stroke_width=0).move_to(ORIGIN)
        self.add(stat_bg)
        jobs_stat = STAT(JOBS_LABEL, color=C_HOT1).scale(0.68).move_to(ORIGIN)
        slam_in(self, jobs_stat, bounces=2, run_t=0.6)

        # Brief explanation below stat
        jobs_exp = TAG("Not a prediction. Goldman Sachs, 2023.",
                       color=C_DIM, size=14).move_to(DOWN * 0.88)
        self.play(FadeIn(jobs_exp, shift=UP * 0.08), run_time=0.4)

        src2 = SRC(JOBS_SOURCE)
        self.play(FadeIn(src2), run_time=0.4)
        self.wait(T_JOBS_HOLD)

        # Clear
        self.remove(erase_counter)
        job_group = VGroup(
            *spiral_dots, stat_bg, jobs_stat,
            jobs_exp, src2, intro_lbl, counter_lbl
        )
        self.play(
            FadeOut(job_group),
            FadeOut(sec2),
            run_time=0.6
        )

        # ══════════════════════════════════════════════════════════════════
        # BEAT 3  (7:48 – 8:00)  ~12s
        # VORTEX CONTROL
        #
        # Three coloured spiral streams (USA, China, EU) wind inward
        # toward a central shifting gold point — built as parametric
        # spiral VMobjects with arrowheads at their tips.
        # The centre point (control node) drifts slightly away from
        # each stream as it arrives — always just out of reach.
        # Brief labels name each stream. "Who controls it?" writes in.
        # ══════════════════════════════════════════════════════════════════

        sec3 = corner_lbl("Control")
        self.play(FadeIn(sec3), run_time=0.3)

        # Central control node — glowing gold dot, drifts
        ctrl_node = VGroup(
            Circle(radius=0.42, fill_color=C_STAT,
                   fill_opacity=0.10, stroke_width=0),
            Circle(radius=0.26, fill_color=C_STAT,
                   fill_opacity=0.22, stroke_width=0),
            Circle(radius=0.13, fill_color=C_STAT,
                   fill_opacity=1.0,  stroke_width=0),
        ).move_to(ORIGIN)

        self.play(
            FadeIn(ctrl_node, scale=0.05, rate_func=rush_into),
            run_time=0.5
        )
        ripple(self, ORIGIN, color=C_STAT, n=3, base_r=0.2, run_t=0.6)

        # Build three inward spiral streams
        # Each spiral: starts 2.8 units out at a given angle,
        # winds ~1.5 turns inward but stops 0.55 units from centre
        VORTEX_DATA = [
            {"label": "USA",   "color": C_USER,  "start_angle": 0},
            {"label": "China", "color": C_HOT1,  "start_angle": 120},
            {"label": "EU",    "color": C_INFRA, "start_angle": 240},
        ]

        def make_spiral_stream(start_angle_deg, color, n_pts=120,
                               r_start=2.8, r_end=0.6, n_winds=1.5):
            """Inward spiral from r_start to r_end, n_winds full turns."""
            sa    = start_angle_deg * DEGREES
            t_arr = np.linspace(0, n_winds * TAU, n_pts)
            pts   = []
            for t in t_arr:
                frac = t / (n_winds * TAU)
                r    = r_start * (1 - frac) + r_end * frac
                angle = sa - t           # winds clockwise inward
                pts.append([r * np.cos(angle), r * np.sin(angle), 0])
            vm = VMobject(color=color, stroke_width=2.8, stroke_opacity=0.85)
            vm.set_points_smoothly([np.array(p) for p in pts])
            return vm, np.array(pts[-1])   # also return tip position

        streams      = []
        stream_tips  = []
        stream_lbls  = []

        for vd in VORTEX_DATA:
            vm, tip = make_spiral_stream(
                vd["start_angle"], vd["color"],
                r_start=2.8, r_end=0.58, n_winds=1.4
            )
            # Arrow tip — small triangle at end of spiral
            tip_dir = tip / (np.linalg.norm(tip) + 1e-6)
            arr_tip = Arrow(
                tip - tip_dir * 0.35, tip + tip_dir * 0.01,
                color=vd["color"], stroke_width=2.5,
                max_tip_length_to_length_ratio=0.55, buff=0
            )
            # Label near the outer start of spiral
            sa   = vd["start_angle"] * DEGREES
            lpos = np.array([3.2 * np.cos(sa), 3.2 * np.sin(sa), 0])
            lpos[0] = np.clip(lpos[0], -5.5, 5.5)
            lpos[1] = np.clip(lpos[1], -3.0, 3.0)
            lbl  = TAG(vd["label"], color=vd["color"], size=16)
            lbl.move_to(lpos)

            streams.append(VGroup(vm, arr_tip))
            stream_tips.append(tip)
            stream_lbls.append(lbl)

        # Streams draw in with LaggedStart — each one spirals inward
        self.play(
            LaggedStart(
                *[Create(s[0], run_time=1.1, rate_func=smooth)
                  for s in streams],
                lag_ratio=0.28
            ),
            LaggedStart(
                *[FadeIn(lbl) for lbl in stream_lbls],
                lag_ratio=0.28
            ),
            run_time=1.6
        )

        # Arrow tips appear at spiral ends
        self.play(
            LaggedStart(
                *[FadeIn(s[1], scale=0.3) for s in streams],
                lag_ratio=0.18
            ),
            run_time=0.5
        )

        # Control node drifts — shifts slightly as each stream arrives
        # giving the feeling it's always just out of reach
        drift_positions = [
            UP * 0.28 + RIGHT * 0.18,
            DOWN * 0.22 + LEFT * 0.25,
            RIGHT * 0.30 + UP * 0.12,
            ORIGIN,
        ]
        for drift_pos in drift_positions:
            self.play(
                ctrl_node.animate.move_to(drift_pos),
                run_time=0.45, rate_func=smooth
            )

        # Orb pulses — alone, uncaptured
        for _ in range(2):
            ripple(self, ctrl_node.get_center(),
                   color=C_STAT, n=3, base_r=0.18, run_t=0.65)
            self.wait(0.15)

        self.wait(0.3)

        # "Who controls it?" writes in below
        ctrl_q = BODY(CONTROL_Q, color=C_STAT, size=26)
        ctrl_q.move_to(DOWN * 2.9)
        self.play(AddTextLetterByLetter(ctrl_q, time_per_char=0.055))

        # Brief subtext
        ctrl_sub = TAG("The answer will define the next century.",
                       color=C_DIM, size=15).move_to(DOWN * 3.45)
        self.play(FadeIn(ctrl_sub, shift=UP * 0.08), run_time=0.5)

        self.wait(T_CONTROL_HOLD)

        # ── End fade ──
        orb_group = VGroup(
            ctrl_node, ctrl_q, ctrl_sub,
            *streams, *stream_lbls
        )
        self.play(
            FadeOut(orb_group),
            FadeOut(sec3),
            FadeOut(bg),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()