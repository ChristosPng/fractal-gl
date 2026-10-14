# Fractal Explorer GL

A high-performance, GPU-accelerated 64-bit fractal renderer built with Python, Pygame, ModernGL, and custom GLSL fragment shaders.

Features continuous logarithmic iteration coloring, smooth mouse panning and targeting zoom, and hardware-accelerated double precision math for deep zoom exploration.

## Downloads

Pre-compiled standalone Windows executables are available under the [Releases](https://github.com/ChristosPng/fractal-gl/releases) page. No Python or environment setup required.

## Features

- 64-bit Floating Point Precision (GLSL double precision up to 10^-15 depth)
- Dynamic GLSL Raymarching 
- Smooth Continuous Iteration Coloring (Inigo Quilez Cosine Palettes)
- Click-and-drag panning and cursor-targeted mouse wheel zooming
- Support for multiple fractal sets:
  - Mandelbrot Set
  - Julia Set (with randomized constant generation)
  - Burning Ship Fractal
  - Multibrot Set (z^3 + c)

## Requirements (Running from Source)

- Python 3.8 or higher
- OpenGL 4.0 capable GPU hardware

Dependencies:
- pygame
- moderngl
- numpy

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ChristosPng/fractal-gl.git
   cd fractal-gl

2. Install dependencies:
   ```bash
   pip install pygame moderngl numpy

3. Run the application:
   ```bash
   python main.py

## Controls

| Key / Input | Action |
| :--- | :--- |
| Scroll Wheel | Zoom in / out at cursor location |
| Left Click + Drag | Pan across the complex plane |
| 1 | Switch to Mandelbrot Set |
| 2 | Switch to Julia Set |
| 3 | Switch to Burning Ship Fractal |
| 4 | Switch to Multibrot Set (z^3) |
| C | Generate a random color palette |
| R | Generate a new random Julia Set constant |
| SPACE | Cycle through preset color palettes |
| F / F11 | Toggle fullscreen |
| ESC | Exit application |
