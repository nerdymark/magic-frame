"""
Shading Demo - Flat, Gouraud, and Bump mapping on a rotating lit sphere.
Classic rendering technique showcase.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def shading_demo(pixels, width=WIDTH, height=HEIGHT, delay=0.02, max_frames=500):
    log_module_start("shading_demo", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    cx = width / 2.0
    cy = height / 2.0
    radius = 7.5
    r2 = radius * radius

    # Pre-compute which pixels are inside/outside the sphere
    sphere_pixels = []
    outside_pixels = []
    for y in range(height):
        dy = y - cy
        for x in range(width):
            dx = x - cx
            d2 = dx * dx + dy * dy
            if d2 <= r2:
                nz = math.sqrt(r2 - d2)
                inv_r = 1.0 / radius
                sphere_pixels.append((x, y, dx * inv_r, dy * inv_r, nz * inv_r))
            else:
                outside_pixels.append((x, y))

    frames_per_phase = max_frames // 3

    # Set background black once at start
    clear_pixels(pixels)

    while frame_count < max_frames:
        phase = frame_count // frames_per_phase  # 0=flat, 1=gouraud, 2=bump
        t = frame_count * 0.04

        # Light direction (orbiting)
        lx = math.sin(t) * 0.7
        ly = -0.3
        lz = math.cos(t) * 0.7
        # Normalize
        ll = math.sqrt(lx * lx + ly * ly + lz * lz)
        lx /= ll
        ly /= ll
        lz /= ll

        for x, y, nx, ny, nz in sphere_pixels:
            if phase == 0:
                # Flat shading: quantize normal to 6 sectors
                qnx = int(nx * 3) / 3.0
                qny = int(ny * 3) / 3.0
                qnz = nz
                dot = qnx * lx + qny * ly + qnz * lz
            elif phase == 1:
                # Gouraud: smooth per-pixel normal dot light
                dot = nx * lx + ny * ly + nz * lz
            else:
                # Bump mapping: perturb normals with sine pattern
                bump = math.sin(nx * 12.0 + t * 2) * 0.3
                bump2 = math.sin(ny * 10.0 - t * 1.5) * 0.25
                bnx = nx + bump
                bny = ny + bump2
                # Re-normalize roughly
                bl = math.sqrt(bnx * bnx + bny * bny + nz * nz)
                dot = (bnx * lx + bny * ly + nz * lz) / bl

            # Brightness
            bright = max(0.0, min(1.0, dot))
            ambient = 0.08

            # Base color: copper/gold
            r = int((bright * 0.9 + ambient) * 60)
            g = int((bright * 0.5 + ambient) * 45)
            b = int((bright * 0.15 + ambient) * 20)
            set_pixel(pixels, x, y, (min(60, r), min(60, g), min(60, b)), auto_write=False)

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("shading_demo", frame_count=frame_count, duration=duration)
