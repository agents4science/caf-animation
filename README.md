# CAF Animation

Generate a narrated video explaining the **Common Agentic Framework (CAF)**, a DOE Genesis ModCon Base project for scalable AI agent orchestration in scientific computing.

## Video Segments

The video includes eight segments:

1. **Title Slide** - Animated robots with CAF branding
2. **Patterns Annotated** - Seven agentic patterns with mini-animations
3. **Academy Slide** - Static slide introducing Academy orchestration framework
4. **OPAL Agents** - Multi-agent collaboration for protein design
5. **Aegis Slide** - Static slide introducing Aegis inference software
6. **Tree Reduction** - Distributed LLM inference with binder inset overlay
7. **Hex Broadcast** - Scaling to 4000 nodes with speedometer visualization
8. **Architecture Overlay** - Final slide showing CAF adoption across Genesis

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate voiceover (requires ElevenLabs API key)
python generate_voiceover_elevenlabs.py

# Build final video at 4K
python build_video_with_audio.py
```

Output: `caf_final_with_voiceover_4k.mp4`

## Requirements

- Python 3.9+
- FFmpeg (must be installed separately)
- Manim (Community Edition)
- ElevenLabs API key (for voiceover generation)

## Project Structure

```
├── build_video_with_audio.py    # Main build script - assembles segments with voiceover
├── generate_voiceover_elevenlabs.py  # Generate voiceover using ElevenLabs TTS
├── caf_voiceover_script_v3.txt  # Voiceover script
├── voiceover_caf_v3.mp3         # Generated voiceover audio
├── llm_tree_reduction_v3.py     # Tree reduction animation (standalone)
├── animations/                   # Manim animation source files
│   ├── architecture_overlay.py  # Final architecture slide animation
│   ├── hex_broadcast.py         # Hex grid broadcast with speedometer
│   ├── opal_agents_v3.py        # OPAL/FAMOUS protein design agents
│   ├── patterns_annotated.py    # Seven CAF patterns with animations
│   └── title_slide_robots.py    # Animated title with robots
├── assets/                       # Images and video assets
│   ├── Academy_Slide.png        # Academy static slide
│   ├── Aegis_Slide.png          # Aegis static slide
│   ├── binder_black.mp4         # Molecular docking video for inset
│   ├── CAF_Patterns.png         # Patterns slide background
│   ├── coffee_cup_white_transparent.png  # Coffee cup for OPAL
│   ├── New_Final_Slide.png      # Architecture overlay background
│   ├── robot_white_clean.png    # Robot image for title
│   └── Title_Slide_norobots.png # Title slide background
└── media/videos/                 # Rendered animation outputs
```

## Rendering Individual Animations

```bash
# Render at 4K quality
python animations/title_slide_robots.py 4k
python animations/patterns_annotated.py 4k --loop
python animations/opal_agents_v3.py 4k
python llm_tree_reduction_v3.py 4k
python animations/hex_broadcast.py 4k
python animations/architecture_overlay.py 4k

# Preview at low quality
python animations/patterns_annotated.py low --loop --preview
```

## Build Options

| Quality | Resolution | FPS | Use Case |
|---------|------------|-----|----------|
| `low`   | 854x480    | 15  | Quick preview |
| `medium`| 1280x720   | 30  | Web sharing |
| `high`  | 1920x1080  | 60  | Presentations |
| `4k`    | 3840x2160  | 60  | High-quality export |

## Segment Timing

The build script (`build_video_with_audio.py`) defines segment timing to sync with the voiceover:

| Segment | Start | Duration | Source |
|---------|-------|----------|--------|
| Title | 0.0s | 10.6s | TitleSlideRobots animation |
| Patterns | 11.6s | 22.4s | PatternsAnnotated animation |
| Academy | 35.0s | 8.0s | Static image |
| OPAL Agents | 43.0s | 13.7s | OpalAgentsV3 animation |
| Aegis | 56.7s | 3.0s | Static image |
| Tree Reduction | 59.7s | 32.3s | LLMTreeReductionV3 + binder inset |
| Hex Broadcast | 89.0s | 18.2s | LLMHexBroadcastFixed4 animation |
| Architecture | 108.2s | 24.6s | ArchitectureOverlay animation |

## Voiceover

The voiceover is generated using ElevenLabs TTS. Edit `caf_voiceover_script_v3.txt` to modify the narration, then regenerate:

```bash
python generate_voiceover_elevenlabs.py
```

## Output Files

- `caf_final_with_voiceover_4k.mp4` - Main output (4K with voiceover)
- `caf_final_imperial_march.mp4` - Version with Imperial March background music
