#!/usr/bin/env python3
"""
Build the CAF video from configuration.

Reads config.yaml to determine segments, generates audio from scripts,
renders animations, and combines everything into a final video.

Usage:
    python build_video.py [quality] [options]

    quality: low, medium, high, 4k (default: low)

Options:
    --skip-render    Skip rendering animations (use existing)
    --skip-audio     Skip generating audio (use existing)
    --config FILE    Use alternative config file (default: config.yaml)
"""

import subprocess
import os
import sys
import argparse
import yaml
import tempfile
import asyncio

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_duration(filepath):
    """Get media duration in seconds."""
    result = subprocess.run([
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0", filepath
    ], capture_output=True, text=True)
    return float(result.stdout.strip())


async def generate_audio(text, output_path, voice, rate="+0%"):
    """Generate audio from text using edge-tts."""
    import edge_tts

    communicate = edge_tts.Communicate(text.strip(), voice, rate=rate)
    await communicate.save(output_path)


def generate_audio_sync(text, output_path, voice, rate="+0%"):
    """Synchronous wrapper for audio generation."""
    asyncio.run(generate_audio(text, output_path, voice, rate))


def render_animation(script_path, scene_class, quality, config):
    """Render a manim animation at specified quality."""
    preset = config['quality_presets'][quality]
    height, width, fps = preset['height'], preset['width'], preset['fps']
    folder = preset['folder']

    # Determine output filename
    output_name = f"{scene_class}_{quality}"
    output_path = os.path.join(SCRIPT_DIR, "media", "videos", folder, f"{output_name}.mp4")

    if os.path.exists(output_path):
        print(f"    Skipping {scene_class} (exists)")
        return output_path

    print(f"    Rendering {scene_class}...")

    # Run the animation script with quality argument
    full_script_path = os.path.join(SCRIPT_DIR, script_path)
    subprocess.run([
        "python", full_script_path, quality
    ], cwd=SCRIPT_DIR, capture_output=True)

    return output_path


def build_segment_with_audio(video_path, audio_path, output_path, preset, is_slide=False, slide_duration=None):
    """Combine a video segment with its audio."""
    height, width, fps = preset['height'], preset['width'], preset['fps']

    if is_slide:
        # Convert slide to video with audio
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", video_path,
            "-i", audio_path,
            "-c:v", "libx264", "-t", str(slide_duration),
            "-pix_fmt", "yuv420p",
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black",
            "-r", str(fps),
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_path
        ], capture_output=True)
    else:
        # Normalize video and add audio
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,fps={fps}",
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v", "-map", "1:a",
            "-shortest",
            output_path
        ], capture_output=True)


def main():
    parser = argparse.ArgumentParser(description="Build CAF video from configuration")
    parser.add_argument("quality", nargs="?", default="low",
                       choices=["low", "medium", "high", "4k"])
    parser.add_argument("--skip-render", action="store_true",
                       help="Skip rendering animations (use existing)")
    parser.add_argument("--skip-audio", action="store_true",
                       help="Skip generating audio (use existing)")
    parser.add_argument("--config", default="config.yaml",
                       help="Config file path (default: config.yaml)")
    args = parser.parse_args()

    # Load configuration
    config_path = os.path.join(SCRIPT_DIR, args.config)
    config = load_config(config_path)

    quality = args.quality
    preset = config['quality_presets'][quality]

    print("=" * 60)
    print(f"Building: {config['title']}")
    print(f"Quality: {quality} ({preset['width']}x{preset['height']} @ {preset['fps']}fps)")
    print("=" * 60)

    # Create directories
    audio_dir = os.path.join(SCRIPT_DIR, "audio_segments")
    temp_dir = os.path.join(SCRIPT_DIR, "temp_segments")
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    segments = config['segments']
    tts_config = config['tts']

    # Step 1: Generate audio for each segment
    if not args.skip_audio:
        print("\n=== Generating audio ===")
        for i, segment in enumerate(segments):
            audio_path = os.path.join(audio_dir, f"{i+1:02d}_{segment['name']}.mp3")
            if os.path.exists(audio_path):
                print(f"  [{i+1}/{len(segments)}] {segment['name']} (exists)")
            else:
                print(f"  [{i+1}/{len(segments)}] {segment['name']}...")
                generate_audio_sync(
                    segment['script'],
                    audio_path,
                    tts_config['voice'],
                    tts_config.get('rate', '+0%')
                )
                dur = get_duration(audio_path)
                print(f"    Generated: {dur:.1f}s")

    # Step 2: Render animations if needed
    if not args.skip_render:
        print("\n=== Rendering animations ===")
        for segment in segments:
            if segment['type'] == 'animation':
                render_animation(
                    segment['source'],
                    segment['scene_class'],
                    quality,
                    config
                )

    # Step 3: Build each segment with audio
    print("\n=== Building segments with audio ===")
    segment_files = []

    for i, segment in enumerate(segments):
        print(f"  [{i+1}/{len(segments)}] {segment['name']}")

        audio_path = os.path.join(audio_dir, f"{i+1:02d}_{segment['name']}.mp3")
        if not os.path.exists(audio_path):
            print(f"    ERROR: Audio not found: {audio_path}")
            continue

        # Determine video path
        if segment['type'] == 'slide':
            video_path = os.path.join(SCRIPT_DIR, segment['source'])
            is_slide = True
            slide_duration = segment.get('duration', 10)
        else:
            # Animation - construct path
            folder = preset['folder']
            scene_class = segment['scene_class']
            video_path = os.path.join(
                SCRIPT_DIR, "media", "videos", folder,
                f"{scene_class}_{quality}.mp4"
            )
            is_slide = False
            slide_duration = None

        if not os.path.exists(video_path):
            print(f"    ERROR: Video not found: {video_path}")
            continue

        output_path = os.path.join(temp_dir, f"segment_{i:02d}.mp4")
        build_segment_with_audio(
            video_path, audio_path, output_path,
            preset, is_slide, slide_duration
        )

        if os.path.exists(output_path):
            segment_files.append(output_path)
            dur = get_duration(output_path)
            print(f"    OK: {dur:.1f}s")

    # Step 4: Concatenate all segments
    print("\n=== Concatenating segments ===")

    concat_list = os.path.join(temp_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for seg_file in segment_files:
            f.write(f"file '{seg_file}'\n")

    output_filename = config.get('output_filename', 'output')
    output_file = os.path.join(SCRIPT_DIR, f"{output_filename}_{quality}.mp4")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        output_file
    ], capture_output=True)

    # Cleanup
    for f in segment_files:
        os.remove(f)
    os.remove(concat_list)
    os.rmdir(temp_dir)

    # Report
    if os.path.exists(output_file):
        duration = get_duration(output_file)
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n{'=' * 60}")
        print(f"SUCCESS!")
        print(f"  Output: {output_file}")
        print(f"  Duration: {duration:.1f}s ({duration/60:.1f} min)")
        print(f"  Size: {size:.1f} MB")
        print("=" * 60)
    else:
        print("\nERROR: Failed to create video")
        sys.exit(1)


if __name__ == "__main__":
    main()
