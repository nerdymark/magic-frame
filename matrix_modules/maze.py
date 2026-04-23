"""
10 PRINT style maze generator for the NeoPixel matrix.
Fills the grid with random diagonal lines (/ and \\ characters),
animated row by row, then dissolves and regenerates with new colors.
"""
import random
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT

PALETTES = (
    ((0, 200, 255), (255, 0, 180)),    # Cyan / Magenta
    ((255, 120, 0), (255, 255, 0)),     # Orange / Yellow
    ((0, 255, 80), (80, 0, 255)),       # Green / Purple
    ((255, 50, 50), (50, 50, 255)),     # Red / Blue
    ((255, 255, 255), (100, 100, 255)), # White / Light Blue
    ((255, 200, 0), (0, 255, 100)),     # Gold / Emerald
    ((255, 80, 200), (80, 255, 200)),   # Pink / Teal
)


def maze(pixels, width=WIDTH, height=HEIGHT, delay=0.02, max_frames=1500):
    log_module_start("maze", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    cols = width // 2
    rows = height // 2
    pal_idx = random.randint(0, len(PALETTES) - 1)

    while frame_count < max_frames:
        c1, c2 = PALETTES[pal_idx]
        pal_idx = (pal_idx + 1) % len(PALETTES)

        clear_pixels(pixels)
        frame_count += 1

        # Generate maze row by row
        for cy in range(rows):
            if frame_count >= max_frames:
                break
            for cx in range(cols):
                px = cx * 2
                py = cy * 2
                if random.random() < 0.5:
                    # Draw /
                    set_pixel(pixels, px, py + 1, c1, auto_write=False)
                    set_pixel(pixels, px + 1, py, c1, auto_write=False)
                else:
                    # Draw backslash
                    set_pixel(pixels, px, py, c2, auto_write=False)
                    set_pixel(pixels, px + 1, py + 1, c2, auto_write=False)
            pixels.show()
            frame_count += 1
            time.sleep(delay)

        if frame_count >= max_frames:
            break

        # Hold completed maze
        hold = min(60, max_frames - frame_count)
        for _ in range(hold):
            frame_count += 1
            time.sleep(0.05)

        if frame_count >= max_frames:
            break

        # Dissolve effect
        cells = []
        for cy in range(rows):
            for cx in range(cols):
                cells.append((cx, cy))
        random.shuffle(cells)

        batch = max(1, len(cells) // 12)
        i = 0
        while i < len(cells) and frame_count < max_frames:
            end = min(i + batch, len(cells))
            for j in range(i, end):
                cx, cy = cells[j]
                px = cx * 2
                py = cy * 2
                set_pixel(pixels, px, py, (0, 0, 0), auto_write=False)
                set_pixel(pixels, px + 1, py, (0, 0, 0), auto_write=False)
                set_pixel(pixels, px, py + 1, (0, 0, 0), auto_write=False)
                set_pixel(pixels, px + 1, py + 1, (0, 0, 0), auto_write=False)
            pixels.show()
            frame_count += 1
            time.sleep(delay)
            i = end

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("maze", frame_count=frame_count, duration=duration)
