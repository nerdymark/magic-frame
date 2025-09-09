"""
Common utility functions for the LED matrix.
ULTRA-OPTIMIZED FOR MAXIMUM SPEED! 🚀
"""
import time
import math
from matrix_modules.constants import (WIDTH, HEIGHT, ULTRA_SINE_LUT, ULTRA_COS_LUT, 
                                     SQRT_LUT, SINE_LUT_SIZE, PI_2)

# Pre-computed pixel index mapping for serpentine layout - ULTIMATE SPEED!
SERPENTINE_MAP = []
for y in range(18):
    for x in range(18):
        if y % 2 == 0:  # Even rows: right-to-left
            SERPENTINE_MAP.append(y * 18 + (17 - x))
        else:  # Odd rows: left-to-right
            SERPENTINE_MAP.append(y * 18 + x)

# ULTRA FAST math functions using lookup tables
def ultra_sin(x):
    """Lightning fast sine using pre-computed lookup table"""
    return ULTRA_SINE_LUT[int(x * SINE_LUT_SIZE / PI_2) % SINE_LUT_SIZE]

def ultra_cos(x):
    """Lightning fast cosine using pre-computed lookup table"""
    return ULTRA_COS_LUT[int(x * SINE_LUT_SIZE / PI_2) % SINE_LUT_SIZE]

def ultra_sqrt(x):
    """Ultra fast square root for values 0-255"""
    if x < 256:
        return SQRT_LUT[int(x)]
    return math.sqrt(x)  # Fallback for larger values

def ultra_distance(x1, y1, x2, y2):
    """Ultra fast distance calculation with lookup table"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if dx < 256 and dy < 256:
        return ultra_sqrt(dx*dx + dy*dy)
    return math.sqrt(dx*dx + dy*dy)

def test_pixels(pixels):
    """
    Test the pixels by turning them all red for 1 second.
    """
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()


def set_pixel(pixels, x, y, color, brightness=None, auto_write=True):
    """
    ULTRA-FAST pixel setting using pre-computed serpentine map! 🚀
    """
    if 0 <= x < 18 and 0 <= y < 18:  # Bounds check optimized
        index = SERPENTINE_MAP[y * 18 + x]
        pixels[index] = color
        if brightness is not None:
            # Apply brightness scaling
            r, g, b = color
            pixels[index] = (int(r * brightness), int(g * brightness), int(b * brightness))
    if auto_write:
        pixels.show()

def ultra_set_pixel_direct(pixels, index, color):
    """
    MAXIMUM SPEED: Set pixel by direct index - NO BOUNDS CHECKING! ⚡
    Use this when you're 100% sure the index is valid
    """
    pixels[index] = color

def ultra_clear_pixels(pixels):
    """
    ULTRA-FAST pixel clearing using list comprehension! 🚀
    """
    black = (0, 0, 0)
    for i in range(len(pixels)):
        pixels[i] = black


def clear_pixels(pixels):
    """
    Clear all the pixels.
    """
    pixels.fill((0, 0, 0))
    pixels.show()


def set_all_pixels(pixels, color):
    """
    Set all the pixels to the given color.
    """
    pixels.fill(color)
    pixels.show()


def set_row(pixels, y, color):
    """
    Set all the pixels in the given row to the given color.
    """
    for x in range(18):
        set_pixel(pixels, x, y, color)


def set_column(pixels, x, color):
    """
    Set all the pixels in the given column to the given color.
    """
    for y in range(18):
        set_pixel(pixels, x, y, color)


def get_pixel(pixels, x, y):
    """
    Get the color of the pixel at the given x, y coordinates.
    Handles serpentine wiring: even rows right-to-left, odd rows left-to-right.
    """
    if x < 0 or x >= 18 or y < 0 or y >= 18:
        return None
    # Serpentine wiring: even rows reversed, odd rows normal
    if y % 2 == 0:  # Even rows (0, 2, 4, ...): right-to-left
        index = y * 18 + (17 - x)
    else:  # Odd rows (1, 3, 5, ...): left-to-right
        index = y * 18 + x
    return pixels[index]


def game_over(pixels, delay=0.5):
    """
    Flash the pixels red 3 times and then turn them off.
    """
    for _ in range(3):
        # set_all_pixels((255, 0, 0))
        pixels.show()
        time.sleep(delay)
        clear_pixels(pixels)
        pixels.show()
        time.sleep(delay)
    clear_pixels(pixels)
    pixels.show()


def log_module_start(module_name, **kwargs):
    """
    Log when a module starts with optional parameters.
    
    Args:
        module_name: Name of the module starting
        **kwargs: Optional parameters to display (e.g., mode="ukraine", max_frames=1000)
    """
    params = ""
    if kwargs:
        param_strs = []
        for key, value in kwargs.items():
            if isinstance(value, str):
                param_strs.append(f"{key}='{value}'")
            else:
                param_strs.append(f"{key}={value}")
        params = f" ({', '.join(param_strs)})"
    
    print(f"🚀 Starting {module_name}{params}")


def log_module_finish(module_name, frame_count=None, duration=None):
    """
    Log when a module finishes with optional statistics.
    
    Args:
        module_name: Name of the module finishing
        frame_count: Number of frames rendered (optional)
        duration: How long it ran in seconds (optional)
    """
    stats = ""
    if frame_count is not None or duration is not None:
        stat_parts = []
        if frame_count is not None:
            stat_parts.append(f"{frame_count} frames")
        if duration is not None:
            stat_parts.append(f"{duration:.1f}s")
        if stat_parts:
            stats = f" - {', '.join(stat_parts)}"
            
        # Calculate FPS if both are available
        if frame_count is not None and duration is not None and duration > 0:
            fps = frame_count / duration
            stats += f" ({fps:.1f} FPS)"
    
    print(f"✅ Finished {module_name}{stats}")


def with_module_logging(module_name):
    """
    Decorator to automatically log module start and finish.
    
    Usage:
        @with_module_logging("starfield")
        def starfield(pixels, width=WIDTH, height=HEIGHT, ...):
            # module code here
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Log start with any non-default parameters
            log_params = {}
            if 'mode' in kwargs:
                log_params['mode'] = kwargs['mode']
            if 'max_frames' in kwargs and kwargs['max_frames'] != 1000:
                log_params['max_frames'] = kwargs['max_frames']
            if 'show_log' in kwargs:
                log_params['show_log'] = kwargs['show_log']
            
            log_module_start(module_name, **log_params)
            
            start_time = time.monotonic()
            try:
                result = func(*args, **kwargs)
                duration = time.monotonic() - start_time
                log_module_finish(module_name, duration=duration)
                return result
            except Exception as e:
                duration = time.monotonic() - start_time
                print(f"❌ Error in {module_name} after {duration:.1f}s: {e}")
                raise
        return wrapper
    return decorator