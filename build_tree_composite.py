"""
Build tree reduction composite with binder inset overlay.

Creates the tree_with_inset_{quality}.mp4 files needed by build_video_with_audio.py.
"""

import subprocess
import os
import argparse

# Quality settings matching build_video_with_audio.py
QUALITY_MAP = {
    "low": {"dir": "480p15", "suffix": "low", "fps": 15, "scale": 108, "pad": 8, "margin": 20},
    "medium": {"dir": "720p30", "suffix": "medium", "fps": 30, "scale": 162, "pad": 12, "margin": 30},
    "high": {"dir": "1080p60", "suffix": "high", "fps": 60, "scale": 243, "pad": 12, "margin": 45},
    "4k": {"dir": "2160p60", "suffix": "4k", "fps": 60, "scale": 486, "pad": 16, "margin": 90},
}

TEMP_DIR = "/tmp/caf_build"
BINDER_SOURCE = "assets/binder_black.mp4"

# Binder inset parameters:
# - Extract seconds 6-11 from binder_black.mp4
# - Crop: 1/3 from left, 1/3 from right, 1/4 from top (crop=366:434:457:215)
# - Add semi-transparent background padding
# - Overlay at top-right, starting at 15.8s in tree reduction

BINDER_CROP = "crop=366:434:457:215"
BINDER_START = 6
BINDER_DURATION = 5
OVERLAY_START = 15.8


def build_composite(quality):
    """Build tree reduction composite with binder inset at specified quality."""
    q = QUALITY_MAP[quality]
    os.makedirs(TEMP_DIR, exist_ok=True)

    tree_video = f"media/videos/{q['dir']}/LLMTreeReductionV3_{q['suffix']}.mp4"
    binder_inset = f"{TEMP_DIR}/binder_alpha_{q['suffix']}.mov"
    output = f"{TEMP_DIR}/tree_with_inset_{q['suffix']}.mp4"

    # Check tree video exists
    if not os.path.exists(tree_video):
        print(f"Error: {tree_video} not found. Render it first with:")
        print(f"  python animations/llm_tree_reduction_v3.py {quality}")
        return False

    # Create binder inset with alpha channel
    print(f"Creating binder inset at {q['suffix']} quality...")
    scale = q["scale"]
    pad = q["pad"]
    fps = q["fps"]

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(BINDER_START),
        "-i", BINDER_SOURCE,
        "-t", str(BINDER_DURATION),
        "-vf", f"{BINDER_CROP},fps={fps},scale={scale}:-2,format=rgba,pad=w=iw+{pad}:h=ih+{pad}:x={pad//2}:y={pad//2}:color=black@0.3",
        "-c:v", "png",
        binder_inset
    ], capture_output=True)

    # Overlay onto tree reduction
    print(f"Building composite...")
    margin = q["margin"]

    subprocess.run([
        "ffmpeg", "-y",
        "-i", tree_video,
        "-i", binder_inset,
        "-filter_complex", f"[1:v]setpts=PTS-STARTPTS+{OVERLAY_START}/TB[inset];[0:v][inset]overlay=W-w-{margin}:{margin}:eof_action=pass[out]",
        "-map", "[out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-an",
        output
    ], capture_output=True)

    print(f"Done: {output}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build tree reduction composite with binder inset")
    parser.add_argument(
        "quality",
        nargs="?",
        default="4k",
        choices=["low", "medium", "high", "4k"],
        help="Output quality (default: 4k)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all quality levels"
    )
    args = parser.parse_args()

    if args.all:
        for q in QUALITY_MAP:
            print(f"\n=== Building {q} ===")
            build_composite(q)
    else:
        build_composite(args.quality)
