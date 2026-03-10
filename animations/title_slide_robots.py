"""
Animated Title Slide with Robots

Uses Title_Slide_norobots.png as background and adds animated white robots.
"""

from manim import *
from manim.constants import RESAMPLING_ALGORITHMS
import numpy as np
import argparse


class TitleSlideRobots(Scene):
    """
    Title slide background with 4 white robots that circulate.
    """

    def construct(self):
        # Load the title slide as background (cropped version: 990x558)
        bg = ImageMobject("assets/Title_Slide_norobots.png")
        # Scale to fill frame height
        bg.scale_to_fit_height(config.frame_height)
        bg.move_to(ORIGIN)

        # Add background first
        self.add(bg)

        # Load the white coffee cup - 50% larger and shifted left
        cup = ImageMobject("assets/coffee_cup_white_transparent.png")
        cup.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
        cup.scale(0.225)  # 50% larger (was 0.15)
        cup_center = LEFT * 5.5 + DOWN * 0.1  # Shifted more left
        cup.move_to(cup_center)

        # Create 4 white robot copies - 50% larger with smooth interpolation
        robots = []
        for i in range(4):
            robot = ImageMobject("assets/robot_white_clean.png")
            robot.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
            robot.scale(0.12)  # 50% larger (was 0.08)
            robots.append(robot)

        # Use cup center for robot orbit
        cup_center = cup.get_center()

        # Starting angles: top-left, top-right, bottom-right, bottom-left
        start_radius = 0.75  # 50% larger (was 0.5)
        orbit_radius = 1.05  # 50% larger (was 0.7)
        start_angles = [3*PI/4, PI/4, -PI/4, -3*PI/4]  # TL, TR, BR, BL

        # Position robots at starting positions
        # Bottom right robot (index 2) offset adjusted - 50% larger
        br_offset = RIGHT * 0.105 + DOWN * 0.12
        # Bottom left robot (index 3) offset - 50% larger
        bl_offset = DOWN * 0.12
        for i, (robot, angle) in enumerate(zip(robots, start_angles)):
            x = cup_center[0] + start_radius * np.cos(angle)
            y = cup_center[1] + start_radius * np.sin(angle) * 0.7  # Elliptical
            pos = np.array([x, y, 0])
            if i == 2:  # Bottom right robot
                pos = pos + br_offset
            elif i == 3:  # Bottom left robot
                pos = pos + bl_offset
            robot.move_to(pos)

        robot_group = Group(*robots)

        # Animation sequence

        # Phase 0: Cup appears
        self.play(
            FadeIn(cup, scale=1.05),
            run_time=0.6
        )

        # Phase 1: Robots appear
        self.play(
            LaggedStart(*[FadeIn(r, scale=1.2) for r in robots], lag_ratio=0.15),
            run_time=0.6
        )

        # Phase 2: Robots move outward to orbit positions
        orbit_positions = []
        for i, angle in enumerate(start_angles):
            x = cup_center[0] + orbit_radius * np.cos(angle)
            y = cup_center[1] + orbit_radius * np.sin(angle) * 0.7
            pos = np.array([x, y, 0])
            if i == 2:  # Bottom right robot
                pos = pos + br_offset
            elif i == 3:  # Bottom left robot
                pos = pos + bl_offset
            orbit_positions.append(pos)

        self.play(
            *[robot.animate.move_to(pos) for robot, pos in zip(robots, orbit_positions)],
            run_time=0.8,
            rate_func=smooth
        )

        # Phase 3: Robots rotate smoothly around the center
        current_offset = [0]

        def orbit_robots(angle_delta, run_time):
            """Animate robots along elliptical orbit while staying upright."""
            start_offset = current_offset[0]
            end_offset = start_offset + angle_delta

            def update_positions(alpha):
                offset = start_offset + (end_offset - start_offset) * alpha
                for i, robot in enumerate(robots):
                    ang = start_angles[i] + offset
                    x = cup_center[0] + orbit_radius * np.cos(ang)
                    y = cup_center[1] + orbit_radius * np.sin(ang) * 0.7
                    pos = np.array([x, y, 0])
                    if i == 2:  # Bottom right robot
                        pos = pos + br_offset
                    elif i == 3:  # Bottom left robot
                        pos = pos + bl_offset
                    robot.move_to(pos)

            self.play(
                UpdateFromAlphaFunc(robot_group, lambda m, a: update_positions(a)),
                run_time=run_time,
                rate_func=linear
            )
            current_offset[0] = end_offset

        # Rotate multiple times
        orbit_robots(PI * 2, 4.0)  # Full rotation

        # Phase 4: Robots move back inward
        final_offset = current_offset[0]
        start_positions = []
        for i, angle in enumerate(start_angles):
            ang = angle + final_offset
            x = cup_center[0] + start_radius * np.cos(ang)
            y = cup_center[1] + start_radius * np.sin(ang) * 0.7
            pos = np.array([x, y, 0])
            if i == 2:  # Bottom right robot
                pos = pos + br_offset
            elif i == 3:  # Bottom left robot
                pos = pos + bl_offset
            start_positions.append(pos)

        self.play(
            *[robot.animate.move_to(pos) for robot, pos in zip(robots, start_positions)],
            run_time=0.8,
            rate_func=smooth
        )

        # Hold
        self.wait(2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Title Slide with Robots")
    parser.add_argument(
        "quality",
        nargs="?",
        default="low",
        choices=["low", "medium", "high", "4k"],
        help="Output quality (default: low)"
    )
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

    config.output_file = f"TitleSlideRobots_{args.quality}"

    print(f"Rendering at {args.quality} quality: {width}x{height} @ {fps}fps")

    scene = TitleSlideRobots()
    scene.render()
