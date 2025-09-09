"""
Raster Bars - Classic demoscene horizontal color bars.
Simple, smooth horizontal bars that move vertically with sine wave motion.
Pure classic demoscene aesthetic with smooth color transitions.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, RASTER_BARS_MAX_FRAMES


def raster_bars(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=RASTER_BARS_MAX_FRAMES):
    """
    Generate classic raster bar effects - smooth horizontal colored bars.
    Simple, elegant demoscene effect with sine wave movement.
    """
    log_module_start("raster_bars", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Subtle color palette for smooth raster bars
    bar_colors = [
        (120, 40, 40),   # Muted red
        (120, 80, 30),   # Muted orange
        (100, 100, 30),  # Muted yellow
        (60, 120, 30),   # Muted yellow-green
        (30, 120, 30),   # Muted green
        (30, 120, 80),   # Muted green-cyan
        (30, 100, 120),  # Muted cyan
        (30, 60, 120),   # Muted blue-cyan
        (30, 30, 120),   # Muted blue
        (60, 30, 120),   # Muted blue-purple
        (100, 30, 120),  # Muted magenta
        (120, 30, 80),   # Muted pink
    ]
    
    # Define 3 subtle raster bars with better spacing
    bars = [
        {'y': 4, 'height': 4, 'color_idx': 0, 'speed': 0.5, 'amplitude': 1.5},
        {'y': 9, 'height': 5, 'color_idx': 4, 'speed': 0.4, 'amplitude': 2.0},
        {'y': 14, 'height': 4, 'color_idx': 8, 'speed': 0.6, 'amplitude': 1.8},
    ]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Initialize all pixels to black to avoid flicker
        for y in range(height):
            for x in range(width):
                pixels[pixel_map[y * width + x]] = (0, 0, 0)
        
        # Draw each raster bar
        for bar in bars:
            # Calculate moving position with sine wave
            base_y = bar['y']
            offset = bar['amplitude'] * ultra_sin(t * bar['speed'])
            current_y = base_y + offset
            
            # Get very slowly cycling color
            color_offset = int(t * 5) % len(bar_colors)  # Much slower color cycling
            color_idx = (bar['color_idx'] + color_offset) % len(bar_colors)
            bar_color = bar_colors[color_idx]
            
            # Draw the bar with smooth gradient
            bar_height = bar['height']
            for dy in range(-bar_height * 2, bar_height * 2 + 1):  # Wider gradient for smoother fade
                y_pos = int(current_y + dy)
                
                if 0 <= y_pos < height:
                    # Calculate smooth fade from center using cosine for natural falloff
                    distance_from_center = abs(dy)
                    max_distance = bar_height * 2
                    
                    if distance_from_center <= max_distance:
                        # Smooth cosine falloff
                        intensity = (1 + math.cos(distance_from_center * math.pi / max_distance)) / 2
                        intensity = intensity * 0.7  # Reduce overall brightness for subtlety
                    else:
                        intensity = 0
                    
                    # Apply color with intensity
                    final_color = (
                        int(bar_color[0] * intensity),
                        int(bar_color[1] * intensity),
                        int(bar_color[2] * intensity)
                    )
                    
                    # Draw entire horizontal line
                    for x in range(width):
                        pixel_idx = pixel_map[y_pos * width + x]
                        current = pixels[pixel_idx]
                        
                        # Smooth blending for overlapping bars (not too bright)
                        pixels[pixel_idx] = (
                            min(255, current[0] + final_color[0]),
                            min(255, current[1] + final_color[1]),
                            min(255, current[2] + final_color[2])
                        )
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.08)  # ~12 FPS for smooth, classic feel
    
    log_module_finish("raster_bars", frame_count=frame, duration=time.monotonic() - start_time)