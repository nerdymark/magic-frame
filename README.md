# NeoPixel LED Matrix Picture Frame

A mesmerizing 18x18 LED matrix display featuring animations, games, optical illusions, and visual effects. Built with CircuitPython for the Raspberry Pi Pico W.

🎮 **[Try the Live Web Simulation →](https://nerdymark.com/magic-frame-sim)**

![LED Matrix Demo](https://img.shields.io/badge/LEDs-324-brightgreen) ![CircuitPython](https://img.shields.io/badge/CircuitPython-9.x-blueviolet) ![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- **50+ Animation Modules**: From serene water ripples to dynamic plasma effects, mathematical visualizations, and particle systems
- **Optical Illusions**: Afterimage/cone fatigue, simultaneous contrast, and Hermann/scintillating grid effects
- **Games**: Self-playing Snake, Strategic Snake AI, and Conway's Game of Life
- **Flag Displays**: Pride, Trans, Ukraine, USA, and Palestine flags with realistic wave physics
- **Particle Systems**: Fish schooling, bug swarms, Matrix rain, bubbles, and starfields
- **Mathematical Art**: Mandelbrot/Julia fractals, Lissajous curves, plasma effects, and tunnel visualization
- **Retro Demoscene Effects**: C64-style copper bars, raster bars, rotozoomer, Glenz vectors, Mode 7, and lens flare
- **3D Graphics**: Hypercube (tesseract), voxel terrain, Rubik's cube, and shading demos
- **Ultra-Optimized Performance**: CPU overclocking, lookup tables, and efficient serpentine wiring support

## 🛠️ Hardware Requirements

- **Microcontroller**: Raspberry Pi Pico W (or compatible CircuitPython board)
- **LED Strip**: WS2812B (NeoPixel) strip with 324 LEDs
- **Power Supply**: 5V power supply capable of at least 20A (324 LEDs × 60mA max per LED = 19.44A theoretical max)
- **Additional Components**:
  - 1000µF capacitor (across power supply terminals)
  - 470Ω resistor (between data pin and first LED)
  - Optional: Logic level shifter for 3.3V → 5V conversion

## 📐 Hardware Build Instructions

### LED Matrix Layout

The 324 LEDs are arranged in an 18×18 matrix with serpentine wiring:
- **Even rows** (0, 2, 4...): Right to left
- **Odd rows** (1, 3, 5...): Left to right

```
Row 0: ←←←←←←←←←←←←←←←←←← (LEDs 0-17)
Row 1: →→→→→→→→→→→→→→→→→→ (LEDs 18-35)
Row 2: ←←←←←←←←←←←←←←←←←← (LEDs 36-53)
...and so on
```

### Wiring Diagram

```
Raspberry Pi Pico W          NeoPixel Strip
┌─────────────────┐         ┌─────────────┐
│                 │         │             │
│            GP1  ├─[470Ω]──┤ DIN         │
│                 │         │             │
│            VBUS ├─────────┤ 5V+         │
│                 │         │             │
│            GND  ├─────────┤ GND         │
│                 │         │             │
└─────────────────┘         └─────────────┘
                                   │
                              [1000µF Cap]
                                   │
                            5V Power Supply
```

### Assembly Steps

1. **Prepare the LED Matrix**
   - Cut WS2812B strip into 18 segments of 18 LEDs each
   - Solder strips in serpentine pattern (alternate direction each row)
   - Mount on backing material (foam board, wood, or 3D printed frame)

2. **Power Connections**
   - Connect 5V power supply to LED strip power terminals
   - Add 1000µF capacitor across power terminals (observe polarity!)
   - Connect ground between Pico and LED strip

3. **Data Connection**
   - Solder 470Ω resistor to GP1 pin
   - Connect resistor output to DIN of first LED
   - Optional: Use logic level shifter for more reliable operation

4. **Final Setup**
   - Mount Pico W securely
   - Ensure all connections are solid
   - Add diffusion material over LEDs for better visual effect

## 💾 Software Installation

1. **Install CircuitPython**
   - Download CircuitPython 9.x for Raspberry Pi Pico W
   - Hold BOOTSEL button while connecting USB
   - Copy the .uf2 file to the RPI-RP2 drive

2. **Install Dependencies**
   - Copy the `neopixel.mpy` library to the `lib` folder
   - Ensure `adafruit_pixelbuf.mpy` is also present

3. **Deploy Code**
   - Copy `code.py` to the root of CIRCUITPY drive
   - Copy entire `matrix_modules` folder to CIRCUITPY drive
   - The animations will start automatically!

## 🎨 Animation Modules

### **🧠 Optical Illusions**

These modules exploit specific quirks in human visual perception. They work best when viewed from a comfortable distance (2–4 feet).

#### 🔴 **afterimage**
Exploits cone fatigue — staring at a bright saturated color for several seconds tires the retinal cones sensitive to that hue. When the display switches to neutral white, the viewer briefly sees the complementary color as an afterimage. Cycles through six patterns (halves, cross, bullseye, checkerboard, diagonal, quadrants) using cyan, yellow, and magenta. *Fix your gaze on the center for ~7 seconds, then hold still when it turns white.*

#### 🟦 **simultaneous_contrast**
The exact same neutral gray square appears dramatically different depending on its surrounding color. On a blue background it looks warm; the identical square on an orange background looks cool. The visual cortex compensates for assumed "ambient light" by shifting perceived hue in the complementary direction. Cycles through six contrasting background pairs.

#### ⬛ **scintillating_grid**
A 3×3 arrangement of dark squares separated by bright corridors creates phantom dark smudges at the corridor intersections (Hermann grid effect). Adding brighter blobs at each intersection causes them to appear to flicker as your eyes scan across (scintillating grid variant). Alternates between both variants across four color themes. *Let your gaze wander freely — don't fixate.*

### **Particle & Natural Effects**

#### 🌊 **water_ripples**
Soothing underwater scene with gentle ripples spreading across the surface. Features realistic ripple physics, depth-based blue-green coloring, and random ripple generation for a peaceful aquatic atmosphere.

#### 🫧 **bubbles**
Endless floating bubbles rising through water with realistic physics. Bubbles vary in size and speed, with natural horizontal drift and shimmer effects. Includes occasional surface bubble bursts.

#### ❄️ **blizzard**
Immersive snowfall animation with wind effects and ground accumulation. Features dynamic wind gusts, varying snowflake sizes, realistic physics, and snow buildup patterns.

#### 🔥 **fire**
Realistic fire simulation with turbulent flames and ember particles. Uses cellular automata for natural flame behavior with heat diffusion and particle physics.

#### ⭐ **starfield**
Ultra-optimized 3D starfield with stars moving toward the viewer. Features parallax motion, varying star brightness, and smooth depth-based movement for a space travel effect.

#### 🌋 **lava_lamp**
Relaxing lava lamp effect with realistic blob physics. Features temperature-based buoyancy, organic blob shapes, merging/splitting behavior, and warm ambient colors.

### **Aquatic & Marine Life**

#### 🐟 **fish_schooling**
Realistic fish schooling behavior with multiple species swimming in coordinated groups. Features boids flocking algorithm, species-based coloring, and 3D-like depth effects.

#### 🐠 **fishtank**
Complete aquarium simulation with sandy bottom, shimmering blue water, rising bubbles, and fish swimming by. Non-uniform fish patterns create a realistic underwater environment.

#### 🐛 **bug_swarm**
A leader bug guides a swarm of followers using advanced flocking behavior. Features boids algorithm, dynamic trail effects, collision avoidance, and emergent group behaviors.

### **Games & Interactive**

#### 🐍 **snake_game**
Classic self-playing Snake game with intelligent pathfinding AI. Features wall avoidance, food-seeking behavior, and oscillation prevention for extended gameplay.

#### 🐍 **strategic_snake**
Advanced AI Snake that uses edge-following pathfinding to build the longest possible tail. Features A* pathfinding, trap avoidance, and strategic movement for maximum scores.

#### 🧬 **john_conways_game_of_life**
Conway's Game of Life with colorful mutations and visitor injection system. Features color inheritance, dynamic mutation rates, automatic restart, and population management.

#### 🧩 **maze**
Procedurally generated mazes with animated solving. Generates a new solvable maze each run and animates the pathfinding solution.

### **Mathematical & Fractal Art**

#### 🌀 **mandelbrot_julia**
Beautiful Mandelbrot and Julia set fractals with smooth color transitions. Features deep ocean color themes, zooming effects, and mathematically precise rendering.

#### 🌊 **plasma** & **plasma_two** & **diamond_plasma** & **ripple_plasma** & **spiral_plasma**
Multiple plasma effect variations using mathematical wave functions. Each features unique interference patterns, color cycling, blob physics, and hypnotic visual effects.

#### 📐 **lissajous_curves**
Animated Lissajous curves showing mathematical relationships between sine waves. Features parametric equations, color trails, and smooth curve evolution.

#### 🌀 **moire_patterns**
Hypnotic moiré interference patterns created by overlapping mathematical grids. Features rotation effects, scaling animations, and optical illusion phenomena.

#### 🧬 **dna_helix**
Double helix DNA structure with rotating base pairs and genetic code visualization. Features scientifically accurate structure, smooth rotation, and nucleotide coloring.

### **3D Graphics & Visualization**

#### 🔮 **hypercube_4d**
A four-dimensional hypercube (tesseract) projected into 2D and animated through 4D rotation. Features smooth perspective projection, depth-based coloring, and continuous rotation through multiple axes.

#### 🏔️ **voxel_terrain**
Voxel-based terrain flythrough with procedurally generated landscapes. Features height maps, depth shading, and smooth camera movement over rolling terrain.

#### 🎲 **rubiks_cube**
Animated Rubik's cube with scrambling and solving sequences. Features accurate face rotation mechanics, bright color faces, and isometric-style projection.

#### 💡 **shading_demo**
Demonstration of 3D shading and lighting techniques including Lambertian diffuse shading, specular highlights, and ambient occlusion on simple geometric forms.

#### 🔷 **glenz_vectors**
Classic demoscene Glenz vector effect — semi-transparent 3D wireframe objects with correct face ordering and color blending. Named after the Glenz demo that popularized the technique.

#### 🎮 **mode7**
SNES-style Mode 7 perspective floor transformation with tiled texture mapping. Recreates the iconic scaling/rotation effect used in classic games like F-Zero and Mario Kart.

### **Classic Demoscene Effects**

#### 🌈 **tunnel**
Classic 3D tunnel effect with rainbow colors and smooth animation. Features perspective transformation, texture mapping, and psychedelic color cycling.

#### 🔧 **rotozoomer**
Rotating and zooming texture effects inspired by classic demos. Features mathematical transformation matrices, texture sampling, and smooth motion.

#### 🌈 **copper_bars**
C64-style horizontal copper bars with smooth color gradients. Features classic demoscene aesthetics, color interpolation, and nostalgic 8-bit styling.

#### 📺 **raster_bars**
Retro raster bar effects with sine wave motion and color cycling. Features smooth gradients, wave distortion, and classic computer demo aesthetics.

#### ✨ **lens_flare**
Realistic lens flare effects with multiple light sources and optical artifacts. Features bloom effects, chromatic aberration, and cinematic lighting.

#### 💻 **c64_demoscene**
Comprehensive Commodore 64 demoscene tribute with multiple classic effects. Features authentic color palettes, bitmap fonts, and retro visual styling.

#### 🟣 **shadebobs**
Classic demoscene shadebob effect — multiple glowing blobs that bounce and combine, creating smooth additive color blending and psychedelic trails.

#### 🫁 **metaballs**
Organic metaball fluid simulation where circular fields merge smoothly into blob-like shapes. Features real-time isosurface rendering and fluid color transitions.

#### 📜 **parallax_scroller**
Classic multi-layer parallax scrolling with foreground, midground, and background layers moving at different speeds. Recreates the depth illusion from early arcade and console games.

### **Text & Communication**

#### 📜 **sine_scrollers**
Smooth scrolling text with sine wave motion. Features classic demo-style text animation and wave distortion.

#### 📱 **qr_renderer**
QR code generation and display with error correction. Features dynamic code generation, proper formatting, and scannable output.

#### 🍎 **apple_event_sep_2025**
Special Apple-themed animation for events. Features Apple logo aesthetics and smooth transitions.

### **Abstract & Artistic**

#### 🎯 **vector_balls**
Animated vector balls with physics simulation and trail effects. Features collision detection, momentum conservation, and smooth particle motion.

#### 🔦 **search_light**
Three searchlights hunting for hidden targets with celebration effects. Features dynamic movement patterns, collision detection, and rainbow victory animations.

#### 📀 **dvd_screen_saver**
Classic bouncing DVD logo with color changes on wall hits. Features accurate physics simulation and nostalgia-inducing movement.

#### 🧱 **falling_blocks**
Tetris-inspired falling blocks that stack and clear. Features collision detection, block rotation, stacking physics, and automatic reset functionality.

#### 💊 **the_matrix**
Iconic Matrix digital rain effect with trailing characters. Features authentic green color scheme, random character generation, and fade effects.

#### 🏳️ **flag_wave**
Animated flags with realistic wave physics — sine wave distortion, dynamic lighting, and smooth color transitions. Available modes:
- **pride** — 7-stripe rainbow
- **trans** — blue/pink/white
- **ukraine** — blue and yellow
- **usa** — stars and stripes with blue canton
- **palestine** — black/white/green stripes with red triangle

## 📁 Project Structure

```
/CIRCUITPY/
├── code.py                          # Main entry point — random shuffle animation loop
├── lib/                             # CircuitPython libraries
│   ├── neopixel.mpy
│   └── adafruit_pixelbuf.mpy
└── matrix_modules/                  # 50+ Animation modules
    ├── __init__.py
    ├── constants.py                 # Lookup tables, timing constants, CPU overclocking
    ├── utils.py                     # Shared utilities & serpentine pixel mapping
    │
    ├── # Optical Illusions
    ├── afterimage.py               # Cone fatigue & complementary color afterimage
    ├── simultaneous_contrast.py    # Same color looks different on contrasting backgrounds
    ├── scintillating_grid.py       # Hermann grid & scintillating grid phantom spots
    │
    ├── # Particle & Natural Effects
    ├── water_ripples.py            # Soothing water simulation
    ├── bubbles.py                  # Floating bubbles with physics
    ├── blizzard.py                 # Snow simulation with wind
    ├── fire.py                     # Realistic fire simulation
    ├── starfield.py                # 3D star travel effect
    ├── lava_lamp.py                # Relaxing lava lamp physics
    │
    ├── # Aquatic & Marine Life
    ├── fish_schooling.py           # Boids flocking algorithm
    ├── fishtank.py                 # Complete aquarium simulation
    ├── bug_swarm.py                # Leader-follower swarm behavior
    │
    ├── # Games & Interactive
    ├── snake_game.py               # Classic AI Snake game
    ├── strategic_snake.py          # Advanced pathfinding Snake
    ├── john_conways_game_of_life.py # Game of Life with mutations
    ├── maze.py                     # Procedural maze generation & solving
    │
    ├── # Mathematical & Fractal Art
    ├── mandelbrot_julia.py         # Fractal visualization
    ├── plasma.py                   # Classic plasma effect
    ├── plasma_two.py               # Alternative plasma algorithm
    ├── diamond_plasma.py           # Diamond-pattern plasma
    ├── ripple_plasma.py            # Ripple interference plasma
    ├── spiral_plasma.py            # Spiral interference patterns
    ├── lissajous_curves.py         # Parametric curve animation
    ├── moire_patterns.py           # Optical interference effects
    ├── dna_helix.py                # Double helix visualization
    │
    ├── # 3D Graphics & Visualization
    ├── hypercube_4d.py             # 4D tesseract rotation
    ├── voxel_terrain.py            # Voxel terrain flythrough
    ├── rubiks_cube.py              # Animated Rubik's cube
    ├── shading_demo.py             # 3D shading & lighting techniques
    ├── glenz_vectors.py            # Semi-transparent 3D wireframes
    ├── mode7.py                    # SNES-style perspective floor
    │
    ├── # Classic Demoscene Effects
    ├── tunnel.py                   # 3D tunnel with rainbow colors
    ├── rotozoomer.py               # Rotating/zooming textures
    ├── copper_bars.py              # C64-style color gradients
    ├── raster_bars.py              # Retro raster effects
    ├── lens_flare.py               # Cinematic lighting effects
    ├── c64_demoscene.py            # Comprehensive C64 tribute
    ├── shadebobs.py                # Bouncing glowing blobs
    ├── metaballs.py                # Organic fluid metaballs
    ├── parallax_scroller.py        # Multi-layer parallax scrolling
    │
    ├── # Text & Communication
    ├── sine_scrollers.py           # Wave-distorted scrolling text
    ├── qr_renderer.py              # QR code generation
    ├── apple_event_sep_2025.py     # Apple-themed animation
    │
    └── # Abstract & Artistic
        ├── vector_balls.py         # Physics-based particle motion
        ├── search_light.py         # Target-hunting searchlights
        ├── dvd_screen_saver.py     # Classic bouncing logo
        ├── falling_blocks.py       # Tetris-inspired blocks
        ├── the_matrix.py           # Matrix digital rain
        └── flag_wave.py            # Animated flags (pride/trans/ukraine/usa/palestine)
```

## 🔧 Customization

### Adding Animations
1. Create a new file in `matrix_modules/`
2. Implement the standard animation function signature:
```python
def my_animation(pixels, width=WIDTH, height=HEIGHT, delay=0, max_frames=1000):
    pass
```
3. Add a try/except import block and an entry in the `_all_animations` list in `code.py`

### Adjusting Brightness
Modify `DEFAULT_BRIGHTNESS` in `matrix_modules/constants.py`:
```python
DEFAULT_BRIGHTNESS = 0.2  # Range: 0.0 to 1.0
```

## ⚡ Performance Optimizations

### **Hardware Overclocking**
- **CPU Speed**: Overclocked to **250MHz** via `boot.py` (configured in `constants.py`)
- **Real-time Performance**: 20–60+ FPS depending on animation complexity

### **Software Optimizations**
- **Ultra-Fast Lookup Tables**: Pre-calculated sine, cosine, and square root in `constants.py`
- **Serpentine Pixel Mapping**: Pre-calculated in `utils.py` as `SERPENTINE_MAP`
- **Batch Pixel Updates**: `auto_write=False` throughout with a single `pixels.show()` per frame
- **Integer Math**: Avoided floating-point operations in hot paths

### **Animation Utilities**
- `ultra_sin()`, `ultra_cos()` — lookup-table trig (~10x faster than `math.sin`)
- `ultra_sqrt()` — lookup-table square root for values 0–255
- `set_pixel(pixels, x, y, color, auto_write=False)` — serpentine-aware pixel setter
- `log_module_start()` / `log_module_finish()` — automatic FPS logging

## 🐛 Troubleshooting

**LEDs not lighting up**
- Check power connections and capacitor
- Verify data pin is GP1
- Ensure ground is connected between Pico and LEDs

**Animations running slowly**
- Reduce `delay` parameter to `0`
- Check power supply capacity (needs ~20A at full brightness)

**Random flickering**
- Add logic level shifter
- Shorten data wire length
- Increase resistor value to 1kΩ

**Module import error on boot**
- Failed imports are printed as warnings and skipped — the rest of the animations continue
- Check `/error_log.txt` on the CIRCUITPY drive for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests with new animations or improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Adafruit for CircuitPython and NeoPixel library
- The maker community for inspiration
- Contributors who've added animations and improvements

---

*Built with ❤️ for the LED art community*
