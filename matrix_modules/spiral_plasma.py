"""
Spiral Plasma effect inspired by polar coordinate transformations.
Creates rotating spiral patterns with flowing colors.
Optimized for LED matrix display with hypnotic spiral animations.
"""
import math
import time
from matrix_modules.utils import set_pixel, ultra_sin, ultra_cos, ultra_sqrt, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def spiral_plasma(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate spiral plasma effect using polar coordinates and rotations.
    Creates mesmerizing spiral patterns with dynamic color flows.
    """
    log_module_start("spiral_plasma", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Center point
    cx = width / 2.0
    cy = height / 2.0
    
    # Pre-calculate polar coordinates
    polar_coords = []
    for y in range(height):
        row = []
        for x in range(width):
            dx = x - cx
            dy = y - cy
            
            # Distance from center
            r = ultra_sqrt(dx * dx + dy * dy)
            
            # Angle in radians  
            angle = math.atan2(dy, dx)
            
            # Normalize angle to 0-1 range
            angle_norm = (angle + math.pi) / (2 * math.pi)
            
            row.append((r, angle, angle_norm))
        polar_coords.append(row)
    
    # Use ultra-fast lookup tables from constants/utils
    def fast_sin(x):
        return ultra_sin(x)
    
    def fast_cos(x):
        return ultra_cos(x)
    
    # Create spiral-themed color palette
    def create_spiral_palette(time_offset):
        palette = []
        for i in range(256):
            # Create flowing spectrum
            hue_cycle = (i * 3 + time_offset * 60) % 360
            
            # Vary saturation in spiral pattern
            sat = 0.8 + 0.2 * ultra_sin(i * math.pi / 32)
            
            # Brightness varies with spiral flow
            val = 0.7 + 0.3 * ultra_cos(i * math.pi / 64)
            
            # Convert HSV to RGB
            h = hue_cycle % 360
            c = val * sat
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = val - c
            
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
            
            palette.append((
                int((r + m) * 255),
                int((g + m) * 255),
                int((b + m) * 255)
            ))
        return palette
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Multiple spiral animations with different parameters
        spiral_params = [
            {'speed': 2.0, 'arms': 3, 'freq': 0.2, 'phase': 0},
            {'speed': -1.5, 'arms': 5, 'freq': 0.15, 'phase': math.pi},
            {'speed': 2.5, 'arms': 2, 'freq': 0.3, 'phase': math.pi/2},
            {'speed': -3.0, 'arms': 4, 'freq': 0.25, 'phase': math.pi*1.5},
        ]
        
        # Dynamic color palette
        palette = create_spiral_palette(t)
        
        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                r, angle, angle_norm = polar_coords[y][x]
                
                spiral_value = 0
                
                for params in spiral_params:
                    # Calculate spiral pattern
                    spiral_angle = angle + r * params['freq'] + t * params['speed']
                    
                    # Create spiral arms
                    arm_pattern = fast_sin(spiral_angle * params['arms'] + params['phase'])
                    
                    # Add distance-based modulation
                    distance_mod = fast_sin(r * 0.3 + t * 1.5)
                    
                    # Combine patterns
                    spiral_contribution = arm_pattern * distance_mod
                    
                    # Weight by distance (fade at edges)
                    distance_weight = 1.0 / (1.0 + r * 0.1)
                    spiral_value += spiral_contribution * distance_weight
                
                # Add radial waves
                radial_wave = fast_sin(r * 0.4 + t * 3.0)
                
                # Add angular waves
                angular_wave = fast_sin(angle * 8 + t * 2.0)
                
                # Combine all patterns
                combined = (spiral_value + radial_wave * 0.3 + angular_wave * 0.2) / 2.0
                
                # Create psychedelic color cycling
                color_base = angle_norm * 256 + r * 5
                color_mod = combined * 50 + t * 80
                final_color_idx = int(color_base + color_mod) % 256
                
                base_color = palette[final_color_idx]
                
                # Apply spiral brightness effect
                brightness = 0.6 + 0.4 * ((combined + 1.0) / 2.0)
                
                # Add center glow
                center_glow = 1.0
                if r < 3:
                    center_glow = 1.5 + 0.5 * fast_sin(t * 4.0)
                
                # Add spiral highlight effect
                spiral_highlight = 1.0
                for params in spiral_params:
                    spiral_phase = angle + r * params['freq'] + t * params['speed']
                    arm_intensity = abs(fast_sin(spiral_phase * params['arms']))
                    if arm_intensity > 0.9:
                        spiral_highlight += 0.3 * (arm_intensity - 0.9) * 10
                
                total_brightness = brightness * center_glow * min(2.0, spiral_highlight)
                
                final_color = (
                    int(base_color[0] * total_brightness),
                    int(base_color[1] * total_brightness),
                    int(base_color[2] * total_brightness)
                )
                
                # Clamp values
                final_color = (
                    min(255, max(0, final_color[0])),
                    min(255, max(0, final_color[1])),
                    min(255, max(0, final_color[2]))
                )
                
                # Add twinkling effect on spiral arms
                if frame % 30 < 5:
                    twinkle_chance = 0
                    for params in spiral_params:
                        spiral_phase = angle + r * params['freq'] + t * params['speed']
                        arm_match = abs(fast_sin(spiral_phase * params['arms']))
                        if arm_match > 0.95:
                            twinkle_chance += 0.3
                    
                    if twinkle_chance > 0.2:
                        sparkle = fast_sin(t * 10 + x + y) * twinkle_chance
                        if sparkle > 0:
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
            time.sleep(0.03)  # 33 FPS for smooth spiral motion
    
    duration = time.monotonic() - start_time
    log_module_finish("spiral_plasma", frame_count=frame, duration=duration)