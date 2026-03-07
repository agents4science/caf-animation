from manim import *
import random
import os
import argparse


class OpalAgentsAnimation(Scene):
    """
    Animation showing agents communicating over the OPAL architecture diagram.
    Messages flow between agents, and some trigger compute task generation.
    """

    def construct(self):
        # Load background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(script_dir, "..", "assets", "OPAL-SPLASH.png")
        background = ImageMobject(bg_path)

        # Scale to fit full image width (no cropping)
        background.width = config.frame_width
        background.move_to(ORIGIN)
        self.add(background)

        # Define agent positions (mapped to image locations)
        # Positions are approximate based on the image layout
        agents = {
            "user": np.array([-6.0, 0.0, 0]),
            "literature": np.array([-3.2, 1.8, 0]),
            "optimization": np.array([-3.2, -1.5, 0]),
            "planning_top": np.array([0.3, 1.2, 0]),
            "planning_bottom": np.array([0.3, -0.8, 0]),
            "simulation": np.array([3.5, 1.8, 0]),
            "binder": np.array([3.5, -1.2, 0]),
            "resources": np.array([6.0, 0.0, 0]),
        }

        # Create agent markers (larger, more obvious)
        agent_markers = {}
        agent_glows = {}

        for name, pos in agents.items():
            # Outer glow - larger and brighter
            glow = Circle(radius=0.6, color=YELLOW, fill_opacity=0.35, stroke_width=0)
            glow.move_to(pos)

            # Inner marker - larger and more visible
            marker = Circle(radius=0.25, color=YELLOW, fill_opacity=1.0, stroke_width=3, stroke_color=WHITE)
            marker.move_to(pos)

            # Add a label dot in center for emphasis
            center_dot = Dot(pos, radius=0.08, color=WHITE)

            agent_markers[name] = VGroup(marker, center_dot)
            agent_glows[name] = glow

        # Add all markers
        for name in agents:
            self.add(agent_glows[name], agent_markers[name])

        # Animate markers appearing
        self.play(
            *[GrowFromCenter(agent_markers[name]) for name in agents],
            *[FadeIn(agent_glows[name]) for name in agents],
            run_time=0.8
        )

        # Pulse the markers
        self.play(
            *[agent_glows[name].animate.scale(1.4).set_opacity(0.15) for name in agents],
            run_time=0.4
        )
        self.play(
            *[agent_glows[name].animate.scale(1/1.4).set_opacity(0.35) for name in agents],
            run_time=0.4
        )

        self.wait(0.3)

        # Define message flows
        # Each flow: (from_agent, to_agent, triggers_compute, num_tasks)
        message_flows = [
            # User sends request to planning
            ("user", "planning_top", False, 0),
            # Planning queries literature and simulation
            ("planning_top", "literature", False, 0),
            ("planning_top", "simulation", True, 20),  # Triggers 20 compute tasks
            # Literature responds
            ("literature", "planning_top", False, 0),
            # Simulation spawns compute tasks and responds
            ("simulation", "planning_bottom", False, 0),
            # Planning coordinates with optimization
            ("planning_bottom", "optimization", False, 0),
            # Optimization queries binder design
            ("optimization", "binder", True, 20),  # Triggers 20 compute tasks
            # Binder accesses resources
            ("binder", "resources", False, 0),
            # Resources respond
            ("resources", "binder", False, 0),
            # Results flow back
            ("binder", "planning_bottom", False, 0),
            ("planning_bottom", "user", False, 0),
        ]

        # Animate message flows
        for from_agent, to_agent, triggers_compute, num_tasks in message_flows:
            start_pos = agents[from_agent]
            end_pos = agents[to_agent]

            # Create message particle - more visible
            message = Dot(start_pos, radius=0.18, color=BLUE)
            message.set_stroke(WHITE, width=2)

            # Create trail - thicker and brighter
            trail = TracedPath(
                message.get_center,
                dissipating_time=0.5,
                stroke_width=5,
                stroke_color=BLUE_A
            )

            self.add(trail, message)

            # Animate message traveling
            self.play(
                message.animate.move_to(end_pos),
                run_time=0.4,
                rate_func=smooth
            )

            # Highlight receiving agent
            self.play(
                agent_markers[to_agent].animate.scale(1.3),
                agent_glows[to_agent].animate.set_color(BLUE).set_opacity(0.5),
                run_time=0.15
            )

            # If triggers compute, spawn compute tasks
            if triggers_compute and num_tasks > 0:
                self.spawn_compute_tasks(end_pos, num_tasks=num_tasks)

            # Reset agent appearance
            self.play(
                agent_markers[to_agent].animate.scale(1/1.3),
                agent_glows[to_agent].animate.set_color(YELLOW).set_opacity(0.35),
                run_time=0.15
            )

            self.remove(message, trail)

        # Final flourish - all agents pulse together
        self.play(
            *[agent_glows[name].animate.scale(1.5).set_opacity(0.5).set_color(GREEN) for name in agents],
            *[agent_markers[name].animate.scale(1.2) for name in agents],
            run_time=0.4
        )
        self.play(
            *[agent_glows[name].animate.scale(1/1.5).set_opacity(0.35).set_color(YELLOW) for name in agents],
            *[agent_markers[name].animate.scale(1/1.2) for name in agents],
            run_time=0.4
        )

        self.wait(1.0)

    def spawn_compute_tasks(self, center_pos, num_tasks=10):
        """Spawn compute tasks in a 4x5 grid below the agent, lasting up to 3 seconds"""
        tasks = []
        task_end_positions = []

        # Grid layout: 5 columns x 4 rows = 20 positions
        cols = 5
        rows = 4
        spacing = 0.25
        grid_width = (cols - 1) * spacing
        grid_height = (rows - 1) * spacing

        # Start position is below the agent (0.8 units down)
        grid_start = center_pos + DOWN * 0.8 + LEFT * (grid_width / 2) + UP * (grid_height / 2)

        # Create grid positions in order (row by row)
        grid_positions = []
        for row in range(rows):
            for col in range(cols):
                pos = grid_start + RIGHT * col * spacing + DOWN * row * spacing
                grid_positions.append(pos)

        # Use first num_tasks positions (or all 20 if num_tasks >= 20)
        grid_positions = grid_positions[:num_tasks]

        for end_pos in grid_positions:
            # Task starts at agent position
            task = Dot(center_pos, radius=0.1, color=RED)
            task.set_stroke(WHITE, width=2)
            tasks.append(task)
            task_end_positions.append(end_pos)
            self.add(task)

        # Animate all tasks moving to grid positions
        move_animations = [task.animate.move_to(end_pos) for task, end_pos in zip(tasks, task_end_positions)]
        self.play(*move_animations, run_time=0.3, rate_func=rush_from)

        # Pulse while "computing"
        self.play(*[task.animate.scale(1.15) for task in tasks], run_time=0.2)
        self.play(*[task.animate.scale(1/1.15) for task in tasks], run_time=0.2)

        # Fade out in waves over max 3 seconds total
        # Randomly assign tasks to 3 groups
        shuffled_tasks = list(tasks)
        random.shuffle(shuffled_tasks)

        n = len(shuffled_tasks)
        wave1_tasks = shuffled_tasks[:n//3]
        wave2_tasks = shuffled_tasks[n//3:2*n//3]
        wave3_tasks = shuffled_tasks[2*n//3:]

        # Wave 1 fade (1s)
        if wave1_tasks:
            self.play(*[task.animate.set_opacity(0) for task in wave1_tasks], run_time=1.0)
            for task in wave1_tasks:
                self.remove(task)

        # Wave 2 fade (1s)
        if wave2_tasks:
            self.play(*[task.animate.set_opacity(0) for task in wave2_tasks], run_time=1.0)
            for task in wave2_tasks:
                self.remove(task)

        # Wave 3 fade (1s)
        if wave3_tasks:
            self.play(*[task.animate.set_opacity(0) for task in wave3_tasks], run_time=1.0)
            for task in wave3_tasks:
                self.remove(task)


class OpalAgentsAnimationV2(Scene):
    """
    Multi-agent collaboration for protein design over OPAL architecture.

    Shows:
    - Agent nodes positioned over OPAL architecture diagram
    - Message passing between agents (literature, planning, simulation, etc.)
    - HPC task dispatch when simulation/binder agents are activated
    - Multiple iterations demonstrating ongoing collaboration

    Generated from prompt: "Show agents communicating over OPAL architecture,
    messages trigger HPC compute tasks, multiple rounds of collaboration."
    """

    def construct(self):
        # Set background color to match intro slide (dark navy blue)
        self.camera.background_color = "#0d1b2a"

        # Load background image FIRST (so it's behind everything)
        bg_path = os.path.join(os.path.dirname(__file__), "OPAL-SPLASH.png")
        background = ImageMobject(bg_path)
        background.width = config.frame_width
        background.move_to(ORIGIN + DOWN * 0.5)  # Shift down to make room for title
        self.add(background)

        # Add title and subtitle ON TOP of background
        # 5% from top, Arial font, 36pt (frame height is 8, so 5% = 0.4 units)
        title = Text("DOE Science is Becoming Agentic", font="Arial", font_size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        subtitle = Text("Scalable Agentic Reasoning for Biologics Design", font_size=24, color=GRAY_B)
        subtitle.next_to(title, DOWN, buff=0.15)

        self.add(title, subtitle)

        # Agent positions
        agents = {
            "user": np.array([-6.0, 0.0, 0]),
            "literature": np.array([-3.2, 1.8, 0]),
            "optimization": np.array([-3.2, -1.5, 0]),
            "planning_top": np.array([0.3, 1.2, 0]),
            "planning_bottom": np.array([0.3, -0.8, 0]),
            "simulation": np.array([3.5, 1.8, 0]),
            "binder": np.array([3.5, -1.2, 0]),
            "resources": np.array([6.0, 0.0, 0]),
        }

        # HPC system position (bottom right area)
        hpc_pos = np.array([5.6, -2.4, 0])

        # Create HPC system visual
        hpc_box = RoundedRectangle(
            width=2.8, height=1.1, corner_radius=0.1,
            fill_color=DARK_BLUE, fill_opacity=0.8,
            stroke_color=BLUE, stroke_width=3
        )
        hpc_box.move_to(hpc_pos)

        hpc_label = Text("HPC System", font_size=18, color=WHITE, weight=BOLD)
        hpc_label.move_to(hpc_pos + UP * 0.3)

        # HPC "cores" - larger node boxes
        hpc_cores = VGroup()
        core_rows, core_cols = 2, 8
        core_size = 0.25
        core_spacing = 0.30
        cores_start = hpc_pos + LEFT * (core_cols - 1) * core_spacing / 2 + DOWN * 0.06

        for row in range(core_rows):
            for col in range(core_cols):
                core = Square(side_length=core_size, fill_color=GRAY, fill_opacity=0.5, stroke_width=1, stroke_color=WHITE)
                core.move_to(cores_start + RIGHT * col * core_spacing + DOWN * row * core_spacing)
                hpc_cores.add(core)

        hpc_group = VGroup(hpc_box, hpc_label, hpc_cores)

        # Create agent markers
        agent_markers = {}
        agent_glows = {}

        for name, pos in agents.items():
            glow = Circle(radius=0.6, color=YELLOW, fill_opacity=0.35, stroke_width=0)
            glow.move_to(pos)

            marker = Circle(radius=0.25, color=YELLOW, fill_opacity=1.0, stroke_width=3, stroke_color=WHITE)
            marker.move_to(pos)

            center_dot = Dot(pos, radius=0.08, color=WHITE)

            agent_markers[name] = VGroup(marker, center_dot)
            agent_glows[name] = glow

        # Add all markers
        for name in agents:
            self.add(agent_glows[name], agent_markers[name])

        # Animate markers appearing
        self.play(
            *[GrowFromCenter(agent_markers[name]) for name in agents],
            *[FadeIn(agent_glows[name]) for name in agents],
            run_time=0.6
        )

        # Add HPC system
        self.play(FadeIn(hpc_group), run_time=0.5)

        # Define communication patterns to repeat
        comm_patterns = [
            [("user", "planning_top"), ("planning_top", "simulation"), ("planning_top", "literature")],
            [("literature", "planning_top"), ("simulation", "planning_bottom")],
            [("planning_bottom", "optimization"), ("optimization", "binder")],
            [("binder", "resources"), ("resources", "binder")],
            [("binder", "planning_bottom"), ("planning_bottom", "user")],
        ]

        # Agents that spawn HPC tasks
        hpc_spawning_agents = ["simulation", "binder"]

        # Run N iterations
        num_iterations = 3

        for iteration in range(num_iterations):
            for pattern in comm_patterns:
                # Send messages in this pattern simultaneously
                messages = []
                trails = []
                destinations = []
                dest_names = []

                for from_agent, to_agent in pattern:
                    start_pos = agents[from_agent]
                    end_pos = agents[to_agent]

                    message = Dot(start_pos, radius=0.18, color=BLUE)
                    message.set_stroke(WHITE, width=2)

                    trail = TracedPath(
                        message.get_center,
                        dissipating_time=0.5,
                        stroke_width=5,
                        stroke_color=BLUE_A
                    )

                    messages.append(message)
                    trails.append(trail)
                    destinations.append(end_pos)
                    dest_names.append(to_agent)

                    self.add(trail, message)

                # Animate all messages in pattern
                self.play(
                    *[msg.animate.move_to(dest) for msg, dest in zip(messages, destinations)],
                    run_time=0.4,
                    rate_func=smooth
                )

                # Highlight receiving agents and spawn HPC tasks if applicable
                highlight_anims = []
                for dest_name in dest_names:
                    highlight_anims.append(agent_markers[dest_name].animate.scale(1.2))
                    highlight_anims.append(agent_glows[dest_name].animate.set_color(BLUE).set_opacity(0.5))

                self.play(*highlight_anims, run_time=0.15)

                # Spawn tasks to HPC for relevant agents
                for dest_name in dest_names:
                    if dest_name in hpc_spawning_agents:
                        self.spawn_hpc_tasks(agents[dest_name], hpc_pos, hpc_cores, num_tasks=10)

                # Reset highlights
                reset_anims = []
                for dest_name in dest_names:
                    reset_anims.append(agent_markers[dest_name].animate.scale(1/1.2))
                    reset_anims.append(agent_glows[dest_name].animate.set_color(YELLOW).set_opacity(0.35))

                self.play(*reset_anims, run_time=0.15)

                # Clean up messages
                for msg, trail in zip(messages, trails):
                    self.remove(msg, trail)

        # Final flourish
        self.play(
            *[agent_glows[name].animate.scale(1.5).set_opacity(0.5).set_color(GREEN) for name in agents],
            hpc_box.animate.set_stroke(GREEN, width=4),
            run_time=0.4
        )
        self.play(
            *[agent_glows[name].animate.scale(1/1.5).set_opacity(0.35).set_color(YELLOW) for name in agents],
            hpc_box.animate.set_stroke(BLUE, width=3),
            run_time=0.4
        )

        self.wait(1.0)

    def spawn_hpc_tasks(self, agent_pos, hpc_pos, hpc_cores, num_tasks=10):
        """Spawn tasks that travel from agent to HPC system"""
        tasks = []

        # Create tasks at agent position
        for i in range(num_tasks):
            task = Dot(agent_pos, radius=0.08, color=RED)
            task.set_stroke(WHITE, width=1)
            tasks.append(task)
            self.add(task)

        # Pick random cores as destinations
        core_list = list(hpc_cores)
        random.shuffle(core_list)
        target_cores = core_list[:num_tasks]

        # Animate tasks moving to HPC
        move_anims = [task.animate.move_to(core.get_center()) for task, core in zip(tasks, target_cores)]
        self.play(*move_anims, run_time=0.5, rate_func=smooth)

        # Light up the cores
        light_anims = [core.animate.set_fill(RED, opacity=0.8) for core in target_cores]
        self.play(*light_anims, run_time=0.2)

        # Remove task dots (they're now "in" the cores)
        for task in tasks:
            self.remove(task)

        # Cores process (pulse)
        self.play(*[core.animate.set_fill(ORANGE, opacity=1.0) for core in target_cores], run_time=0.3)
        self.play(*[core.animate.set_fill(GRAY, opacity=0.5) for core in target_cores], run_time=0.5)


class OpalAgentsAnimationLoop(Scene):
    """
    Continuous loop version showing ongoing agent communication.
    """

    def construct(self):
        # Load background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(script_dir, "..", "assets", "OPAL-SPLASH.png")
        background = ImageMobject(bg_path)
        background.height = config.frame_height
        background.move_to(ORIGIN)
        self.add(background)

        # Agent positions
        agents = {
            "user": np.array([-6.0, 0.0, 0]),
            "literature": np.array([-3.2, 1.8, 0]),
            "optimization": np.array([-3.2, -1.5, 0]),
            "planning_top": np.array([0.3, 1.2, 0]),
            "planning_bottom": np.array([0.3, -0.8, 0]),
            "simulation": np.array([3.5, 1.8, 0]),
            "binder": np.array([3.5, -1.2, 0]),
            "resources": np.array([6.0, 0.0, 0]),
        }

        # Create markers
        agent_markers = {}
        for name, pos in agents.items():
            marker = Circle(radius=0.12, color=YELLOW, fill_opacity=0.9, stroke_width=2, stroke_color=WHITE)
            marker.move_to(pos)
            agent_markers[name] = marker
            self.add(marker)

        self.play(*[GrowFromCenter(m) for m in agent_markers.values()], run_time=0.5)

        # Continuous communication - multiple messages at once
        agent_list = list(agents.keys())

        for _ in range(3):  # 3 rounds of parallel communication
            # Create multiple simultaneous messages
            num_messages = 5
            messages = []
            trails = []
            paths = []

            random.seed()

            for _ in range(num_messages):
                # Random source and destination
                src = random.choice(agent_list)
                dst = random.choice([a for a in agent_list if a != src])

                start_pos = agents[src]
                end_pos = agents[dst]

                message = Dot(start_pos, radius=0.08, color=BLUE_B)
                trail = TracedPath(
                    message.get_center,
                    dissipating_time=0.4,
                    stroke_width=2,
                    stroke_color=BLUE_B
                )

                messages.append(message)
                trails.append(trail)
                paths.append(end_pos)

                self.add(trail, message)

            # Animate all messages
            self.play(
                *[msg.animate.move_to(path) for msg, path in zip(messages, paths)],
                run_time=0.5
            )

            # Spawn compute tasks at random locations
            compute_pos = agents[random.choice(["simulation", "optimization", "binder"])]
            self.spawn_compute_tasks(compute_pos, num_tasks=8)

            # Clean up
            for msg, trail in zip(messages, trails):
                self.remove(msg, trail)

        self.wait(1.0)

    def spawn_compute_tasks(self, center_pos, num_tasks=10):
        tasks = []
        animations = []

        for i in range(num_tasks):
            angle = random.uniform(0, TAU)
            distance = random.uniform(0.2, 0.6)
            end_pos = center_pos + distance * np.array([np.cos(angle), np.sin(angle), 0])

            task = Dot(center_pos, radius=0.04, color=RED_A)
            tasks.append(task)
            self.add(task)
            animations.append(task.animate.move_to(end_pos).set_opacity(0))

        self.play(*animations, run_time=0.3, rate_func=rush_from)

        for task in tasks:
            self.remove(task)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OPAL Agents Animation")
    parser.add_argument(
        "quality",
        nargs="?",
        default="low",
        choices=["low", "medium", "high", "4k"],
        help="Output quality (default: low)"
    )
    parser.add_argument("--preview", "-p", action="store_true", help="Preview after rendering")
    parser.add_argument("--version", "-v", choices=["v1", "v2", "loop"], default="v2",
                       help="Animation version (default: v2)")
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

    # Select scene class based on version
    if args.version == "v1":
        scene_class = OpalAgentsAnimation
        name = "OpalAgentsAnimation"
    elif args.version == "loop":
        scene_class = OpalAgentsAnimationLoop
        name = "OpalAgentsAnimationLoop"
    else:
        scene_class = OpalAgentsAnimationV2
        name = "OpalAgentsAnimationV2"

    config.output_file = f"{name}_{args.quality}"

    print(f"Rendering {name} at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = scene_class()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/{height}p{fps}/{name}_{args.quality}.mp4"
        subprocess.run(["open", output_path])
