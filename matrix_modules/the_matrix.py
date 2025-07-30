"""
Emulates the classic "rain of code" made famous by the movie "The Matrix".
"""
import time
import random
from matrix_modules.utils import clear_pixels

def the_matrix(pixels, width, height, delay=0.001, max_frames=1000):
    """
    Optimized matrix rain effect for maximum performance with smooth movement.
    """
    # Configuration for visual effect
    fade_factor = 30
    max_drops = width * 2  # More drops for denser effect
    
    # Drops with fractional positions for smoother movement
    # Each drop is (x, y_float, speed, intensity, trail_length)
    drops = []
    
    # Precalculate pixel indices for the entire matrix (accounting for zigzag pattern)
    # This eliminates repeated calculations during animation
    pixel_map = {}
    for y in range(height):
        for x in range(width):
            # Handle zigzag pattern - odd rows are right to left
            adjusted_x = (width - 1 - x) if y % 2 == 1 else x
            pixel_map[(x, y)] = y * width + adjusted_x
    
    # Clear display once at start for clean slate
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 0)
    pixels.show()
    
    # Track active columns to prevent multiple drops in same column
    active_columns = set()
    frame_number = 0
    
    while frame_number < max_frames:
        # Fade existing pixels for streaking effect
        for i in range(len(pixels)):
            r, g, b = pixels[i]
            pixels[i] = (max(0, r-1), max(0, g-fade_factor), max(0, b-1))
        
        # Add new drops if needed, ensuring they start from the top
        while len(drops) < max_drops:
            # Find an available column that doesn't already have a drop
            attempts = 0
            while attempts < 10:  # Limit attempts to avoid infinite loop
                x = random.randint(0, width-1)
                if x not in active_columns:
                    break
                attempts += 1
                
            # Create new drop with varied speeds
            r = random.random()
            if r < 0.25:  # 25% slow
                speed = random.uniform(0.3, 0.6)
            elif r < 0.75:  # 50% medium
                speed = random.uniform(0.8, 1.2)
            else:  # 25% fast
                speed = random.uniform(1.5, 2.2)
                
            intensity = random.randint(180, 255)
            trail_length = max(2, min(7, int(speed * 2)))
            
            # Always start from the top (y=0.0)
            drops.append([x, 0.0, speed, intensity, trail_length])
            active_columns.add(x)
        
        # Process each drop
        remaining_drops = []
        for drop in drops:
            x, y_float, speed, intensity, trail_length = drop
            
            # Calculate integer position
            y_int = int(y_float)
            prev_y_int = int(y_float - speed)
            
            # Draw all positions between previous and current y to ensure smooth movement
            for y_pos in range(max(0, prev_y_int), y_int + 1):
                if 0 <= y_pos < height:
                    # Draw the head of the drop
                    if y_pos == y_int:
                        pixel_idx = pixel_map.get((x, y_pos), 0)
                        pixels[pixel_idx] = (0, intensity, 0)
                    
                    # Draw the trail with fading intensity
                    for t in range(1, trail_length + 1):
                        trail_y = y_pos - t
                        if 0 <= trail_y < height:
                            # Calculate trail intensity with smooth falloff
                            trail_factor = 0.7 ** t
                            trail_intensity = int(intensity * trail_factor)
                            
                            # Add occasional character variations
                            r = trail_intensity // 8 if random.random() < 0.05 and trail_y % 3 == 0 else 0
                            g = trail_intensity
                            b = trail_intensity // 10 if trail_y % 4 == 0 else 0
                            
                            # Set pixel directly using our lookup map
                            pixel_idx = pixel_map.get((x, trail_y), 0)
                            pixels[pixel_idx] = (r, g, b)
            
            # Move drop down with variable speed
            y_float += speed
            
            # Keep drop if it's still on screen
            if y_int < height:
                remaining_drops.append([x, y_float, speed, intensity, trail_length])
            else:
                # Remove from active columns when drop goes off screen
                active_columns.discard(x)
        
        # Update drops list
        drops = remaining_drops
        
        # Show the frame
        pixels.show()
        time.sleep(delay)
        frame_number += 1