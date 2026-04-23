"""
Parallax Scroller - multi-layered scrolling background creating depth.
Classic demoscene and game effect with layers at different speeds.
"""
import random
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def parallax_scroller(pixels, width=WIDTH, height=HEIGHT, delay=0.03, max_frames=1500):
    log_module_start("parallax_scroller", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    # Layer definitions: (y_start, y_end, speed, pattern_len)
    # Generate repeating height profiles for each layer

    # Stars layer (top 4 rows) - sparse dots
    star_len = 36
    stars = []
    for i in range(12):
        stars.append((random.randint(0, star_len - 1), random.randint(0, 3)))

    # Mountain layer (rows 4-8) - jagged silhouette
    mtn_len = 36
    mtn_profile = []
    h = 2
    for i in range(mtn_len):
        h += random.choice((-1, 0, 0, 1))
        h = max(0, min(4, h))
        mtn_profile.append(h)

    # Hills layer (rows 8-12) - smoother rolling hills
    hill_len = 32
    hill_profile = []
    h = 2
    for i in range(hill_len):
        h += random.choice((-1, 0, 1))
        h = max(0, min(3, h))
        hill_profile.append(h)

    # Ground layer (rows 12-17) - flat with details
    ground_len = 28
    ground_detail = []
    for i in range(ground_len):
        # Random grass/flower colors
        if random.random() < 0.15:
            ground_detail.append((40, 10, 10))   # Flower
        elif random.random() < 0.15:
            ground_detail.append((40, 40, 0))    # Yellow flower
        else:
            ground_detail.append(None)

    sky_color = (0, 0, 8)
    star_color = (50, 50, 40)
    mtn_color = (20, 10, 30)
    hill_color = (0, 25, 5)
    ground_color = (0, 35, 0)
    ground_dark = (0, 18, 0)

    while frame_count < max_frames:
        pixels.fill((0, 0, 0))
        t = frame_count

        # Sky background
        for y in range(4):
            for x in range(width):
                set_pixel(pixels, x, y, sky_color, auto_write=False)

        # Stars (slowest - 0.2 px/frame)
        star_off = t * 0.2
        for sx, sy in stars:
            draw_x = int((sx - star_off) % star_len)
            if 0 <= draw_x < width:
                set_pixel(pixels, draw_x, sy, star_color, auto_write=False)

        # Mountains (slow - 0.4 px/frame)
        mtn_off = int(t * 0.4) % mtn_len
        mtn_base = 8  # Bottom of mountain area
        for x in range(width):
            mi = (x + mtn_off) % mtn_len
            mh = mtn_profile[mi]
            for y in range(mtn_base - mh, mtn_base):
                if 4 <= y < mtn_base:
                    set_pixel(pixels, x, y, mtn_color, auto_write=False)

        # Hills (medium - 0.8 px/frame)
        hill_off = int(t * 0.8) % hill_len
        hill_base = 12
        for x in range(width):
            hi = (x + hill_off) % hill_len
            hh = hill_profile[hi]
            for y in range(hill_base - hh, hill_base):
                if 8 <= y < hill_base:
                    set_pixel(pixels, x, y, hill_color, auto_write=False)

        # Ground (fastest - 1.5 px/frame)
        ground_off = int(t * 1.5) % ground_len
        for y in range(12, height):
            for x in range(width):
                if y == 12:
                    set_pixel(pixels, x, y, ground_color, auto_write=False)
                else:
                    # Alternate light/dark ground rows
                    gc = ground_color if y % 2 == 0 else ground_dark
                    set_pixel(pixels, x, y, gc, auto_write=False)

        # Ground details (flowers etc)
        for x in range(width):
            gi = (x + ground_off) % ground_len
            detail = ground_detail[gi]
            if detail is not None:
                set_pixel(pixels, x, 12, detail, auto_write=False)

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("parallax_scroller", frame_count=frame_count, duration=duration)
