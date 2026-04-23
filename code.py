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
import time
import board  # pyright: ignore[reportMissingImports] # pylint: disable=import-error
import neopixel  # type: ignore # pylint: disable=import-error
import microcontroller  # pyright: ignore[reportMissingImports] # pylint: disable=import-error

# Import constants first
from matrix_modules.constants import NUM_PIXELS, DEFAULT_BRIGHTNESS, TARGET_CPU_FREQUENCY
from matrix_modules.utils import test_pixels  # Ultra-optimized test function


def log_error(module_name, error):
    """Append error to log file, keeping only last 50 lines to save storage."""
    try:
        entry = f"{time.monotonic():.0f}s | {module_name}: {error}\n"
        # Read existing lines
        lines = []
        try:
            with open("/error_log.txt", "r") as f:
                lines = f.readlines()
        except OSError:
            pass
        # Keep last 49 lines + new entry
        lines = lines[-49:] + [entry]
        with open("/error_log.txt", "w") as f:
            f.writelines(lines)
    except OSError:
        pass  # Filesystem not writable - fall back to print only

# Report CPU frequency (overclocking is handled in boot.py)
print(f"CPU: {microcontroller.cpu.frequency / 1_000_000:.0f} MHz")
snake_game = john_conways_game_of_life = flag_wave = dvd_screen_saver = None
the_matrix = blizzard = plasma = falling_blocks = plasma_two = bug_swarm = None
fish_schooling = water_ripples = search_light = apple_event_sep_2025 = fire = None
tunnel = diamond_plasma = ripple_plasma = spiral_plasma = strategic_snake = None
moire_patterns = c64_demoscene = qr_renderer = lissajous_curves = sine_scrollers = None
starfield = rotozoomer = copper_bars = lens_flare = mandelbrot_julia = None
vector_balls = raster_bars = dna_helix = bubbles = lava_lamp = fishtank = None
rubiks_cube = hypercube_4d = maze = shadebobs = metaballs = None
glenz_vectors = mode7 = voxel_terrain = shading_demo = parallax_scroller = None
afterimage = simultaneous_contrast = scintillating_grid = None

try:
    from matrix_modules import snake_game
except Exception as e:
    print(f"⚠️ import snake_game: {e}")
try:
    from matrix_modules import john_conways_game_of_life
except Exception as e:
    print(f"⚠️ import john_conways_game_of_life: {e}")
try:
    from matrix_modules import flag_wave
except Exception as e:
    print(f"⚠️ import flag_wave: {e}")
try:
    from matrix_modules import dvd_screen_saver
except Exception as e:
    print(f"⚠️ import dvd_screen_saver: {e}")
try:
    from matrix_modules import the_matrix
except Exception as e:
    print(f"⚠️ import the_matrix: {e}")
try:
    from matrix_modules import blizzard
except Exception as e:
    print(f"⚠️ import blizzard: {e}")
try:
    from matrix_modules import plasma
except Exception as e:
    print(f"⚠️ import plasma: {e}")
try:
    from matrix_modules import falling_blocks
except Exception as e:
    print(f"⚠️ import falling_blocks: {e}")
try:
    from matrix_modules import plasma_two
except Exception as e:
    print(f"⚠️ import plasma_two: {e}")
try:
    from matrix_modules import bug_swarm
except Exception as e:
    print(f"⚠️ import bug_swarm: {e}")
try:
    from matrix_modules import fish_schooling
except Exception as e:
    print(f"⚠️ import fish_schooling: {e}")
try:
    from matrix_modules import water_ripples
except Exception as e:
    print(f"⚠️ import water_ripples: {e}")
try:
    from matrix_modules import search_light
except Exception as e:
    print(f"⚠️ import search_light: {e}")
try:
    from matrix_modules import apple_event_sep_2025
except Exception as e:
    print(f"⚠️ import apple_event_sep_2025: {e}")
try:
    from matrix_modules import fire
except Exception as e:
    print(f"⚠️ import fire: {e}")
try:
    from matrix_modules import tunnel
except Exception as e:
    print(f"⚠️ import tunnel: {e}")
try:
    from matrix_modules import diamond_plasma
except Exception as e:
    print(f"⚠️ import diamond_plasma: {e}")
try:
    from matrix_modules import ripple_plasma
except Exception as e:
    print(f"⚠️ import ripple_plasma: {e}")
try:
    from matrix_modules import spiral_plasma
except Exception as e:
    print(f"⚠️ import spiral_plasma: {e}")
try:
    from matrix_modules import strategic_snake
except Exception as e:
    print(f"⚠️ import strategic_snake: {e}")
try:
    from matrix_modules import moire_patterns
except Exception as e:
    print(f"⚠️ import moire_patterns: {e}")
try:
    from matrix_modules import c64_demoscene
except Exception as e:
    print(f"⚠️ import c64_demoscene: {e}")
try:
    from matrix_modules import qr_renderer
