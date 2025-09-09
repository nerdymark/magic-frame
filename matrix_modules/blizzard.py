"""
Display a snowstorm on the LED matrix.
"""
import time
import random
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def blizzard(pixels, width=WIDTH, height=HEIGHT, delay=0.01, max_frames=1000):
    """
    Display a snowstorm on the LED matrix with wind effect and varied flake patterns.
    """
    log_module_start("blizzard", max_frames=max_frames)
    start_time = time.monotonic()
    # Create pixel mapping to handle zigzag wiring pattern
    pixel_map = {}
    for y in range(height):
        for x in range(width):
            # Handle zigzag pattern - odd rows are right to left
            adjusted_x = (width - 1 - x) if y % 2 == 1 else x
            pixel_map[(x, y)] = y * width + adjusted_x
            
    flakes = []  # Each flake is [x, y, intensity, drift, shape, trail]
    
    # Wind effect variables
    wind = 0  # Current wind strength (-1 to 1)
    target_wind = 0  # Target wind strength
    wind_change_delay = 0  # Counter for wind changes
    
    # Removed draw_flake function - now handled in background blending
    
    frame_number = 0
    # Initialize background for smoother fading
    background = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    
    while frame_number < max_frames:
        # Fade background instead of clearing for smoother animation
        for y in range(height):
            for x in range(width):
                r, g, b = background[y][x]
                background[y][x] = (max(0, r - 15), max(0, g - 15), max(0, b - 15))

        # Wind effect logic
        wind_change_delay -= 1
        if wind_change_delay <= 0:
            target_wind = random.uniform(-0.8, 0.8)
            wind_change_delay = random.randint(30, 100)
        
        wind += (target_wind - wind) * 0.05

        # Add new flakes
        if random.random() < 0.3:
            x = random.randint(0, width-1)
            drift = random.choice([-0.2, 0, 0, 0.2]) + (wind * 0.5)
            intensity = random.randint(100, 255)  # Vary brightness for size impression
            shape = random.randint(0, 2)  # 0=single pixel, 1=square, 2=diamond
            flakes.append([float(x), 0, intensity, drift, shape, []])

        new_flakes = []
        for flake in flakes:
            x, y, intensity, drift, shape, trail = flake
            
            # Add current position to trail
            trail.append((x, y))
            if len(trail) > 3:  # Keep last 3 positions
                trail.pop(0)
            
            # Draw trail with fading effect
            for i, (trail_x, trail_y) in enumerate(trail):
                t_x, t_y = int(trail_x) % width, int(trail_y)
                if 0 <= t_y < height:
                    fade_factor = (i + 1) / len(trail)
                    trail_brightness = int(intensity * fade_factor * 0.4)
                    
                    # Add to background for blending
                    old_r, old_g, old_b = background[t_y][t_x]
                    background[t_y][t_x] = (
                        min(255, old_r + trail_brightness),
                        min(255, old_g + trail_brightness),
                        min(255, old_b + trail_brightness)
                    )
            
            # Add current snowflake to background
            int_x = int(x) % width
            int_y = int(y)
            
            if 0 <= int_y < height:
                # Main flake
                old_r, old_g, old_b = background[int_y][int_x]
                background[int_y][int_x] = (
                    min(255, old_r + intensity),
                    min(255, old_g + intensity),
                    min(255, old_b + intensity)
                )
                
                # Add shape effects for larger flakes
                if shape == 1 and int_x + 1 < width:  # Square shape
                    old_r, old_g, old_b = background[int_y][int_x + 1]
                    half_bright = intensity // 2
                    background[int_y][int_x + 1] = (
                        min(255, old_r + half_bright),
                        min(255, old_g + half_bright),
                        min(255, old_b + half_bright)
                    )
                elif shape == 2:  # Diamond shape
                    half_bright = intensity // 3
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = (int_x + dx) % width, int_y + dy
                        if 0 <= ny < height:
                            old_r, old_g, old_b = background[ny][nx]
                            background[ny][nx] = (
                                min(255, old_r + half_bright),
                                min(255, old_g + half_bright),
                                min(255, old_b + half_bright)
                            )

            # Move flake down and apply drift
            new_drift = drift + (wind * 0.1)
            new_x = x + new_drift
            new_y = y + 1
            
            # Wrap horizontally
            if new_x < 0:
                new_x = width - 1
            elif new_x >= width:
                new_x = 0
                
            # Keep only flakes still on screen
            if new_y < height:
                new_flakes.append([new_x, new_y, intensity, new_drift, shape, trail])

        flakes = new_flakes
        
        # Apply final background to display with fixed serpentine wiring
        for y in range(height):
            for x in range(width):
                # Fix serpentine wiring calculation
                display_x = (width - 1 - x) if y % 2 == 1 else x
                pixel_index = y * width + display_x
                pixels[pixel_index] = background[y][x]
        
        pixels.show()
        time.sleep(delay)
        frame_number += 1
    
    log_module_finish("blizzard", frame_count=frame_number, duration=time.monotonic() - start_time)