#!/usr/bin/env python3
"""
Distributed LLM inference with tree reduction for binder design.

Shows:
- 8 leaf nodes receive protein-target design queries
- Each node returns Kd binding affinity and modality
- Results flow upward through pairwise comparison stages
- Final winner (best binder) emerges at top

Legend in upper-left explains leaf node contents:
protein, target, Kd (result), modality (result)

Generated from prompt: "Distributed LLM query fan-out and tree reduction.
Results flow upward through combine levels until winner emerges."
Refined: "Add legend explaining leaf contents. Keep legend visible throughout."
"""

from manim import *
import numpy as np
import argparse

# Color scheme
COLORS = {
    "bg": "#1a1a2e",
    "node_idle": "#4a4a6a",
    "node_active": "#00d9ff",
    "node_complete": "#00ff88",
    "winner": "#ffcc00",
    "query_text": "#ff6b6b",
    "combine": "#b088f9",
    "text": "#ffffff",
    "subtext": "#aaaaaa",
    "arrow": "#00d9ff",
}

# Leaf query data
LEAF_QUERIES = [
    {"protein": "PARP16", "target": "NMNAT2", "kd": "2.3 nM", "modality": "Monobody"},
    {"protein": "PD-L1", "target": "PD-1", "kd": "0.8 nM", "modality": "Macrocycle"},
    {"protein": "KRAS", "target": "SOS1", "kd": "15 nM", "modality": "Covalent"},
    {"protein": "TNF-α", "target": "TNFR1", "kd": "45 pM", "modality": "VHH"},
    {"protein": "ACE2", "target": "Spike", "kd": "1.2 nM", "modality": "DARPin"},
    {"protein": "BCL-2", "target": "BAX", "kd": "0.3 nM", "modality": "Stapled"},
    {"protein": "MDM2", "target": "p53", "kd": "0.9 nM", "modality": "Small mol"},
    {"protein": "IL-6", "target": "IL-6R", "kd": "50 pM", "modality": "Bispecific"},
]

# Winners at each level
L1_WINNERS = [1, 3, 5, 7]  # PD-L1, TNF-α, BCL-2, IL-6


