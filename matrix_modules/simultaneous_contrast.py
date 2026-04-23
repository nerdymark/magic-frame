"""
Simultaneous contrast optical illusion.

The exact same neutral gray square appears dramatically different depending on the color
of its surroundings. A gray patch on a blue background looks warm/orange-ish; the
identical gray on an orange background looks cool/blue-ish.

This is color constancy at work: the visual cortex assumes the surrounding color is
"ambient light" and compensates in the opposite direction, shifting the perceived hue
of any neutral object away from the background color.

Both center squares are identical — only the background differs.
"""
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT

CENTER_COLOR     = (115, 115, 115)   # neutral gray — identical on both panels
ILLUSION_BRIGHTNESS = 0.5
SQ_W             = 5                 # center square half-width  → 5 columns wide
SQ_H             = 7                 # center square half-height → 7 rows tall
DISPLAY_SECS     = 7.0

# Strongly contrasting complementary background pairs
BG_PAIRS = [
    ((0,   0, 255), (255, 130,  0)),   # Pure blue    vs orange
    ((0, 220,   0), (220,   0,  80)),  # Green        vs crimson
    ((160,  0, 200), (150, 160,  0)),  # Purple       vs yellow-green
    ((0, 160, 180), (200,  60,  0)),   # Teal         vs burnt orange
    ((10,  10,  10), (230, 230, 230)), # Near-black   vs near-white
    ((0,   0, 180), (180,   0,  0)),   # Blue         vs red
]


def _draw_frame(pixels, w, h, left_bg, right_bg):
    mid      = w // 2          # 9 — left panel x=0..8, right panel x=9..17
    left_cx  = mid // 2        # 4
    right_cx = mid + mid // 2  # 13
    cy       = h // 2          # 9

    for y in range(h):
        for x in range(w):
            set_pixel(pixels, x, y, left_bg if x < mid else right_bg, auto_write=False)

    # Draw identical center squares over each half
    for dy in range(-SQ_H // 2, SQ_H // 2 + 1):
        for dx in range(-SQ_W // 2, SQ_W // 2 + 1):
            set_pixel(pixels, left_cx  + dx, cy + dy, CENTER_COLOR, auto_write=False)
            set_pixel(pixels, right_cx + dx, cy + dy, CENTER_COLOR, auto_write=False)

    pixels.show()


def simultaneous_contrast(pixels, width=WIDTH, height=HEIGHT, delay=0, max_frames=800):
    log_module_start("simultaneous_contrast", max_frames=max_frames)
    start_time          = time.monotonic()
    orig_brightness     = pixels.brightness
    pixels.brightness   = ILLUSION_BRIGHTNESS
    end_time            = start_time + max_frames / 15.0
    pair_idx            = 0
    renders             = 0

    while time.monotonic() < end_time:
        left_bg, right_bg = BG_PAIRS[pair_idx % len(BG_PAIRS)]
        _draw_frame(pixels, width, height, left_bg, right_bg)
        renders += 1

        remaining = end_time - time.monotonic()
        time.sleep(min(DISPLAY_SECS, max(0, remaining)))

        pair_idx += 1

    pixels.brightness = orig_brightness
    pixels.fill((0, 0, 0))
    pixels.show()
    log_module_finish("simultaneous_contrast", frame_count=renders,
                      duration=time.monotonic() - start_time)
