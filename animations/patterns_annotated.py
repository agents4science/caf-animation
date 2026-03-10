"""
Patterns Slide Annotated Animation

Shows the assets/CAF_Patterns.png with 7 mini-animations overlaid on each pattern box,
demonstrating what each CAF pattern does.

Patterns:
1. Local Agent Execution - Single pulsing agent on a workstation
2. Federated Agent Execution - Agents moving between connected institutions
3. Massively Parallel Inference - Fan-out/fan-in from center to many nodes
4. Governed Tool Use at Scale - Tools with policy gates
5. Multi-Agent Coordination - Multiple agents with shared governance
6. Long-Lived Autonomous Agents - Agent persisting over time with state
7. Agent-Mediated Scientific Workflows - Dynamic workflow construction
"""

from manim import *
import numpy as np
import argparse


class PatternsAnnotated(Scene):
    """
    Main scene that displays the patterns slide with overlaid mini-animations.
    """

    def construct(self):
        # Load and display the slide as background
        slide = ImageMobject("assets/CAF_Patterns.png")
        slide.height = config.frame_height
        slide.move_to(ORIGIN)
        self.add(slide)

        # Define the approximate positions for each pattern box
        # These are relative to the slide dimensions (normalized coordinates)
        # The slide has 4 boxes in row 1 and 3 boxes in row 2

        # Approximate box positions (center of each box's content area)
        # Based on the slide layout - adjusted for Manim's coordinate system
        frame_w = config.frame_width
        frame_h = config.frame_height

        # Row 1 boxes (4 boxes) - y position roughly at 0.25 of frame height from center
        # UPDATED: After cropping black borders, scale factor 1.526
        row1_y = 1.22  # was 0.8 * 1.526
        row1_x_positions = [-7.33, -2.44, 2.44, 7.33]  # was [-4.8, -1.6, 1.6, 4.8] * 1.526

        # Row 2 boxes (3 boxes) - y position roughly at -0.35 of frame height from center
        row2_y = -2.14  # was -1.4 * 1.526
        row2_x_positions = [-5.80, 0.0, 5.80]  # was [-3.8, 0.0, 3.8] * 1.526

        # Box size for animations (smaller than actual boxes to fit inside)
        # Scaled by 1.526 to match cropped image
        box_w = 3.05  # was 2.0 * 1.526
        box_h = 1.83  # was 1.2 * 1.526

        # Create animation groups for each pattern
        anim_groups = []

        # Pattern 1: Local Agent Execution (single pulsing agent)
        p1_center = np.array([row1_x_positions[0], row1_y, 0])
        p1_anim = self.create_local_agent_animation(p1_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("local", p1_center, p1_anim))

        # Pattern 2: Federated Agent Execution (connected institutions)
        p2_center = np.array([row1_x_positions[1], row1_y, 0])
        p2_anim = self.create_federated_animation(p2_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("federated", p2_center, p2_anim))

        # Pattern 3: Massively Parallel Inference (fan-out)
        p3_center = np.array([row1_x_positions[2], row1_y, 0])
        p3_anim = self.create_parallel_inference_animation(p3_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("parallel", p3_center, p3_anim))

        # Pattern 4: Governed Tool Use at Scale (tools with policy)
        p4_center = np.array([row1_x_positions[3], row1_y, 0])
        p4_anim = self.create_governed_tools_animation(p4_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("governed", p4_center, p4_anim))

        # Pattern 5: Multi-Agent Coordination
        p5_center = np.array([row2_x_positions[0], row2_y, 0])
        p5_anim = self.create_multi_agent_animation(p5_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("multi_agent", p5_center, p5_anim))

        # Pattern 6: Long-Lived Autonomous Agents
        p6_center = np.array([row2_x_positions[1], row2_y, 0])
        p6_anim = self.create_long_lived_animation(p6_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("long_lived", p6_center, p6_anim))

        # Pattern 7: Agent-Mediated Scientific Workflows
        p7_center = np.array([row2_x_positions[2], row2_y, 0])
        p7_anim = self.create_workflow_animation(p7_center, box_w * 0.4, box_h * 0.4)
        anim_groups.append(("workflow", p7_center, p7_anim))

        # Add all static elements first
        for name, center, (static_group, animations) in anim_groups:
            self.add(static_group)

        # Play all animations in a loop (3 cycles)
        for cycle in range(3):
            all_anims = []
            for name, center, (static_group, animations) in anim_groups:
                all_anims.extend(animations)

            if all_anims:
                self.play(*all_anims, run_time=2.0)

            self.wait(0.5)

        self.wait(1.0)

    def create_local_agent_animation(self, center, width, height):
        """
        Pattern 1: Local Agent Execution
        Shows a single workstation with a pulsing agent circle.
        """
        # Workstation base (rectangle)
        workstation = RoundedRectangle(
            width=width * 1.5,
            height=height * 0.8,
            corner_radius=0.1
        )
        workstation.set_fill(BLUE_E, opacity=0.3)
        workstation.set_stroke(BLUE, width=2)
        workstation.move_to(center)

        # Agent circle
        agent = Circle(radius=width * 0.25)
        agent.set_fill(YELLOW, opacity=0.8)
        agent.set_stroke(YELLOW_A, width=2)
        agent.move_to(center)

        # Pulse rings
        pulse1 = Circle(radius=width * 0.25)
        pulse1.set_stroke(YELLOW, width=2, opacity=0.6)
        pulse1.move_to(center)

        pulse2 = Circle(radius=width * 0.25)
        pulse2.set_stroke(YELLOW, width=2, opacity=0.3)
        pulse2.move_to(center)

        static_group = VGroup(workstation, agent, pulse1, pulse2)

        # Animations - pulse expanding outward
        animations = [
            pulse1.animate.scale(2.0).set_opacity(0),
            pulse2.animate.scale(2.5).set_opacity(0),
        ]

        return (static_group, animations)

    def create_federated_animation(self, center, width, height):
        """
        Pattern 2: Federated Agent Execution
        Shows multiple institutions connected with agents moving between them.
        """
        # Three institution circles
        inst_radius = width * 0.3
        positions = [
            center + LEFT * width * 0.6,
            center + RIGHT * width * 0.6,
            center + UP * height * 0.5,
        ]

        institutions = VGroup()
        for pos in positions:
            inst = Circle(radius=inst_radius)
            inst.set_fill(BLUE_E, opacity=0.4)
            inst.set_stroke(BLUE, width=2)
            inst.move_to(pos)
            institutions.add(inst)

        # Connection lines
        lines = VGroup()
        for i, pos1 in enumerate(positions):
            for j, pos2 in enumerate(positions):
                if i < j:
                    line = Line(pos1, pos2, stroke_width=2, color=GRAY)
                    line.set_opacity(0.5)
                    lines.add(line)

        # Moving agent dot
        agent = Dot(radius=width * 0.1, color=YELLOW)
        agent.move_to(positions[0])

        static_group = VGroup(lines, institutions, agent)

        # Animation - agent moves between institutions
        path = VMobject()
        path.set_points_smoothly([positions[0], positions[2], positions[1], positions[0]])

        animations = [MoveAlongPath(agent, path, rate_func=linear)]

        return (static_group, animations)

    def create_parallel_inference_animation(self, center, width, height):
        """
        Pattern 3: Massively Parallel Inference
        Shows fan-out from center to many peripheral nodes.
        """
        # Center node
        center_node = Circle(radius=width * 0.15)
        center_node.set_fill(YELLOW, opacity=0.8)
        center_node.set_stroke(YELLOW_A, width=2)
        center_node.move_to(center)

        # Peripheral nodes in a ring
        num_nodes = 8
        peripheral_nodes = VGroup()
        peripheral_positions = []
        for i in range(num_nodes):
            angle = i * TAU / num_nodes
            pos = center + np.array([
                np.cos(angle) * width * 0.8,
                np.sin(angle) * height * 0.8,
                0
            ])
            peripheral_positions.append(pos)
            node = Circle(radius=width * 0.08)
            node.set_fill(BLUE, opacity=0.6)
            node.set_stroke(BLUE_A, width=1)
            node.move_to(pos)
            peripheral_nodes.add(node)

        # Rays from center to periphery
        rays = VGroup()
        for pos in peripheral_positions:
            ray = Line(center, pos, stroke_width=1, color=YELLOW)
            ray.set_opacity(0.4)
            rays.add(ray)

        static_group = VGroup(rays, peripheral_nodes, center_node)

        # Animation - rays pulse outward
        animations = [
            rays.animate.set_opacity(0.8),
            peripheral_nodes.animate.set_fill(RED, opacity=0.8),
        ]

        return (static_group, animations)

    def create_governed_tools_animation(self, center, width, height):
        """
        Pattern 4: Governed Tool Use at Scale
        Shows tools with policy gates/shields.
        """
        # Tool icon (gear-like)
        tool = Circle(radius=width * 0.2)
        tool.set_fill(PURPLE_E, opacity=0.6)
        tool.set_stroke(PURPLE, width=2)
        tool.move_to(center + RIGHT * width * 0.4)

        # Agent
        agent = Circle(radius=width * 0.15)
        agent.set_fill(YELLOW, opacity=0.8)
        agent.set_stroke(YELLOW_A, width=2)
        agent.move_to(center + LEFT * width * 0.5)

        # Policy gate (vertical bar)
        gate = Rectangle(width=width * 0.1, height=height * 0.8)
        gate.set_fill(GREEN, opacity=0.6)
        gate.set_stroke(GREEN_A, width=2)
        gate.move_to(center)

        # Shield icon on gate
        shield = Triangle()
        shield.scale(width * 0.1)
        shield.rotate(PI)
        shield.set_fill(GREEN, opacity=0.8)
        shield.set_stroke(WHITE, width=1)
        shield.move_to(gate.get_center())

        static_group = VGroup(agent, gate, shield, tool)

        # Animation - gate pulses green (approval)
        animations = [
            gate.animate.set_fill(GREEN, opacity=0.9),
            shield.animate.set_fill(GREEN_A, opacity=1.0),
        ]

        return (static_group, animations)

    def create_multi_agent_animation(self, center, width, height):
        """
        Pattern 5: Multi-Agent Coordination
        Shows multiple agents with shared governance element.
        """
        # Central governance node
        governance = Circle(radius=width * 0.2)
        governance.set_fill(GREEN_E, opacity=0.6)
        governance.set_stroke(GREEN, width=2)
        governance.move_to(center)

        # Multiple agent nodes around governance
        num_agents = 5
        agents = VGroup()
        agent_positions = []
        for i in range(num_agents):
            angle = i * TAU / num_agents - PI/2  # Start from top
            pos = center + np.array([
                np.cos(angle) * width * 0.7,
                np.sin(angle) * height * 0.7,
                0
            ])
            agent_positions.append(pos)
            agent = Circle(radius=width * 0.1)
            agent.set_fill(YELLOW, opacity=0.7)
            agent.set_stroke(YELLOW_A, width=1)
            agent.move_to(pos)
            agents.add(agent)

        # Connection lines from agents to governance
        connections = VGroup()
        for pos in agent_positions:
            line = Line(center, pos, stroke_width=1, color=GREEN)
            line.set_opacity(0.5)
            connections.add(line)

        static_group = VGroup(connections, governance, agents)

        # Animation - connections pulse, agents sync
        animations = [
            connections.animate.set_opacity(1.0),
            governance.animate.set_fill(GREEN, opacity=0.9),
        ]

        return (static_group, animations)

    def create_long_lived_animation(self, center, width, height):
        """
        Pattern 6: Long-Lived Autonomous Agents
        Shows an agent persisting over time with state/memory bubble.
        """
        # Timeline arrow
        timeline = Arrow(
            center + LEFT * width * 0.8,
            center + RIGHT * width * 0.8,
            stroke_width=2,
            color=GRAY
        )
        timeline.shift(DOWN * height * 0.3)

        # Agent circle
        agent = Circle(radius=width * 0.2)
        agent.set_fill(YELLOW, opacity=0.8)
        agent.set_stroke(YELLOW_A, width=2)
        agent.move_to(center + UP * height * 0.1)

        # State/memory bubble (growing)
        state_bubble = Circle(radius=width * 0.3)
        state_bubble.set_fill(BLUE_E, opacity=0.3)
        state_bubble.set_stroke(BLUE, width=1, opacity=0.5)
        state_bubble.move_to(agent.get_center())

        # Time markers on timeline
        markers = VGroup()
        for i in range(4):
            x = center[0] + (i - 1.5) * width * 0.4
            marker = Line(
                [x, timeline.get_center()[1] - 0.05, 0],
                [x, timeline.get_center()[1] + 0.05, 0],
                stroke_width=2,
                color=GRAY
            )
            markers.add(marker)

        static_group = VGroup(timeline, markers, state_bubble, agent)

        # Animation - state bubble grows (memory accumulating)
        animations = [
            state_bubble.animate.scale(1.5).set_fill(BLUE_E, opacity=0.5),
        ]

        return (static_group, animations)

    def create_workflow_animation(self, center, width, height):
        """
        Pattern 7: Agent-Mediated Scientific Workflows
        Shows dynamic workflow nodes being connected.
        """
        # Workflow nodes
        positions = [
            center + LEFT * width * 0.6 + UP * height * 0.3,
            center + UP * height * 0.4,
            center + RIGHT * width * 0.6 + UP * height * 0.2,
            center + LEFT * width * 0.4 + DOWN * height * 0.3,
            center + RIGHT * width * 0.3 + DOWN * height * 0.4,
        ]

        nodes = VGroup()
        for i, pos in enumerate(positions):
            node = Circle(radius=width * 0.1)
            if i == 0:
                # Start node
                node.set_fill(GREEN, opacity=0.7)
                node.set_stroke(GREEN_A, width=2)
            elif i == len(positions) - 1:
                # End node
                node.set_fill(RED, opacity=0.7)
                node.set_stroke(RED_A, width=2)
            else:
                node.set_fill(BLUE, opacity=0.6)
                node.set_stroke(BLUE_A, width=1)
            node.move_to(pos)
            nodes.add(node)

        # Workflow edges (dynamic)
        edges = VGroup()
        edge_pairs = [(0, 1), (1, 2), (0, 3), (3, 4), (2, 4)]
        for i, j in edge_pairs:
            edge = Arrow(
                positions[i],
                positions[j],
                buff=width * 0.12,
                stroke_width=2,
                color=GRAY
            )
            edge.set_opacity(0.5)
            edges.add(edge)

        # Agent mediator in center
        agent = Circle(radius=width * 0.08)
        agent.set_fill(YELLOW, opacity=0.8)
        agent.set_stroke(YELLOW_A, width=1)
        agent.move_to(center)

        static_group = VGroup(edges, nodes, agent)

        # Animation - edges light up showing flow
        animations = [
            edges.animate.set_opacity(1.0).set_color(YELLOW),
        ]

        return (static_group, animations)