class LLMTreeReductionV3(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]

        # Y positions (bottom to top)
        Y_LEAF = -3.0       # Leaf nodes at bottom
        Y_L1 = -1.0         # Level 1 combine
        Y_L2 = 1.0          # Level 2 combine
        Y_FINAL = 2.8       # Final winner at top

        # ============================================================
        # PHASE 1: Show leaf query and create leaf nodes
        # ============================================================

        # Title
        title = Text("Distributed Binder Design Query", font_size=32, color=COLORS["text"])
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Show the leaf query template
        leaf_query_box = self.create_query_box(
            "LEAF QUERY",
            "Design the best possible binder that can inhibit\n{TARGET} interactions for {PROTEIN}",
            COLORS["query_text"]
        )
        leaf_query_box.move_to(UP * 1.5)
        self.play(FadeIn(leaf_query_box))
        self.wait(1)

        # Create 8 leaf nodes at bottom
        leaf_nodes = VGroup()
        node_spacing = 1.55
        start_x = -5.4

        for i, q in enumerate(LEAF_QUERIES):
            node = self.create_leaf_node_with_query(q)
            node.move_to(RIGHT * (start_x + i * node_spacing) + UP * Y_LEAF)
            leaf_nodes.add(node)

        # Show legend in upper left when leaf nodes appear
        legend = self.create_legend()
        legend.to_corner(UL, buff=0.4)

        # Animate nodes appearing
        self.play(
            LaggedStart(*[FadeIn(node, shift=DOWN*0.3) for node in leaf_nodes], lag_ratio=0.1),
            FadeIn(legend),
            run_time=1.5
        )

        # Show "dispatching" indicator
        dispatch_text = Text("Dispatching to 8 Aurora nodes...", font_size=22, color=COLORS["arrow"])
        dispatch_text.next_to(leaf_query_box, DOWN, buff=0.3)
        self.play(Write(dispatch_text))

        # Pulse nodes as processing
        self.play(
            *[node[0].animate.set_fill(COLORS["node_active"], opacity=0.7) for node in leaf_nodes],
            run_time=0.5
        )
        self.wait(0.5)

        self.play(FadeOut(leaf_query_box), FadeOut(dispatch_text))

        # ============================================================
        # PHASE 2: Results appear in leaf nodes
        # ============================================================

        results_label = Text("Results streaming back...", font_size=22, color=COLORS["node_complete"])
        results_label.move_to(UP * 1.5)
        self.play(Write(results_label))

        # Fill in results (staggered by latency)
        order = [6, 1, 3, 4, 0, 5, 2, 7]

        for idx in order:
            q = LEAF_QUERIES[idx]
            result_text = self.create_result_text(q["kd"], q["modality"])
            result_text.move_to(leaf_nodes[idx].get_center() + DOWN * 0.28)

            self.play(
                leaf_nodes[idx][0].animate.set_fill(COLORS["node_complete"], opacity=0.6),
                FadeIn(result_text, shift=UP*0.1),
                run_time=0.2
            )
            leaf_nodes[idx].add(result_text)

        self.play(FadeOut(results_label))
        self.wait(0.3)

        # ============================================================
        # PHASE 3: Level 1 Combine (results flow UP)
        # ============================================================

        # Show combine query
        combine_query_box = self.create_query_box(
            "COMBINE QUERY",
            "Compare designs and identify which is\nenergetically more favorable",
            COLORS["combine"]
        )
        combine_query_box.move_to(UP * 1.5)
        self.play(FadeIn(combine_query_box))
        self.wait(0.8)

        # Create L1 combine nodes ABOVE leaf nodes
        l1_nodes = VGroup()
        l1_positions = [-4.0, -1.35, 1.35, 4.0]

        for pos in l1_positions:
            node = self.create_combine_node_empty()
            node.move_to(RIGHT * pos + UP * Y_L1)
            l1_nodes.add(node)

        # Draw arrows flowing UP from leaf nodes to L1
        l1_arrows = VGroup()
        for i, l1_node in enumerate(l1_nodes):
            left_leaf = leaf_nodes[i * 2]
            right_leaf = leaf_nodes[i * 2 + 1]

            arrow_l = Arrow(left_leaf.get_top(), l1_node.get_bottom(),
                          color=COLORS["combine"], buff=0.1, stroke_width=2,
                          max_tip_length_to_length_ratio=0.15)
            arrow_r = Arrow(right_leaf.get_top(), l1_node.get_bottom(),
                          color=COLORS["combine"], buff=0.1, stroke_width=2,
                          max_tip_length_to_length_ratio=0.15)
            l1_arrows.add(arrow_l, arrow_r)

        self.play(
            *[GrowArrow(a) for a in l1_arrows],
            FadeIn(l1_nodes),
            run_time=1
        )

        self.play(FadeOut(combine_query_box))

        # Fill in L1 results
        l1_winner_data = [
            ("PD-L1", "0.8 nM"),
            ("TNF-α", "45 pM"),
            ("BCL-2", "0.3 nM"),
            ("IL-6", "50 pM"),
        ]

        for i, (l1_node, (name, kd)) in enumerate(zip(l1_nodes, l1_winner_data)):
            result = self.create_combine_result(name, kd)
            result.move_to(l1_node.get_center())

            # Highlight winner, fade loser at leaf level
            winner_idx = L1_WINNERS[i]
            loser_idx = (i * 2) if (i * 2) != winner_idx else (i * 2 + 1)

            self.play(
                l1_node[0].animate.set_fill(COLORS["combine"], opacity=0.5),
                FadeIn(result),
                leaf_nodes[winner_idx][0].animate.set_stroke(COLORS["winner"], width=3),
                leaf_nodes[loser_idx].animate.set_opacity(0.3),
                run_time=0.35
            )
            l1_node.add(result)

        self.play(FadeOut(l1_arrows))
        self.wait(0.3)

        # ============================================================
        # PHASE 4: Level 2 Combine (results continue UP)
        # ============================================================

        combine2_label = Text("Second reduction...", font_size=22, color=COLORS["combine"])
        combine2_label.move_to(UP * 2.5)
        self.play(Write(combine2_label))

        # Create L2 nodes ABOVE L1
        l2_nodes = VGroup()
        l2_positions = [-2.7, 2.7]

        for pos in l2_positions:
            node = self.create_combine_node_empty(width=1.8)
            node.move_to(RIGHT * pos + UP * Y_L2)
            l2_nodes.add(node)

        # Arrows from L1 UP to L2
        l2_arrows = VGroup()
        for i, l2_node in enumerate(l2_nodes):
            left_l1 = l1_nodes[i * 2]
            right_l1 = l1_nodes[i * 2 + 1]

            arrow_l = Arrow(left_l1.get_top(), l2_node.get_bottom(),
                          color=COLORS["combine"], buff=0.1, stroke_width=2,
                          max_tip_length_to_length_ratio=0.15)
            arrow_r = Arrow(right_l1.get_top(), l2_node.get_bottom(),
                          color=COLORS["combine"], buff=0.1, stroke_width=2,
                          max_tip_length_to_length_ratio=0.15)
            l2_arrows.add(arrow_l, arrow_r)

        self.play(
            *[GrowArrow(a) for a in l2_arrows],
            FadeIn(l2_nodes),
            FadeOut(combine2_label),
            run_time=0.8
        )

        # Fill L2 results
        l2_winner_data = [("TNF-α", "45 pM"), ("IL-6", "50 pM")]

        for i, (l2_node, (name, kd)) in enumerate(zip(l2_nodes, l2_winner_data)):
            result = self.create_combine_result(name, kd)
            result.move_to(l2_node.get_center())

            # Fade loser at L1 (PD-L1 and BCL-2)
            loser_idx = i * 2

            self.play(
                l2_node[0].animate.set_fill(COLORS["node_complete"], opacity=0.5),
                FadeIn(result),
                l1_nodes[loser_idx].animate.set_opacity(0.3),
                run_time=0.35
            )
            l2_node.add(result)

        self.play(FadeOut(l2_arrows))
        self.wait(0.3)

        # ============================================================
        # PHASE 5: Final Synthesis (winner at TOP)
        # ============================================================

        final_label = Text("Final synthesis...", font_size=22, color=COLORS["winner"])
        final_label.to_edge(UP, buff=0.5)
        self.play(FadeOut(title), Write(final_label))

        # Winner node at top
        winner_node = self.create_winner_node()
        winner_node.move_to(UP * Y_FINAL)

        # Arrows from L2 UP to winner
        final_arrows = VGroup(
            Arrow(l2_nodes[0].get_top(), winner_node.get_bottom(),
                 color=COLORS["winner"], buff=0.1, stroke_width=3,
                 max_tip_length_to_length_ratio=0.1),
            Arrow(l2_nodes[1].get_top(), winner_node.get_bottom(),
                 color=COLORS["winner"], buff=0.1, stroke_width=3,
                 max_tip_length_to_length_ratio=0.1),
        )

        self.play(
            *[GrowArrow(a) for a in final_arrows],
            run_time=0.8
        )

        self.play(
            FadeIn(winner_node),
            l2_nodes[0].animate.set_opacity(0.5),  # TNF-α loses to IL-6
            FadeOut(final_label),
            run_time=0.8
        )

        # Flash winner
        self.play(
            Flash(winner_node, color=COLORS["winner"], num_lines=16, line_length=0.5),
            winner_node.animate.scale(1.05),
            run_time=1
        )

        # Stats at bottom
        #stats = VGroup(
            #Text("8 parallel queries → 7 reductions → 1 winner", font_size=20, color=COLORS["subtext"]),
            #Text("Total time: 8.9s  |  Speedup: 3.6×", font_size=20, color=COLORS["node_complete"]),
        #).arrange(DOWN, buff=0.15)
        #stats.to_edge(DOWN, buff=0.3)

        #self.play(FadeIn(stats))
        self.wait(2)

    # ============================================================
    # Helper methods
    # ============================================================

    def create_leaf_node_with_query(self, query):
        rect = RoundedRectangle(
            width=1.45, height=1.1, corner_radius=0.1,
            color=COLORS["node_idle"], stroke_width=2
        )
        rect.set_fill(COLORS["node_idle"], opacity=0.4)

        protein = Text(query["protein"], font_size=16, color=COLORS["text"], weight=BOLD)
        target = Text(f"↔ {query['target']}", font_size=14, color=COLORS["text"])

        content = VGroup(protein, target).arrange(DOWN, buff=0.05)
        content.move_to(rect.get_center() + UP * 0.25)

        return VGroup(rect, content)

    def create_result_text(self, kd, modality):
        kd_text = Text(kd, font_size=14, color=COLORS["node_complete"], weight=BOLD)
        mod_text = Text(modality, font_size=14, color=COLORS["text"])
        return VGroup(kd_text, mod_text).arrange(DOWN, buff=0.03)

    def create_combine_node_empty(self, width=1.6):
        rect = RoundedRectangle(
            width=width, height=0.9, corner_radius=0.1,
            color=COLORS["combine"], stroke_width=2
        )
        rect.set_fill(COLORS["combine"], opacity=0.2)
        return VGroup(rect)

    def create_combine_result(self, name, kd):
        name_text = Text(name, font_size=16, color=COLORS["text"], weight=BOLD)
        kd_text = Text(kd, font_size=14, color=COLORS["node_complete"])
        return VGroup(name_text, kd_text).arrange(DOWN, buff=0.05)

    def create_query_box(self, title, query_text, color):
        box = RoundedRectangle(
            width=8, height=1.4, corner_radius=0.15,
            color=color, stroke_width=2
        )
        box.set_fill(color, opacity=0.15)

        title_text = Text(title, font_size=20, color=color, weight=BOLD)
        query = Text(query_text, font_size=20, color=COLORS["text"])

        content = VGroup(title_text, query).arrange(DOWN, buff=0.12)

        return VGroup(box, content)

    def create_legend(self):
        """Create a legend explaining leaf node contents."""
        # Example leaf node box
        box = RoundedRectangle(
            width=1.6, height=1.3, corner_radius=0.08,
            color=COLORS["node_complete"], stroke_width=2
        )
        box.set_fill(COLORS["node_complete"], opacity=0.3)

        # Content inside box - protein/target at top, results at bottom
        protein = Text("PARP16", font_size=16, color=COLORS["text"], weight=BOLD)
        target = Text("↔ NMNAT2", font_size=14, color=COLORS["text"])
        kd = Text("2.3 nM", font_size=15, color=COLORS["node_complete"], weight=BOLD)
        modality = Text("Monobody", font_size=14, color=COLORS["text"])

        top_content = VGroup(protein, target).arrange(DOWN, buff=0.06)
        bottom_content = VGroup(kd, modality).arrange(DOWN, buff=0.06)
        box_content = VGroup(top_content, bottom_content).arrange(DOWN, buff=0.15)
        box_content.move_to(box.get_center())

        example_box = VGroup(box, box_content)

        # Labels with arrows - align to right edge of box
        label_protein = Text("← protein", font_size=14, color=COLORS["subtext"])
        label_target = Text("← target", font_size=14, color=COLORS["subtext"])
        label_kd = Text("← Kd (result)", font_size=14, color=COLORS["subtext"])
        label_modality = Text("← modality (result)", font_size=14, color=COLORS["subtext"])

        # Position labels at box right edge, vertically aligned with content
        box_right = box.get_right()[0] + 0.15
        label_protein.move_to([box_right + label_protein.width/2, protein.get_center()[1], 0])
        label_target.move_to([box_right + label_target.width/2, target.get_center()[1], 0])
        label_kd.move_to([box_right + label_kd.width/2, kd.get_center()[1], 0])
        label_modality.move_to([box_right + label_modality.width/2, modality.get_center()[1], 0])

        labels = VGroup(label_protein, label_target, label_kd, label_modality)

        # Title
        title = Text("Leaf Node:", font_size=16, color=COLORS["text"], weight=BOLD)
        title.next_to(example_box, UP, buff=0.15)

        legend = VGroup(title, example_box, labels)

        # Background for legend
        bg = RoundedRectangle(
            width=legend.width + 0.3,
            height=legend.height + 0.25,
            corner_radius=0.1,
            color=COLORS["bg"],
            stroke_width=1,
            stroke_color=COLORS["subtext"]
        )
        bg.set_fill(COLORS["bg"], opacity=0.9)
        bg.move_to(legend.get_center())

        return VGroup(bg, legend)

    def create_winner_node(self):
        rect = RoundedRectangle(
            width=4.2, height=1.4, corner_radius=0.15,
            color=COLORS["winner"], stroke_width=4
        )
        rect.set_fill(COLORS["winner"], opacity=0.15)

        title = Text("★ WINNER ★", font_size=18, color=COLORS["winner"], weight=BOLD)
        name = Text("IL-6 Bispecific Nanobody", font_size=18, color=COLORS["text"], weight=BOLD)
        kd = Text("Kd = 50 pM", font_size=16, color=COLORS["node_complete"])

        content = VGroup(title, name, kd).arrange(DOWN, buff=0.08)

        return VGroup(rect, content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Tree Reduction Animation")
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
    config.output_file = f"LLMTreeReductionV3_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = LLMTreeReductionV3()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/llm_tree_reduction_v3/{height}p{fps}/LLMTreeReductionV3_{args.quality}.mp4"
        subprocess.run(["open", output_path])
