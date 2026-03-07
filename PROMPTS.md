# Development Prompts

This document captures the key prompts used to generate and refine the animations in this project.

## OPAL Agents (`animations/opal_agents.py`)

**Initial prompt:**
> Show agents communicating over the OPAL architecture diagram. Messages flow between agents, and some trigger compute task generation.

**Refinements:**
> Add an HPC system visual. Show tasks being dispatched to HPC cores when simulation and binder agents are activated.

> Add title "DOE Science is Becoming Agentic" and subtitle "Scalable Agentic Reasoning for Biologics Design"

> Run multiple iterations of agent communication to show ongoing collaboration.

## Scaling Sliders (`animations/scaling_sliders.py`)

**Initial prompt:**
> Create a control panel with three sliders showing the scaling dimensions of CAF: Entity Count (agents, tools), Interaction Intensity (communication variety/volume), and Persistence (state maintenance over time).

**Refinements:**
> For Entity Count, show agents and tools accumulating in a grid as the slider rises.

> For Interaction Intensity, show network nodes with connections appearing, then animated messages flowing along edges.

> For Persistence, replace the timeline visualization with a day counter that shows 1 → 7 → 30 → 90 → 365 days as the slider increases.

> Add 6.5 second initial pause so viewers can read the title before animations begin.

## Tree Reduction (`animations/tree_reduction.py`)

**Initial prompt:**
> Show distributed LLM query fan-out and tree reduction. Dispatcher at top sends queries down to leaf nodes at bottom. Results flow upward through combine levels. Final winner emerges at top.

**Refinements:**
> Each leaf node should show a protein-target pair with results (Kd value and modality).

> Add a legend in upper left explaining what the leaf node contents represent: protein, target, Kd result, modality result.

> Keep the legend visible throughout the entire animation, not just briefly.

> Make target text white instead of gray for visibility.

## Hex Broadcast (`animations/hex_broadcast.py`)

**Initial prompt:**
> Create a hex-lattice broadcast and reduction visualization. Show broadcast ring-by-ring using hex-neighbor edges. Each sender forwards to two neighbors. Include a node anatomy panel showing Agent Logic → Inference Server → GPU.

**Refinements:**
> Add a speedometer panel on the right showing "Tokens/s" with scale 0-2M. Animate the needle ramping up during inference phase.

> Color the node anatomy components to match the current phase: yellow during broadcast (agent logic), red during inference (inference server + GPU), blue during reduction.

> Make the animation faster: reduce slow_time from 1.0 to 0.7, fast_time from 0.35 to 0.25, pulsate from 5 to 3 iterations.

## Build System (`build_video.py`)

**Initial prompt:**
> Create a build script that combines video segments with audio. Support multiple quality levels (low/medium/high/4k).

**Refinements:**
> Move all configuration to config.yaml: segment definitions, voiceover scripts, TTS settings.

> Generate audio on-the-fly from the scripts in config.yaml using edge-tts.

> Support both static slides (PNG with duration) and animations (Manim scripts).

> Use relative paths throughout so the project is portable.
