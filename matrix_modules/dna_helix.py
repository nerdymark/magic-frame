"""
DNA Helix - Smooth double helix structure animation with base pairs.
Simplified visualization of DNA double helix with rotating base pairs.
Optimized for smooth, non-flickery animation on LED matrix.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, DNA_HELIX_MAX_FRAMES, CENTER_X, CENTER_Y


def dna_helix(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=DNA_HELIX_MAX_FRAMES):
    """
    Generate smooth DNA double helix animation with base pairs.
    Simplified for flicker-free display on LED matrix.
    """
    log_module_start("dna_helix", max_frames=max_frames)
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
    cx = CENTER_X
    cy = CENTER_Y
    
    # Use ultra-fast lookup tables from constants/utils
    def fast_sin(degrees):
        # Convert degrees to radians for ultra_sin
        return ultra_sin(degrees * math.pi / 180)
    
    def fast_cos(degrees):
        # Convert degrees to radians for ultra_cos
        return ultra_cos(degrees * math.pi / 180)
    
    # DNA base pair colors (scientifically accurate)
    base_colors = {
        'A': (255, 100, 100),   # Adenine - Red
        'T': (100, 100, 255),   # Thymine - Blue  
        'G': (100, 255, 100),   # Guanine - Green
        'C': (255, 255, 100),   # Cytosine - Yellow
    }
    
    # Base pair combinations (A-T, G-C)
    base_pairs = [
        ('A', 'T'), ('T', 'A'), ('G', 'C'), ('C', 'G'),
        ('A', 'T'), ('G', 'C'), ('T', 'A'), ('C', 'G'),
        ('G', 'C'), ('A', 'T'), ('C', 'G'), ('T', 'A'),
    ]
    
    # Backbone color (phosphate-sugar)
    backbone_color = (200, 200, 200)  # White/silver
    
    # Helix parameters
    helix_radius = 4.0
    helix_pitch = 6  # Shorter pitch for more turns visible
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Initialize all pixels to black to avoid artifacts
        for y in range(height):
            for x in range(width):
                pixels[pixel_map[y * width + x]] = (0, 0, 0)
        
        # Smooth animation parameters
        rotation_speed = 20  # Slower rotation
        vertical_scroll = t * 1.5  # Slower vertical movement
        
        # Draw DNA strands with improved visualization
        for strand_offset in [0, 180]:  # Two strands 180 degrees apart
            for y in range(height):
                # Calculate smooth helical motion
                angle = (y / helix_pitch * 360 + t * rotation_speed + strand_offset) % 360
                
                # 3D helix coordinates projected to 2D
                helix_x = cx + helix_radius * fast_cos(angle)
                
                # Draw backbone with subtle glow
                if 0 <= helix_x < width:
                    pixel_idx = pixel_map[y * width + int(helix_x)]
                    pixels[pixel_idx] = backbone_color
                    
                    # Add subtle glow around backbone
                    for dx in [-1, 1]:
                        glow_x = int(helix_x) + dx
                        if 0 <= glow_x < width:
                            glow_idx = pixel_map[y * width + glow_x]
                            current = pixels[glow_idx]
                            glow_color = (
                                min(255, current[0] + 30),
                                min(255, current[1] + 30),
                                min(255, current[2] + 30)
                            )
                            pixels[glow_idx] = glow_color
        
        # Draw base pairs with proper A-T, G-C pairing
        for y in range(0, height, 2):  # Base pairs every 2 pixels
            # Calculate positions of both strands at this height
            angle1 = (y / helix_pitch * 360 + t * rotation_speed) % 360
            angle2 = (angle1 + 180) % 360
            
            x1 = cx + helix_radius * fast_cos(angle1)
            x2 = cx + helix_radius * fast_cos(angle2)
            
            # Get proper base pair for this position
            base_index = int(y + t * 3) % len(base_pairs)
            base1, base2 = base_pairs[base_index]
            color1 = base_colors[base1]
            color2 = base_colors[base2]
            
            # Draw base pair connection with color interpolation
            steps = max(1, int(abs(x2 - x1)))
            for step in range(steps + 1):
                if steps == 0:
                    continue
                    
                t_interpolate = step / steps
                
                # Interpolate position
                x_pos = x1 + (x2 - x1) * t_interpolate
                
                # Interpolate color (ends are base colors, middle is hydrogen bonds)
                if t_interpolate < 0.3:
                    color = color1
                elif t_interpolate > 0.7:
                    color = color2
                else:
                    # Fade to lighter color in middle (hydrogen bonds)
                    mid_factor = abs(t_interpolate - 0.5) * 4  # 0 at center, 1 at edges
                    color = (
                        int(200 * (1 - mid_factor) + (color1[0] + color2[0]) * mid_factor * 0.25),
                        int(200 * (1 - mid_factor) + (color1[1] + color2[1]) * mid_factor * 0.25),
                        int(200 * (1 - mid_factor) + (color1[2] + color2[2]) * mid_factor * 0.25)
                    )
                
                if 0 <= x_pos < width and 0 <= y < height:
                    pixel_idx = pixel_map[y * width + int(x_pos)]
                    current = pixels[pixel_idx]
                    
                    # Blend with existing pixels
                    pixels[pixel_idx] = (
                        min(255, max(current[0], color[0])),
                        min(255, max(current[1], color[1])),
                        min(255, max(current[2], color[2]))
                    )
        
        # Add subtle groove effect (major groove)
        groove_intensity = 20 + int(10 * fast_sin(t * 2))
        groove_color = (0, groove_intensity, int(groove_intensity * 0.8))
        
        for y in range(height):
            groove_angle = (y / helix_pitch * 360 + t * rotation_speed) % 360
            if 60 <= groove_angle <= 120:  # Major groove region
                groove_x = cx + (helix_radius + 1.5) * fast_cos(groove_angle)
                if 0 <= groove_x < width:
                    pixel_idx = pixel_map[y * width + int(groove_x)]
                    current = pixels[pixel_idx]
                    pixels[pixel_idx] = (
                        min(255, current[0] + groove_color[0]),
                        min(255, current[1] + groove_color[1]),
                        min(255, current[2] + groove_color[2])
                    )
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.1)  # 10 FPS for smooth, non-flickery animation
    
    log_module_finish("dna_helix", frame_count=frame, duration=time.monotonic() - start_time)