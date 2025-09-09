"""
Diamond Plasma effect inspired by Rosetta Code variations.
Creates diamond-shaped patterns using Manhattan distance calculations.
Optimized for LED matrix display with rainbow colors.
"""
import math
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT


def diamond_plasma(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate diamond plasma effect using Manhattan distance and rotation.
    Creates flowing diamond patterns with rainbow colors.
    """
    log_module_start("diamond_plasma", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate coordinate transformations
    cx = width / 2.0
    cy = height / 2.0
    
    # Pre-calculate Manhattan distances and diamond coordinates
    diamond_coords = []
    for y in range(height):
        row = []
        for x in range(width):
            # Diamond coordinates (rotated 45 degrees)
            dx = x - cx
            dy = y - cy
            
            # Manhattan distance for diamond effect
            manhattan = abs(dx) + abs(dy)
            
            # Rotated coordinates for diamond patterns
            rot_x = dx * 0.707 - dy * 0.707
            rot_y = dx * 0.707 + dy * 0.707
            
            row.append((manhattan, rot_x, rot_y))
        diamond_coords.append(row)
    
    # Use ultra-fast lookup tables from constants/utils
    def fast_sin(x):
        return ultra_sin(x)
    
    # Rainbow color palette using HSV
    def hsv_to_rgb(h, s, v):
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    # Pre-generate rainbow palette
    rainbow_palette = []
    for i in range(256):
        hue = i * 360 / 256
        r, g, b = hsv_to_rgb(hue, 0.9, 0.9)
        rainbow_palette.append((r, g, b))
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Animation parameters for diamond effects
        time1 = t * 1.5
        time2 = t * 2.0
        time3 = t * 1.2
        
        # Color cycling
        color_offset = int(t * 60) % 256
        
        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                manhattan, rot_x, rot_y = diamond_coords[y][x]
                
                # Diamond plasma calculation using multiple sine waves
                # Pattern 1: Manhattan distance-based diamonds
                v1 = fast_sin(manhattan * 0.3 + time1)
                
                # Pattern 2: Rotating diamond grid
                v2 = fast_sin(rot_x * 0.25 + time2)
                v3 = fast_sin(rot_y * 0.25 + time2)
                
                # Pattern 3: Concentric diamond rings
                ring_dist = manhattan * 0.4
                v4 = fast_sin(ring_dist + time3)
                
                # Pattern 4: Diamond waves
                wave = abs(rot_x) + abs(rot_y)
                v5 = fast_sin(wave * 0.2 + time1)
                
                # Pattern 5: Cross-hatching effect
                cross = fast_sin(x * 0.3 + time2) + fast_sin(y * 0.3 + time3)
                v6 = cross * 0.5
                
                # Combine all patterns
                combined = (v1 + v2 + v3 + v4 + v5 + v6) / 6.0
                
                # Create diamond-specific color effect
                # Use Manhattan distance to modify color cycling
                color_mod = int(manhattan * 8 + combined * 50) % 256
                final_color_idx = (color_mod + color_offset) % 256
                
                # Apply diamond brightness effect
                # Brighter at diamond edges and intersections
                edge_factor = 1.0
                if manhattan > 1:
                    # Create bright edges at diamond boundaries
                    diamond_edge = abs(fast_sin(manhattan * 0.5))
                    edge_factor = 0.6 + 0.4 * diamond_edge
                
                # Get base color from rainbow palette
                base_color = rainbow_palette[final_color_idx]
                
                # Apply brightness and edge effects
                final_color = (
                    int(base_color[0] * edge_factor),
                    int(base_color[1] * edge_factor),
                    int(base_color[2] * edge_factor)
                )
                
                # Add sparkle to diamond centers
                if manhattan < 2 and frame % 40 < 5:
                    sparkle = 0.5 * fast_sin(t * 8 + x + y)
                    final_color = (
                        min(255, int(final_color[0] * (1 + sparkle))),
                        min(255, int(final_color[1] * (1 + sparkle))),
                        min(255, int(final_color[2] * (1 + sparkle)))
                    )
                
                pixels[pixel_map[pixel_idx]] = final_color
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.02)  # 50 FPS
    
    log_module_finish("diamond_plasma", frame_count=frame, duration=time.monotonic() - start_time)