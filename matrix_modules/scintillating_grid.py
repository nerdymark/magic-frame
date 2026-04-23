"""
Hermann grid / Scintillating grid optical illusion.

A 3×3 arrangement of dark squares separated by bright corridors creates phantom
dark smudges at the corridor intersections — the Hermann grid effect.

Adding a brighter blob at each intersection (scintillating grid) makes those spots
appear to flash and disappear as your eyes scan the display.

Mechanism — lateral inhibition: at a corridor intersection, bright pixels surround
the cell on all four sides instead of two, so inhibition is strongest there,
making intersections appear darker than the corridor midpoints.

How to see it: let your gaze wander freely — don't fixate on any single spot.
The phantom smudges vanish the moment you look directly at an intersection.

Grid layout (18×18): 2px corridors, 4px squares
  [corridor 2px][square 4px][corridor 2px][square 4px][corridor 2px][square 4px]
   x = 0,1       x = 2–5     x = 6,7       x = 8–11    x = 12,13     x = 14–17
"""
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT

ILLUSION_BRIGHTNESS = 0.45

THEMES = [
    # (square_color, corridor_color, blob_color, hold_secs)
    ((5,   5,  15), (200, 200, 200), (255, 255, 255), 10),  # classic
    ((15,  3,   3), (  0, 200, 200), (  0, 255, 255), 10),  # dark / cyan
    ((3,  15,   3), (200,   0, 200), (255,   0, 255), 10),  # dark / magenta
    ((15, 10,   0), (  0, 150, 220), (  0, 200, 255), 10),  # amber / blue
]

HERMANN_SECS = 5.0   # shorter pure-Hermann phase after each scintillating phase


def _is_corridor(pos):
    return pos % 6 < 2


def _draw_grid(pixels, w, h, square_c, corridor_c, blob_c):
    for y in range(h):
        y_cor = _is_corridor(y)
        for x in range(w):
            x_cor = _is_corridor(x)
            if x_cor and y_cor:
                c = blob_c
            elif x_cor or y_cor:
                c = corridor_c
            else:
                c = square_c
            set_pixel(pixels, x, y, c, auto_write=False)
    pixels.show()


def scintillating_grid(pixels, width=WIDTH, height=HEIGHT, delay=0, max_frames=1200):
    log_module_start("scintillating_grid", max_frames=max_frames)
    start_time          = time.monotonic()
    orig_brightness     = pixels.brightness
    pixels.brightness   = ILLUSION_BRIGHTNESS
    end_time            = start_time + max_frames / 15.0
    theme_idx           = 0
    renders             = 0

    while time.monotonic() < end_time:
        sq_c, cor_c, blob_c, secs = THEMES[theme_idx % len(THEMES)]

        # Scintillating variant — bright blobs at intersections
        _draw_grid(pixels, width, height, sq_c, cor_c, blob_c)
        renders += 1
        remaining = end_time - time.monotonic()
        time.sleep(min(secs, max(0, remaining)))
        if time.monotonic() >= end_time:
            break

        # Hermann variant — no blobs, pure corridors at intersections
        _draw_grid(pixels, width, height, sq_c, cor_c, cor_c)
        renders += 1
        remaining = end_time - time.monotonic()
        time.sleep(min(HERMANN_SECS, max(0, remaining)))

        theme_idx += 1

    pixels.brightness = orig_brightness
    pixels.fill((0, 0, 0))
    pixels.show()
    log_module_finish("scintillating_grid", frame_count=renders,
                      duration=time.monotonic() - start_time)
