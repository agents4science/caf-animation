"""
Build final video with voiceover audio.

Combines video segments according to timing and adds voiceover.
"""

import subprocess
import os

# Video segments with timing based on caf_voiceover_script_v3.txt
SEGMENTS = [
    # Segment 1: Title - "The Common Agentic Framework..."
    {"start": 0.0, "duration": 10.63, "video": "media/videos/2160p60/TitleSlideRobots_4k.mp4", "offset": 0},

    # Segment 2: Patterns - "Analysis of agentic requirements..."
    {"start": 11.63, "duration": 22.37, "video": "media/videos/2160p60/PatternsAnnotated_4k.mp4", "offset": 0},

    # Segment 3: Academy slide - "A first solution is Academy..."
    {"start": 35.0, "duration": 8.0, "image": "assets/Academy_Slide.png"},

    # Segment 4: OPAL Agents - "For example, the OPAL/FAMOUS..."
    {"start": 43.0, "duration": 13.66, "video": "media/videos/2160p60/OpalAgentsV3_4k.mp4", "offset": 0},

    # Segment 5: Aegis slide - "A second Caf solution is Aegis..."
    {"start": 56.66, "duration": 3.0, "image": "assets/Aegis_Slide.png"},

    # Segment 6: Tree Reduction - "...biological design application..."
    {"start": 59.66, "duration": 32.3, "video": "/tmp/caf_build/tree_with_inset.mp4", "offset": 0},

    # Segment 7: Hex Broadcast - "Using Aegis, we distribute..."
    {"start": 89.04, "duration": 18.20, "video": "media/videos/2160p60/LLMHexBroadcastFixed4_4k.mp4", "offset": 0},

    # Segment 8: Architecture - "Agentic patterns..." + "Important next steps..."
    {"start": 108.24, "duration": 24.64, "video": "media/videos/2160p60/ArchitectureOverlay_4k.mp4", "offset": 0},
]

AUDIO = "voiceover_caf_v3.mp3"
OUTPUT = "caf_final_with_voiceover_4k.mp4"
TEMP_DIR = "/tmp/caf_build"


def get_video_duration(path):
    """Get video duration in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def build_video():
    os.makedirs(TEMP_DIR, exist_ok=True)

    segment_files = []

    for i, seg in enumerate(SEGMENTS):
        target_duration = seg["duration"]
        output_seg = f"{TEMP_DIR}/seg_{i:02d}.mp4"

        # Handle static image
        if "image" in seg:
            image_path = seg["image"]
            print(f"Segment {i+1}: {image_path} (static image)")
            subprocess.run([
                "ffmpeg", "-y",
                "-loop", "1", "-i", image_path,
                "-t", str(target_duration),
                "-vf", "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p",
                output_seg
            ], capture_output=True)
            print(f"  Created {target_duration:.1f}s video from image")
            segment_files.append(output_seg)
            continue

        video_path = seg["video"]
        video_duration = get_video_duration(video_path)

        print(f"Segment {i+1}: {video_path}")
        print(f"  Video duration: {video_duration:.1f}s, Target: {target_duration:.1f}s")

        if video_duration >= target_duration:
            # Video is long enough - just trim
            subprocess.run([
                "ffmpeg", "-y", "-i", video_path,
                "-t", str(target_duration),
                "-vf", "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-an",  # No audio
                output_seg
            ], capture_output=True)
            print(f"  Trimmed to {target_duration:.1f}s")
        else:
            # Video is shorter - slow it down to fit
            speed_factor = video_duration / target_duration
            pts_factor = 1 / speed_factor
            subprocess.run([
                "ffmpeg", "-y", "-i", video_path,
                "-vf", f"setpts={pts_factor}*PTS,scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-an",
                output_seg
            ], capture_output=True)
            print(f"  Slowed by {speed_factor:.2f}x to fit {target_duration:.1f}s")

        segment_files.append(output_seg)

    # Concatenate all segments using filter_complex (more reliable than concat demuxer)
    print("\nConcatenating segments...")
    combined_video = f"{TEMP_DIR}/combined.mp4"

    # Build ffmpeg command with filter_complex
    cmd = ["ffmpeg", "-y"]
    for seg_file in segment_files:
        cmd.extend(["-i", seg_file])

    # Build filter string: [0:v][1:v][2:v]...concat=n=N:v=1:a=0[outv]
    n = len(segment_files)
    filter_inputs = "".join(f"[{i}:v]" for i in range(n))
    filter_str = f"{filter_inputs}concat=n={n}:v=1:a=0[outv]"

    cmd.extend([
        "-filter_complex", filter_str,
        "-map", "[outv]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        combined_video
    ])

    subprocess.run(cmd, capture_output=True)

    # Add audio
    print("Adding voiceover audio...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", combined_video,
        "-i", AUDIO,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT
    ], capture_output=True)

    # Get final duration
    final_duration = get_video_duration(OUTPUT)
    file_size = os.path.getsize(OUTPUT) / (1024 * 1024)

    print(f"\nDone! Output: {OUTPUT}")
    print(f"Duration: {final_duration:.1f}s ({final_duration/60:.1f} min)")
    print(f"Size: {file_size:.1f} MB")

    # Cleanup (disabled for debugging)
    # for f in segment_files:
    #     os.unlink(f)
    # os.unlink(concat_file)
    # os.unlink(combined_video)
    print(f"\nTemp files kept in {TEMP_DIR} for debugging")


if __name__ == "__main__":
    build_video()
