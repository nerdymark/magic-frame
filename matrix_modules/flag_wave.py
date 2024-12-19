"""
Display a waving flag on the screen.
"""
import time
import math
from matrix_modules.utils import set_pixel


AMPLITUDE = 1.5
FREQUENCY = 0.5
WAVE_SPEED = 4.0


def flag_wave(pixels, height, width, mode="pride", delay=0.02, duration=30):      
    """
    Display a smoothly waving flag animation.
    """
    # Color definitions
    stripes = {
        "pride": [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                 (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)],
        "trans": [(91, 206, 250), (245, 169, 184), (255, 255, 255),
                  (245, 169, 184), (91, 206, 250)],
        "usa": [
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0)
            ]
    }

    colors = stripes.get(mode, stripes["pride"])
    stripe_height = height / len(colors)

    # Wave parameters

    def get_stripe_color(y):
        stripe_index = int(y / stripe_height)
        return colors[min(stripe_index, len(colors) - 1)]

    def interpolate_color(color1, color2, factor):
        return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

    def adjust_brightness(color, factor):
        """Adjust color brightness while preserving hue"""
        return tuple(min(255, max(0, int(c * factor))) for c in color)
    
    def get_lighting_factor(x, time):
        """Calculate lighting factor based on wave position"""
        phase = x * FREQUENCY + time * WAVE_SPEED
        wave_pos = math.sin(phase)
        # Peaks are brighter (1.2), troughs are darker (0.8)
        return 1.0 + (wave_pos * 0.2)

    start_time = time.monotonic()

    while True:
        current_time = time.monotonic() - start_time
        if current_time > duration:
            break

        for x in range(width):
            for y in range(height):
                # Calculate wave offset
                phase = x * FREQUENCY + current_time * WAVE_SPEED
                offset = AMPLITUDE * math.sin(phase)

                # Calculate new y position with wave effect
                wave_y = y + offset

                # Get colors for interpolation
                base_y = int(wave_y)
                frac = wave_y - base_y

                if 0 <= base_y < height - 1:
                    color1 = get_stripe_color(base_y)
                    color2 = get_stripe_color(base_y + 1)
                    color = interpolate_color(color1, color2, frac)
                elif base_y < 0:
                    color = get_stripe_color(0)
                else:
                    color = get_stripe_color(height - 1)

                # Apply lighting effect
                lighting = get_lighting_factor(x, current_time)
                color = adjust_brightness(color, lighting)

                # Apply special patterns for USA flag
                if mode == "usa" and x < width // 3 and y < height // 2:
                    base_color = (0, 0, 255) if (x + y) % 2 == 0 else (255, 255, 255)
                    color = adjust_brightness(base_color, lighting)

                # Account for zigzag LED pattern
                display_x = abs(x - width + 1) if y % 2 == 0 else x
                set_pixel(pixels, display_x, y, color, auto_write=False)

        pixels.show()
        time.sleep(delay)