class PatternsAnnotatedLoop(Scene):
    """
    Looping version that continuously animates all patterns.
    """

    def construct(self):
        # Load and display the slide as background
        slide = ImageMobject("assets/CAF_Patterns.png")
        slide.height = config.frame_height
        slide.move_to(ORIGIN)
        self.add(slide)

        # Create all pattern animations with better positioning
        self.play_all_patterns()

    def play_all_patterns(self):
        """Create and play all 7 pattern animations."""

        # More precise box positions based on actual slide layout
        # UPDATED: After cropping black borders from CAF_Patterns.png (712x401 from 792x612)
        # Scale factor: 1.526 (all positions multiplied by this factor)
        # Row 1 (4 boxes) - positioned in the white card areas
        row1_y_center = 0.34  # was 0.84, shifted down 0.5
        row1_xs = [-5.17, -0.37, 4.37, 9.17]  # was [-7.17, -2.37, 2.37, 7.17], shifted right 2

        # Row 2 (3 boxes)
        row2_y_center = -3.02  # was -2.52, shifted down 0.5
        row2_xs = [-3.95, 2.76, 8.87]  # was [-5.95, 0.76, 6.87], shifted right 2

        # Offset for "bottom right" positioning within each box
        br_offset_x = 0.76  # was 0.5 * 1.526
        br_offset_y = -0.53  # was -0.35 * 1.526

        # Animation size - scaled by 1.526 to match cropped image
        anim_scale = 1.526

        # Create all the mini-animations
        all_mobjects = VGroup()

        # Pattern 1: Local Agent
        p1_center = [row1_xs[0] + br_offset_x + 0.14, row1_y_center + br_offset_y + 0.52, 0]
        p1 = self.local_agent(p1_center, anim_scale)
        all_mobjects.add(p1)

        # Pattern 2: Federated - moved right a little more
        p2_center = [row1_xs[1] + br_offset_x - 1.54, row1_y_center + br_offset_y + 0.5, 0]
        p2 = self.federated_agent(p2_center, anim_scale)
        all_mobjects.add(p2)

        # Pattern 3: Massively Parallel LLM Inference
        p3_center = [row1_xs[2] - 1.85, row1_y_center + 0.04, 0]
        p3 = self.parallel_inference(p3_center, anim_scale * 0.75)
        all_mobjects.add(p3)

        # Pattern 4: Governed tools - right 0.5
        p4_center = [row1_xs[3] - 3.37, row1_y_center + 0.04, 0]
        p4 = self.governed_tools(p4_center, anim_scale)
        all_mobjects.add(p4)

        # Pattern 5: Multi-agent
        p5_center = [row2_xs[0] + 0.29, row2_y_center + 0.68, 0]
        p5 = self.multi_agent(p5_center, anim_scale * 0.8)
        all_mobjects.add(p5)

        # Pattern 6: Long-lived (no arrow)
        p6_center = [row2_xs[1] - 1.85, row2_y_center + 0.63, 0]
        p6 = self.long_lived(p6_center, anim_scale)
        all_mobjects.add(p6)

        # Pattern 7: Workflows
        p7_center = [row2_xs[2] - 3.22, row2_y_center + 0.6, 0]
        p7 = self.workflow(p7_center, anim_scale)
        all_mobjects.add(p7)

        # Fade in all animations
        self.play(FadeIn(all_mobjects), run_time=0.5)

        # Run animation cycles - more cycles to keep animations going
        for _ in range(4):
            self.animate_cycle_with_p6(p1, p2, p3, p4, p5, p6, p7)

        self.wait(1)

    def local_agent(self, center, scale):
        """Pattern 1: Local Agent Execution.

        Shows a person interacting with two agents that also interact with each other.
        """
        group = VGroup()
        center = np.array(center)

        # Person icon (simple stick figure head) - brown outline
        person_pos = center + LEFT * 0.4*scale
        person_head = Circle(radius=0.1*scale)
        person_head.set_fill(WHITE, opacity=1.0)
        person_head.set_stroke("#8B4513", width=3)  # Brown outline
        person_head.move_to(person_pos)

        # Person body (simple line) - brown color
        person_body = Line(
            person_pos + DOWN * 0.1*scale,
            person_pos + DOWN * 0.28*scale,
            stroke_width=4,
            color="#8B4513"  # Brown
        )

        person = VGroup(person_head, person_body)
        group.add(person)

        # Two agent circles that interact with each other (orange moved down for separation)
        agent1_pos = center + RIGHT * 0.15*scale + UP * 0.12*scale
        agent2_pos = center + RIGHT * 0.15*scale + DOWN * 0.25*scale

        agent1 = Circle(radius=0.12*scale)
        agent1.set_fill(YELLOW, opacity=1.0)
        agent1.set_stroke(WHITE, width=3)
        agent1.move_to(agent1_pos)

        agent2 = Circle(radius=0.12*scale)
        agent2.set_fill(ORANGE, opacity=1.0)
        agent2.set_stroke(WHITE, width=3)
        agent2.move_to(agent2_pos)

        group.add(agent1, agent2)

        # Connection lines: person to agents
        line_p_a1 = Line(person_pos, agent1_pos, stroke_width=3, color=WHITE)
        line_p_a1.set_opacity(0.8)
        line_p_a2 = Line(person_pos, agent2_pos, stroke_width=3, color=WHITE)
        line_p_a2.set_opacity(0.8)

        # Connection line: agent to agent (interaction)
        line_a1_a2 = Line(agent1_pos, agent2_pos, stroke_width=4, color=YELLOW)
        line_a1_a2.set_opacity(0.8)

        group.add(line_p_a1, line_p_a2, line_a1_a2)

        # Store references for animation
        group.agent1 = agent1
        group.agent2 = agent2
        group.person = person
        group.line_a1_a2 = line_a1_a2
        group.line_p_a1 = line_p_a1
        group.line_p_a2 = line_p_a2
        group.center = center

        return group

    def federated_agent(self, center, scale):
        """Pattern 2: Federated Agent Execution.

        Shows two sites (rounded boxes), each with agents that interact across sites.
        """
        group = VGroup()
        center = np.array(center)

        # Site 1 (left) - rounded box
        site1_pos = center + LEFT * 0.32*scale
        site1_box = RoundedRectangle(
            width=0.5*scale,
            height=0.45*scale,
            corner_radius=0.05*scale
        )
        site1_box.set_fill(BLUE, opacity=0.4)
        site1_box.set_stroke(BLUE, width=4)
        site1_box.move_to(site1_pos)
        group.add(site1_box)

        # Site 2 (right) - rounded box
        site2_pos = center + RIGHT * 0.32*scale
        site2_box = RoundedRectangle(
            width=0.5*scale,
            height=0.45*scale,
            corner_radius=0.05*scale
        )
        site2_box.set_fill(PURPLE, opacity=0.4)
        site2_box.set_stroke(PURPLE, width=4)
        site2_box.move_to(site2_pos)
        group.add(site2_box)

        # Connection line between sites (federation link)
        federation_line = Line(
            site1_pos + RIGHT * 0.25*scale,
            site2_pos + LEFT * 0.25*scale,
            stroke_width=4,
            color=WHITE
        )
        federation_line.set_opacity(0.8)
        group.add(federation_line)

        # Agents in site 1
        agent1a_pos = site1_pos + UP * 0.1*scale + LEFT * 0.08*scale
        agent1b_pos = site1_pos + DOWN * 0.1*scale + RIGHT * 0.08*scale

        agent1a = Dot(radius=0.08*scale, color=YELLOW)
        agent1a.move_to(agent1a_pos)
        agent1a.set_z_index(1)

        agent1b = Dot(radius=0.08*scale, color=YELLOW)
        agent1b.move_to(agent1b_pos)
        agent1b.set_z_index(1)

        group.add(agent1a, agent1b)

        # Agents in site 2
        agent2a_pos = site2_pos + UP * 0.1*scale + RIGHT * 0.08*scale
        agent2b_pos = site2_pos + DOWN * 0.1*scale + LEFT * 0.08*scale

        agent2a = Dot(radius=0.08*scale, color=ORANGE)
        agent2a.move_to(agent2a_pos)
        agent2a.set_z_index(1)

        agent2b = Dot(radius=0.08*scale, color=ORANGE)
        agent2b.move_to(agent2b_pos)
        agent2b.set_z_index(1)

        group.add(agent2a, agent2b)

        # Cross-site interaction line (will animate)
        cross_line = Line(
            agent1b_pos,
            agent2b_pos,
            stroke_width=4,
            color=GREEN
        )
        cross_line.set_opacity(0.6)
        group.add(cross_line)

        # Store references for animation
        group.site1_box = site1_box
        group.site2_box = site2_box
        group.agent1a = agent1a
        group.agent1b = agent1b
        group.agent2a = agent2a
        group.agent2b = agent2b
        group.cross_line = cross_line
        group.federation_line = federation_line
        group.site1_pos = site1_pos
        group.site2_pos = site2_pos

        return group

    def parallel_inference(self, center, scale):
        """Pattern 3: Massively parallel fan-out with pulsing requests."""
        group = VGroup()
        center = np.array(center)

        # Center hub
        hub = Dot(radius=0.15*scale, color=YELLOW)
        hub.move_to(center)
        hub.set_z_index(2)
        group.add(hub)

        # Outer nodes
        num_nodes = 8
        outer_nodes = VGroup()
        node_positions = []
        for i in range(num_nodes):
            angle = i * TAU / num_nodes
            pos = center + np.array([np.cos(angle), np.sin(angle), 0]) * 0.4*scale
            node_positions.append(pos)
            node = Dot(radius=0.08*scale, color=BLUE)
            node.move_to(pos)
            outer_nodes.add(node)

        # Rays
        rays = VGroup()
        for pos in node_positions:
            ray = Line(center, pos, stroke_width=3, color=YELLOW)
            ray.set_opacity(0.6)
            rays.add(ray)

        # Pulse dots that travel along rays (start at center)
        pulses = VGroup()
        for i in range(num_nodes):
            pulse = Dot(radius=0.05*scale, color=RED)
            pulse.move_to(center)
            pulse.set_z_index(3)
            pulses.add(pulse)

        group.add(rays)
        group.add(outer_nodes)
        group.add(pulses)

        group.rays = rays
        group.outer_nodes = outer_nodes
        group.hub = hub
        group.pulses = pulses
        group.center_pos = center
        group.node_positions = node_positions

        return group

    def governed_tools(self, center, scale):
        """Pattern 4: Tools with policy gates - thick lines to barrier, thin lines through."""
        group = VGroup()
        center = np.array(center)

        agent_pos = center + LEFT * 0.35*scale
        gate_pos = center
        tool_pos = center + RIGHT * 0.35*scale

        # Agent on left
        agent = Dot(radius=0.12*scale, color=YELLOW)
        agent.move_to(agent_pos)
        group.add(agent)

        # Gate in middle
        gate = Rectangle(width=0.1*scale, height=0.5*scale)
        gate.set_fill(GREEN, opacity=0.8)
        gate.set_stroke(WHITE, width=3)
        gate.move_to(gate_pos)
        group.add(gate)

        # Tool on right
        tool = Circle(radius=0.14*scale)
        tool.set_fill(PURPLE, opacity=0.8)
        tool.set_stroke(WHITE, width=3)
        tool.move_to(tool_pos)
        group.add(tool)

        # Thick lines from agent to gate (blocked requests)
        thick_lines = VGroup()
        for offset in [UP * 0.1*scale, DOWN * 0.1*scale]:
            line = Line(agent_pos + offset, gate_pos + LEFT * 0.05*scale + offset,
                       stroke_width=5, color=RED)
            line.set_opacity(0.6)
            thick_lines.add(line)
        group.add(thick_lines)

        # Thin lines that go through (allowed requests)
        thin_lines = VGroup()
        thin_line = Line(agent_pos, tool_pos, stroke_width=2, color=GREEN)
        thin_line.set_opacity(0.4)
        thin_lines.add(thin_line)
        group.add(thin_lines)

        group.gate = gate
        group.agent = agent
        group.tool = tool
        group.thick_lines = thick_lines
        group.thin_lines = thin_lines

        return group

    def multi_agent(self, center, scale):
        """Pattern 5: Multiple agents with shared governance."""
        group = VGroup()
        center = np.array(center)

        # Central governance
        governance = Circle(radius=0.14*scale)
        governance.set_fill(GREEN, opacity=0.8)
        governance.set_stroke(WHITE, width=3)
        governance.move_to(center)
        group.add(governance)

        # Surrounding agents
        agents = VGroup()
        num_agents = 5
        agent_positions = []
        for i in range(num_agents):
            angle = i * TAU / num_agents - PI/2
            pos = center + np.array([np.cos(angle), np.sin(angle), 0]) * 0.35*scale
            agent_positions.append(pos)
            agent = Dot(radius=0.08*scale, color=YELLOW)
            agent.move_to(pos)
            agents.add(agent)

        # Connections
        connections = VGroup()
        for pos in agent_positions:
            conn = Line(center, pos, stroke_width=3, color=GREEN)
            conn.set_opacity(0.7)
            connections.add(conn)

        group.add(connections)
        group.add(agents)

        group.governance = governance
        group.connections = connections
        group.agents_group = agents

        return group

    def long_lived(self, center, scale):
        """Pattern 6: Long-lived agent with state and day counter (no arrow)."""
        group = VGroup()
        center = np.array(center)

        # Timeline arrow REMOVED per user request

        # Agent
        agent = Dot(radius=0.12*scale, color=YELLOW)
        agent.move_to(center + LEFT * 0.25*scale)
        agent.set_z_index(1)
        group.add(agent)

        # State bubble
        state = Circle(radius=0.18*scale)
        state.set_fill(BLUE, opacity=0.4)
        state.set_stroke(BLUE, width=3, opacity=0.8)
        state.move_to(agent.get_center())
        group.add(state)

        # Day counter number - moved right by 0.2 units (was RIGHT * 0.1, now RIGHT * 0.3)
        day_num = Text("1", font="Arial", font_size=int(32*scale), color=YELLOW, weight=BOLD)
        day_num_pos = center + RIGHT * 0.3*scale + UP * 0.08*scale
        day_num.move_to(day_num_pos)
        group.add(day_num)

        # "days" label - moved right by 0.2 units (was RIGHT * 0.1, now RIGHT * 0.3)
        day_label = Text("days", font="Arial", font_size=int(22*scale), color=YELLOW, weight=BOLD)
        day_label_pos = center + RIGHT * 0.3*scale + DOWN * 0.12*scale
        day_label.move_to(day_label_pos)
        group.add(day_label)

        group.agent = agent
        group.state = state
        group.day_num = day_num
        group.day_label = day_label
        group.day_num_pos = day_num_pos
        group.day_label_pos = day_label_pos
        group.day_counter_scale = scale

        return group

    def workflow(self, center, scale):
        """Pattern 7: Dynamic scientific workflow with evolving nodes and edges."""
        group = VGroup()
        center = np.array(center)

        # Define node positions for the workflow
        positions = [
            center + LEFT * 0.4*scale + UP * 0.15*scale,      # 0: start
            center + UP * 0.25*scale,                          # 1: middle top
            center + RIGHT * 0.4*scale + UP * 0.1*scale,      # 2: right
            center + LEFT * 0.25*scale + DOWN * 0.2*scale,    # 3: bottom left
            center + RIGHT * 0.2*scale + DOWN * 0.25*scale,   # 4: end
            center + DOWN * 0.05*scale,                        # 5: new middle (appears later)
        ]

        # Initial nodes (some start hidden)
        nodes = VGroup()
        colors = [GREEN, BLUE, BLUE, BLUE, RED, PURPLE]
        for i, (pos, color) in enumerate(zip(positions, colors)):
            node = Dot(radius=0.09*scale, color=color)
            node.move_to(pos)
            if i == 5:  # New node starts hidden
                node.set_opacity(0)
            nodes.add(node)

        # Initial edges (some start hidden)
        edges = VGroup()
        edge_pairs = [(0, 1), (1, 2), (0, 3), (3, 4), (2, 4)]
        for i, j in edge_pairs:
            edge = Line(positions[i], positions[j], stroke_width=3, color=WHITE)
            edge.set_opacity(0.7)
            edges.add(edge)

        # Additional edges that appear/disappear (start hidden)
        extra_edges = VGroup()
        extra_pairs = [(1, 5), (5, 4), (0, 5)]
        for i, j in extra_pairs:
            edge = Line(positions[i], positions[j], stroke_width=3, color=BLUE)
            edge.set_opacity(0)
            extra_edges.add(edge)

        group.add(edges)
        group.add(extra_edges)
        group.add(nodes)

        # Mediator agent
        mediator = Dot(radius=0.07*scale, color=YELLOW)
        mediator.move_to(center)
        mediator.set_z_index(1)
        group.add(mediator)

        group.edges = edges
        group.extra_edges = extra_edges
        group.nodes = nodes
        group.new_node = nodes[5]  # The node that appears/disappears
        group.mediator = mediator

        return group

    def animate_cycle(self, p1, p2, p3, p4, p5, p6, p7):
        """Run one animation cycle for all patterns."""

        # Day counter for P6: powers of 2 (1, 2, 4, 8, 16, 32)
        if not hasattr(self, 'day_index'):
            self.day_index = 0
        day_values = [1, 2, 4, 8, 16, 32]
        self.day_index = (self.day_index + 1) % len(day_values)
        day_val = day_values[self.day_index]

        # Create new day number (fixed position)
        new_day_num = Text(str(day_val), font_size=int(32*p6.day_counter_scale), color=YELLOW, weight=BOLD)
        new_day_num.move_to(p6.day_num_pos)

        # Create new day label ("day" or "days")
        day_word = "day" if day_val == 1 else "days"
        new_day_label = Text(day_word, font_size=int(22*p6.day_counter_scale), color=YELLOW, weight=BOLD)
        new_day_label.move_to(p6.day_label_pos)

        # P3 pulse animations - move pulses from center to outer nodes
        p3_pulse_out_anims = [
            p3.pulses[i].animate.move_to(p3.node_positions[i])
            for i in range(len(p3.pulses))
        ]

        # Animation phase 1: activation/interaction
        self.play(
            # P1: Person-agent connections light up, agent-agent interaction pulses
            p1.line_p_a1.animate.set_opacity(1.0).set_color(YELLOW),
            p1.line_p_a2.animate.set_opacity(1.0).set_color(YELLOW),
            p1.line_a1_a2.animate.set_opacity(1.0).set_color(GREEN),
            p1.agent1.animate.scale(1.2),
            p1.agent2.animate.scale(1.2),
            # P2: Cross-site interaction lights up, sites pulse
            p2.cross_line.animate.set_opacity(1.0).set_color(GREEN),
            p2.federation_line.animate.set_opacity(1.0).set_color(YELLOW),
            p2.site1_box.animate.set_fill(BLUE_E, opacity=0.5),
            p2.site2_box.animate.set_fill(PURPLE_E, opacity=0.5),
            # P3: rays brighten, pulses move outward
            p3.rays.animate.set_opacity(0.8),
            p3.outer_nodes.animate.set_fill(RED),
            *p3_pulse_out_anims,
            # P4: gate glows
            p4.gate.animate.set_fill(GREEN, opacity=0.9),
            # P5: connections brighten
            p5.connections.animate.set_opacity(0.9),
            # P6: state grows, day counter updates
            p6.state.animate.scale(1.3).set_fill(BLUE_E, opacity=0.5),
            Transform(p6.day_num, new_day_num),
            Transform(p6.day_label, new_day_label),
            # P7: workflow evolves - new node and edges appear, some edges light up
            p7.edges.animate.set_opacity(1.0).set_color(YELLOW),
            p7.new_node.animate.set_opacity(1.0),
            p7.extra_edges.animate.set_opacity(0.8),
            run_time=1.5
        )

        # P3 pulse animations - move pulses back to center
        p3_pulse_back_anims = [
            p3.pulses[i].animate.move_to(p3.center_pos)
            for i in range(len(p3.pulses))
        ]

        # Reset animations
        self.play(
            # P1 reset
            p1.line_p_a1.animate.set_opacity(0.6).set_color(GRAY),
            p1.line_p_a2.animate.set_opacity(0.6).set_color(GRAY),
            p1.line_a1_a2.animate.set_opacity(0.5).set_color(YELLOW),
            p1.agent1.animate.scale(1/1.2),
            p1.agent2.animate.scale(1/1.2),
            # P2 reset
            p2.cross_line.animate.set_opacity(0.3).set_color(GREEN),
            p2.federation_line.animate.set_opacity(0.6).set_color(GRAY),
            p2.site1_box.animate.set_fill(BLUE_E, opacity=0.3),
            p2.site2_box.animate.set_fill(PURPLE_E, opacity=0.3),
            # P3 reset - pulses return to center
            p3.rays.animate.set_opacity(0.3),
            p3.outer_nodes.animate.set_fill(BLUE),
            *p3_pulse_back_anims,
            p4.gate.animate.set_fill(GREEN, opacity=0.6),
            p5.connections.animate.set_opacity(0.4),
            p6.state.animate.scale(1/1.3).set_fill(BLUE_E, opacity=0.3),
            # P7 reset: new node and extra edges fade, original edges dim
            p7.edges.animate.set_opacity(0.5).set_color(GRAY),
            p7.new_node.animate.set_opacity(0),
            p7.extra_edges.animate.set_opacity(0),
            run_time=0.5
        )

    def animate_cycle_no_p6(self, p1, p2, p3, p4, p5, p7):
        """Run one animation cycle without p6."""

        # P3 pulse animations - move pulses from center to outer nodes
        p3_pulse_out_anims = [
            p3.pulses[i].animate.move_to(p3.node_positions[i])
            for i in range(len(p3.pulses))
        ]

        # Animation phase 1: activation/interaction
        self.play(
            # P1: Person-agent connections pulsate
            p1.line_p_a1.animate.set_opacity(1.0).set_color(YELLOW),
            p1.line_p_a2.animate.set_opacity(1.0).set_color(YELLOW),
            p1.line_a1_a2.animate.set_opacity(1.0).set_color(GREEN),
            p1.agent1.animate.scale(1.2),
            p1.agent2.animate.scale(1.2),
            # P2: Lines pulsate
            p2.cross_line.animate.set_opacity(1.0).set_color(GREEN),
            p2.federation_line.animate.set_opacity(1.0).set_color(YELLOW),
            p2.site1_box.animate.set_fill(BLUE_E, opacity=0.5),
            p2.site2_box.animate.set_fill(PURPLE_E, opacity=0.5),
            # P3: rays brighten, pulses move outward
            p3.rays.animate.set_opacity(0.8),
            p3.outer_nodes.animate.set_fill(RED),
            *p3_pulse_out_anims,
            # P4: thick lines brighten (blocked), thin lines through
            p4.gate.animate.set_fill(GREEN, opacity=0.9),
            p4.thick_lines.animate.set_opacity(1.0),
            p4.thin_lines.animate.set_opacity(0.9).set_color(GREEN),
            # P5: connections brighten
            p5.connections.animate.set_opacity(0.9),
            p5.governance.animate.set_fill(GREEN, opacity=0.9),
            # P7: workflow evolves
            p7.edges.animate.set_opacity(1.0).set_color(YELLOW),
            p7.new_node.animate.set_opacity(1.0),
            p7.extra_edges.animate.set_opacity(0.8),
            run_time=1.5
        )

        # P3 pulse animations - move pulses back to center
        p3_pulse_back_anims = [
            p3.pulses[i].animate.move_to(p3.center_pos)
            for i in range(len(p3.pulses))
        ]

        # Reset animations
        self.play(
            # P1 reset
            p1.line_p_a1.animate.set_opacity(0.6).set_color(GRAY),
            p1.line_p_a2.animate.set_opacity(0.6).set_color(GRAY),
            p1.line_a1_a2.animate.set_opacity(0.5).set_color(YELLOW),
            p1.agent1.animate.scale(1/1.2),
            p1.agent2.animate.scale(1/1.2),
            # P2 reset
            p2.cross_line.animate.set_opacity(0.3).set_color(GREEN),
            p2.federation_line.animate.set_opacity(0.6).set_color(GRAY),
            p2.site1_box.animate.set_fill(BLUE_E, opacity=0.3),
            p2.site2_box.animate.set_fill(PURPLE_E, opacity=0.3),
            # P3 reset - pulses return to center
            p3.rays.animate.set_opacity(0.3),
            p3.outer_nodes.animate.set_fill(BLUE),
            *p3_pulse_back_anims,
            # P4 reset
            p4.gate.animate.set_fill(GREEN, opacity=0.6),
            p4.thick_lines.animate.set_opacity(0.4),
            p4.thin_lines.animate.set_opacity(0.3),
            # P5 reset
            p5.connections.animate.set_opacity(0.4),
            p5.governance.animate.set_fill(GREEN, opacity=0.6),
            # P7 reset
            p7.edges.animate.set_opacity(0.5).set_color(GRAY),
            p7.new_node.animate.set_opacity(0),
            p7.extra_edges.animate.set_opacity(0),
            run_time=0.5
        )

    def animate_cycle_with_p6(self, p1, p2, p3, p4, p5, p6, p7):
        """Run one animation cycle including p6."""

        # Day counter for P6: powers of 2 (1, 2, 4, 8, 16, 32)
        if not hasattr(self, 'day_index'):
            self.day_index = 0
        day_values = [1, 2, 4, 8, 16, 32]
        self.day_index = (self.day_index + 1) % len(day_values)
        day_val = day_values[self.day_index]

        # Create new day number
        new_day_num = Text(str(day_val), font="Arial", font_size=int(32*p6.day_counter_scale), color=YELLOW, weight=BOLD)
        new_day_num.move_to(p6.day_num_pos)

        # Create new day label
        day_word = "day" if day_val == 1 else "days"
        new_day_label = Text(day_word, font="Arial", font_size=int(22*p6.day_counter_scale), color=YELLOW, weight=BOLD)
        new_day_label.move_to(p6.day_label_pos)

        # P3 pulse animations - move pulses from center to outer nodes
        p3_pulse_out_anims = [
            p3.pulses[i].animate.move_to(p3.node_positions[i])
            for i in range(len(p3.pulses))
        ]

        # Animation phase 1: activation/interaction
        self.play(
            # P1: Person-agent connections pulsate
            p1.line_p_a1.animate.set_opacity(1.0).set_color(YELLOW),
            p1.line_p_a2.animate.set_opacity(1.0).set_color(YELLOW),
            p1.line_a1_a2.animate.set_opacity(1.0).set_color(GREEN),
            p1.agent1.animate.scale(1.2),
            p1.agent2.animate.scale(1.2),
            # P2: Lines pulsate
            p2.cross_line.animate.set_opacity(1.0).set_color(GREEN),
            p2.federation_line.animate.set_opacity(1.0).set_color(YELLOW),
            p2.site1_box.animate.set_fill(BLUE_E, opacity=0.5),
            p2.site2_box.animate.set_fill(PURPLE_E, opacity=0.5),
            # P3: rays brighten, pulses move outward
            p3.rays.animate.set_opacity(0.8),
            p3.outer_nodes.animate.set_fill(RED),
            *p3_pulse_out_anims,
            # P4: thick lines brighten (blocked), thin lines through
            p4.gate.animate.set_fill(GREEN, opacity=0.9),
            p4.thick_lines.animate.set_opacity(1.0),
            p4.thin_lines.animate.set_opacity(0.9).set_color(GREEN),
            # P5: connections brighten
            p5.connections.animate.set_opacity(0.9),
            p5.governance.animate.set_fill(GREEN, opacity=0.9),
            # P6: state grows, day counter updates
            p6.state.animate.scale(1.3).set_fill(BLUE_E, opacity=0.5),
            Transform(p6.day_num, new_day_num),
            Transform(p6.day_label, new_day_label),
            # P7: workflow evolves
            p7.edges.animate.set_opacity(1.0).set_color(YELLOW),
            p7.new_node.animate.set_opacity(1.0),
            p7.extra_edges.animate.set_opacity(0.8),
            run_time=1.5
        )

        # P3 pulse animations - move pulses back to center
        p3_pulse_back_anims = [
            p3.pulses[i].animate.move_to(p3.center_pos)
            for i in range(len(p3.pulses))
        ]

        # Reset animations
        self.play(
            # P1 reset
            p1.line_p_a1.animate.set_opacity(0.6).set_color(GRAY),
            p1.line_p_a2.animate.set_opacity(0.6).set_color(GRAY),
            p1.line_a1_a2.animate.set_opacity(0.5).set_color(YELLOW),
            p1.agent1.animate.scale(1/1.2),
            p1.agent2.animate.scale(1/1.2),
            # P2 reset
            p2.cross_line.animate.set_opacity(0.3).set_color(GREEN),
            p2.federation_line.animate.set_opacity(0.6).set_color(GRAY),
            p2.site1_box.animate.set_fill(BLUE_E, opacity=0.3),
            p2.site2_box.animate.set_fill(PURPLE_E, opacity=0.3),
            # P3 reset - pulses return to center
            p3.rays.animate.set_opacity(0.3),
            p3.outer_nodes.animate.set_fill(BLUE),
            *p3_pulse_back_anims,
            # P4 reset
            p4.gate.animate.set_fill(GREEN, opacity=0.6),
            p4.thick_lines.animate.set_opacity(0.4),
            p4.thin_lines.animate.set_opacity(0.3),
            # P5 reset
            p5.connections.animate.set_opacity(0.4),
            p5.governance.animate.set_fill(GREEN, opacity=0.6),
            # P6 reset
            p6.state.animate.scale(1/1.3).set_fill(BLUE_E, opacity=0.3),
            # P7 reset
            p7.edges.animate.set_opacity(0.5).set_color(GRAY),
            p7.new_node.animate.set_opacity(0),
            p7.extra_edges.animate.set_opacity(0),
            run_time=0.5
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patterns Annotated Animation")
    parser.add_argument(
        "quality",
        nargs="?",
        default="low",
        choices=["low", "medium", "high", "4k"],
        help="Output quality (default: low)"
    )
    parser.add_argument("--preview", "-p", action="store_true", help="Preview after rendering")
    parser.add_argument("--loop", "-l", action="store_true", help="Use looping version")
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

    scene_class = PatternsAnnotatedLoop if args.loop else PatternsAnnotated
    config.output_file = f"PatternsAnnotated_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = scene_class()
    scene.render()

    if args.preview:
        import subprocess
        output_path = f"media/videos/{height}p{fps}/PatternsAnnotated_{args.quality}.mp4"
        subprocess.run(["open", output_path])
