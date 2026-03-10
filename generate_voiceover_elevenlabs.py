"""
Generate TTS Voiceover using ElevenLabs API

Generates audio from the CAF voiceover script using ElevenLabs text-to-speech.
"""

import os
import argparse
from pathlib import Path

try:
    from elevenlabs import ElevenLabs
except ImportError:
    print("ElevenLabs package not installed. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "elevenlabs"], check=True)
    from elevenlabs import ElevenLabs


def generate_voiceover(
    script_path: str = "caf_voiceover_script_v3.txt",
    output_path: str = "voiceover_caf_v3.mp3",
    voice: str = "Adam",  # Default professional male voice
    model: str = "eleven_multilingual_v2",
    api_key: str = None
):
    """
    Generate voiceover audio from script using ElevenLabs.

    Args:
        script_path: Path to the voiceover script text file
        output_path: Path for output audio file
        voice: ElevenLabs voice name (Adam, Rachel, Domi, Bella, Antoni, etc.)
        model: ElevenLabs model ID
        api_key: ElevenLabs API key (or set ELEVENLABS_API_KEY env var)
    """
    # Get API key
    api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "No API key provided. Set ELEVENLABS_API_KEY environment variable "
            "or pass --api-key argument."
        )

    # Read script
    script_file = Path(script_path)
    if not script_file.exists():
        raise FileNotFoundError(f"Script file not found: {script_path}")

    text = script_file.read_text().strip()
    print(f"Script loaded: {len(text)} characters")

    # Initialize client
    client = ElevenLabs(api_key=api_key)

    # Common voice IDs (pre-made voices)
    # See: https://elevenlabs.io/docs/voices/premade-voices
    VOICE_IDS = {
        "adam": "pNInz6obpgDQGcFmaJgB",      # American male, deep
        "antoni": "ErXwobaYiN019PkySvjV",    # American male, well-rounded
        "arnold": "VR6AewLTigWG4xSOukaG",    # American male, crisp
        "bella": "EXAVITQu4vr4xnSDxMaL",     # American female, soft
        "domi": "AZnzlk1XvdvUeBnXmlld",      # American female, strong
        "elli": "MF3mGyEYCl7XYWbV9V6O",      # American female, emotional
        "josh": "TxGEqnHWrfWFTfGW9XjX",      # American male, deep
        "rachel": "21m00Tcm4TlvDq8ikWAM",    # American female, calm
        "sam": "yoZ06aMxZJJ28mfd3POQ",       # American male, raspy
    }

    # Find voice ID
    voice_id = VOICE_IDS.get(voice.lower(), voice)
    print(f"\nUsing voice: {voice} ({voice_id})")

    # Generate audio
    print(f"\nGenerating audio with model: {model}")
    print("This may take a moment...")

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=model,
        output_format="mp3_44100_128"
    )

    # Save audio - audio is a generator, need to consume it
    output_file = Path(output_path)
    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"\nAudio saved to: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate TTS voiceover using ElevenLabs"
    )
    parser.add_argument(
        "--script", "-s",
        default="caf_voiceover_script_v3.txt",
        help="Path to voiceover script (default: caf_voiceover_script_v3.txt)"
    )
    parser.add_argument(
        "--output", "-o",
        default="voiceover_caf_v3.mp3",
        help="Output audio file path (default: voiceover_caf_v3.mp3)"
    )
    parser.add_argument(
        "--voice", "-v",
        default="Adam",
        help="Voice name or ID (default: Adam)"
    )
    parser.add_argument(
        "--model", "-m",
        default="eleven_multilingual_v2",
        help="Model ID (default: eleven_multilingual_v2)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="ElevenLabs API key (or set ELEVENLABS_API_KEY env var)"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available voices and exit"
    )

    args = parser.parse_args()

    if args.list_voices:
        print("Available pre-made voices:")
        print("  adam    - American male, deep")
        print("  antoni  - American male, well-rounded")
        print("  arnold  - American male, crisp")
        print("  bella   - American female, soft")
        print("  domi    - American female, strong")
        print("  elli    - American female, emotional")
        print("  josh    - American male, deep")
        print("  rachel  - American female, calm")
        print("  sam     - American male, raspy")
        return

    generate_voiceover(
        script_path=args.script,
        output_path=args.output,
        voice=args.voice,
        model=args.model,
        api_key=args.api_key
    )


if __name__ == "__main__":
    main()