except Exception as e:
    print(f"⚠️ import qr_renderer: {e}")
try:
    from matrix_modules import lissajous_curves
except Exception as e:
    print(f"⚠️ import lissajous_curves: {e}")
try:
    from matrix_modules import sine_scrollers
except Exception as e:
    print(f"⚠️ import sine_scrollers: {e}")
try:
    from matrix_modules import starfield
except Exception as e:
    print(f"⚠️ import starfield: {e}")
try:
    from matrix_modules import rotozoomer
except Exception as e:
    print(f"⚠️ import rotozoomer: {e}")
try:
    from matrix_modules import copper_bars
except Exception as e:
    print(f"⚠️ import copper_bars: {e}")
try:
    from matrix_modules import lens_flare
except Exception as e:
    print(f"⚠️ import lens_flare: {e}")
try:
    from matrix_modules import mandelbrot_julia
except Exception as e:
    print(f"⚠️ import mandelbrot_julia: {e}")
try:
    from matrix_modules import vector_balls
except Exception as e:
    print(f"⚠️ import vector_balls: {e}")
try:
    from matrix_modules import raster_bars
except Exception as e:
    print(f"⚠️ import raster_bars: {e}")
try:
    from matrix_modules import dna_helix
except Exception as e:
    print(f"⚠️ import dna_helix: {e}")
try:
    from matrix_modules import bubbles
except Exception as e:
    print(f"⚠️ import bubbles: {e}")
try:
    from matrix_modules import lava_lamp
except Exception as e:
    print(f"⚠️ import lava_lamp: {e}")
try:
    from matrix_modules import fishtank
except Exception as e:
    print(f"⚠️ import fishtank: {e}")
try:
    from matrix_modules import rubiks_cube
except Exception as e:
    print(f"⚠️ import rubiks_cube: {e}")
try:
    from matrix_modules import hypercube_4d
except Exception as e:
    print(f"⚠️ import hypercube_4d: {e}")
try:
    from matrix_modules import maze
except Exception as e:
    print(f"⚠️ import maze: {e}")
try:
    from matrix_modules import shadebobs
except Exception as e:
    print(f"⚠️ import shadebobs: {e}")
try:
    from matrix_modules import metaballs
except Exception as e:
    print(f"⚠️ import metaballs: {e}")
try:
    from matrix_modules import glenz_vectors
except Exception as e:
    print(f"⚠️ import glenz_vectors: {e}")
try:
    from matrix_modules import mode7
except Exception as e:
    print(f"⚠️ import mode7: {e}")
try:
    from matrix_modules import voxel_terrain
except Exception as e:
    print(f"⚠️ import voxel_terrain: {e}")
try:
    from matrix_modules import shading_demo
except Exception as e:
    print(f"⚠️ import shading_demo: {e}")
try:
    from matrix_modules import parallax_scroller
except Exception as e:
    print(f"⚠️ import parallax_scroller: {e}")
try:
    from matrix_modules import afterimage
except Exception as e:
    print(f"⚠️ import afterimage: {e}")
try:
    from matrix_modules import simultaneous_contrast
except Exception as e:
    print(f"⚠️ import simultaneous_contrast: {e}")
try:
    from matrix_modules import scintillating_grid
except Exception as e:
    print(f"⚠️ import scintillating_grid: {e}")

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


