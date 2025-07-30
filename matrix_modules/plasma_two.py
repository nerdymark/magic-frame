"""
True plasma effect based on sine wave mathematics.
Implements the classic plasma algorithm using multiple sine functions
combined to create smooth, flowing patterns.
"""
import math
import time
from matrix_modules.utils import set_pixel


def plasma_two(pixels, width, height, delay=0.0, max_frames=1000):
    """
    Generate plasma effect using sine wave mathematics.
    Based on the classic plasma algorithm from lodev.org
    Optimized for 30+ FPS performance.
    """
    start_time = time.monotonic()
    
    # Pre-calculate static sine values for coordinates to avoid repeated calculations
    x_sins = [math.sin(x / 6.0) for x in range(width)]
    y_sins = [math.sin(y / 4.5) for y in range(height)]
    xy_sins = [[math.sin((x + y) / 7.0) for x in range(width)] for y in range(height)]
    
    frame = 0
    while frame < max_frames:
        frame_start = time.monotonic()
        current_time = time.monotonic() - start_time
        
        # Time-based animation parameters (faster for visible motion)
        time1 = current_time * 3.0
        time2 = current_time * 2.5
        time3 = current_time * 2.0
        
        # Pre-calculate moving centers and time-based values once per frame
        center_x = width * 0.5 + 4.0 * math.sin(time1 * 0.3)
        center_y = height * 0.5 + 3.0 * math.cos(time2 * 0.25)
        center_x2 = width * 0.5 + 3.0 * math.cos(time3 * 0.4)
        center_y2 = height * 0.5 + 2.0 * math.sin(time3 * 0.35)
        
        # Pre-calculate time-based sine values
        sin_time1 = math.sin(time1 * 0.7)
        cos_time1 = math.cos(time1 * 0.7)
        sin_time2 = math.sin(time2 * 0.8 + 2.094)
        cos_time2 = math.cos(time2 * 0.8 + 2.094)
        sin_time3 = math.sin(time3 * 0.9 + 4.188)
        cos_time3 = math.cos(time3 * 0.9 + 4.188)
        
        for y in range(height):
            for x in range(width):
                # Use pre-calculated static values
                value1 = x_sins[x]
                value2 = y_sins[y]
                value3 = xy_sins[y][x]
                
                # Calculate distance-based patterns (optimized)
                dx = x - center_x
                dy = y - center_y
                distance = (dx * dx + dy * dy) ** 0.5  # Slightly faster than math.sqrt
                value4 = math.sin(distance * 0.333)  # /3.0 as multiplication
                
                dx2 = x - center_x2
                dy2 = y - center_y2
                distance2 = (dx2 * dx2 + dy2 * dy2) ** 0.5
                value5 = math.sin(distance2 * 0.25)  # /4.0 as multiplication
                
                # Combine patterns with pre-calculated time values
                combined = (value1 + value2 + value3 + 
                           math.sin(value4 + time1) + 
                           math.sin(value5 + time2)) * 0.2  # /5.0 as multiplication
                
                # Use pre-calculated time-based sine/cosine for RGB
                combined_sin = math.sin(combined)
                
                red = int(128.0 + 120.0 * combined_sin * sin_time1)
                green = int(128.0 + 120.0 * combined_sin * sin_time2)
                blue = int(128.0 + 120.0 * combined_sin * sin_time3)
                
                # Clamp values (faster than max/min)
                red = 255 if red > 255 else (0 if red < 0 else red)
                green = 255 if green > 255 else (0 if green < 0 else green)
                blue = 255 if blue > 255 else (0 if blue < 0 else blue)
                
                # Handle serpentine LED layout
                display_x = width - 1 - x if y % 2 == 0 else x
                
                # Direct pixel access for maximum speed
                pixel_index = y * width + display_x
                pixels[pixel_index] = (red, green, blue)
        
        pixels.show()
        frame += 1
        
        # Target 30+ FPS (33ms per frame max)
        if delay > 0:
            elapsed = time.monotonic() - frame_start
            target_frame_time = 1.0 / 30.0  # 33ms for 30 FPS
            sleep_time = max(0, target_frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)