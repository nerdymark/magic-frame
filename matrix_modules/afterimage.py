"""
Afterimage optical illusion.

Staring at a bright saturated color for several seconds fatigues the retinal cone
cells sensitive to that hue. When the display switches to neutral white, the viewer
briefly perceives the complementary color in the same regions — the afterimage.

  Cyan  induces  RED afterimage
  Yellow induces  BLUE afterimage
  Magenta induces GREEN afterimage

How to see it: Fix your gaze on the center of the display and hold still for ~7 seconds.
When the display turns white, keep your eyes on the same spot and wait 1-2 seconds.
"""
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish, ultra_sqrt
from matrix_modules.constants import WIDTH, HEIGHT

CYAN    = (0, 255, 255)
YELLOW  = (255, 255, 0)
MAGENTA = (255, 0, 255)
WHITE   = (220, 220, 220)
BLACK   = (0, 0, 0)

ILLUSION_BRIGHTNESS = 0.55
INDUCER_SECS        = 7.0
BLANK_SECS          = 0.15
WHITE_SECS          = 5.0


def _draw_pattern(pixels, w, h, idx):
    cx  = w // 2
    cy  = h // 2
    cxf = (w - 1) / 2.0
    cyf = (h - 1) / 2.0

    if idx == 0:
        # Horizontal halves: CYAN top, YELLOW bottom
        for y in range(h):
            c = CYAN if y < cy else YELLOW
            for x in range(w):
                set_pixel(pixels, x, y, c, auto_write=False)

    elif idx == 1:
        # MAGENTA cross on YELLOW background
        for y in range(h):
            for x in range(w):
                c = MAGENTA if (abs(x - cx) <= 1 or abs(y - cy) <= 1) else YELLOW
                set_pixel(pixels, x, y, c, auto_write=False)

    elif idx == 2:
        # Bullseye: concentric CYAN / YELLOW rings
        for y in range(h):
            for x in range(w):
                dx = x - cxf
                dy = y - cyf
                d    = ultra_sqrt(dx * dx + dy * dy)
                ring = int(d / 3) % 2
                set_pixel(pixels, x, y, CYAN if ring == 0 else YELLOW, auto_write=False)

    elif idx == 3:
        # 3×3-tile checkerboard: CYAN and MAGENTA
        for y in range(h):
            for x in range(w):
                c = CYAN if (x // 3 + y // 3) % 2 == 0 else MAGENTA
                set_pixel(pixels, x, y, c, auto_write=False)

    elif idx == 4:
        # Diagonal split: CYAN upper-left, MAGENTA lower-right
        for y in range(h):
            for x in range(w):
                set_pixel(pixels, x, y, CYAN if (x + y) < w else MAGENTA, auto_write=False)

    elif idx == 5:
        # 4 quadrants: TL=CYAN, TR=YELLOW, BL=MAGENTA, BR=CYAN
        for y in range(h):
            for x in range(w):
                if   x < cx and y < cy:  c = CYAN
                elif x >= cx and y < cy: c = YELLOW
                elif x < cx:             c = MAGENTA
                else:                    c = CYAN
                set_pixel(pixels, x, y, c, auto_write=False)

    pixels.show()


def afterimage(pixels, width=WIDTH, height=HEIGHT, delay=0, max_frames=900):
    log_module_start("afterimage", max_frames=max_frames)
    start_time      = time.monotonic()
    orig_brightness = pixels.brightness
    # treat max_frames as ~15fps equivalent for total duration
    end_time        = start_time + max_frames / 15.0
    num_patterns    = 6
    pattern_idx     = 0
    renders         = 0

    while time.monotonic() < end_time:
        # --- Inducer phase: bright saturated pattern ---
        pixels.brightness = ILLUSION_BRIGHTNESS
        _draw_pattern(pixels, width, height, pattern_idx % num_patterns)
        renders += 1

        remaining = end_time - time.monotonic()
        time.sleep(min(INDUCER_SECS, max(0, remaining)))
        if time.monotonic() >= end_time:
            break

        # Brief black flash to reset
        pixels.fill(BLACK)
        pixels.show()
        time.sleep(BLANK_SECS)

        # --- Test phase: neutral white — afterimage appears here ---
        pixels.brightness = orig_brightness
        pixels.fill(WHITE)
        pixels.show()
        renders += 1

        remaining = end_time - time.monotonic()
        time.sleep(min(WHITE_SECS, max(0, remaining)))

        pattern_idx += 1

    pixels.brightness = orig_brightness
    pixels.fill(BLACK)
    pixels.show()
    log_module_finish("afterimage", frame_count=renders,
                      duration=time.monotonic() - start_time)
