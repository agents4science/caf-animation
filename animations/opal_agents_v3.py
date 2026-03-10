#!/usr/bin/env python3
"""
OPAL Agents Animation V3 - Simplified intro with gradual agent introduction.

Structure:
1. Problem statement - what challenge are we solving
2. Solution intro - AI agents collaborate
3. Agents introduced one by one
4. Collaboration visualization
5. Results/Impact statement

Generated from feedback: "First slide too complicated. Break it up.
Say something about problems being addressed. Make a statement about impact."
"""

from manim import *
import random
import os
import argparse


class OpalAgentsV3(Scene):
    """
    Redesigned OPAL animation with clearer narrative flow.
    """

    def construct(self):
        self.camera.background_color = "#0d1b2a"
        random.seed(42)

        # ============================================================
        # PHASE 1: Problem Statement
        # ============================================================

        problem_title = Text(
            "The Challenge",
            font="Arial", font_size=44, color=WHITE, weight=BOLD
        )
        problem_title.to_edge(UP, buff=0.8)

        problem_text = Text(
            "Design protein binders to inhibit specified targets",
            font="Arial", font_size=28, color=GRAY_B
        )
        problem_text.next_to(problem_title, DOWN, buff=0.4)

        # More interesting protein shape - blob-like
        def create_protein_blob(color, num_bumps=6, radius=0.8):
            points = []
            for i in range(num_bumps * 4):
                angle = i * TAU / (num_bumps * 4)
                r = radius * (1 + 0.2 * np.sin(num_bumps * angle))
                points.append([r * np.cos(angle), r * np.sin(angle), 0])
            blob = Polygon(*points, fill_color=color, fill_opacity=0.7, stroke_color=color, stroke_width=2)
            return blob

        protein = create_protein_blob(BLUE, num_bumps=5, radius=0.7)
        protein.shift(LEFT * 2.0 + DOWN * 0.3)
        protein_label = Text("Designed\nBinder", font="Arial", font_size=16, color=BLUE)
        protein_label.next_to(protein, DOWN, buff=0.15)

        target = create_protein_blob(RED, num_bumps=7, radius=0.6)
        target.shift(RIGHT * 2.0 + DOWN * 0.3)
        target_label = Text("Designated\nTarget", font="Arial", font_size=16, color=RED)
        target_label.next_to(target, DOWN, buff=0.15)

        # Arrow with question mark
        arrow = Arrow(LEFT * 0.8 + DOWN * 0.3, RIGHT * 0.8 + DOWN * 0.3, color=YELLOW, stroke_width=4)
        question = Text("?", font="Arial", font_size=48, color=YELLOW)
        question.next_to(arrow, UP, buff=0.1)

        self.play(Write(problem_title), run_time=0.6)
        self.play(Write(problem_text), run_time=0.6)
        self.play(
            FadeIn(protein), FadeIn(protein_label),
            FadeIn(target), FadeIn(target_label),
            run_time=0.6
        )
        self.play(GrowArrow(arrow), Write(question), run_time=0.5)
        self.wait(1.0)

        # Clear phase 1
        self.play(
            FadeOut(problem_title), FadeOut(problem_text),
            FadeOut(protein), FadeOut(protein_label),
            FadeOut(target), FadeOut(target_label),
            FadeOut(arrow), FadeOut(question),
            run_time=0.5
        )

        # ============================================================
        # PHASE 2: Solution - AI Agents
        # ============================================================

        solution_title = Text(
            "The Solution: AI Agent Teams",
            font="Arial", font_size=38, color=WHITE, weight=BOLD
        )
        solution_title.to_edge(UP, buff=0.8)

        solution_text = Text(
            "Specialized agents collaborate to explore the design space",
            font="Arial", font_size=24, color=GRAY_B
        )
        solution_text.next_to(solution_title, DOWN, buff=0.3)

        self.play(Write(solution_title), run_time=0.6)
        self.play(Write(solution_text), run_time=0.6)
        self.wait(0.5)

        # ============================================================
        # PHASE 3: Introduce agents one by one
        # ============================================================

        # Agent definitions with positions, colors, and icons
        agents_info = [
            ("Literature", LEFT * 4.5 + UP * 0.3, BLUE_D, "10K papers"),
            ("Hypothesis", LEFT * 1.5 + UP * 0.3, GREEN_D, "Novel designs"),
            ("Simulation", RIGHT * 1.5 + UP * 0.3, ORANGE, "4,000 parallel"),
            ("Analysis", RIGHT * 4.5 + UP * 0.3, PURPLE, "Ranks results"),
        ]

        # Icon creation functions
        def create_book_icon(color):
            book = VGroup()
            cover = Rectangle(width=0.35, height=0.45, fill_color=color, fill_opacity=0.8, stroke_width=1)
            spine = Line(cover.get_left() + RIGHT * 0.05, cover.get_left() + RIGHT * 0.05 + DOWN * 0.45, stroke_width=2, color=WHITE)
            lines = VGroup(*[Line(LEFT * 0.1, RIGHT * 0.1, stroke_width=1, color=WHITE).shift(UP * (0.1 - i * 0.12)) for i in range(3)])
            lines.move_to(cover.get_center())
            return VGroup(cover, spine, lines)

        def create_lightbulb_icon(color):
            bulb = Circle(radius=0.18, fill_color=YELLOW, fill_opacity=0.9, stroke_width=0)
            base = Rectangle(width=0.12, height=0.1, fill_color=GRAY, fill_opacity=0.9, stroke_width=0)
            base.next_to(bulb, DOWN, buff=0)
            rays = VGroup(*[Line(ORIGIN, UP * 0.12, stroke_width=2, color=YELLOW).rotate(i * TAU / 6).shift(UP * 0.28) for i in range(6)])
            return VGroup(bulb, base, rays)

        def create_computer_icon(color):
            screen = Rectangle(width=0.4, height=0.3, fill_color=color, fill_opacity=0.6, stroke_color=WHITE, stroke_width=1)
            base = Rectangle(width=0.15, height=0.08, fill_color=GRAY, fill_opacity=0.8, stroke_width=0)
            base.next_to(screen, DOWN, buff=0.02)
            stand = Rectangle(width=0.25, height=0.03, fill_color=GRAY, fill_opacity=0.8, stroke_width=0)
            stand.next_to(base, DOWN, buff=0)
            return VGroup(screen, base, stand)

        def create_chart_icon(color):
            bars = VGroup()
            heights = [0.15, 0.3, 0.22, 0.38]
            for i, h in enumerate(heights):
                bar = Rectangle(width=0.08, height=h, fill_color=color, fill_opacity=0.8, stroke_width=0)
                bar.move_to(RIGHT * (i - 1.5) * 0.12 + UP * h / 2)
                bars.add(bar)
            axis = Line(LEFT * 0.25 + DOWN * 0.02, RIGHT * 0.25 + DOWN * 0.02, stroke_width=1, color=WHITE)
            return VGroup(bars, axis)

        icon_funcs = [create_book_icon, create_lightbulb_icon, create_computer_icon, create_chart_icon]

        agents = []
        agent_markers = []

        for i, (name, pos, color, description) in enumerate(agents_info):
            # Agent box
            box = RoundedRectangle(
                width=1.8, height=1.4, corner_radius=0.15,
                fill_color=color, fill_opacity=0.25,
                stroke_color=color, stroke_width=3
            )
            box.move_to(pos + DOWN * 0.7)

            # Icon at top of box
            icon = icon_funcs[i](color)
            icon.scale(0.9)
            icon.move_to(box.get_center() + UP * 0.35)

            # Agent name below icon
            label = Text(name, font="Arial", font_size=18, color=WHITE, weight=BOLD)
            label.move_to(box.get_center() + DOWN * 0.15)

            # Description at bottom
            desc = Text(description, font="Arial", font_size=14, color=GRAY_B)
            desc.move_to(box.get_center() + DOWN * 0.5)

            agent_group = VGroup(box, icon, label, desc)
            agents.append(agent_group)
            agent_markers.append(box)

            # Animate each agent appearing
            self.play(
                FadeIn(box, shift=UP * 0.3),
                FadeIn(icon),
                Write(label),
                FadeIn(desc),
                run_time=0.5
            )

        self.wait(0.5)

        # ============================================================
        # PHASE 4: Collaboration - messages between agents
        # ============================================================

        collab_text = Text(
            "Agents communicate and coordinate",
            font="Arial", font_size=24, color=YELLOW
        )
        collab_text.next_to(solution_title, DOWN, buff=0.3)

        self.play(Transform(solution_text, collab_text), run_time=0.4)

        # Message passing animation
        message_pairs = [
            (0, 1), (1, 2), (2, 3), (3, 1), (1, 0), (2, 1), (0, 2), (3, 2)
        ]

        for round_num in range(2):
            particles = []
            for i, (src, dst) in enumerate(message_pairs[round_num*4:(round_num+1)*4]):
                src_pos = agent_markers[src].get_center()
                dst_pos = agent_markers[dst].get_center()

                particle = Dot(radius=0.1, color=WHITE)
                particle.move_to(src_pos)
                particles.append((particle, dst_pos))
                self.add(particle)

            # Move all particles
            self.play(
                *[p.animate.move_to(dst) for p, dst in particles],
                run_time=0.5
            )

            # Pulse destination agents
            dsts = set([dst for _, dst_idx in enumerate(message_pairs[round_num*4:(round_num+1)*4]) for dst in [message_pairs[round_num*4 + _][1]]])
            self.play(
                *[agent_markers[d].animate.set_stroke(WHITE, width=5) for d in dsts],
                run_time=0.2
            )
            self.play(
                *[agent_markers[d].animate.set_stroke(agents_info[d][2], width=3) for d in dsts],
                run_time=0.2
            )

            for p, _ in particles:
                self.remove(p)

        # ============================================================
        # PHASE 5: HPC Integration
        # ============================================================

        hpc_text = Text(
            "Powered by HPC: thousands of parallel evaluations",
            font="Arial", font_size=24, color=TEAL
        )
        hpc_text.next_to(solution_title, DOWN, buff=0.3)

        self.play(Transform(solution_text, hpc_text), run_time=0.4)

        # Show compute tasks spawning from Simulation agent
        sim_agent = agent_markers[2]

        # Create HPC visual below
        hpc_nodes = VGroup()
        for row in range(2):
            for col in range(8):
                node = Square(side_length=0.25, fill_color=TEAL_E, fill_opacity=0.6, stroke_width=1)
                node.move_to(LEFT * 1.75 + RIGHT * col * 0.35 + DOWN * 2.5 + DOWN * row * 0.35)
                hpc_nodes.add(node)

        hpc_label = Text("Aurora Supercomputer", font="Arial", font_size=16, color=TEAL)
        hpc_label.next_to(hpc_nodes, DOWN, buff=0.2)

        self.play(FadeIn(hpc_nodes), FadeIn(hpc_label), run_time=0.5)

        # Tasks flow to HPC
        for _ in range(2):
            tasks = []
            target_nodes = random.sample(list(hpc_nodes), 6)
            for node in target_nodes:
                task = Dot(radius=0.08, color=ORANGE)
                task.move_to(sim_agent.get_center())
                tasks.append((task, node))
                self.add(task)

            self.play(
                *[t.animate.move_to(n.get_center()) for t, n in tasks],
                run_time=0.4
            )
            self.play(
                *[n.animate.set_fill(ORANGE, opacity=0.8) for _, n in tasks],
                run_time=0.2
            )
            self.play(
                *[n.animate.set_fill(TEAL_E, opacity=0.6) for _, n in tasks],
                run_time=0.2
            )
            for t, _ in tasks:
                self.remove(t)

        # ============================================================
        # PHASE 6: Results / Impact
        # ============================================================

        self.play(
            FadeOut(hpc_nodes), FadeOut(hpc_label),
            *[FadeOut(a) for a in agents],
            FadeOut(solution_text),
            run_time=0.5
        )

        result_title = Text(
            "Results: Accelerating Drug Discovery",
            font="Arial", font_size=38, color=GREEN, weight=BOLD
        )
        result_title.move_to(solution_title.get_center())

        self.play(Transform(solution_title, result_title), run_time=0.5)

        # Impact stats with numbers
        stats = [
            ("4,000", "parallel LLM evaluations"),
            ("50 pM", "binding affinity achieved"),
            ("48 hrs", "design to candidate"),
        ]

        stat_groups = VGroup()
        for i, (number, label) in enumerate(stats):
            num_text = Text(number, font="Arial", font_size=42, color=YELLOW, weight=BOLD)
            label_text = Text(label, font="Arial", font_size=22, color=WHITE)
            label_text.next_to(num_text, DOWN, buff=0.1)
            stat_group = VGroup(num_text, label_text)
            stat_group.move_to(LEFT * 3.5 + RIGHT * i * 3.5 + DOWN * 0.5)
            stat_groups.add(stat_group)

        for sg in stat_groups:
            self.play(FadeIn(sg, shift=UP * 0.2), run_time=0.4)

        self.wait(1)

        # Final statement
        final_text = Text(
            "AI agents transforming biologics discovery",
            font="Arial", font_size=26, color=TEAL, weight=BOLD
        )
        final_text.move_to(DOWN * 2.2)
        self.play(FadeIn(final_text), run_time=0.5)

        self.wait(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OPAL Agents Animation V3")
    parser.add_argument(
        "quality",
        nargs="?",
        default="low",
        choices=["low", "medium", "high", "4k"],
        help="Output quality (default: low)"
    )
    parser.add_argument("--preview", "-p", action="store_true", help="Preview after rendering")
    args = parser.parse_args()

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
    config.output_file = f"OpalAgentsV3_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = OpalAgentsV3()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/{height}p{fps}/OpalAgentsV3_{args.quality}.mp4"
        subprocess.run(["open", output_path])
