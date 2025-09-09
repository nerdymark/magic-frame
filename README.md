# NeoPixel LED Matrix Picture Frame

A mesmerizing 18x18 LED matrix display featuring beautiful animations, games, and visual effects. Built with CircuitPython for the Raspberry Pi Pico W.

🎮 **[Try the Live Web Simulation →](https://nerdymark.com/magic-frame-sim)**

![LED Matrix Demo](https://img.shields.io/badge/LEDs-324-brightgreen) ![CircuitPython](https://img.shields.io/badge/CircuitPython-8.x-blueviolet) ![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- **35+ Stunning Animation Modules**: From serene water ripples to dynamic plasma effects, mathematical visualizations, and particle systems
- **Interactive Games**: Self-playing Snake, Strategic Snake AI, and Conway's Game of Life
- **Flag Displays**: Pride, Trans, Ukraine, and USA flags with realistic wave effects
- **Particle Systems**: Fish schooling, bug swarms, Matrix rain, bubbles, and starfields
- **Mathematical Art**: Mandelbrot/Julia fractals, Lissajous curves, plasma effects, and tunnel visualization
- **Retro Demoscene Effects**: C64-style copper bars, raster bars, rotozoomer, and lens flare
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
   - Download CircuitPython 8.x for Raspberry Pi Pico W
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

### **Text & Communication**

#### 📜 **sine_scrollers**
Smooth scrolling text with sine wave motion displaying "hello world! hello apple! oh hi mark!" Features classic demo-style text animation and wave distortion.

#### 📱 **qr_renderer**
QR code generation and display with error correction. Features dynamic code generation, proper formatting, and scannable output.

#### 🍎 **apple_event_sep_2025**
Special Apple-themed animation for events. Features Apple logo aesthetics, smooth transitions, and corporate branding elements.

### **Abstract & Artistic**

#### 🎯 **vector_balls**
Animated vector balls with physics simulation and trail effects. Features collision detection, momentum conservation, and smooth particle motion.

#### 🔦 **search_light**
Three searchlights hunting for hidden targets with celebration effects. Features dynamic movement patterns, collision detection, and rainbow victory animations.

#### 📀 **dvd_screen_saver**
Classic bouncing DVD logo with color changes on wall hits. Features accurate physics simulation, spin effects, and nostalgia-inducing movement.

#### 🧱 **falling_blocks**
Tetris-inspired falling blocks that stack and clear. Features collision detection, block rotation, stacking physics, and automatic reset functionality.

#### 💊 **the_matrix**
Iconic Matrix digital rain effect with trailing characters. Features authentic green color scheme, random character generation, and fade effects.

#### 🏳️ **flag_wave**
Animated flags (Pride, Trans, Ukraine, USA) with realistic wave physics. Features sine wave distortion, dynamic lighting, and smooth patriotic color transitions.

## 📁 Project Structure

```
/CIRCUITPY/
├── code.py                          # Main entry point with animation orchestrator
├── lib/                             # CircuitPython libraries
│   ├── neopixel.mpy
│   └── adafruit_pixelbuf.mpy
└── matrix_modules/                  # 35+ Animation modules
    ├── __init__.py
    ├── constants.py                 # Ultra-optimized lookup tables & CPU overclocking
    ├── utils.py                     # Shared utilities & performance functions
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
    │
    ├── # Mathematical & Fractal Art
    ├── mandelbrot_julia.py         # Fractal visualization
    ├── plasma.py                   # Classic plasma effect
    ├── plasma_two.py               # Alternative plasma algorithm
    ├── diamond_plasma.py           # Diamond-pattern plasma
    ├── ripple_plasma.py            # Ultra-optimized ripples
    ├── spiral_plasma.py            # Spiral interference patterns
    ├── lissajous_curves.py         # Parametric curve animation
    ├── moire_patterns.py           # Optical interference effects
    ├── dna_helix.py                # Double helix visualization
    │
    ├── # Classic Demoscene Effects
    ├── tunnel.py                   # 3D tunnel with rainbow colors
    ├── rotozoomer.py              # Rotating/zooming textures
    ├── copper_bars.py             # C64-style color gradients
    ├── raster_bars.py             # Retro raster effects
    ├── lens_flare.py              # Cinematic lighting effects
    ├── c64_demoscene.py           # Comprehensive C64 tribute
    │
    ├── # Text & Communication
    ├── sine_scrollers.py          # Wave-distorted scrolling text
    ├── qr_renderer.py             # QR code generation
    ├── apple_event_sep_2025.py    # Apple-themed animation
    │
    └── # Abstract & Artistic
        ├── vector_balls.py         # Physics-based particle motion
        ├── search_light.py         # Target-hunting searchlights
        ├── dvd_screen_saver.py     # Classic bouncing logo
        ├── falling_blocks.py       # Tetris-inspired blocks
        ├── the_matrix.py           # Matrix digital rain
        └── flag_wave.py            # Animated flags with physics
```

## 🔧 Customization

### Changing Animation Order
Edit `code.py` to modify the animation sequence:

```python
while True:
    # Add or reorder animations here
    plasma.plasma(pixels, WIDTH, HEIGHT, delay=0.0, max_frames=1000)
    # Your custom animation
    my_animation.animate(pixels, WIDTH, HEIGHT)
```

### Adjusting Brightness
Modify `DEFAULT_BRIGHTNESS` in `code.py`:
```python
DEFAULT_BRIGHTNESS = 0.05  # Range: 0.0 to 1.0
```

### Creating Custom Animations
1. Create a new file in `matrix_modules/`
2. Implement your animation function:
```python
def my_animation(pixels, width, height, delay=0.1, **kwargs):
    # Your animation code here
    pass
```
3. Import and add to the main loop in `code.py`

## ⚡ Performance Optimizations

This system implements **ultra-aggressive performance optimizations**:

### **Hardware Overclocking**
- **CPU Speed**: Overclocked from 125MHz to **350MHz** (2.8x boost!)
- **Memory**: Optimized memory access patterns for maximum bandwidth
- **Real-time Performance**: Achieving 50+ FPS on most animations

### **Software Optimizations**
- **Ultra-Fast Lookup Tables**: Pre-calculated sine, cosine, and square root functions
- **Serpentine Pixel Mapping**: Pre-calculated LED coordinate transformations
- **Batch Pixel Updates**: Use `auto_write=False` and single `pixels.show()` calls
- **Mathematical Optimizations**: Integer math where possible, avoiding floating-point operations

### **Animation Tuning**
- Keep `delay=0.0` for maximum frame rates
- Use `max_frames` parameters to control animation duration
- Pre-calculate complex values outside render loops
- Leverage the ultra-fast utility functions: `ultra_sin()`, `ultra_cos()`, `ultra_sqrt()`

### **Performance Monitoring**
All animations include start/finish logging with:
- Frame count tracking
- Duration measurement  
- Automatic FPS calculation
- Performance regression detection

## 🐛 Troubleshooting

**LEDs not lighting up**
- Check power connections and capacitor
- Verify data pin is GP1
- Ensure ground is connected between Pico and LEDs

**Animations running slowly**
- Reduce `delay` parameter
- Disable `animations` flag in Game of Life
- Check power supply capacity

**Random flickering**
- Add logic level shifter
- Shorten data wire length
- Increase resistor value to 1kΩ

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