"""
Fire effect based on classic algorithm from lodev.org.
Creates realistic but gentle fire animation with hot base and cooling/spreading upward.
Epilepsy-friendly version with smoother transitions and less flickering.
"""
import random
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def fire(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate gentle fire effect with smooth transitions.
    Epilepsy-safe with reduced flickering and softer colors.
    """
    log_module_start("fire", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Initialize fire buffer with smoothing
    fire_buffer = [[0 for _ in range(width)] for _ in range(height)]
    prev_buffer = [[0 for _ in range(width)] for _ in range(height)]
    
    # Softer fire color palette (less intense, more amber/warm)
    fire_palette = []
    for i in range(256):
        if i < 48:
            # Black to very dark red (slower transition)
            t = i / 48
            r = int(60 * t)
            g = 0
            b = 0
        elif i < 96:
            # Dark red to warm red
            t = (i - 48) / 48
            r = int(60 + 100 * t)
            g = int(20 * t)
            b = 0
        elif i < 144:
            # Warm red to orange
            t = (i - 96) / 48
            r = int(160 + 60 * t)
            g = int(20 + 80 * t)
            b = int(10 * t)
        elif i < 192:
            # Orange to warm yellow
            t = (i - 144) / 48
            r = int(220 + 30 * t)
            g = int(100 + 100 * t)
            b = int(10 + 30 * t)
        else:
            # Warm yellow to soft white
            t = (i - 192) / 64
            r = int(250)
            g = int(200 + 50 * t)
            b = int(40 + 60 * t)
        
        # Reduce overall intensity for gentler effect
        r = min(200, max(0, int(r * 0.8)))
        g = min(200, max(0, int(g * 0.8)))
        b = min(200, max(0, int(b * 0.8)))
        fire_palette.append((r, g, b))
    
    # Gentler cooling map
    cooling_map = []
    for y in range(height):
        row = []
        for x in range(width):
            # Less aggressive cooling
            cool_factor = 1.0 + (height - y) * 0.08 / height
            row.append(cool_factor)
        cooling_map.append(row)
    
    frame = 0
    spark_probability = 0.5  # Reduced spark probability
    
    while frame < max_frames:
        # Generate gentler heat sources at bottom row
        for x in range(width):
            if random.random() < spark_probability:
                # Create warm spots (not as hot)
                fire_buffer[height - 1][x] = random.randint(120, 200)
            else:
                # Gentle cooling
                fire_buffer[height - 1][x] = max(0, fire_buffer[height - 1][x] - random.randint(0, 10))
        
        # Less frequent hot spots
        if frame % 10 == 0:
            hot_x = random.randint(2, width - 3)
            fire_buffer[height - 1][hot_x] = 220
            if hot_x > 0:
                fire_buffer[height - 1][hot_x - 1] = 180
            if hot_x < width - 1:
                fire_buffer[height - 1][hot_x + 1] = 180
        
        # Process fire physics with smoothing
        for y in range(height - 2, -1, -1):
            for x in range(width):
                # Get heat from below with spreading
                heat = 0
                count = 0
                
                # Direct below
                if y < height - 1:
                    heat += fire_buffer[y + 1][x] * 2
                    count += 2
                
                # Left-below
                if y < height - 1 and x > 0:
                    heat += fire_buffer[y + 1][x - 1]
                    count += 1
                
                # Right-below
                if y < height - 1 and x < width - 1:
                    heat += fire_buffer[y + 1][x + 1]
                    count += 1
                
                # Two rows below for spread
                if y < height - 2:
                    heat += fire_buffer[y + 2][x] * 0.5
                    count += 0.5
                
                # Average and cool gently
                if count > 0:
                    new_heat = heat / (count * cooling_map[y][x])
                    
                    # Very subtle randomness (less flickering)
                    new_heat -= random.random() * 0.5
                    
                    # Smooth with previous frame (reduces flicker)
                    new_heat = (new_heat * 0.7 + prev_buffer[y][x] * 0.3)
                    
                    # Update buffer
                    fire_buffer[y][x] = max(0, min(255, int(new_heat)))
                else:
                    fire_buffer[y][x] = 0
        
        # Very gentle wind effect
        if frame % 20 == 0:
            wind_dir = random.choice([0, 0, 0, -1, 1])  # Mostly no wind
            if wind_dir != 0:
                for y in range(height - 1):
                    if wind_dir > 0:
                        for x in range(width - 1, 0, -1):
                            fire_buffer[y][x] = (fire_buffer[y][x] * 3 + fire_buffer[y][x - 1]) // 4
                    else:
                        for x in range(width - 1):
                            fire_buffer[y][x] = (fire_buffer[y][x] * 3 + fire_buffer[y][x + 1]) // 4
        
        # Convert buffer to pixels with temporal smoothing
        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                # Get fire intensity
                intensity = fire_buffer[y][x]
                
                # Store for next frame smoothing
                prev_buffer[y][x] = intensity
                
                # Map to color palette
                color = fire_palette[min(255, max(0, intensity))]
                
                # Set pixel
                pixels[pixel_map[pixel_idx]] = color
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        # Slower, smoother animation
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.05)  # 20 FPS for gentler movement
    
    log_module_finish("fire", frame_count=frame, duration=time.monotonic() - start_time)