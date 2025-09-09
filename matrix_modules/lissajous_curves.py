"""
Lissajous Curves - Beautiful mathematical curve patterns.
Creates flowing parametric curves using sine and cosine functions with different frequencies.
Classic mathematical visualization with smooth animations.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, LISSAJOUS_MAX_FRAMES, CENTER_X, CENTER_Y


def lissajous_curves(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=LISSAJOUS_MAX_FRAMES):
    """
    Generate animated Lissajous curves with varying frequencies and phases.
    Creates beautiful mathematical patterns that flow and evolve over time.
    """
    log_module_start("lissajous_curves", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Center coordinates
    cx = width / 2.0
    cy = height / 2.0
    
    # Use ultra-fast lookup tables from constants/utils
    def fast_sin(angle):
        return ultra_sin(angle)
    
    def fast_cos(angle):
        return ultra_cos(angle)
    
    # Color palette for different curves
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
    
    # Classic Lissajous parameter sets - FAMOUS MATHEMATICAL PATTERNS!
    curve_sets = [
        # Perfect circle (1:1 ratio with 90° phase shift)
        {'a': 1, 'b': 1, 'phase': math.pi/2, 'scale': 0.8, 'name': 'Circle'},
        # Figure-8 (1:2 ratio)
        {'a': 1, 'b': 2, 'phase': 0, 'scale': 0.7, 'name': 'Figure-8'},
        # Three-leaf rose (3:2 ratio with phase shift)
        {'a': 3, 'b': 2, 'phase': math.pi/2, 'scale': 0.6, 'name': '3-Leaf Rose'},
        # Four-leaf clover (3:4 ratio)
        {'a': 3, 'b': 4, 'phase': math.pi/4, 'scale': 0.5, 'name': '4-Leaf Clover'},
        # Complex orbital pattern (5:4 ratio)
        {'a': 5, 'b': 4, 'phase': 0, 'scale': 0.5, 'name': 'Orbital'},
        # Intricate flower (5:6 ratio)
        {'a': 5, 'b': 6, 'phase': math.pi/3, 'scale': 0.45, 'name': 'Flower'},
    ]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Initialize all pixels to black to avoid flicker
        for y in range(height):
            for x in range(width):
                pixels[pixel_map[y * width + x]] = (0, 0, 0)
        
        # Cycle through different curve sets with longer display time
        current_set = frame // 400 % len(curve_sets)  # Show each pattern longer
        params = curve_sets[current_set]
        
        # Display pattern name briefly at start of each cycle
        if frame % 400 < 60:  # Show name for first 60 frames
            pattern_name = params.get('name', f'Pattern {current_set + 1}')
            # Add title display at top of screen
            title_y = 1
            for i, char in enumerate(pattern_name[:6]):  # Limit to 6 chars
                if i * 3 < width - 3:
                    pixels[pixel_map[title_y * width + i * 3]] = (100, 100, 100)
        
        # Animation parameters
        time_phase = t * 0.5
        color_shift = t * 30
        
        # Single clear curve for better visibility
        num_curves = 1  # Simplified to one clear curve
        
        for curve_idx in range(num_curves):
            # Each curve has different parameters
            curve_phase = curve_idx * 2 * math.pi / num_curves
            curve_color_offset = curve_idx * 120  # 120 degrees apart
            
            # Modified parameters for this curve
            a = params['a'] + curve_idx * 0.1
            b = params['b'] + curve_idx * 0.15
            phase = params['phase'] + curve_phase
            scale = params['scale'] * (0.8 + curve_idx * 0.1)
            
            # Calculate curve points with higher resolution for smoothness
            curve_points = []
            resolution = 300  # Higher resolution for smoother curves
            
            for i in range(resolution):
                # Parameter t for the curve
                t_param = i * 4 * math.pi / resolution + time_phase
                
                # Lissajous parametric equations - CLASSIC MATHEMATICAL CURVES!
                # x = A * sin(a*t + φ)  |  y = B * sin(b*t)
                # These create beautiful figure-8, flower, and orbital patterns
                x_param = scale * fast_sin(a * t_param + phase) * (width - 1) / 2
                y_param = scale * fast_sin(b * t_param) * (height - 1) / 2
                
                # Convert to screen coordinates
                screen_x = int(cx + x_param)
                screen_y = int(cy + y_param)
                
                # Store valid points
                if 0 <= screen_x < width and 0 <= screen_y < height:
                    # Color based on position along curve - BRIGHT AND CLEAR!
                    hue = (i * 3 + color_shift + curve_color_offset) % 360
                    saturation = 1.0  # Full saturation for vivid colors
                    value = 0.9 + 0.1 * fast_sin(t_param + curve_phase)  # Much brighter
                    
                    color = hsv_to_rgb(hue, saturation, value)
                    curve_points.append((screen_x, screen_y, color))
            
            # Draw the curve with anti-aliasing effect
            for point in curve_points:
                screen_x, screen_y, color = point
                pixel_idx = pixel_map[screen_y * width + screen_x]
                
                # Set pixel directly for bright, clear curves
                pixels[pixel_idx] = color
                
                # Add bright glow effect to make curves more visible
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    glow_x = screen_x + dx
                    glow_y = screen_y + dy
                    
                    if 0 <= glow_x < width and 0 <= glow_y < height:
                        glow_idx = pixel_map[glow_y * width + glow_x]
                        glow_color = (color[0] // 3, color[1] // 3, color[2] // 3)  # Brighter glow
                        current = pixels[glow_idx]
                        pixels[glow_idx] = (
                            min(255, current[0] + glow_color[0]),
                            min(255, current[1] + glow_color[1]),
                            min(255, current[2] + glow_color[2])
                        )
        
        # Add sparkle effect at curve intersections
        if frame % 10 == 0:
            for _ in range(3):
                spark_x = int(cx + fast_sin(t * 3.7) * 6)
                spark_y = int(cy + fast_cos(t * 2.3) * 6)
                
                if 0 <= spark_x < width and 0 <= spark_y < height:
                    spark_idx = pixel_map[spark_y * width + spark_x]
                    spark_color = (255, 255, 200)  # Bright yellow sparkle
                    pixels[spark_idx] = spark_color
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.04)  # 25 FPS for smooth curve animation
    
    log_module_finish("lissajous_curves", frame_count=frame, duration=time.monotonic() - start_time)