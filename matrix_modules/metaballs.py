"""
Metaballs - organic blob-like shapes that merge and pull apart.
Classic demoscene effect using distance fields.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def metaballs(pixels, width=WIDTH, height=HEIGHT, delay=0.01, max_frames=1500):
    log_module_start("metaballs", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    cx = width / 2.0
    cy = height / 2.0
    threshold = 1.0

    # Ball definitions: (radius², orbit_rx, orbit_ry, freq_x, freq_y, phase_x, phase_y, r, g, b)
    balls = (
        (20, 5.0, 4.0, 0.04, 0.03, 0.0, 0.0, 255, 80, 0),     # Orange
        (18, 4.0, 5.5, 0.03, 0.05, 2.0, 1.0, 255, 0, 120),     # Magenta
        (16, 5.5, 3.5, 0.05, 0.04, 4.0, 3.0, 0, 180, 255),     # Cyan
    )

    while frame_count < max_frames:
        t = frame_count

        # Compute ball positions once per frame
        bx0 = cx + balls[0][1] * math.sin(t * balls[0][3] + balls[0][5])
        by0 = cy + balls[0][2] * math.sin(t * balls[0][4] + balls[0][6])
        bx1 = cx + balls[1][1] * math.sin(t * balls[1][3] + balls[1][5])
        by1 = cy + balls[1][2] * math.sin(t * balls[1][4] + balls[1][6])
        bx2 = cx + balls[2][1] * math.sin(t * balls[2][3] + balls[2][5])
        by2 = cy + balls[2][2] * math.sin(t * balls[2][4] + balls[2][6])

        r2_0 = balls[0][0]
        r2_1 = balls[1][0]
        r2_2 = balls[2][0]

        for y in range(height):
            for x in range(width):
                # Distance² to each ball
                dx0 = x - bx0
                dy0 = y - by0
                d0 = dx0 * dx0 + dy0 * dy0
                dx1 = x - bx1
                dy1 = y - by1
                d1 = dx1 * dx1 + dy1 * dy1
                dx2 = x - bx2
                dy2 = y - by2
                d2 = dx2 * dx2 + dy2 * dy2

                # Sum field values (avoid div by zero)
                f0 = r2_0 / (d0 + 0.5)
                f1 = r2_1 / (d1 + 0.5)
                f2 = r2_2 / (d2 + 0.5)
                total = f0 + f1 + f2

                if total > threshold:
                    # Blend colors by contribution
                    inv = 1.0 / total
                    w0 = f0 * inv
                    w1 = f1 * inv
                    w2 = f2 * inv
                    bright = min(1.0, total * 0.5)
                    r = int((w0 * 255 + w1 * 255 + w2 * 0) * bright * 0.25)
                    g = int((w0 * 80 + w1 * 0 + w2 * 180) * bright * 0.25)
                    b = int((w0 * 0 + w1 * 120 + w2 * 255) * bright * 0.25)
                    set_pixel(pixels, x, y, (min(60, r), min(60, g), min(60, b)), auto_write=False)
                else:
                    set_pixel(pixels, x, y, (0, 0, 0), auto_write=False)

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("metaballs", frame_count=frame_count, duration=duration)
