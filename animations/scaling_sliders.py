from manim import *
import random
import argparse


class AgenticScalingSliders(Scene):
    """
    Control panel with three sliders showing the scaling dimensions of
    the Common Agentic Framework:
    - Entity Count (agents, tools)
    - Interaction Intensity (communication variety/volume)
    - Persistence (state maintenance over time)
    """

    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # Add title at the top - 5% from top, Arial font, 36pt
        title = Text(
            "DOE Agentic Science Must Scale Along 3 Dimensions",
            font="Arial",
            font_size=36,
            color=WHITE,
            weight=BOLD
        )
        title.to_edge(UP, buff=0.4)
        self.add(title)

        # Create three slider panels
        slider_width = 0.4
        slider_height = 2.5
        panel_width = 3.8
        panel_height = 4.0

        # Colors for each dimension
        entity_color = BLUE
        interaction_color = GREEN
        persistence_color = ORANGE

        # Create the three panels with sliders and visualization areas
        panels = []
        sliders = []
        viz_areas = []
        slider_fills = []
        slider_knobs = []
        value_texts = []

        labels = ["Entity Count", "Interaction Intensity", "Persistence"]
        colors = [entity_color, interaction_color, persistence_color]

        for i, (label, color) in enumerate(zip(labels, colors)):
            # Panel background
            panel = RoundedRectangle(
                width=panel_width, height=panel_height,
                corner_radius=0.15,
                fill_color="#252540",
                fill_opacity=0.9,
                stroke_color=color,
                stroke_width=2
            )

            # Position panels horizontally
            x_pos = (i - 1) * (panel_width + 0.3)
            panel.move_to(DOWN * 0.3 + RIGHT * x_pos)
            panels.append(panel)

            # Label at top of panel
            panel_label = Text(label, font_size=20, color=color, weight=BOLD)
            panel_label.move_to(panel.get_top() + DOWN * 0.35)

            # Slider track (on the left side of panel)
            track = RoundedRectangle(
                width=slider_width, height=slider_height,
                corner_radius=0.1,
                fill_color="#1a1a2e",
                fill_opacity=1,
                stroke_color=GRAY,
                stroke_width=1
            )
            track.move_to(panel.get_left() + RIGHT * 0.5 + DOWN * 0.3)

            # Slider fill (starts empty)
            fill = Rectangle(
                width=slider_width - 0.1, height=0.01,
                fill_color=color,
                fill_opacity=0.8,
                stroke_width=0
            )
            fill.move_to(track.get_bottom() + UP * 0.05)
            fill.align_to(track, DOWN)
            slider_fills.append(fill)

            # Slider knob
            knob = Circle(
                radius=0.15,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_color=color,
                stroke_width=3
            )
            knob.move_to(track.get_bottom() + UP * 0.15)
            slider_knobs.append(knob)

            # Value text placeholder (not displayed)
            value_text = Text("", font_size=16, color=WHITE)
            value_text.move_to(track.get_bottom() + DOWN * 0.3)
            value_texts.append(value_text)

            # Visualization area (right side of panel)
            viz_area = RoundedRectangle(
                width=panel_width - 1.2, height=slider_height + 0.4,
                corner_radius=0.1,
                fill_color="#1a1a2e",
                fill_opacity=1,
                stroke_color=GRAY,
                stroke_width=1
            )
            viz_area.move_to(panel.get_center() + RIGHT * 0.35 + DOWN * 0.2)
            viz_areas.append(viz_area)

            sliders.append({
                'track': track,
                'fill': fill,
                'knob': knob,
                'value_text': value_text,
                'label': panel_label,
                'viz_area': viz_area,
                'color': color
            })

            # Add to scene (value_text omitted - no percentage display)
            self.add(panel, panel_label, track, fill, knob, viz_area)

        # Add subtitle text under each panel
        subtitles = ["Agents, Tools", "Point-to-Point→Broadcast", "Transient→Months"]
        for i, (panel, subtitle_text) in enumerate(zip(panels, subtitles)):
            subtitle = Text(subtitle_text, font="Arial", font_size=16, color=GRAY_B)
            subtitle.move_to(panel.get_bottom() + DOWN * 0.25)
            self.add(subtitle)

        # Initial pause to let viewers read the title and layout
        self.wait(6.5)

        # Animate each slider with its visualization

        # 1. ENTITY COUNT - Show agents and tools accumulating
        self.animate_entity_count(sliders[0], slider_height)
        self.wait(0.3)

        # 2. INTERACTION INTENSITY - Show network connections
        self.animate_interaction_intensity(sliders[1], slider_height)
        self.wait(0.3)

        # 3. PERSISTENCE - Show timeline with state
        self.animate_persistence(sliders[2], slider_height)
        self.wait(1.0)

    def animate_entity_count(self, slider, slider_height):
        """Animate the entity count slider with agents/tools appearing"""
        viz_area = slider['viz_area']
        color = slider['color']

        # Create agent and tool icons
        def create_agent(size=0.15):
            head = Circle(radius=size * 0.35, fill_color=BLUE_D, fill_opacity=1,
                         stroke_width=1, stroke_color=BLUE_E)
            head.shift(UP * size * 0.5)
            body = Triangle(fill_color=BLUE_D, fill_opacity=1,
                           stroke_width=1, stroke_color=BLUE_E)
            body.scale(size * 0.5)
            body.shift(DOWN * size * 0.1)
            return VGroup(head, body)

        def create_tool(size=0.15):
            gear = RegularPolygon(n=6, fill_color=TEAL, fill_opacity=1,
                                  stroke_width=1, stroke_color=TEAL_E)
            gear.scale(size * 0.4)
            hole = Circle(radius=size * 0.12, fill_color="#1a1a2e", fill_opacity=1, stroke_width=0)
            return VGroup(gear, hole)

        # Generate entities in a grid to avoid overlaps
        num_entities = 125
        entities = []
        random.seed(42)

        viz_center = viz_area.get_center()
        viz_w = viz_area.width * 0.9
        viz_h = viz_area.height * 0.9

        # Grid layout - compute rows and cols
        icon_size = 0.08
        spacing = 0.18
        cols = int(viz_w / spacing)
        rows = int(viz_h / spacing)

        # Generate grid positions
        positions = []
        for row in range(rows):
            for col in range(cols):
                x = viz_center[0] - viz_w/2 + (col + 0.5) * (viz_w / cols)
                y = viz_center[1] - viz_h/2 + (row + 0.5) * (viz_h / rows)
                # Add small jitter to avoid perfect grid look
                x += random.uniform(-0.02, 0.02)
                y += random.uniform(-0.02, 0.02)
                positions.append([x, y, 0])

        # Shuffle and take num_entities
        random.shuffle(positions)
        positions = positions[:num_entities]

        for pos in positions:
            if random.random() < 0.35:
                icon = create_tool(size=icon_size)
            else:
                icon = create_agent(size=icon_size)

            icon.move_to(pos)
            icon.set_opacity(0)
            entities.append(icon)
            self.add(icon)

        # Animate slider and entities together
        track_bottom = slider['track'].get_bottom()[1]
        track_top = slider['track'].get_top()[1]

        # Animate in steps - more steps for more entities
        steps = 10
        batch_size = num_entities // steps

        for step in range(steps):
            progress = (step + 1) / steps
            new_height = slider_height * progress
            new_knob_y = track_bottom + 0.15 + (slider_height - 0.1) * progress

            # Update slider
            new_fill = Rectangle(
                width=slider['fill'].width, height=new_height,
                fill_color=color, fill_opacity=0.8, stroke_width=0
            )
            # Position at track's x-coordinate and align to bottom
            track_center = slider['track'].get_center()
            new_fill.move_to([track_center[0], track_bottom + new_height/2 + 0.05, 0])

            # Entities for this batch
            batch_start = step * batch_size
            batch_end = min((step + 1) * batch_size, num_entities)
            batch = entities[batch_start:batch_end]

            anims = [
                Transform(slider['fill'], new_fill),
                slider['knob'].animate.move_to([slider['knob'].get_center()[0], new_knob_y, 0]),
            ]
            anims.extend([e.animate.set_opacity(1) for e in batch])

            self.play(*anims, run_time=0.25)

    def animate_interaction_intensity(self, slider, slider_height):
        """Animate interaction intensity with network connections and many messages"""
        viz_area = slider['viz_area']
        color = slider['color']

        # Create nodes
        num_nodes = 8
        nodes = []
        viz_center = viz_area.get_center()
        radius = min(viz_area.width, viz_area.height) * 0.35

        for i in range(num_nodes):
            angle = i * TAU / num_nodes
            pos = viz_center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            node = Dot(pos, radius=0.08, color=GREEN_D)
            nodes.append(node)
            self.add(node)

        # Create connections (edges) - will reveal progressively
        all_edges = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                edge = Line(
                    nodes[i].get_center(), nodes[j].get_center(),
                    stroke_width=2, color=GREEN
                )
                edge.set_opacity(0)
                all_edges.append(edge)
                self.add(edge)

        random.shuffle(all_edges)

        # Animate slider and connections
        track_bottom = slider['track'].get_bottom()[1]
        steps = 5
        edges_per_step = len(all_edges) // steps

        for step in range(steps):
            progress = (step + 1) / steps
            new_height = slider_height * progress
            new_knob_y = track_bottom + 0.15 + (slider_height - 0.1) * progress

            new_fill = Rectangle(
                width=slider['fill'].width, height=new_height,
                fill_color=color, fill_opacity=0.8, stroke_width=0
            )
            # Position at track's x-coordinate and align to bottom
            track_center = slider['track'].get_center()
            new_fill.move_to([track_center[0], track_bottom + new_height/2 + 0.05, 0])

            # Edges for this step
            edge_start = step * edges_per_step
            edge_end = min((step + 1) * edges_per_step, len(all_edges))
            batch_edges = all_edges[edge_start:edge_end]

            anims = [
                Transform(slider['fill'], new_fill),
                slider['knob'].animate.move_to([slider['knob'].get_center()[0], new_knob_y, 0]),
            ]
            anims.extend([e.animate.set_opacity(0.6) for e in batch_edges])

            self.play(*anims, run_time=0.4)

        # Add many animated "messages" flowing simultaneously
        num_message_waves = 5
        messages_per_wave = 8

        for wave in range(num_message_waves):
            particles = []
            animations = []

            for _ in range(messages_per_wave):
                edge = random.choice(all_edges)
                # Randomly choose direction
                if random.random() < 0.5:
                    start = edge.get_start()
                    end = edge.get_end()
                else:
                    start = edge.get_end()
                    end = edge.get_start()

                particle = Dot(start, radius=0.04, color=WHITE)
                particles.append(particle)
                self.add(particle)
                animations.append(particle.animate.move_to(end))

            self.play(*animations, run_time=0.25)

            for p in particles:
                self.remove(p)

    def animate_persistence(self, slider, slider_height):
        """Animate persistence with day counter showing long-term operation"""
        viz_area = slider['viz_area']
        color = slider['color']
        viz_center = viz_area.get_center()

        # Milestones: (number, label, slider_progress)
        milestones = [
            ("1", "day", 0.2),
            ("7", "days", 0.4),
            ("30", "days", 0.6),
            ("90", "days", 0.8),
            ("365", "days", 1.0),
        ]

        # Create initial counter display
        day_count = Text("1", font_size=72, color=ORANGE, weight=BOLD)
        day_count.move_to(viz_center + UP * 0.2)

        day_label = Text("day", font_size=28, color=GRAY_B)
        day_label.move_to(viz_center + DOWN * 0.6)

        self.add(day_count, day_label)

        # Animate slider with counter milestones
        track_bottom = slider['track'].get_bottom()[1]

        for i, (num, label, progress) in enumerate(milestones):
            new_height = slider_height * progress
            new_knob_y = track_bottom + 0.15 + (slider_height - 0.1) * progress

            new_fill = Rectangle(
                width=slider['fill'].width, height=new_height,
                fill_color=color, fill_opacity=0.8, stroke_width=0
            )
            track_center = slider['track'].get_center()
            new_fill.move_to([track_center[0], track_bottom + new_height/2 + 0.05, 0])

            # New counter text
            new_day_count = Text(num, font_size=72, color=ORANGE, weight=BOLD)
            new_day_count.move_to(viz_center + UP * 0.2)

            new_day_label = Text(label, font_size=28, color=GRAY_B)
            new_day_label.move_to(viz_center + DOWN * 0.6)

            anims = [
                Transform(slider['fill'], new_fill),
                slider['knob'].animate.move_to([slider['knob'].get_center()[0], new_knob_y, 0]),
                Transform(day_count, new_day_count),
                Transform(day_label, new_day_label),
            ]

            self.play(*anims, run_time=0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agentic Scaling Sliders Animation")
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
    config.output_file = f"AgenticScalingSliders_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = AgenticScalingSliders()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/{height}p{fps}/AgenticScalingSliders_{args.quality}.mp4"
        subprocess.run(["open", output_path])