# Define all available animations - only include modules that imported successfully
_all_animations = [
    # Visual Effects
    ("hypercube_4d", hypercube_4d, lambda: hypercube_4d.hypercube_4d(pixels)),
    ("search_light", search_light, lambda: search_light.search_light(pixels)),
    ("lissajous_curves", lissajous_curves, lambda: lissajous_curves.lissajous_curves(pixels)),
    ("water_ripples", water_ripples, lambda: water_ripples.water_ripples(pixels)),
    ("starfield", starfield, lambda: starfield.starfield(pixels)),
    ("bug_swarm", bug_swarm, lambda: bug_swarm.bug_swarm(pixels)),
    ("copper_bars", copper_bars, lambda: copper_bars.copper_bars(pixels)),
    ("fish_schooling", fish_schooling, lambda: fish_schooling.fish_schooling(pixels)),
    ("rotozoomer", rotozoomer, lambda: rotozoomer.rotozoomer(pixels)),
    ("fire", fire, lambda: fire.fire(pixels)),
    ("sine_scrollers", sine_scrollers, lambda: sine_scrollers.sine_scrollers(pixels)),
    ("tunnel", tunnel, lambda: tunnel.tunnel(pixels)),
    ("lens_flare", lens_flare, lambda: lens_flare.lens_flare(pixels)),
    ("diamond_plasma", diamond_plasma, lambda: diamond_plasma.diamond_plasma(pixels)),
    ("vector_balls", vector_balls, lambda: vector_balls.vector_balls(pixels)),
    ("ripple_plasma", ripple_plasma, lambda: ripple_plasma.ripple_plasma(pixels)),
    ("mandelbrot_julia", mandelbrot_julia, lambda: mandelbrot_julia.mandelbrot_julia(pixels)),
    ("spiral_plasma", spiral_plasma, lambda: spiral_plasma.spiral_plasma(pixels)),
    ("raster_bars", raster_bars, lambda: raster_bars.raster_bars(pixels)),
    ("dna_helix", dna_helix, lambda: dna_helix.dna_helix(pixels)),
    ("moire_patterns", moire_patterns, lambda: moire_patterns.moire_patterns(pixels)),
    ("c64_demoscene", c64_demoscene, lambda: c64_demoscene.c64_demoscene(pixels)),
    ("apple_event_sep_2025", apple_event_sep_2025, lambda: apple_event_sep_2025.apple_event_sep_2025(pixels)),
    ("plasma_two", plasma_two, lambda: plasma_two.plasma_two(pixels)),
    ("falling_blocks", falling_blocks, lambda: falling_blocks.falling_blocks(pixels)),
    ("plasma", plasma, lambda: plasma.plasma(pixels)),
    ("blizzard", blizzard, lambda: blizzard.blizzard(pixels)),
    ("bubbles", bubbles, lambda: bubbles.bubbles(pixels)),
    ("lava_lamp", lava_lamp, lambda: lava_lamp.lava_lamp(pixels)),
    ("fishtank", fishtank, lambda: fishtank.fishtank(pixels)),
    ("rubiks_cube", rubiks_cube, lambda: rubiks_cube.rubiks_cube(pixels, width=18, height=18)),
    ("maze", maze, lambda: maze.maze(pixels)),
    ("shadebobs", shadebobs, lambda: shadebobs.shadebobs(pixels)),
    ("metaballs", metaballs, lambda: metaballs.metaballs(pixels)),
    ("glenz_vectors", glenz_vectors, lambda: glenz_vectors.glenz_vectors(pixels)),
    ("mode7", mode7, lambda: mode7.mode7(pixels)),
    ("voxel_terrain", voxel_terrain, lambda: voxel_terrain.voxel_terrain(pixels)),
    ("shading_demo", shading_demo, lambda: shading_demo.shading_demo(pixels)),
    ("parallax_scroller", parallax_scroller, lambda: parallax_scroller.parallax_scroller(pixels)),
    ("the_matrix", the_matrix, lambda: the_matrix.the_matrix(pixels)),
    ("dvd_screen_saver", dvd_screen_saver, lambda: dvd_screen_saver.dvd_screen_saver(pixels)),

    # Optical Illusions
    ("afterimage", afterimage, lambda: afterimage.afterimage(pixels)),
    ("simultaneous_contrast", simultaneous_contrast, lambda: simultaneous_contrast.simultaneous_contrast(pixels)),
    ("scintillating_grid", scintillating_grid, lambda: scintillating_grid.scintillating_grid(pixels)),

    # Flag Variations
    ("flag_wave_ukraine", flag_wave, lambda: flag_wave.flag_wave(pixels, mode="ukraine")),
    ("flag_wave_trans", flag_wave, lambda: flag_wave.flag_wave(pixels, mode="trans")),
    ("flag_wave_usa", flag_wave, lambda: flag_wave.flag_wave(pixels, mode="usa")),
    ("flag_wave_pride", flag_wave, lambda: flag_wave.flag_wave(pixels, mode="pride")),
    ("flag_wave_palestine", flag_wave, lambda: flag_wave.flag_wave(pixels, mode="palestine")),

    # Games
    ("strategic_snake", strategic_snake, lambda: strategic_snake.strategic_snake(pixels, 18, 18, show_log=False)),
    ("snake_game", snake_game, lambda: snake_game.snake_game(pixels, show_log=False)),
    ("john_conways_game_of_life", john_conways_game_of_life, lambda: john_conways_game_of_life.john_conways_game_of_life(pixels,
                                                              allow_mutations=True,
                                                              allow_visitors=True,
                                                              show_log=False,
                                                              animations=False,
                                                              max_frames=300)),
]

# Filter out animations whose modules failed to import
animations = [(name, func) for name, mod, func in _all_animations if mod is not None]
_skipped = [name for name, mod, _ in _all_animations if mod is None]
if _skipped:
    print(f"⚠️ Skipped {len(_skipped)} animations (import failed): {', '.join(_skipped)}")
del _all_animations, _skipped  # Free memory

print(f"🎬 Initialized {len(animations)} animations for infinite random shuffle")

# Infinite random shuffle loop
while True:
    # Pick a random animation and run it
    animation_name, animation_func = random.choice(animations)
    try:
        animation_func()
    except MemoryError:
        # Free memory and log before continuing
        import gc
        gc.collect()
        print(f"❌ MemoryError in {animation_name}")
        log_error(animation_name, "MemoryError")
    except Exception as e:
        print(f"❌ Error in {animation_name}: {e}")
        log_error(animation_name, e)
        # Continue with next animation instead of crashing
