"""
Display a waving flag on the screen.
"""
import time
import math
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import FLAG_DURATION_FRAMES, READABLE_DELAY, WIDTH, HEIGHT

AMPLITUDE = 1.5
FREQUENCY = 0.5
WAVE_SPEED = 4.0

def flag_wave(pixels, width=WIDTH, height=HEIGHT, mode="pride", delay=READABLE_DELAY, max_frames=FLAG_DURATION_FRAMES):
    """
    Display a smoothly waving flag animation.
    """
    log_module_start("flag_wave", mode=mode, max_frames=max_frames)
    stripes = {
        "pride": [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                 (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)],
        "trans": [
            (45, 105, 135),   # dimmer blue
            (165, 105, 120),  # dimmer pink
            (150, 150, 150),  # dimmer gray
            (165, 105, 120),  # dimmer pink
            (45, 105, 135)    # dimmer blue
        ],
        "ukraine": [
            (0, 87, 183),     # Ukrainian blue
            (255, 215, 0)     # Ukrainian yellow
        ],
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

    def get_stripe_color(y):
        stripe_index = int(y / stripe_height)
        return colors[min(stripe_index, len(colors) - 1)]

    def interpolate_color(color1, color2, factor):
        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor)
        )

    def adjust_brightness(color, factor):
        return (
            min(255, max(0, int(color[0] * factor))),
            min(255, max(0, int(color[1] * factor))),
            min(255, max(0, int(color[2] * factor)))
        )

    def get_lighting_factor(x, t):
        phase = x * FREQUENCY + t * WAVE_SPEED
        wave_pos = math.sin(phase)
        return 1.0 + (wave_pos * 0.2)

    start_time = time.monotonic()
    frame = 0

    while frame < max_frames:
        current_time = time.monotonic() - start_time

        # Precompute lighting for each x for this frame
        lighting_factors = [get_lighting_factor(x, current_time) for x in range(width)]

        for y in range(height):
            for x in range(width):
                phase = x * FREQUENCY + current_time * WAVE_SPEED
                offset = AMPLITUDE * math.sin(phase)
                wave_y = y + offset
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

                color = adjust_brightness(color, lighting_factors[x])

                if mode == "usa" and x < width // 3 and y < height // 2:
                    base_color = (0, 0, 255) if (x + y) % 2 == 0 else (255, 255, 255)
                    color = adjust_brightness(base_color, lighting_factors[x])

                set_pixel(pixels, x, y, color, auto_write=False)

        pixels.show()
        frame += 1
        if delay > 0:
            time.sleep(delay)
    
    log_module_finish("flag_wave", frame_count=frame, duration=time.monotonic() - start_time)
