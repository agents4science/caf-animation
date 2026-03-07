# CAF Animation

Generate a narrated video explaining the **Common Agentic Framework (CAF)**, a DOE initiative for scalable AI agent orchestration in scientific computing.

The video includes four animated segments:
1. **OPAL Agents** - Multi-agent collaboration for protein design
2. **Scaling Dimensions** - Entity count, interaction intensity, persistence
3. **Tree Reduction** - Distributed LLM inference with result aggregation
4. **Hex Broadcast** - Scaling to 4096 nodes on Aurora supercomputer

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Build video (low quality for quick preview)
python build_video.py low

# Build production quality
python build_video.py high
```

Output: `caf_video_final_<quality>.mp4`

## Requirements

- Python 3.9+
- FFmpeg (must be installed separately)
- Dependencies: `pip install -r requirements.txt`

## Customization

Edit `config.yaml` to change:

**Voiceover scripts** - Modify the `script` field for any segment:
```yaml
segments:
  - name: "intro"
    script: |
      Your custom narration text here...
```

**TTS voice** - Change the narrator voice:
```yaml
tts:
  voice: "en-US-GuyNeural"  # See edge-tts for available voices
  rate: "+0%"               # Speed adjustment
```

**Slide timing** - Adjust duration for static slides:
```yaml
  - name: "intro"
    type: slide
    duration: 9  # seconds
```

## Project Structure

```
├── build_video.py      # Main build script
├── config.yaml         # Video configuration (scripts, settings)
├── animations/         # Manim animation source files
├── slides/             # Static slide images (PNG)
├── assets/             # Animation assets
└── PROMPTS.md          # Prompts used to generate the code
```

## Development

See [PROMPTS.md](PROMPTS.md) for the prompts used to generate and refine each animation. Each animation file also includes docstrings describing the generative intent.

## Build Options

| Quality | Resolution | FPS | Use Case |
|---------|------------|-----|----------|
| `low`   | 854x480    | 15  | Quick preview |
| `medium`| 1280x720   | 30  | Web sharing |
| `high`  | 1920x1080  | 60  | Presentations |
| `4k`    | 3840x2160  | 60  | High-quality export |

```bash
python build_video.py <quality> [options]

Options:
  --skip-render    Use existing rendered animations
  --skip-audio     Use existing generated audio
  --config FILE    Use alternative config file
```

## Rendering Individual Animations

```bash
python animations/opal_agents.py high --preview
python animations/scaling_sliders.py high --preview
python animations/tree_reduction.py high --preview
python animations/hex_broadcast.py high --preview
```
