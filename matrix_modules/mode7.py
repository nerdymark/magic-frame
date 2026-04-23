"""
Mode 7 - SNES-style rotating/scaling ground plane.
Creates a 3D perspective view of a checkerboard floor.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def mode7(pixels, width=WIDTH, height=HEIGHT, delay=0.02, max_frames=1500):
    log_module_start("mode7", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    horizon = 6
    half_w = width / 2.0
    camera_h = 4.0
    tile_size = 4

    # Sky gradient colors (dark to light blue)
    sky = []
    for row in range(horizon):
        b = 15 + row * 6
        sky.append((0, 0, min(60, b)))

    # Tile colors
    c1 = (0, 40, 10)    # Dark green
    c2 = (0, 15, 40)    # Dark teal
    c3 = (40, 20, 0)    # Brown
    c4 = (10, 10, 40)   # Dark blue

    while frame_count < max_frames:
        t = frame_count * 0.03
        cos_a = math.cos(t)
        sin_a = math.sin(t)
        # Camera moves forward
        cam_x = frame_count * 0.3
        cam_z = frame_count * 0.2

        # Draw sky
        for y in range(horizon):
            for x in range(width):
                set_pixel(pixels, x, y, sky[y], auto_write=False)

        # Draw ground with Mode 7 projection
        for y in range(horizon, height):
            # Distance from camera (further rows = further away)
            depth = camera_h * height / (y - horizon + 1)
            # Brightness decreases with distance
            bright = min(1.0, 3.0 / (depth + 1))

            for x in range(width):
                # Screen-space to world-space
                sx = (x - half_w) * depth / height

                # World position (rotated)
                wx = sx * cos_a - depth * sin_a + cam_x
                wz = sx * sin_a + depth * cos_a + cam_z

                # Tile coordinates
                tx = int(wx) // tile_size
                tz = int(wz) // tile_size

                # Checkerboard with two color schemes
                if (tx + tz) % 2 == 0:
                    if (tx // 2 + tz // 2) % 2 == 0:
                        base = c1
                    else:
                        base = c2
                else:
                    if (tx // 2 + tz // 2) % 2 == 0:
                        base = c3
                    else:
                        base = c4

                r = int(base[0] * bright)
                g = int(base[1] * bright)
                b = int(base[2] * bright)
                set_pixel(pixels, x, y, (r, g, b), auto_write=False)

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("mode7", frame_count=frame_count, duration=duration)
