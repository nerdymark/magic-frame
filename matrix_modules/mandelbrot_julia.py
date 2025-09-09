"""
Mandelbrot and Julia Sets - Classic fractal mathematics visualization.
Beautiful complex plane fractals with smooth coloring and zooming animations.
Showcases the infinite complexity at the boundary between order and chaos.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, MANDELBROT_MAX_FRAMES, CENTER_X, CENTER_Y, MANDELBROT_MAX_ITER


def mandelbrot_julia(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=MANDELBROT_MAX_FRAMES):
    """
    Generate Mandelbrot and Julia set fractals with smooth coloring.
    Alternates between different Julia sets and zooming Mandelbrot.
    """
    log_module_start("mandelbrot_julia", max_frames=max_frames)
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
    coord_x = []
    coord_y = []
    for x in range(width):
        coord_x.append((x - CENTER_X) / (width/4.0))
    for y in range(height):
        coord_y.append((y - CENTER_Y) / (height/4.0))
    
    # Smooth, relaxing color palette - NO ABRUPT CHANGES!
    def get_fractal_color(iterations, max_iter, smooth_value=0):
        if iterations >= max_iter:
            return (5, 5, 20)  # Very dark blue instead of black for depth
        
        # Smooth coloring using continuous escape count
        smooth_iter = iterations + 1 - math.log(math.log(max(smooth_value, 2.0))) / math.log(2.0)
        
        # Single, smooth gradient - RELAXING DEEP OCEAN THEME
        t = smooth_iter / max_iter
        
        # Very gentle time-based color shift (much slower, more subtle)
        time_shift = (time.monotonic() - start_time) * 0.1  # 10x slower color evolution
        
        # Deep ocean gradient: dark blue -> teal -> light blue -> white
        # Add very subtle time-based hue shifting
        base_hue = 200 + ultra_sin(time_shift) * 30  # Gentle shift between blue-cyan range
        
        if t < 0.3:
            # Deep blue to medium blue
            intensity = t / 0.3
            r = int(5 + 25 * intensity)   # Very dark blue to darker blue
            g = int(10 + 60 * intensity)  # Slight blue-green tint
            b = int(40 + 80 * intensity)  # Deep blue base
        elif t < 0.6:
            # Medium blue to teal
            intensity = (t - 0.3) / 0.3
            r = int(30 + 20 * intensity)  # Gentle increase
            g = int(70 + 80 * intensity)  # Blue to teal transition
            b = int(120 + 60 * intensity) # Maintain blue richness
        elif t < 0.85:
            # Teal to light blue
            intensity = (t - 0.6) / 0.25
            r = int(50 + 60 * intensity)  # Gentle lightening
            g = int(150 + 60 * intensity) # Bright teal to light blue
            b = int(180 + 40 * intensity) # Light blue
        else:
            # Light blue to soft white
            intensity = (t - 0.85) / 0.15
            r = int(110 + 100 * intensity) # Soft white highlights
            g = int(210 + 40 * intensity)  # Maintain slight blue tint
            b = int(220 + 30 * intensity)  # Soft blue-white
        
        # Apply very subtle time-based modulation (much gentler)
        time_mod = 0.9 + 0.1 * ultra_sin(time_shift * 0.5)  # Very subtle brightness variation
        
        return (
            int(min(255, r * time_mod)),
            int(min(255, g * time_mod)),
            int(min(255, b * time_mod))
        )
    
    def mandelbrot_iterations(cx, cy, max_iter):
        """Calculate Mandelbrot iterations with smooth escape value"""
        zx = zy = 0.0
        
        for i in range(max_iter):
            if zx*zx + zy*zy > 4.0:
                # Smooth escape value for continuous coloring
                smooth_val = zx*zx + zy*zy
                return i, smooth_val
            
            # z = z^2 + c
            new_zx = zx*zx - zy*zy + cx
            zy = 2*zx*zy + cy
            zx = new_zx
        
        return max_iter, 0
    
    def julia_iterations(zx, zy, cx, cy, max_iter):
        """Calculate Julia set iterations with smooth escape value"""
        for i in range(max_iter):
            if zx*zx + zy*zy > 4.0:
                smooth_val = zx*zx + zy*zy
                return i, smooth_val
            
            # z = z^2 + c (where c is constant for Julia set)
            new_zx = zx*zx - zy*zy + cx
            zy = 2*zx*zy + cy
            zx = new_zx
        
        return max_iter, 0
    
    # Interesting Julia set constants
    julia_constants = [
        (-0.4, 0.6),      # Dragon fractal
        (-0.8, 0.156),    # Lightning
        (-0.7269, 0.1889), # Spiral
        (0.285, 0.01),    # Leaf-like
        (-0.12, 0.74),    # Swirl
        (-0.75, 0.0),     # Dust
        (0.3, 0.5),       # Feather
        (-1.0, 0.0),      # Cauliflower
    ]
    
    frame = 0
    max_iterations = MANDELBROT_MAX_ITER  # Balanced for performance
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Don't clear pixels to avoid flicker - overwrite all pixels instead
        
        # Determine which fractal to show - MUCH LONGER DISPLAY TIME
        fractal_cycle = int(t / 45) % (len(julia_constants) + 2)  # 45 seconds per pattern instead of 15
        
        if fractal_cycle < len(julia_constants):
            # Julia set mode
            cx, cy = julia_constants[fractal_cycle]
            
            # Very gentle animation of Julia constant - more relaxing
            cx += 0.02 * ultra_sin(t * 0.1)  # Much slower, subtler movement
            cy += 0.015 * ultra_cos(t * 0.13)
            
            # Very gentle zoom animation
            zoom = 1.0 + 0.15 * ultra_sin(t * 0.05)  # Much slower, subtler zoom
            
            for y in range(height):
                for x in range(width):
                    # Map to complex plane with zoom
                    zx = coord_x[x] / zoom
                    zy = coord_y[y] / zoom
                    
                    iterations, smooth_val = julia_iterations(zx, zy, cx, cy, max_iterations)
                    color = get_fractal_color(iterations, max_iterations, smooth_val)
                    
                    pixel_idx = pixel_map[y * width + x]
                    pixels[pixel_idx] = color
        
        elif fractal_cycle == len(julia_constants):
            # Gentle Mandelbrot exploration
            zoom = 1.0 + 0.2 * ultra_sin(t * 0.05)  # Much gentler zoom
            offset_x = -0.5 + 0.1 * ultra_sin(t * 0.03)  # Slower drift
            offset_y = 0.0 + 0.05 * ultra_cos(t * 0.04)  # Subtle movement
            
            for y in range(height):
                for x in range(width):
                    # Map to complex plane with zoom and offset
                    cx = coord_x[x] / zoom + offset_x
                    cy = coord_y[y] / zoom + offset_y
                    
                    iterations, smooth_val = mandelbrot_iterations(cx, cy, max_iterations)
                    color = get_fractal_color(iterations, max_iterations, smooth_val)
                    
                    pixel_idx = pixel_map[y * width + x]
                    pixels[pixel_idx] = color
        
        else:
            # Deep zoom Mandelbrot at interesting location
            # Zoom into the "seahorse valley"
            center_x = -0.743643887037151
            center_y = 0.13182590420533
            
            # Exponential zoom
            zoom_factor = 1.0 + math.pow(2.0, (t % 10) - 5)
            
            for y in range(height):
                for x in range(width):
                    cx = center_x + coord_x[x] / zoom_factor
                    cy = center_y + coord_y[y] / zoom_factor
                    
                    iterations, smooth_val = mandelbrot_iterations(cx, cy, max_iterations + 20)
                    color = get_fractal_color(iterations, max_iterations + 20, smooth_val)
                    
                    pixel_idx = pixel_map[y * width + x]
                    pixels[pixel_idx] = color
        
        # Very gentle breathing effect - much more subtle
        if frame % 300 < 150:  # Much slower, gentler breathing
            breath = ultra_sin(t * 0.5) * 0.05 + 0.95  # Much more subtle variation
            for i in range(len(pixels)):
                current = pixels[i]
                pixels[i] = (
                    int(current[0] * breath),
                    int(current[1] * breath),
                    int(current[2] * breath)
                )
        
        # Very subtle corner indicators - blend with ocean theme
        indicator_color = (20, 40, 60)  # Very subtle dark blue indicators
        if fractal_cycle < len(julia_constants):
            # Julia set indicator - top corners (very subtle)
            pixels[pixel_map[0]] = indicator_color
            pixels[pixel_map[width-1]] = indicator_color
        else:
            # Mandelbrot indicator - bottom corners (very subtle) 
            pixels[pixel_map[(height-1) * width]] = indicator_color
            pixels[pixel_map[(height-1) * width + width-1]] = indicator_color
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.12)  # Slower, more relaxing pace - ~8 FPS
    
    log_module_finish("mandelbrot_julia", frame_count=frame, duration=time.monotonic() - start_time)