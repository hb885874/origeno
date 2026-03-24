"""
clip_09_closing.py  —  Origeno
━━━━━━━━━━━━━━━━━━━━
Chapter 1 · "Yeh Daud Rukegi Nahi — Closing"
Scenes: mushroom_to_network, taiwan_teaser
Duration: ~60 seconds  (10:00 – 11:00)
RENDER: manim -pqh clip_09_closing.py Closing
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
WEAPON_OLD   = "Bomb"
WEAPON_NEW   = "Algorithm"
SPREAD_NODES = ["Phone", "Office", "Policy", "Economy", "Military"]

TEASER_WORD  = "CHIPS"
TEASER_SUB   = "Agle episode mein..."
TAIWAN_LABEL = "Taiwan"
NEXT_TITLE   = "Episode 2 — The Chip War"

# Timing
T_CLOUD_BUILD  = 1.4
T_MORPH        = 1.6
T_SPREAD_LAG   = 0.20
T_NET_HOLD     = 2.8
T_TEASER_HOLD  = 3.5
T_OUTRO        = 1.4
# ╚══════════════════════════════════════╝


# ── Icon builders ─────────────────────────────────────────────────────────────

def mushroom_cloud(color=C_HOT2, scale=1.0):
    """
    Stylised nuclear mushroom cloud built from geometry:
      stem  — tapered trapezoid rising from bottom
      cap   — large circle on top
      ring  — torus-like ellipse around cap base
    All anchored so cloud base sits at y=0.
    """
    # Stem — trapezoid: narrow at top, wider at bottom
    stem = Polygon(
        LEFT  * 0.22 * scale + UP   * 0.0,
        RIGHT * 0.22 * scale + UP   * 0.0,
        RIGHT * 0.42 * scale + DOWN * 1.1 * scale,
        LEFT  * 0.42 * scale + DOWN * 1.1 * scale,
        fill_color=color, fill_opacity=0.85, stroke_width=0
    )
    # Cap — large filled circle
    cap = Circle(radius=0.78 * scale,
                 fill_color=color, fill_opacity=0.85, stroke_width=0)
    cap.move_to(UP * 0.72 * scale)
    # Ring — ellipse around cap base for the classic mushroom look
    ring = Ellipse(width=1.85 * scale, height=0.42 * scale,
                   fill_color=color, fill_opacity=0.65, stroke_width=0)
    ring.move_to(UP * 0.08 * scale)
    # Inner lighter highlight on cap
    highlight = Circle(radius=0.38 * scale,
                       fill_color=C_HOT3, fill_opacity=0.35, stroke_width=0)
    highlight.move_to(UP * 0.88 * scale)
    return VGroup(stem, ring, cap, highlight)


def neural_net(color=C_GPT, n_layers=4, nodes_per_layer=None, spread=1.0):
    """
    Feed-forward neural network diagram.
    Layers spaced horizontally. Nodes in each layer spaced vertically.
    All edges drawn first (dim), then nodes on top.
    Returns VGroup(edges, nodes).
    """
    if nodes_per_layer is None:
        nodes_per_layer = [3, 4, 4, 3]

    layer_xs = np.linspace(-spread * 1.4, spread * 1.4, n_layers)
    # node positions per layer
    all_pts = []
    for i, n in enumerate(nodes_per_layer):
        ys = np.linspace(-(n - 1) * 0.48 * spread,
                          (n - 1) * 0.48 * spread, n)
        all_pts.append([(layer_xs[i], y, 0) for y in ys])

    edges = VGroup()
    for i in range(n_layers - 1):
        for pa in all_pts[i]:
            for pb in all_pts[i + 1]:
                edges.add(
                    Line(pa, pb, color=color,
                         stroke_width=0.7, stroke_opacity=0.30)
                )

    nodes = VGroup()
    for layer in all_pts:
        for pt in layer:
            nodes.add(
                Circle(radius=0.13 * spread,
                       fill_color=color, fill_opacity=1,
                       stroke_width=0).move_to(pt)
            )

    return VGroup(edges, nodes)


def globe_outline(r=1.4, color=C_INFRA):
    """Simple globe: outer circle + 3 lat arcs + 2 lon arcs."""
    outer = Circle(radius=r, color=color,
                   stroke_width=1.6, stroke_opacity=0.55, fill_opacity=0)
    lats  = VGroup(*[
        Ellipse(width=2 * r, height=2 * r * abs(np.sin(a)),
                color=color, stroke_width=0.7, stroke_opacity=0.28,
                fill_opacity=0)
        for a in [0.3, 0.65, 1.1]
    ])
    lons  = VGroup(*[
        Ellipse(width=2 * r * abs(np.sin(a)), height=2 * r,
                color=color, stroke_width=0.7, stroke_opacity=0.28,
                fill_opacity=0)
        for a in [0.5, 1.0]
    ])
    return VGroup(outer, lats, lons)


def taiwan_dot_on_globe(globe_centre, globe_r, color=C_STAT):
    """
    Taiwan is roughly at lon=121°E, lat=24°N on a simple orthographic
    projection facing front (lon=0 at screen centre).
    """
    lon = (121 - 20) * DEGREES    # offset so globe faces ~80°E
    lat = 24 * DEGREES
    x   = globe_r * np.cos(lat) * np.sin(lon)
    y   = globe_r * np.sin(lat)
    pos = globe_centre + np.array([x, y, 0])
    dot = Dot(radius=0.12, color=color, fill_opacity=1)
    dot.move_to(pos)
    return dot, pos


# ── Main scene ────────────────────────────────────────────────────────────────

class Closing(MovingCameraScene):
    def construct(self):
        self.camera.background_color = C_BG
        bg = circuit_bg(self)
        self.camera.frame.save_state()

        # ══════════════════════════════════════════════════════════════════
        # BEAT 1  (10:00 – 10:30)  ~30s
        # MUSHROOM → NEURAL NETWORK
        #
        # A mushroom cloud builds from bottom — stem rises, cap blooms.
        # "Bomb" label appears below. Camera breathes in slowly.
        # Then ReplacementTransform morphs the cloud into a neural
        # network of the same approximate bounding box.
        # "Algorithm" label morphs from "Bomb".
        # Network nodes light up with LaggedStart ripples.
        # Spread nodes fan out from network to edges: Phone, Office,
        # Policy, Economy, Military — each on a dashed spoke.
        # Final tag: "Same energy. Different weapon."
        # ══════════════════════════════════════════════════════════════════

        sec1 = corner_lbl("The New Weapon")
        self.play(FadeIn(sec1), run_time=0.4)

        CLOUD_C = UP * 0.55

        # Build mushroom cloud — stem grows up, then cap blooms
        cloud = mushroom_cloud(color=C_HOT2, scale=1.15)
        cloud.move_to(CLOUD_C)

        # Animate: start from a dot at base, grow upward
        cloud_zero = cloud.copy().scale(0.001)
        self.add(cloud_zero)
        self.play(
            ReplacementTransform(cloud_zero, cloud),
            run_time=T_CLOUD_BUILD, rate_func=smooth
        )

        # Bomb label
        bomb_lbl = H2(WEAPON_OLD, color=C_HOT2).move_to(CLOUD_C + DOWN * 1.85)
        self.play(FadeIn(bomb_lbl, shift=UP * 0.12), run_time=0.5)

        # Camera breathes in on the cloud
        self.play(
            self.camera.frame.animate.scale(0.78).move_to(CLOUD_C),
            run_time=0.7
        )
        self.wait(1.0)
        self.play(self.camera.frame.animate.restore(), run_time=0.6)

        # ── Morph cloud → neural network ──
        net = neural_net(color=C_GPT, n_layers=4,
                         nodes_per_layer=[3, 4, 4, 3], spread=0.92)
        net.move_to(CLOUD_C)

        algo_lbl = H2(WEAPON_NEW, color=C_GPT).move_to(CLOUD_C + DOWN * 1.85)

        self.play(
            ReplacementTransform(cloud,    net),
            ReplacementTransform(bomb_lbl, algo_lbl),
            run_time=T_MORPH, rate_func=smooth
        )

        # Network nodes light up with staggered ripples
        net_nodes = net[1]   # VGroup of node circles
        self.play(
            LaggedStart(
                *[Flash(nd, color=C_GPT, flash_radius=0.22, line_length=0.12)
                  for nd in net_nodes],
                lag_ratio=0.08
            ),
            run_time=1.2
        )
        self.wait(0.4)

        # Camera punch-in on network
        self.play(
            self.camera.frame.animate.scale(0.72).move_to(CLOUD_C),
            run_time=0.55
        )
        self.wait(0.8)
        self.play(self.camera.frame.animate.restore(), run_time=0.5)

        # Spread nodes fan out from network
        # 5 nodes at evenly spaced angles, dashed spokes
        spread_angles = np.linspace(30, 330, len(SPREAD_NODES)) * DEGREES
        SPOKE_LEN     = 2.55
        spread_mobs   = []
        spokes        = []

        for angle, label in zip(spread_angles, SPREAD_NODES):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            end_pos   = CLOUD_C + direction * SPOKE_LEN
            # Clamp to safe frame
            end_pos[0] = np.clip(end_pos[0], -5.8, 5.8)
            end_pos[1] = np.clip(end_pos[1], -2.8, 2.8)

            spoke_solid = Line(CLOUD_C + direction * 1.1, end_pos,
                               color=C_GPT, stroke_width=1.2)
            spoke       = DashedVMobject(spoke_solid,
                                         num_dashes=10, dashed_ratio=0.5)

            node_dot = Circle(radius=0.15, fill_color=C_GPT,
                              fill_opacity=0.20, stroke_color=C_GPT,
                              stroke_width=1.6).move_to(end_pos)
            node_lbl = TAG(label, color=C_GPT, size=14)
            # Place label above or below based on vertical direction
            if direction[1] >= 0:
                node_lbl.next_to(node_dot, UP,   buff=0.12)
            else:
                node_lbl.next_to(node_dot, DOWN, buff=0.12)

            spread_mobs.append(VGroup(spoke, node_dot, node_lbl))
            spokes.append(spoke)

        self.play(
            LaggedStart(
                *[AnimationGroup(
                    Create(sm[0]),
                    FadeIn(sm[1], scale=0.1, rate_func=rush_into),
                    FadeIn(sm[2], shift=ORIGIN),
                  )
                  for sm in spread_mobs],
                lag_ratio=T_SPREAD_LAG
            ),
            run_time=1.6
        )
        self.wait(0.5)

        # Final tag
        weapon_tag = TAG("Same energy.  Different weapon.",
                         color=C_STAT, size=18).move_to(DOWN * 3.1)
        self.play(AddTextLetterByLetter(weapon_tag, time_per_char=0.04))
        self.wait(T_NET_HOLD)

        # Full clear
        beat1_group = VGroup(
            net, algo_lbl, weapon_tag, sec1,
            *spread_mobs
        )
        self.play(FadeOut(beat1_group), run_time=0.7)

        # ══════════════════════════════════════════════════════════════════
        # BEAT 2  (10:30 – 11:00)  ~30s
        # TAIWAN TEASER
        #
        # Screen is dark for a beat — silence before the tease.
        # "CHIPS" slams in massive gold from scale 0, 3 bounces.
        # It shrinks upward to become a title anchor.
        # A wireframe globe builds. Taiwan dot pings with ripples.
        # "Taiwan" label writes in next to the dot.
        # Episode 2 title card fades in below.
        # "Agli baar." writes in last — the hook.
        # ══════════════════════════════════════════════════════════════════

        self.wait(0.6)   # deliberate silence

        # "CHIPS" slams in — biggest moment of the episode
        chips_word = STAT(TEASER_WORD, color=C_STAT)
        chips_word.scale(1.55).move_to(ORIGIN)
        slam_in(self, chips_word, bounces=3, run_t=0.8)
        self.wait(0.7)

        # Chips shrinks to top anchor
        self.play(
            chips_word.animate.scale(0.42).move_to(UP * 3.0),
            run_time=0.55
        )

        # Globe builds arc by arc
        GLOBE_C = UP * 0.3
        GLOBE_R = 1.55
        globe   = globe_outline(r=GLOBE_R, color=C_INFRA)
        globe.move_to(GLOBE_C)

        self.play(
            LaggedStart(
                *[Create(arc) for arc in globe],
                lag_ratio=0.06
            ),
            run_time=1.1
        )

        # Taiwan dot pings
        tw_dot, tw_pos = taiwan_dot_on_globe(GLOBE_C, GLOBE_R, color=C_STAT)
        self.play(
            FadeIn(tw_dot, scale=0.1, rate_func=rush_into),
            run_time=0.4
        )
        ripple(self, tw_pos, color=C_STAT, n=4, base_r=0.15, run_t=0.8)

        # Taiwan label
        tw_lbl = TAG(TAIWAN_LABEL, color=C_STAT, size=17)
        tw_lbl.next_to(tw_dot, RIGHT, buff=0.22)
        self.play(AddTextLetterByLetter(tw_lbl, time_per_char=0.06))
        self.wait(0.4)

        # Camera punch-in on Taiwan dot
        self.play(
            self.camera.frame.animate.scale(0.60).move_to(tw_pos),
            run_time=0.6
        )
        ripple(self, tw_pos, color=C_STAT, n=3, base_r=0.10, run_t=0.6)
        self.wait(0.8)
        self.play(self.camera.frame.animate.restore(), run_time=0.55)

        # Episode 2 title card
        ep2_bg = RoundedRectangle(
            corner_radius=0.14, width=5.6, height=0.72,
            fill_color=C_DARK, fill_opacity=1,
            stroke_color=C_INFRA, stroke_width=1.4
        ).move_to(DOWN * 1.95)
        ep2_title = Text(NEXT_TITLE, font="Arial", weight=BOLD,
                         font_size=20, color=C_INFRA)
        ep2_title.move_to(DOWN * 1.95)

        self.play(
            FadeIn(ep2_bg),
            FadeIn(ep2_title, shift=UP * 0.1),
            run_time=0.6
        )
        self.wait(0.5)

        # "Agli baar." — the hook, writes in slowly
        agli_baar = BODY("Agli baar.", color=C_WHITE, size=28)
        agli_baar.move_to(DOWN * 2.95)
        self.play(AddTextLetterByLetter(agli_baar, time_per_char=0.12))
        self.wait(T_TEASER_HOLD)

        # ── Final fade to black ──
        final_group = VGroup(
            chips_word, globe, tw_dot, tw_lbl,
            ep2_bg, ep2_title, agli_baar, bg
        )
        self.play(
            FadeOut(final_group),
            run_time=T_OUTRO
        )
        self.camera.frame.restore()