"""
Constants module for the LED matrix picture frame.
Centralizes all configuration values and common parameters.
"""

# Hardware Configuration
WIDTH = 18
HEIGHT = 18
NUM_PIXELS = WIDTH * HEIGHT  # 324

# Display Settings
DEFAULT_BRIGHTNESS = 0.025
PIXEL_ORDER = "GRB"  # Most WS2812B use GRB order

# Performance Settings - ULTRA-OPTIMIZED FOR MAXIMUM SPEED! ⚡🚀
TARGET_CPU_FREQUENCY = 350_000_000  # 350 MHz - MAXIMUM OVERDRIVE! 🔥🚀

# Animation Timing
DEFAULT_MAX_FRAMES = 1000
LONG_MAX_FRAMES = 1500
VERY_LONG_MAX_FRAMES = 2000
SHORT_MAX_FRAMES = 500

# Frame Rates (delays in seconds)
FPS_60 = 1/60  # 0.0167s
FPS_30 = 1/30  # 0.0333s
FPS_25 = 1/25  # 0.04s
FPS_20 = 1/20  # 0.05s
FPS_15 = 1/15  # 0.0667s
FPS_12 = 1/12  # 0.083s
FPS_10 = 1/10  # 0.1s

# Common Animation Parameters
DEFAULT_DELAY = 0.0     # Default delay - no artificial delay, algorithm-determined timing
SMOOTH_DELAY = 0.0      # No artificial delay - let the algorithm determine timing
READABLE_DELAY = 0.01   # For text/UI elements that need to be readable
SLOW_DELAY = 0.02       # For slower, more relaxed animations

# Module-specific Max Frames
STARFIELD_MAX_FRAMES = 1500
ROTOZOOMER_MAX_FRAMES = 1500
COPPER_BARS_MAX_FRAMES = 1500
LENS_FLARE_MAX_FRAMES = 1500
SINE_SCROLLERS_MAX_FRAMES = 2000
MANDELBROT_MAX_FRAMES = 2000
VECTOR_BALLS_MAX_FRAMES = 1500
RASTER_BARS_MAX_FRAMES = 1500
DNA_HELIX_MAX_FRAMES = 1500
LISSAJOUS_MAX_FRAMES = 1500
BUBBLES_MAX_FRAMES = 1500

# Game Settings
DEFAULT_MAX_GAMES = 3
DEFAULT_MAX_GENERATIONS = 10

# Flag Display Duration (converted to frames at ~30 FPS)
FLAG_DURATION_FRAMES = 300  # ~10 seconds at 30 FPS

# Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Common Colors for Effects
BACKGROUND_DIM = (10, 10, 10)
GLOW_COLOR = (200, 200, 200)
HIGHLIGHT_COLOR = (255, 255, 255)

# Center coordinates (commonly used)
CENTER_X = WIDTH / 2.0
CENTER_Y = HEIGHT / 2.0

# Mathematical Constants - ULTRA OPTIMIZED
SINE_LUT_SIZE = 512      # Larger lookup tables for precision
TRIG_LUT_SIZE = 720      # Even larger for smooth animations
PI_2 = 6.283185307179586  # 2 * PI for performance

# Pre-computed lookup tables (import math at top of file for initialization)
import math
ULTRA_SINE_LUT = [math.sin(i * PI_2 / SINE_LUT_SIZE) for i in range(SINE_LUT_SIZE)]
ULTRA_COS_LUT = [math.cos(i * PI_2 / SINE_LUT_SIZE) for i in range(SINE_LUT_SIZE)]
SQRT_LUT = [math.sqrt(i) for i in range(256)]  # Precomputed square roots
DISTANCE_LUT = {}  # Will be populated with common distance calculations

# Effect-specific Constants
PLASMA_MAX_ITER = 50
MANDELBROT_MAX_ITER = 50
STARFIELD_NUM_STARS = 80
METABALL_COUNT = 6

# Text and Font
CHAR_WIDTH = 3
CHAR_HEIGHT = 5
CHAR_SPACING = 4  # Including 1 pixel gap

# QR Code Settings
QR_CODE_SIZE = 17  # QR codes are 17x17 to fit in 18x18 matrix with margins