"""
Displays a bouncing DVD logo on the screen.
"""
import time
import random
from matrix_modules.utils import clear_pixels, set_pixel


def dvd_screen_saver(pixels, width, height, delay=0.5, max_frames=1000):
    """
    Displays a bouncing 2x2 block with spin effect.
    """
    # Initialize position and velocities
    x = random.randint(0, width - 3)
    y = random.randint(0, height - 3)
    dx = random.choice([-1, 1]) * random.uniform(0.8, 1.2)
    dy = random.choice([-1, 1]) * random.uniform(0.8, 1.2)

    # Add spin factor
    spin = random.uniform(-0.2, 0.2)

    colors = [
        (255, 0, 0), (255, 165, 0), (255, 255, 0),
        (0, 255, 0), (0, 0, 255), (75, 0, 130),
        (238, 130, 238)
    ]
    color_index = 0

    frame_number = 0
    while frame_number < max_frames:
        clear_pixels(pixels)

        # Update position with floating point precision
        x += dx
        y += dy

        # Bounce handling with spin effect
        if x <= 0 or x >= width - 2:
            dx *= -1
            # Add spin influence to vertical velocity
            dy += spin
            # Randomize new spin
            spin = random.uniform(-0.2, 0.2)
            x = max(0, min(x, width - 2))
            color_index = (color_index + 1) % len(colors)

        if y <= 0 or y >= height - 2:
            dy *= -1
            # Add spin influence to horizontal velocity
            dx += spin
            # Randomize new spin
            spin = random.uniform(-0.2, 0.2)
            y = max(0, min(y, height - 2))
            color_index = (color_index + 1) % len(colors)

        # Normalize velocities to prevent extreme speeds
        speed = (dx * dx + dy * dy) ** 0.5
        if speed > 1.5:
            dx = dx / speed * 1.5
            dy = dy / speed * 1.5

        # Draw 2x2 block
        block_positions = [
            (int(x), int(y)),
            (int(x + 1), int(y)),
            (int(x), int(y + 1)),
            (int(x + 1), int(y + 1))
        ]

        current_color = colors[color_index]
        for bx, by in block_positions:
            plot_x = abs(bx - width + 1) if by % 2 == 0 else bx
            if 0 <= plot_x < width and 0 <= by < height:
                set_pixel(pixels, plot_x, by, current_color, auto_write=False)

        pixels.show()
        frame_number += 1
        time.sleep(delay)
