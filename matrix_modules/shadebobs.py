"""
Shadebobs - moving objects that leave additive color trails.
Classic demoscene effect creating complex glowing patterns.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, SERPENTINE_MAP
from matrix_modules.constants import WIDTH, HEIGHT


def shadebobs(pixels, width=WIDTH, height=HEIGHT, delay=0.01, max_frames=1500):
    log_module_start("shadebobs", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    cx = width / 2.0
    cy = height / 2.0
    rx = width / 2.0 - 1.5
    ry = height / 2.0 - 1.5

    # Bob parameters: (freq_x, freq_y, phase_x, phase_y, r, g, b)
    bobs = (
        (0.037, 0.029, 0.0, 1.0, 40, 8, 0),    # Red-orange
        (0.031, 0.043, 2.0, 0.5, 0, 8, 40),     # Blue
        (0.041, 0.033, 4.0, 3.0, 0, 35, 8),     # Green
    )

    fade_amt = 6

    while frame_count < max_frames:
        # Fade entire display
        for i in range(width * height):
            idx = SERPENTINE_MAP[i]
            r, g, b = pixels[idx]
            if r > 0 or g > 0 or b > 0:
                r = max(0, r - fade_amt)
                g = max(0, g - fade_amt)
                b = max(0, b - fade_amt)
                pixels[idx] = (r, g, b)

        # Draw each bob
        t = frame_count
        for fx, fy, px_off, py_off, br, bg, bb in bobs:
            # Lissajous position
            bx = int(cx + rx * math.sin(t * fx + px_off))
            by = int(cy + ry * math.sin(t * fy + py_off))

            # Draw 3x3 soft blob
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    sx = bx + dx
                    sy = by + dy
                    if 0 <= sx < width and 0 <= sy < height:
                        # Center full, edges half
                        if dx == 0 and dy == 0:
                            ar, ag, ab = br, bg, bb
                        else:
                            ar, ag, ab = br // 2, bg // 2, bb // 2
                        idx = SERPENTINE_MAP[sy * width + sx]
                        cr, cg, cb = pixels[idx]
                        pixels[idx] = (
                            min(255, cr + ar),
                            min(255, cg + ag),
                            min(255, cb + ab),
                        )

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("shadebobs", frame_count=frame_count, duration=duration)
