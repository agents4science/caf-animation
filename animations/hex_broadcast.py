from manim import *
import math
import os
import random
import argparse


class LLMHexBroadcastFixed4(MovingCameraScene):
    """
    Scaling LLM inference to 4096 nodes on Aurora supercomputer.

    Shows:
    - Hex lattice of ~300 nodes representing distributed system
    - Broadcast phase: queries propagate ring-by-ring from center
    - Inference phase: all nodes compute (pulsing red), speedometer shows tokens/s
    - Reduction phase: results flow back to center

    Side panels:
    - Left: Node anatomy (Agent Logic → Inference Server → GPU)
    - Right: Speedometer gauge (0-2M tokens/s)

    Generated from prompt: "Hex-lattice broadcast and reduction. Node anatomy panel.
    Speedometer showing tokens/s ramping up during inference."
    Refined: "Color components to match phase. Reduce animation timing for pacing."
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = int(os.getenv("RADIUS", 10))
        self.seed = int(os.getenv("SEED", 3))
        self.margin = float(os.getenv("MARGIN", 1.25))

        # visual scale
        self.hex_size = float(os.getenv("HEX_SIZE", 0.55))
        self.node_radius = float(os.getenv("NODE_RADIUS", 0.12))
        self.packet_radius = float(os.getenv("PACKET_RADIUS", 0.11))
        self.trail_width = float(os.getenv("TRAIL_WIDTH", 4.0))
        self.trail_decay = float(os.getenv("TRAIL_DECAY", 0.35))

        # pacing
        self.slow_gens = int(os.getenv("SLOW_GENS", 3))
        self.slow_time = float(os.getenv("SLOW_TIME", 0.7))
        self.fast_time = float(os.getenv("FAST_TIME", 0.25))

        random.seed(self.seed)

    # -----------------------------
    # Hex helpers
    # -----------------------------
    def hex_positions(self, radius: int):
        coords = []
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                s = -q - r
                if abs(s) <= radius:
                    coords.append((q, r))
        return coords

    def hex_dist(self, p):
        q, r = p
        return max(abs(q), abs(r), abs(-q - r))

    @staticmethod
    def hex_neighbors():
        return [(1, 0), (-1, 0),
                (0, 1), (0, -1),
                (1, -1), (-1, 1)]

    # -----------------------------
    # Camera fit (no zooming)
    # -----------------------------
    def fit_camera_to_group(self, group: VGroup, margin: float = 1.2):
        w = group.width
        h = group.height

        # Manim frame aspect ratio in scene units
        aspect = config.frame_width / config.frame_height

        # Need a width that fits both width and height
        required_width = max(w * margin, h * margin * aspect)

        self.camera.frame.width = required_width
        self.camera.frame.move_to(group.get_center())

    # -----------------------------
    # Node anatomy panel (permanent, on the left)
    # -----------------------------
    def create_node_anatomy_panel(self, nodes_group, node_map, coords, font_scale):
        """Create and return the node anatomy panel positioned to the left of nodes,
        with connector lines to the middle leftmost node.

        Returns: (panel_group, components_dict, target_node_coord)
        where components_dict has keys: agent_block, agent_text, inference_block,
        inference_text, gpu_block, gpu_text, arrow_to_gpu
        """
        frame = self.camera.frame
        fw = frame.width
        fh = frame.height

        panel_w = 0.22 * fw
        panel_h = 0.38 * fh  # Reduced height for less bottom margin

        bg = RoundedRectangle(width=panel_w, height=panel_h, corner_radius=0.15)
        bg.set_fill(BLACK, opacity=0.75)
        bg.set_stroke(WHITE, width=2, opacity=0.4)

        # Scale font sizes
        title_font = int(24 * font_scale)
        block_font = int(18 * font_scale)

        title = Text("One Node", font_size=title_font, weight=BOLD)
        title.set_color(WHITE)

        # Stack blocks with larger dimensions
        block_w = 0.85 * panel_w
        block_h = 0.14 * panel_h
        block_gap = 0.22 * panel_h

        b1 = RoundedRectangle(width=block_w, height=block_h, corner_radius=0.1)
        b2 = RoundedRectangle(width=block_w, height=block_h, corner_radius=0.1)
        b3 = RoundedRectangle(width=block_w, height=block_h, corner_radius=0.1)

        for b in (b1, b2, b3):
            b.set_fill(WHITE, opacity=0.12)
            b.set_stroke(WHITE, width=2, opacity=0.5)

        t1 = Text("Agent Logic", font_size=block_font).set_color(WHITE)
        t2 = Text("Inference Server", font_size=block_font).set_color(WHITE)
        t3 = Text("GPU", font_size=block_font).set_color(WHITE)

        # Layout within panel
        title.move_to(bg.get_top() + DOWN * (0.12 * panel_h))

        b1.move_to(bg.get_center() + UP * block_gap * 0.9)
        b2.move_to(bg.get_center() + DOWN * block_gap * 0.1)
        b3.move_to(bg.get_center() + DOWN * block_gap * 1.1)

        t1.move_to(b1.get_center())
        t2.move_to(b2.get_center())
        t3.move_to(b3.get_center())

        a1 = Arrow(b1.get_bottom(), b2.get_top(), buff=0.08, stroke_width=3).set_color(WHITE)
        a2 = Arrow(b2.get_bottom(), b3.get_top(), buff=0.08, stroke_width=3).set_color(WHITE)
        a1.set_opacity(0.7)
        a2.set_opacity(0.7)

        panel = VGroup(bg, title, b1, b2, b3, t1, t2, t3, a1, a2)

        # Position to the left of the nodes (reduced buffer to avoid edge truncation)
        panel.next_to(nodes_group, LEFT, buff=2.0)

        # Find the middle leftmost node
        min_q = min(c[0] for c in coords)
        leftmost_nodes = sorted([c for c in coords if c[0] == min_q], key=lambda c: c[1])
        middle_left_node = leftmost_nodes[len(leftmost_nodes) // 2]
        target_node = node_map[middle_left_node]

        # Create connector lines from panel to target node
        connector = DashedLine(
            bg.get_right(),
            target_node.get_center(),
            dash_length=0.15,
            stroke_width=2,
            color=WHITE
        )
        connector.set_opacity(0.6)

        # Circle to highlight the target node
        highlight_circle = Circle(radius=self.node_radius * 2.5, color=WHITE, stroke_width=2)
        highlight_circle.set_fill(opacity=0)
        highlight_circle.move_to(target_node.get_center())
        highlight_circle.set_opacity(0.6)

        panel_group = VGroup(panel, connector, highlight_circle)

        # Components dict for coloring later
        components = {
            "agent_block": b1,
            "agent_text": t1,
            "inference_block": b2,
            "inference_text": t2,
            "gpu_block": b3,
            "gpu_text": t3,
            "arrow_to_gpu": a2,
        }

        return panel_group, components, middle_left_node

    # -----------------------------
    # Speedometer panel (on the right)
    # -----------------------------
    def create_speedometer_panel(self, nodes_group, font_scale):
        """Create a speedometer gauge labeled 'Tokens/s' with scale 0-2M.

        Returns: (panel_group, needle, needle_pivot_point)
        """
        frame = self.camera.frame
        fw = frame.width
        fh = frame.height

        panel_w = 0.22 * fw
        panel_h = 0.38 * fh

        bg = RoundedRectangle(width=panel_w, height=panel_h, corner_radius=0.15)
        bg.set_fill(BLACK, opacity=0.75)
        bg.set_stroke(WHITE, width=2, opacity=0.4)

        # Scale font sizes
        title_font = int(24 * font_scale)
        label_font = int(14 * font_scale)
        value_font = int(32 * font_scale)  # Larger font for speed number

        title = Text("Tokens/s", font_size=title_font, weight=BOLD)
        title.set_color(WHITE)

        # Speedometer arc parameters
        gauge_radius = 0.32 * panel_w
        arc_center = bg.get_center() + DOWN * 0.18 * panel_h  # Moved down to avoid overlap with title

        # Create the arc (semicircle from left to right, 180 degrees)
        # Angle 0 = right, PI = left, so we go from PI to 0 (left to right)
        arc = Arc(
            radius=gauge_radius,
            start_angle=PI,
            angle=-PI,  # sweep 180 degrees clockwise
            arc_center=arc_center,
            stroke_width=3,
            color=WHITE
        )
        arc.set_opacity(0.6)

        # Create tick marks and labels (0, 0.5M, 1M, 1.5M, 2M)
        tick_labels = ["0", "0.5M", "1M", "1.5M", "2M"]
        tick_angles = [PI, 3*PI/4, PI/2, PI/4, 0]  # evenly spaced from left to right

        ticks = VGroup()
        labels = VGroup()

        for i, (label_text, angle) in enumerate(zip(tick_labels, tick_angles)):
            # Tick mark (short line pointing inward)
            tick_outer = arc_center + gauge_radius * np.array([np.cos(angle), np.sin(angle), 0])
            tick_inner = arc_center + (gauge_radius - 0.08 * panel_w) * np.array([np.cos(angle), np.sin(angle), 0])
            tick = Line(tick_inner, tick_outer, stroke_width=2, color=WHITE)
            tick.set_opacity(0.8)
            ticks.add(tick)

            # Label positioned outside the arc
            label_pos = arc_center + (gauge_radius + 0.12 * panel_w) * np.array([np.cos(angle), np.sin(angle), 0])
            label = Text(label_text, font_size=label_font, color=WHITE)
            label.move_to(label_pos)
            label.set_opacity(0.9)
            labels.add(label)

        # Create the needle (starts pointing left = 0)
        needle_length = gauge_radius * 0.85
        needle = Line(
            arc_center,
            arc_center + needle_length * np.array([np.cos(PI), np.sin(PI), 0]),
            stroke_width=4,
            color=YELLOW
        )
        needle.set_opacity(0.9)

        # Needle pivot dot
        pivot_dot = Dot(arc_center, radius=0.03 * panel_w, color=YELLOW)
        pivot_dot.set_opacity(0.9)

        # Value display text (will be updated during animation)
        # Store the font size as an attribute so it persists during animation
        value_text = Text("0", font_size=value_font, color=YELLOW)
        value_text.target_font_size = value_font  # Store for use in updater
        value_text.move_to(arc_center + DOWN * 0.15 * panel_h)

        # Layout
        title.move_to(bg.get_top() + DOWN * 0.1 * panel_h)

        panel = VGroup(bg, title, arc, ticks, labels, pivot_dot)

        # Position to the right of the nodes (reduced buffer to avoid edge truncation)
        panel.next_to(nodes_group, RIGHT, buff=2.0)

        # Move needle and value_text to match panel position
        # Recalculate arc_center after panel move
        new_arc_center = bg.get_center() + DOWN * 0.18 * panel_h  # Match the new offset
        needle.put_start_and_end_on(
            new_arc_center,
            new_arc_center + needle_length * np.array([np.cos(PI), np.sin(PI), 0])
        )
        pivot_dot.move_to(new_arc_center)
        value_text.move_to(new_arc_center + DOWN * 0.15 * panel_h)

        panel.add(value_text)

        return panel, needle, new_arc_center, gauge_radius * 0.85, value_text

    def animate_speedometer(self, needle, pivot, needle_length, value_text, target_value=1.5, run_time=2.0):
        """Animate the speedometer needle from 0 to target_value (in millions) with oscillation.

        target_value: value in millions (e.g., 1.5 for 1.5M)
        """
        # Angle mapping: 0 = PI (left), 2M = 0 (right)
        # target_value of 1.5M = 1.5/2 = 0.75 of the way = angle PI/4
        target_angle = PI - (target_value / 2.0) * PI

        # Create animation to move needle to target
        def needle_updater(mob, alpha):
            current_angle = PI - alpha * (target_value / 2.0) * PI
            end_point = pivot + needle_length * np.array([np.cos(current_angle), np.sin(current_angle), 0])
            mob.put_start_and_end_on(pivot, end_point)

        # Value updater - use stored font size to prevent scaling issues
        fixed_font_size = getattr(value_text, 'target_font_size', 20)
        fixed_center = value_text.get_center().copy()  # Store the initial center position

        def get_value_updater(start_val, end_val):
            def updater(mob, alpha):
                current_val = start_val + alpha * (end_val - start_val)
                if current_val >= 1:
                    new_text = f"{current_val:.1f}M"
                else:
                    new_text = f"{current_val * 1000:.0f}K"
                new_mob = Text(new_text, font_size=fixed_font_size, color=YELLOW)
                new_mob.move_to(fixed_center)  # Use fixed center position
                mob.become(new_mob)
            return updater

        # Main sweep animation
        self.play(
            UpdateFromAlphaFunc(needle, needle_updater),
            UpdateFromAlphaFunc(value_text, get_value_updater(0, target_value)),
            run_time=run_time,
            rate_func=smooth
        )

        # Oscillation around target value
        oscillation_range = 0.1  # +/- 0.1M
        for i in range(4):
            # Oscillate slightly above and below
            offset = oscillation_range * (0.7 ** i) * (1 if i % 2 == 0 else -1)
            new_value = target_value + offset
            new_angle = PI - (new_value / 2.0) * PI

            def make_osc_updater(start_angle, end_angle):
                def updater(mob, alpha):
                    current_angle = start_angle + alpha * (end_angle - start_angle)
                    end_point = pivot + needle_length * np.array([np.cos(current_angle), np.sin(current_angle), 0])
                    mob.put_start_and_end_on(pivot, end_point)
                return updater

            current_angle = PI - (target_value / 2.0) * PI
            self.play(
                UpdateFromAlphaFunc(needle, make_osc_updater(current_angle, new_angle)),
                UpdateFromAlphaFunc(value_text, get_value_updater(target_value, new_value)),
                run_time=0.3,
                rate_func=smooth
            )
            target_value = new_value

    # -----------------------------
    # Main
    # -----------------------------
    def construct(self):
        coords = self.hex_positions(self.radius)
        root = (0, 0)
        neigh = self.hex_neighbors()

        # Build hex nodes - shifted down 1 unit
        node_map = {}
        nodes = []
        for q, r in coords:
            x = self.hex_size * (3 / 2 * q)
            y = self.hex_size * (math.sqrt(3) / 2 * q + math.sqrt(3) * r) - 1.4  # Shift down ~5% more
            node = Circle(radius=self.node_radius)
            node.set_fill(GRAY, opacity=1.0)
            node.set_stroke(GRAY, width=1)
            node.move_to([x, y, 0])
            node_map[(q, r)] = node
            nodes.append(node)

        nodes_group = VGroup(*nodes)

        # Fit camera FIRST, before positioning any UI elements
        self.fit_camera_to_group(nodes_group, margin=self.margin)

        # Shift camera frame UP to push content DOWN visually (by ~8% of frame height)
        self.camera.frame.shift(UP * self.camera.frame.height * 0.08)

        # Calculate font scale based on camera frame width (base size at frame width ~14)
        frame_width = self.camera.frame.width
        font_scale = frame_width / 14.0
        label_font_size = int(36 * font_scale)

        # Add title at the top (position relative to camera frame, not default frame)
        # 5% from top, Arial font, 36pt base (scaled for camera zoom)
        title = Text("Scaling LLM Inference to 4096 Nodes on Aurora", font="Arial", font_size=int(36 * font_scale), color=WHITE, weight=BOLD)
        title.move_to(self.camera.frame.get_top() + DOWN * self.camera.frame.height * 0.05)
        self.add(title)

        self.play(FadeIn(nodes_group), run_time=0.5)

        # Create and show the permanent node anatomy panel on the left
        anatomy_panel, panel_components, target_node_coord = self.create_node_anatomy_panel(nodes_group, node_map, coords, font_scale)
        target_ring = self.hex_dist(target_node_coord)
        self.play(FadeIn(anatomy_panel), run_time=0.4)

        # Create and show the speedometer panel on the right
        speedometer_panel, needle, needle_pivot, needle_length, value_text = self.create_speedometer_panel(nodes_group, font_scale)
        self.play(FadeIn(speedometer_panel), run_time=0.4)
        self.add(needle)  # Add needle separately so we can animate it

        # Precompute rings
        rings = {}
        for node in coords:
            d = self.hex_dist((node[0] - root[0], node[1] - root[1]))
            rings.setdefault(d, []).append(node)
        max_ring = max(rings.keys())

        # Root highlight
        node_map[root].set_color(YELLOW)

        # -----------------------------
        # BROADCAST: ring -> ring, each sender sends to TWO neighbors if possible
        # -----------------------------
        phase = Text("Broadcast", font_size=label_font_size, color=YELLOW)
        phase.next_to(nodes_group, UP, buff=0.5)
        self.play(FadeIn(phase), run_time=0.25)

        for r in range(1, max_ring + 1):
            prev_ring = set(rings[r - 1])
            ring = list(rings[r])

            # Build candidate incoming edges from prev_ring neighbors
            # For ring-consistency + 2-forwarding: we allocate children to parents in prev_ring.
            # Each parent can send to up to 2 children (in this ring).
            children_for_parent = {p: [] for p in prev_ring}

            # Deterministic ordering around ring (for visual stability)
            ring_sorted = sorted(ring, key=lambda t: (t[0], t[1]))

            unassigned = set(ring_sorted)

            # First pass: try to assign each prev_ring node up to 2 outward neighbors
            # Outward neighbors = hex neighbors that are in the current ring.
            for p in sorted(prev_ring, key=lambda t: (t[0], t[1])):
                if not unassigned:
                    break
                pq, pr = p
                candidates = []
                for dq, dr in neigh:
                    c = (pq + dq, pr + dr)
                    if c in unassigned:
                        candidates.append(c)
                # pick up to 2
                for c in candidates[:2]:
                    children_for_parent[p].append(c)
                    unassigned.remove(c)

            # Second pass: any leftover ring nodes get assigned to *some* parent neighbor in prev_ring
            # (still strictly ring->ring, still hex-neighbor only)
            if unassigned:
                for c in list(unassigned):
                    cq, cr = c
                    parent_candidates = []
                    for dq, dr in neigh:
                        p = (cq + dq, cr + dr)
                        if p in prev_ring:
                            parent_candidates.append(p)
                    if parent_candidates:
                        # choose the parent with currently smallest load (keeps things balanced)
                        parent_candidates.sort(key=lambda p: len(children_for_parent[p]))
                        children_for_parent[parent_candidates[0]].append(c)
                        unassigned.remove(c)

            # Now animate all transmissions in parallel (packets draw their own path)
            packets, trails, moves = [], [], []
            for p, kids in children_for_parent.items():
                if not kids:
                    continue
                src = node_map[p].get_center()
                for c in kids:
                    dst = node_map[c].get_center()
                    path = Line(src, dst)

                    packet = Dot(radius=self.packet_radius, color=YELLOW).move_to(src)
                    trail = TracedPath(packet.get_center,
                                       dissipating_time=self.trail_decay,
                                       stroke_width=self.trail_width,
                                       stroke_color=YELLOW)
                    packets.append(packet)
                    trails.append(trail)
                    moves.append(MoveAlongPath(packet, path, rate_func=linear))

            self.add(*packets, *trails)
            run_time = self.slow_time if r <= self.slow_gens else self.fast_time
            self.play(AnimationGroup(*moves, lag_ratio=0), run_time=run_time)
            self.remove(*packets, *trails)

            # Mark ring received
            for n in ring:
                node_map[n].set_color(YELLOW)

            # Color agent logic yellow when target node receives
            if r == target_ring:
                self.play(
                    panel_components["agent_block"].animate.set_fill(YELLOW, opacity=0.5),
                    panel_components["agent_text"].animate.set_color(YELLOW),
                    run_time=0.3
                )

        # Reset agent logic to white before inference
        self.play(
            panel_components["agent_block"].animate.set_fill(WHITE, opacity=0.12),
            panel_components["agent_text"].animate.set_color(WHITE),
            run_time=0.2
        )

        # -----------------------------
        # COMPUTE with pulsing effect
        # -----------------------------
        compute = Text("Inference", font_size=label_font_size, color=RED)
        compute.next_to(nodes_group, UP, buff=0.5)
        self.play(Transform(phase, compute), run_time=0.25)

        # Color inference components red during compute
        self.play(
            nodes_group.animate.set_color(RED),
            panel_components["inference_block"].animate.set_fill(RED, opacity=0.5),
            panel_components["inference_text"].animate.set_color(RED),
            panel_components["gpu_block"].animate.set_fill(RED, opacity=0.5),
            panel_components["gpu_text"].animate.set_color(RED),
            panel_components["arrow_to_gpu"].animate.set_color(RED),
            run_time=0.3
        )

        # Animate speedometer ramping up to ~1.5M tokens/s with oscillation
        self.animate_speedometer(needle, needle_pivot, needle_length, value_text, target_value=1.5, run_time=1.0)

        # Pulsate each node 3 times, expanding to 2x diameter
        for _ in range(3):
            self.play(*[n.animate.scale(2.0) for n in nodes], run_time=0.25)
            self.play(*[n.animate.scale(0.5) for n in nodes], run_time=0.25)

        # Return to gray after inference, reset panel components to white
        self.play(
            nodes_group.animate.set_color(GRAY),
            panel_components["inference_block"].animate.set_fill(WHITE, opacity=0.12),
            panel_components["inference_text"].animate.set_color(WHITE),
            panel_components["gpu_block"].animate.set_fill(WHITE, opacity=0.12),
            panel_components["gpu_text"].animate.set_color(WHITE),
            panel_components["arrow_to_gpu"].animate.set_color(WHITE),
            run_time=0.3
        )

        # -----------------------------
        # REDUCTION: reverse ring -> ring inward, neighbor-only
        # -----------------------------
        reduce = Text("Reduce", font_size=label_font_size, color=BLUE)
        reduce.next_to(nodes_group, UP, buff=0.5)
        self.play(Transform(phase, reduce), run_time=0.25)

        for r in reversed(range(1, max_ring + 1)):
            prev_ring = set(rings[r - 1])
            ring = list(rings[r])

            # Color agent logic blue when target node is sending
            if r == target_ring:
                self.play(
                    panel_components["agent_block"].animate.set_fill(BLUE, opacity=0.5),
                    panel_components["agent_text"].animate.set_color(BLUE),
                    run_time=0.2
                )

            packets, trails, moves = [], [], []
            # Each node in ring sends to ONE neighbor in prev_ring (inward)
            for n in ring:
                nq, nr = n
                parent_candidates = []
                for dq, dr in neigh:
                    p = (nq + dq, nr + dr)
                    if p in prev_ring:
                        parent_candidates.append(p)
                if not parent_candidates:
                    continue
                # deterministic choice
                parent_candidates.sort(key=lambda t: (t[0], t[1]))
                p = parent_candidates[0]

                src = node_map[n].get_center()
                dst = node_map[p].get_center()
                path = Line(src, dst)

                packet = Dot(radius=self.packet_radius, color=BLUE).move_to(src)
                trail = TracedPath(packet.get_center,
                                   dissipating_time=self.trail_decay,
                                   stroke_width=self.trail_width,
                                   stroke_color=BLUE)
                packets.append(packet)
                trails.append(trail)
                moves.append(MoveAlongPath(packet, path, rate_func=linear))

            # Color sending ring blue before they send
            for n in ring:
                node_map[n].set_color(BLUE)

            self.add(*packets, *trails)
            self.play(AnimationGroup(*moves, lag_ratio=0), run_time=self.fast_time)
            self.remove(*packets, *trails)

            # Mark receiving nodes blue
            for n in prev_ring:
                node_map[n].set_color(BLUE)

            # Sending ring turns white after reducing (work done)
            for n in ring:
                node_map[n].set_color(WHITE)

            # Reset agent logic after target node sends
            if r == target_ring:
                self.play(
                    panel_components["agent_block"].animate.set_fill(WHITE, opacity=0.12),
                    panel_components["agent_text"].animate.set_color(WHITE),
                    run_time=0.2
                )

        # -----------------------------
        # FINAL: root node larger and bright green, label at top
        # -----------------------------
        result_label = Text("Final Result", font_size=label_font_size, color=GREEN)
        result_label.next_to(nodes_group, UP, buff=0.5)

        self.play(
            Transform(phase, result_label),
            node_map[root].animate.scale(2.5).set_color(PURE_GREEN),
            run_time=0.4
        )
        self.wait(0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Hex Broadcast Animation")
    parser.add_argument(
        "quality",
        nargs="?",
        default="low",
        choices=["low", "medium", "high", "4k"],
        help="Output quality (default: low)"
    )
    parser.add_argument("--preview", "-p", action="store_true", help="Preview after rendering")
    args = parser.parse_args()

    # Quality settings: (pixel_height, pixel_width, frame_rate)
    QUALITY_MAP = {
        "low": (480, 854, 15),
        "medium": (720, 1280, 30),
        "high": (1080, 1920, 60),
        "4k": (2160, 3840, 60),
    }

    height, width, fps = QUALITY_MAP[args.quality]

    config.pixel_height = height
    config.pixel_width = width
    config.frame_rate = fps
    config.output_file = f"LLMHexBroadcastFixed4_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = LLMHexBroadcastFixed4()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/{height}p{fps}/LLMHexBroadcastFixed4_{args.quality}.mp4"
        subprocess.run(["open", output_path])
