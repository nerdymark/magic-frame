"""
Bubbles Effect - Endless floating bubbles rising up through water.
Creates a soothing underwater scene with bubbles of various sizes floating upward.
Bubbles have natural movement with slight horizontal drift and size variation.
"""
import time
import random
import math
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, BUBBLES_MAX_FRAMES


def bubbles(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=BUBBLES_MAX_FRAMES):
    """
    Display endless rising bubbles with underwater atmosphere.
    Bubbles vary in size, speed, and transparency for realistic effect.
    """
    log_module_start("bubbles", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    bubbles_list = []  # Each bubble: [x, y, size, speed, drift, age, trail]
    
    # Underwater ambient colors
    water_colors = [
        (0, 40, 80),   # Deep blue water
        (0, 60, 100),  # Medium blue
        (10, 80, 120), # Lighter blue
        (20, 100, 140) # Surface blue
    ]
    
    # Current movement variables
    current = 0  # Horizontal water current (-1 to 1)
    target_current = 0
    current_change_delay = 0
    
    frame = 0
    # Background for smooth fading
    background = [[(0, 30, 60) for _ in range(width)] for _ in range(height)]  # Dark water base
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Fade background for smooth trails
        for y in range(height):
            for x in range(width):
                r, g, b = background[y][x]
                # Fade to dark water color, not black
                background[y][x] = (
                    max(0, r - 8),
                    max(20, g - 8), 
                    max(40, b - 8)
                )
        
        # Water current effect (like wind in blizzard)
        current_change_delay -= 1
        if current_change_delay <= 0:
            target_current = random.uniform(-0.4, 0.4)
            current_change_delay = random.randint(50, 150)
        
        current += (target_current - current) * 0.03
        
        # Add new bubbles from bottom
        if random.random() < 0.4:  # Frequent bubble generation
            x = random.randint(2, width - 3)  # Keep away from edges
            size = random.choice([1, 1, 1, 2, 2, 3])  # Mostly small bubbles
            speed = 0.3 + size * 0.1 + random.uniform(0, 0.3)  # Bigger bubbles rise faster
            drift = random.uniform(-0.1, 0.1) + current * 0.5
            bubbles_list.append([float(x), float(height - 1), size, speed, drift, 0, []])
        
        # Update bubbles
        new_bubbles = []
        for bubble in bubbles_list:
            x, y, size, speed, drift, age, trail = bubble
            
            # Add current position to trail
            trail.append((x, y))
            if len(trail) > 4:  # Longer trails than snowflakes
                trail.pop(0)
            
            # Draw bubble trail with fading
            for i, (trail_x, trail_y) in enumerate(trail):
                t_x, t_y = int(trail_x) % width, int(trail_y)
                if 0 <= t_y < height:
                    fade_factor = (i + 1) / len(trail)
                    
                    # Bubble color gets lighter/whiter as it rises
                    bubble_lightness = min(255, 120 + int(age * 2))
                    trail_brightness = int(bubble_lightness * fade_factor * 0.6)
                    
                    # Add bubble shimmer
                    shimmer = int(20 * ultra_sin(age * 0.5 + trail_x))
                    
                    old_r, old_g, old_b = background[t_y][t_x]
                    background[t_y][t_x] = (
                        min(255, old_r + trail_brightness + shimmer),
                        min(255, old_g + trail_brightness + shimmer // 2),
                        min(255, old_b + trail_brightness)
                    )
            
            # Draw main bubble with size effect
            bubble_x, bubble_y = int(x), int(y)
            if 0 <= bubble_y < height:
                # Draw bubble based on size
                bubble_brightness = min(255, 150 + int(age * 1.5))
                
                # Main bubble pixel
                if 0 <= bubble_x < width:
                    old_r, old_g, old_b = background[bubble_y][bubble_x]
                    background[bubble_y][bubble_x] = (
                        min(255, old_r + bubble_brightness),
                        min(255, old_g + bubble_brightness),
                        min(255, old_b + bubble_brightness // 2)
                    )
                
                # Larger bubbles get extra pixels
                if size >= 2:
                    for dx in [-1, 1]:
                        glow_x = bubble_x + dx
                        if 0 <= glow_x < width:
                            old_r, old_g, old_b = background[bubble_y][glow_x]
                            glow_brightness = bubble_brightness // 2
                            background[bubble_y][glow_x] = (
                                min(255, old_r + glow_brightness),
                                min(255, old_g + glow_brightness),
                                min(255, old_b + glow_brightness // 3)
                            )
                
                if size >= 3:  # Very large bubbles get vertical glow too
                    for dy in [-1, 1]:
                        glow_y = bubble_y + dy
                        if 0 <= glow_y < height and 0 <= bubble_x < width:
                            old_r, old_g, old_b = background[glow_y][bubble_x]
                            glow_brightness = bubble_brightness // 3
                            background[glow_y][bubble_x] = (
                                min(255, old_r + glow_brightness),
                                min(255, old_g + glow_brightness),
                                min(255, old_b + glow_brightness // 4)
                            )
            
            # Move bubble up with drift
            new_y = y - speed
            new_x = x + drift + ultra_sin(age * 0.1) * 0.05  # Slight wobble
            new_age = age + 1
            
            # Keep bubble if still on screen
            if new_y >= -2:  # Allow some off-screen buffer
                new_bubbles.append([new_x, new_y, size, speed, drift, new_age, trail])
        
        bubbles_list = new_bubbles
        
        # Copy background to pixels
        for y in range(height):
            for x in range(width):
                pixel_idx = pixel_map[y * width + x]
                pixels[pixel_idx] = background[y][x]
        
        # Add occasional bubble burst effect at top
        if frame % 60 == 0 and random.random() < 0.3:
            burst_x = random.randint(2, width - 3)
            burst_y = random.randint(0, 2)
            
            # Small sparkle effect for bubble popping at surface
            for dy in range(-1, 2):
                for dx in range(-2, 3):
                    if abs(dx) + abs(dy) <= 2:
                        spark_x = burst_x + dx
                        spark_y = burst_y + dy
                        if 0 <= spark_x < width and 0 <= spark_y < height:
                            pixel_idx = pixel_map[spark_y * width + spark_x]
                            current_pixel = pixels[pixel_idx]
                            spark_intensity = 100 - abs(dx) * 20 - abs(dy) * 20
                            pixels[pixel_idx] = (
                                min(255, current_pixel[0] + spark_intensity),
                                min(255, current_pixel[1] + spark_intensity),
                                min(255, current_pixel[2] + spark_intensity // 2)
                            )
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.08)  # ~12 FPS for smooth bubble movement
    
    log_module_finish("bubbles", frame_count=frame, duration=time.monotonic() - start_time)