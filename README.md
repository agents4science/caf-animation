# CAF Animation

Animated video explaining the Common Agentic Framework (CAF), a DOE initiative for scalable AI agent orchestration in scientific computing.

## Overview

This project generates a narrated video demonstrating CAF capabilities through Manim animations:

1. **OPAL Agents** - Agent communication over distributed systems
2. **Scaling Dimensions** - Entity count, interaction intensity, persistence
3. **Tree Reduction** - Distributed LLM query fan-out and reduction
4. **Hex Broadcast** - Scaling inference to 4096 nodes on Aurora

## Requirements

- Python 3.9+
- [Manim](https://docs.manim.community/) (Community Edition)
- FFmpeg
- edge-tts (for text-to-speech)

```bash
pip install manim edge-tts pyyaml
```

## Quick Start

Build the complete video at low quality:

```bash
python build_video.py low
```

Build at higher quality:

```bash
python build_video.py medium   # 720p @ 30fps
python build_video.py high     # 1080p @ 60fps
python build_video.py 4k       # 2160p @ 60fps
```

## Configuration

All video segments, voiceover scripts, and settings are defined in `config.yaml`:

```yaml
segments:
  - name: "intro"
    type: slide
    source: "slides/Title_Slide.png"
    duration: 9
    script: |
      We are here to tell you about the Common Agentic Framework...

  - name: "opal_agents"
    type: animation
    source: "animations/opal_agents.py"
    scene_class: "OpalAgentsAnimationV2"
    script: |
      CAF is developing the agentic orchestration capabilities...
```

### Customizing Content

- **Scripts**: Edit the `script` field for any segment to change narration
- **TTS Voice**: Change `tts.voice` in config (uses [edge-tts voices](https://github.com/rany2/edge-tts))
- **Timing**: Adjust `duration` for slides or modify animation code for videos

## Project Structure

```
.
├── build_video.py          # Main build script
├── config.yaml             # Video configuration
├── animations/             # Manim animation scripts
│   ├── opal_agents.py
│   ├── scaling_sliders.py
│   ├── tree_reduction.py
│   └── hex_broadcast.py
├── slides/                 # Static slide images
│   ├── Title_Slide.png
│   └── architecture.png
├── assets/                 # Animation assets
│   └── OPAL-SPLASH.png
├── audio_segments/         # Generated audio (auto-created)
└── media/                  # Rendered videos (auto-created)
```

## Build Options

```bash
python build_video.py [quality] [options]

Options:
  --skip-render    Skip rendering animations (use existing)
  --skip-audio     Skip generating audio (use existing)
  --config FILE    Use alternative config file
```

## Quality Presets

| Quality | Resolution | FPS | Use Case |
|---------|-----------|-----|----------|
| low     | 854x480   | 15  | Quick preview |
| medium  | 1280x720  | 30  | Web sharing |
| high    | 1920x1080 | 60  | Presentations |
| 4k      | 3840x2160 | 60  | High-quality export |

## Individual Animations

Render animations separately:

```bash
python animations/opal_agents.py high
python animations/scaling_sliders.py high
python animations/tree_reduction.py high
python animations/hex_broadcast.py high
```

Add `--preview` to open the result after rendering.

## License

MIT
