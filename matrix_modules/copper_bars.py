"""
Copper Bars Effect - Classic Amiga/C64 horizontal color bars.
Smooth gradient bars that sweep across the screen with sine wave motion.
Iconic demoscene effect with metallic copper-like colors.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, COPPER_BARS_MAX_FRAMES, SINE_LUT_SIZE


def copper_bars(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=COPPER_BARS_MAX_FRAMES):
    """
    Generate classic copper bars effect with smooth gradients.
    Multiple horizontal bars with sine wave vertical movement.
    """
    log_module_start("copper_bars", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Use ultra-fast lookup tables from constants/utils
    def fast_sin(angle):
        return ultra_sin(angle)
    
    # Copper bar configurations
    bars = [
        {'center': 4, 'width': 6, 'freq': 0.8, 'phase': 0, 'colors': [(60, 30, 0), (255, 150, 50), (255, 200, 100)]},
        {'center': 9, 'width': 4, 'freq': 1.2, 'phase': 1.5, 'colors': [(0, 60, 30), (50, 255, 100), (100, 255, 150)]},
        {'center': 14, 'width': 5, 'freq': 0.6, 'phase': 3.0, 'colors': [(30, 0, 60), (100, 50, 255), (150, 100, 255)]},
    ]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Initialize all pixels to black to avoid flicker, then draw bars
        for y in range(height):
            for x in range(width):
                pixels[pixel_map[y * width + x]] = (0, 0, 0)
        
        # Draw each copper bar
        for bar in bars:
            # Calculate vertical position with sine wave
            bar_center = bar['center'] + 3 * fast_sin(t * bar['freq'] + bar['phase'])
            bar_width = bar['width']
            
            # Draw gradient bar
            for y in range(height):
                distance_from_center = abs(y - bar_center)
                
                if distance_from_center <= bar_width:
                    # Calculate gradient position (0 = center, 1 = edge)
                    gradient_pos = distance_from_center / bar_width
                    
                    # Smooth gradient using cosine
                    intensity = (1 + math.cos(gradient_pos * math.pi)) / 2
                    
                    # Interpolate colors
                    colors = bar['colors']
                    if intensity > 0.7:  # Bright center
                        t_color = (intensity - 0.7) / 0.3
                        color = (
                            int(colors[1][0] * (1 - t_color) + colors[2][0] * t_color),
                            int(colors[1][1] * (1 - t_color) + colors[2][1] * t_color),
                            int(colors[1][2] * (1 - t_color) + colors[2][2] * t_color)
                        )
                    else:  # Darker edges
                        t_color = intensity / 0.7
                        color = (
                            int(colors[0][0] * (1 - t_color) + colors[1][0] * t_color),
                            int(colors[0][1] * (1 - t_color) + colors[1][1] * t_color),
                            int(colors[0][2] * (1 - t_color) + colors[1][2] * t_color)
                        )
                    
                    # Draw entire row
                    for x in range(width):
                        pixel_idx = pixel_map[y * width + x]
                        current = pixels[pixel_idx]
                        # Additive blending for overlapping bars
                        pixels[pixel_idx] = (
                            min(255, current[0] + color[0]),
                            min(255, current[1] + color[1]),
                            min(255, current[2] + color[2])
                        )
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.04)  # 25 FPS
    
    log_module_finish("copper_bars", frame_count=frame, duration=time.monotonic() - start_time)