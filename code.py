"""
nerdymark's magic NeoPixel Picture Frame
REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP1.
* A power source for the NeoPixels.
* A CircuitPython (or MicroPython) board. 
  * This example uses the Raspberry Pi Pico W

The LED strip is arranged in a 18x18 grid.
The first 18 LEDs is the first row,
the next 18 LEDs is the second row, and so on.

Odd rows are arranged from left to right,
and even rows are arranged from right to left.
"""
import random
import board  # pyright: ignore[reportMissingImports] # pylint: disable=import-error
import neopixel  # type: ignore # pylint: disable=import-error
import microcontroller  # pyright: ignore[reportMissingImports] # pylint: disable=import-error

# Import constants first
from matrix_modules.constants import NUM_PIXELS, DEFAULT_BRIGHTNESS, TARGET_CPU_FREQUENCY
from matrix_modules.utils import test_pixels  # Ultra-optimized test function

# Verify overclock from boot.py or set it if not already done
# RP2350 can safely run at higher frequencies
# Default is 150MHz, we target 266MHz for smooth animations
if microcontroller.cpu.frequency < TARGET_CPU_FREQUENCY:
    try:
        microcontroller.cpu.frequency = TARGET_CPU_FREQUENCY
        print(f"CPU overclocked to {microcontroller.cpu.frequency / 1_000_000:.0f} MHz")
    except:
        print(f"Running at {microcontroller.cpu.frequency / 1_000_000:.0f} MHz")
else:
    print(f"Already running at {microcontroller.cpu.frequency / 1_000_000:.0f} MHz")
from matrix_modules import snake_game, john_conways_game_of_life, flag_wave, dvd_screen_saver, \
    the_matrix, blizzard, plasma, falling_blocks, plasma_two, bug_swarm, fish_schooling, \
    water_ripples, search_light, apple_event_sep_2025, fire, tunnel, diamond_plasma, \
    ripple_plasma, spiral_plasma, strategic_snake, moire_patterns, c64_demoscene, qr_renderer, \
    lissajous_curves, sine_scrollers, starfield, rotozoomer, copper_bars, lens_flare, \
    mandelbrot_julia, vector_balls, raster_bars, dna_helix, bubbles, lava_lamp, fishtank

# Hardware configuration is now imported from constants module


# ULTRA-OPTIMIZED NeoPixel initialization
pixels = neopixel.NeoPixel(
    board.GP1,
    NUM_PIXELS,
    brightness=DEFAULT_BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB)  # Most WS2812B use GRB order

# Test ultra-optimized hardware on boot
test_pixels(pixels)


# Define all available animations with their parameters as (name, function) tuples
animations = [
    # Visual Effects
    ("search_light", lambda: search_light.search_light(pixels)),
    ("lissajous_curves", lambda: lissajous_curves.lissajous_curves(pixels)),
    ("water_ripples", lambda: water_ripples.water_ripples(pixels)),
    ("starfield", lambda: starfield.starfield(pixels)),
    ("bug_swarm", lambda: bug_swarm.bug_swarm(pixels)),
    ("copper_bars", lambda: copper_bars.copper_bars(pixels)),
    ("fish_schooling", lambda: fish_schooling.fish_schooling(pixels)),
    ("rotozoomer", lambda: rotozoomer.rotozoomer(pixels)),
    ("fire", lambda: fire.fire(pixels)),
    ("sine_scrollers", lambda: sine_scrollers.sine_scrollers(pixels)),
    ("tunnel", lambda: tunnel.tunnel(pixels)),
    ("lens_flare", lambda: lens_flare.lens_flare(pixels)),
    ("diamond_plasma", lambda: diamond_plasma.diamond_plasma(pixels)),
    ("vector_balls", lambda: vector_balls.vector_balls(pixels)),
    ("ripple_plasma", lambda: ripple_plasma.ripple_plasma(pixels)),
    ("mandelbrot_julia", lambda: mandelbrot_julia.mandelbrot_julia(pixels)),
    ("spiral_plasma", lambda: spiral_plasma.spiral_plasma(pixels)),
    ("raster_bars", lambda: raster_bars.raster_bars(pixels)),
    ("dna_helix", lambda: dna_helix.dna_helix(pixels)),
    ("moire_patterns", lambda: moire_patterns.moire_patterns(pixels)),
    ("c64_demoscene", lambda: c64_demoscene.c64_demoscene(pixels)),
    ("apple_event_sep_2025", lambda: apple_event_sep_2025.apple_event_sep_2025(pixels)),
    ("plasma_two", lambda: plasma_two.plasma_two(pixels)),
    ("falling_blocks", lambda: falling_blocks.falling_blocks(pixels)),
    ("plasma", lambda: plasma.plasma(pixels)),
    ("blizzard", lambda: blizzard.blizzard(pixels)),
    ("bubbles", lambda: bubbles.bubbles(pixels)),
    ("lava_lamp", lambda: lava_lamp.lava_lamp(pixels)),  # NEW: Relaxing lava lamp effect
    ("fishtank", lambda: fishtank.fishtank(pixels)),  # NEW: Peaceful aquarium scene
    ("the_matrix", lambda: the_matrix.the_matrix(pixels)),
    ("dvd_screen_saver", lambda: dvd_screen_saver.dvd_screen_saver(pixels)),
    
    # Flag Variations
    ("flag_wave_ukraine", lambda: flag_wave.flag_wave(pixels, mode="ukraine")),
    ("flag_wave_trans", lambda: flag_wave.flag_wave(pixels, mode="trans")),
    ("flag_wave_usa", lambda: flag_wave.flag_wave(pixels, mode="usa")),
    ("flag_wave_pride", lambda: flag_wave.flag_wave(pixels, mode="pride")),
    
    # Games
    ("strategic_snake", lambda: strategic_snake.strategic_snake(pixels, show_log=False)),
    ("snake_game", lambda: snake_game.snake_game(pixels, show_log=False)),
    ("john_conways_game_of_life", lambda: john_conways_game_of_life.john_conways_game_of_life(pixels,
                                                              allow_mutations=True,
                                                              allow_visitors=True,
                                                              show_log=False,
                                                              animations=False)),  # Disabled for speed
    
    # QR Codes
    # ("qr_renderer_rickroll", lambda: qr_renderer.qr_renderer(pixels, urls=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"])),
    # ("qr_renderer_resume", lambda: qr_renderer.qr_renderer(pixels, urls=["https://nerdymark.com/resume"])),
]

print(f"🎬 Initialized {len(animations)} animations for infinite random shuffle")

# Infinite random shuffle loop
while True:
    # Pick a random animation and run it
    animation_name, animation_func = random.choice(animations)
    try:
        animation_func()
    except Exception as e:
        print(f"❌ Error in {animation_name}: {e}")
        # Continue with next animation instead of crashing
