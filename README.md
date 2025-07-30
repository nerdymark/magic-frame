# NeoPixel LED Matrix Picture Frame

A mesmerizing 18x18 LED matrix display featuring beautiful animations, games, and visual effects. Built with CircuitPython for the Raspberry Pi Pico W.

🎮 **[Try the Live Web Simulation →](https://nerdymark.com/magic-frame-sim)**

![LED Matrix Demo](https://img.shields.io/badge/LEDs-324-brightgreen) ![CircuitPython](https://img.shields.io/badge/CircuitPython-8.x-blueviolet) ![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- **13 Stunning Animation Modules**: From serene water ripples to dynamic plasma effects (15 total animation sequences including flag variations)
- **Interactive Games**: Self-playing Snake and Conway's Game of Life
- **Flag Displays**: Pride, Trans, Ukraine, and USA flags with realistic wave effects
- **Particle Systems**: Fish schooling, bug swarms, and Matrix rain
- **Optimized Performance**: Efficient serpentine wiring support and batch pixel updates

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

### 🔦 **search_light**
Three searchlights hunt for a hidden 2×2 target block. When all lights find the target, the screen erupts in a rainbow celebration!
- **Parameters**: `delay` (speed), `max_cycles` (number of rounds)
- **Features**: Dynamic movement, collision detection, growing rainbow effect

### 🌊 **water_ripples**
Soothing water simulation with gentle ripples spreading across the surface.
- **Parameters**: `delay` (animation speed), `max_frames` (duration)
- **Features**: Realistic ripple physics, depth-based coloring, random ripple generation

### 🐛 **bug_swarm**
A leader bug guides a swarm of followers using flocking behavior.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Boids algorithm, trail effects, collision avoidance

### 🐟 **fish_schooling**
Realistic fish schooling behavior with multiple species swimming together.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Species-based coloring, coordinated movement, 3D-like depth effects

### 🏳️ **flag_wave**
Animated flags with realistic wave motion and lighting effects.
- **Parameters**: `mode` (pride/trans/ukraine/usa), `delay`, `duration`
- **Features**: Sine wave distortion, dynamic lighting, smooth color transitions

### 🌈 **plasma** & **plasma_two**
Mesmerizing plasma effects using mathematical functions.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Multiple wave interference, color cycling, blob physics

### ❄️ **blizzard**
Snowfall animation with wind effects and accumulation.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Wind gusts, varying snowflake sizes, ground accumulation

### 💊 **the_matrix**
The iconic Matrix digital rain effect.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Trailing fade, random character changes, varying drop speeds

### 📀 **dvd_screen_saver**
Classic bouncing DVD logo that changes color on each wall hit.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Physics simulation, spin effects, color cycling

### 🧱 **falling_blocks**
Tetris-inspired falling blocks that stack and clear when reaching the top.
- **Parameters**: `delay` (speed), `max_frames` (duration)
- **Features**: Collision detection, stacking physics, auto-reset

### 🐍 **snake_game**
Self-playing Snake game with intelligent AI.
- **Parameters**: `delay` (speed), `show_log` (debug output)
- **Features**: Pathfinding AI, wall avoidance, oscillation prevention

### 🧬 **john_conways_game_of_life**
Conway's Game of Life with colorful mutations and visitor system.
- **Parameters**: `delay`, `allow_mutations`, `allow_visitors`, `max_generations`
- **Features**: Color inheritance, mutation system, automatic restart, visitor injection

## 📁 Project Structure

```
/CIRCUITPY/
├── code.py                 # Main entry point
├── lib/                    # CircuitPython libraries
│   ├── neopixel.mpy
│   └── adafruit_pixelbuf.mpy
└── matrix_modules/         # Animation modules
    ├── __init__.py
    ├── utils.py            # Shared utilities
    ├── blizzard.py
    ├── bug_swarm.py
    ├── dvd_screen_saver.py
    ├── falling_blocks.py
    ├── fish_schooling.py
    ├── flag_wave.py
    ├── john_conways_game_of_life.py
    ├── plasma.py
    ├── plasma_two.py
    ├── search_light.py
    ├── snake_game.py
    ├── the_matrix.py
    └── water_ripples.py
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

## ⚡ Performance Tips

- Keep `delay` low (0.0-0.01) for smooth animations
- Use `auto_write=False` for batch updates
- Call `pixels.show()` once per frame
- Pre-calculate values outside animation loops

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
