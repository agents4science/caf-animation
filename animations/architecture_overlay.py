#!/usr/bin/env python3
"""
Architecture overlay animation - tasks flow down over the architecture slide.

Shows LLMs, Agents, and Tasks flowing from the top (Science Applications)
down to HPC Systems at the bottom, flowing around the middleware boxes.

Generated from prompt: "Annotate the final slide so that we see tasks overlaid
on the figure, flowing down (avoiding the middleware bits in the middle)"
"""

from manim import *
import random
import argparse

# Colors matching deployment_flow.py
COLORS = {
    "llm": "#3498db",      # Blue for LLMs
    "agent": "#2ecc71",    # Green for Agents
    "task": "#e67e22",     # Orange for Tasks
    "active": "#f1c40f",   # Yellow when active
}


class ArchitectureOverlay(Scene):
    """
    Overlay animation on architecture slide with flowing icons.
    """

    def construct(self):
        # Load background image (990x558 pixels after cropping, aspect 1.774)
        bg_image = ImageMobject("New_Final_Slide.png")
        # Scale to fill frame height (cropped image)
        bg_image.scale_to_fit_height(config.frame_height)
        bg_image.move_to(ORIGIN)
        self.add(bg_image)

        # Project names appearing on the right before the main animation
        projects = [
            "OPAL/FAMOUS",
            "MOAT",
            "SYNAPS",
            "IGNOS",
            "COMB-FLOW",
            "GRID",
        ]

        # Create project name texts on the right side
        # Moved 1/20 left (0.71) and 1/20 down (0.4) from original position
        project_texts = []
        start_y = 1.6  # was 2.0, moved down by 0.4
        spacing = 0.6

        for i, name in enumerate(projects):
            text = Text(name, font="Arial", font_size=32, color=YELLOW, weight=BOLD)
            text.move_to(RIGHT * 5.1 + UP * (start_y - i * spacing))  # moved right to avoid collision
            text.set_opacity(0)
            project_texts.append(text)

        # Animate project names appearing one by one
        for text in project_texts:
            self.play(
                text.animate.set_opacity(1),
                run_time=0.3
            )

        # Brief hold with all names visible
        self.wait(1.5)

        # Fade out project names before main animation
        self.play(
            *[text.animate.set_opacity(0) for text in project_texts],
            run_time=0.5
        )

        # Remove the texts
        for text in project_texts:
            self.remove(text)

        random.seed(42)

        # Image mapping: 990x558 cropped image scaled to frame_height (8.0)
        # Scale factor: 8.0 / 558 ≈ 0.01434 per pixel
        # Image center is at origin after move_to(ORIGIN)
        img_w, img_h = 990, 558
        scale = config.frame_height / img_h

        def px_to_manim(px_x, px_y):
            """Convert pixel coords (from top-left) to Manim coords (center origin)."""
            mx = (px_x - img_w / 2) * scale
            my = (img_h / 2 - px_y) * scale  # flip y
            return mx, my

        # =================================================================
        # CALIBRATED POSITIONS (pixel coordinates in 990x558 CROPPED image)
        # Image: New_Final_Slide.png (cropped: left=55, top=145)
        # These are CELL CENTERS, not grid corners!
        # first_center = center of cell [0,0] (top-left cell)
        # last_center = center of cell [1,5] (bottom-right cell, for 6x2 grid)
        # =================================================================
        # Aurora:     first_center=(213, 445), last_center=(355, 474)
        # Frontier:   first_center=(468, 445), last_center=(610, 474)
        # Perlmutter: first_center=(723, 445), last_center=(865, 474)
        # Genesis box: left_edge=(310, 110), right_edge=(775, 110)
        # =================================================================

        def make_grid_positions(first_center, last_center, cols=6, rows=2):
            """Create grid cell centers by interpolating between first and last cell centers."""
            # first_center = center of cell [0,0]
            # last_center = center of cell [rows-1, cols-1]
            first_x, first_y = first_center
            last_x, last_y = last_center
            # Spacing between adjacent cell centers
            step_x = (last_x - first_x) / (cols - 1) if cols > 1 else 0
            step_y = (last_y - first_y) / (rows - 1) if rows > 1 else 0
            positions = []
            for row in range(rows):
                for col in range(cols):
                    px_x = first_x + col * step_x
                    px_y = first_y + row * step_y
                    mx, my = px_to_manim(px_x, px_y)
                    positions.append((mx, my))
            return positions

        # Use exact calibrated pixel coordinates (adjusted for cropped image)
        aurora_grid = make_grid_positions((213, 445), (355, 474))
        # Frontier and Perlmutter - adjusted for crop
        frontier_grid = make_grid_positions((468, 445), (610, 474))
        perlmutter_grid = make_grid_positions((723, 445), (865, 474))

        all_grids = [aurora_grid, frontier_grid, perlmutter_grid]


        # Calibrated Genesis box edges (adjusted for crop: -55 X, -145 Y)
        genesis_left_px = (310, 110)
        genesis_right_px = (775, 110)
        genesis_left_x, genesis_y = px_to_manim(*genesis_left_px)
        genesis_right_x, _ = px_to_manim(*genesis_right_px)

        # ============================================================
        # Icon creation functions (from deployment_flow.py)
        # ============================================================
        def create_brain(size=0.38, color=COLORS["llm"]):  # scaled by 1.5233 (was 0.25)
            """Simplified brain icon for LLMs."""
            brain = Ellipse(width=size, height=size * 0.8, color=color, fill_opacity=1)
            wave = VMobject()
            wave.set_points_smoothly([
                brain.get_center() + LEFT * size * 0.25 + UP * size * 0.1,
                brain.get_center() + UP * size * 0.15,
                brain.get_center() + RIGHT * size * 0.1 + DOWN * size * 0.05,
                brain.get_center() + RIGHT * size * 0.25 + UP * size * 0.1,
            ])
            wave.set_stroke(color=WHITE, width=1.5, opacity=0.8)
            return VGroup(brain, wave)

        def create_robot(size=0.43, color=COLORS["agent"]):  # scaled by 1.5233 (was 0.28)
            """Robot/android icon for Agents - humanoid shape."""
            body = RoundedRectangle(
                width=size * 0.6, height=size * 0.5, corner_radius=size * 0.08,
                fill_color=color, fill_opacity=1, stroke_width=0
            )
            head = Circle(radius=size * 0.25, fill_color=color, fill_opacity=1, stroke_width=0)
            head.next_to(body, UP, buff=size * 0.05)
            visor = Line(
                head.get_center() + LEFT * size * 0.15,
                head.get_center() + RIGHT * size * 0.15,
                stroke_width=3, color=WHITE
            )
            arm_l = Line(
                body.get_left() + UP * size * 0.1,
                body.get_left() + LEFT * size * 0.2 + DOWN * size * 0.15,
                stroke_width=2.5, color=color
            )
            arm_r = Line(
                body.get_right() + UP * size * 0.1,
                body.get_right() + RIGHT * size * 0.2 + DOWN * size * 0.15,
                stroke_width=2.5, color=color
            )
            return VGroup(body, head, visor, arm_l, arm_r)

        def create_cogwheel(size=0.38, color=COLORS["task"]):  # scaled by 1.5233 (was 0.25)
            """Gear/cogwheel icon for Tasks - with teeth."""
            teeth = 6
            outer_r = size * 0.5
            inner_r = size * 0.35
            points = []
            for i in range(teeth * 2):
                angle = i * PI / teeth
                r = outer_r if i % 2 == 0 else inner_r
                points.append([r * np.cos(angle), r * np.sin(angle), 0])
            gear = Polygon(*points, fill_color=color, fill_opacity=1, stroke_width=0)
            hole = Circle(radius=size * 0.12, fill_color=BLACK, fill_opacity=0.5, stroke_width=0)
            return VGroup(gear, hole)

        def get_flow_path(start_x, exit_x, avoid_zones):
            """
            Generate a path from top to bottom that avoids middleware boxes.
            Returns list of (x, y) waypoints.
            """
            # Simple path: go down left or right side, avoiding middle
            path = [(start_x, entry_y)]

            # Determine which side to flow down
            if start_x < 0:
                # Flow down left side
                side_x = -5.5
            else:
                # Flow down right side
                side_x = 5.5

            # Move to side
            path.append((side_x, entry_y - 0.5))

            # Flow down the side
            path.append((side_x, exit_y + 1.0))

            # Move to exit point
            path.append((exit_x, exit_y))

            return path

        # ============================================================
        # Storage cylinder positions (adjusted for crop: -55 X, -145 Y)
        # ============================================================
        aurora_storage = px_to_manim(402, 460)
        frontier_storage = px_to_manim(657, 460)
        perlmutter_storage = px_to_manim(912, 460)
        storage_positions = [aurora_storage, frontier_storage, perlmutter_storage]

        # ============================================================
        # Animation: Agents in 3 waves, then tasks, then communication
        # ============================================================

        self.wait(0.3)

        # Assign agents to grids: Aurora=2, Frontier=4, Perlmutter=3
        agents_per_system_count = [2, 4, 3]
        agents_per_system = [[], [], []]
        remaining_per_system = [list(grid) for grid in all_grids]

        for grid_idx in range(3):
            num_agents = agents_per_system_count[grid_idx]
            for _ in range(num_agents):
                if remaining_per_system[grid_idx]:
                    pos = remaining_per_system[grid_idx].pop(0)
                    agents_per_system[grid_idx].append(pos)

        # ============================================================
        # Phase 1: Deploy Agents with curved paths, staggered timing
        # Agents flow from Genesis box edges, curve through center, to final positions
        # ============================================================
        agent_icons = []
        agent_queues = [list(positions) for positions in agents_per_system]  # Copy

        # Create all agent icons and their paths upfront
        all_agent_data = []

        for grid_idx in range(3):
            while agent_queues[grid_idx]:
                target_x, target_y = agent_queues[grid_idx].pop(0)

                icon = create_robot(size=0.43)  # scaled by 1.5233 (was 0.28)
                # Start at left edge for Aurora (idx 0), right edge for Perlmutter (idx 2)
                # Frontier (idx 1) alternates
                if grid_idx == 0:
                    start_x = genesis_left_x + random.uniform(-0.3, 0.3)
                elif grid_idx == 2:
                    start_x = genesis_right_x + random.uniform(-0.3, 0.3)
                else:
                    # Frontier - alternate sides
                    start_x = genesis_left_x if len(all_agent_data) % 2 == 0 else genesis_right_x
                    start_x += random.uniform(-0.3, 0.3)

                start_y = genesis_y + random.uniform(-0.15, 0.15)
                icon.move_to(RIGHT * start_x + UP * start_y)
                icon.set_opacity(0)

                # Calculate midpoint - curve through center area
                center_x = 0 + random.uniform(-1.0, 1.0)
                center_y = (start_y + target_y) / 2 + random.uniform(-0.5, 0.5)

                all_agent_data.append({
                    'icon': icon,
                    'start': (start_x, start_y),
                    'mid': (center_x, center_y),
                    'target': (target_x, target_y),
                    'grid_idx': grid_idx,
                    'delay': random.uniform(0, 2.0)  # Stagger over ~2 seconds
                })
                agent_icons.append((icon, target_x, target_y, grid_idx))
                self.add(icon)

        # Sort by delay for proper sequencing
        all_agent_data.sort(key=lambda x: x['delay'])

        # Create curved path animations using bezier-like motion
        def create_curved_path_anim(data, total_duration=3.0):
            """Create animation that follows curved path through midpoint."""
            icon = data['icon']
            start_x, start_y = data['start']
            mid_x, mid_y = data['mid']
            target_x, target_y = data['target']

            # Create a path using quadratic bezier points
            path = VMobject()
            path.set_points_smoothly([
                np.array([start_x, start_y, 0]),
                np.array([mid_x, mid_y, 0]),
                np.array([target_x, target_y, 0])
            ])

            return MoveAlongPath(icon, path, rate_func=smooth)

        # Fade in all agents quickly with slight staggers
        fade_anims = []
        for i, data in enumerate(all_agent_data):
            fade_anims.append(data['icon'].animate.set_opacity(1))

        self.play(LaggedStart(*fade_anims, lag_ratio=0.15), run_time=1.5)

        # Move all agents along curved paths with staggered timing
        path_anims = [create_curved_path_anim(data) for data in all_agent_data]
        self.play(LaggedStart(*path_anims, lag_ratio=0.2), run_time=3.5)

        self.wait(0.3)

        # ============================================================
        # Phase 2: Fill ALL remaining nodes with tasks
        # ============================================================
        all_tasks = []

        # Get remaining positions for tasks (all nodes not occupied by agents)
        task_positions_per_system = remaining_per_system  # Already removed agent positions

        # Create all tasks at once
        all_task_data = []
        for grid_idx in range(3):
            system_agents = [(icon, tx, ty) for icon, tx, ty, gi in agent_icons if gi == grid_idx]
            if not system_agents:
                continue

            # Fill ALL remaining positions with tasks
            for target_x, target_y in task_positions_per_system[grid_idx]:
                source_agent, _, _ = random.choice(system_agents)
                icon = create_cogwheel(size=0.38)  # scaled (was 0.25)
                icon.move_to(source_agent.get_center())
                icon.set_opacity(0)
                all_task_data.append((icon, target_x, target_y, grid_idx))
                all_tasks.append((icon, target_x, target_y, grid_idx))
                self.add(icon)

        # Fade in all tasks with stagger
        if all_task_data:
            fade_anims = [icon.animate.set_opacity(1) for icon, _, _, _ in all_task_data]
            self.play(LaggedStart(*fade_anims, lag_ratio=0.08), run_time=1.0)

            # Move all tasks to positions with stagger
            move_anims = [icon.animate.move_to(RIGHT * tx + UP * ty) for icon, tx, ty, _ in all_task_data]
            self.play(LaggedStart(*move_anims, lag_ratio=0.08), run_time=1.5)

        self.wait(0.3)

        # ============================================================
        # Phase 3: Extended communication + task lifecycle (6 seconds)
        # Tasks fade out randomly and get replaced, continuous communication
        # ============================================================

        def create_data_cylinder(size=0.12, color="#3498db"):
            """Create a small blue cylinder for data items."""
            body = Rectangle(width=size, height=size * 1.2, fill_color=color, fill_opacity=0.9, stroke_width=0)
            top = Ellipse(width=size, height=size * 0.4, fill_color="#5dade2", fill_opacity=1, stroke_width=0)
            top.move_to(body.get_top())
            return VGroup(body, top)

        def create_comm_particle(color, size=0.12):  # scaled by 1.5233 (was 0.08)
            """Create a more visible communication particle with glow effect."""
            outer = Dot(radius=size * 1.5, color=color, fill_opacity=0.3)
            inner = Dot(radius=size, color=color, fill_opacity=1.0)
            return VGroup(outer, inner)

        # Track data items in storage - max items per system: 2, 3, 2
        storage_data_items = [[], [], []]
        max_data_items = [2, 3, 2]

        # Track active tasks and their positions for replacement
        active_tasks = list(all_tasks)  # [(icon, x, y, grid_idx), ...]

        # Run communication and task lifecycle for 6 seconds (12 rounds of 0.5s each)
        for round_num in range(12):
            particles = []
            data_items_this_round = []
            tasks_to_remove = []
            tasks_to_add = []

            # More communication particles per round (6-8 agent->task, 4-6 task->agent)
            for _ in range(random.randint(6, 8)):
                if agent_icons and active_tasks:
                    src_icon, _, _, src_gi = random.choice(agent_icons)
                    matching_tasks = [(icon, gi) for icon, _, _, gi in active_tasks if gi == src_gi]
                    if matching_tasks:
                        dst_icon, _ = random.choice(matching_tasks)
                        p = create_comm_particle(COLORS["agent"])
                        p.move_to(src_icon.get_center())
                        particles.append((p, dst_icon.get_center()))
                        self.add(p)

            for _ in range(random.randint(4, 6)):
                if active_tasks and agent_icons:
                    src_icon, _, _, src_gi = random.choice(active_tasks)
                    matching_agents = [(icon, gi) for icon, _, _, gi in agent_icons if gi == src_gi]
                    if matching_agents:
                        dst_icon, _ = random.choice(matching_agents)
                        p = create_comm_particle(COLORS["task"])
                        p.move_to(src_icon.get_center())
                        particles.append((p, dst_icon.get_center()))
                        self.add(p)

            # Task lifecycle: randomly fade out 1-3 tasks and replace them
            if round_num >= 2 and active_tasks:  # Start after initial setup
                num_to_replace = random.randint(1, min(3, len(active_tasks)))
                tasks_to_fade = random.sample(active_tasks, num_to_replace)

                for old_icon, old_x, old_y, grid_idx in tasks_to_fade:
                    tasks_to_remove.append((old_icon, old_x, old_y, grid_idx))

                    # Create replacement task from an agent
                    system_agents = [(icon, gi) for icon, _, _, gi in agent_icons if gi == grid_idx]
                    if system_agents:
                        source_agent, _ = random.choice(system_agents)
                        new_icon = create_cogwheel(size=0.38)  # scaled (was 0.25)
                        new_icon.move_to(source_agent.get_center())
                        new_icon.set_opacity(0)
                        tasks_to_add.append((new_icon, old_x, old_y, grid_idx))
                        self.add(new_icon)

            # Data items to storage (spread throughout the rounds)
            if round_num in [2, 5, 8]:
                for grid_idx in range(3):
                    system_agents = [(icon, gi) for icon, _, _, gi in agent_icons if gi == grid_idx]
                    if system_agents and len(storage_data_items[grid_idx]) < max_data_items[grid_idx]:
                        src_icon, _ = random.choice(system_agents)
                        storage_x, storage_y = storage_positions[grid_idx]

                        data_item = create_data_cylinder(size=0.24)  # scaled (was 0.16)
                        data_item.move_to(src_icon.get_center())
                        data_item.set_opacity(0)

                        num_items = len(storage_data_items[grid_idx])
                        offset_x = (num_items % 2 - 0.5) * 0.24
                        offset_y = (num_items // 2 - 0.5) * 0.30
                        final_pos = RIGHT * (storage_x + offset_x) + UP * (storage_y + offset_y)

                        data_items_this_round.append((data_item, final_pos, grid_idx))
                        storage_data_items[grid_idx].append(data_item)
                        self.add(data_item)

            # Build animations for this round
            anims = []

            # Particle movement
            for p, dst in particles:
                anims.append(p.animate.move_to(dst))

            # Data items fade in and move
            for item, final_pos, _ in data_items_this_round:
                anims.append(item.animate.set_opacity(1).move_to(final_pos))

            # Fade out old tasks
            for old_icon, _, _, _ in tasks_to_remove:
                anims.append(old_icon.animate.set_opacity(0))

            # Fade in and move new tasks
            for new_icon, tx, ty, _ in tasks_to_add:
                anims.append(new_icon.animate.set_opacity(1).move_to(RIGHT * tx + UP * ty))

            # Play all animations together
            if anims:
                self.play(*anims, run_time=0.5)

            # Cleanup: remove particles and old tasks, update active_tasks list
            for p, _ in particles:
                self.remove(p)

            for old_icon, old_x, old_y, grid_idx in tasks_to_remove:
                self.remove(old_icon)
                active_tasks.remove((old_icon, old_x, old_y, grid_idx))

            for new_icon, tx, ty, grid_idx in tasks_to_add:
                active_tasks.append((new_icon, tx, ty, grid_idx))

        # Final pulse on all remaining icons
        all_icons = [icon for icon, _, _, _ in agent_icons] + [icon for icon, _, _, _ in active_tasks]
        self.play(
            *[icon.animate.scale(1.15) for icon in all_icons],
            run_time=0.25
        )
        self.play(
            *[icon.animate.scale(1/1.15) for icon in all_icons],
            run_time=0.25
        )

        # 8 seconds holding the final state
        self.wait(8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Architecture Overlay Animation")
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
    config.output_file = f"ArchitectureOverlay_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = ArchitectureOverlay()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/{height}p{fps}/ArchitectureOverlay_{args.quality}.mp4"
        subprocess.run(["open", output_path])
