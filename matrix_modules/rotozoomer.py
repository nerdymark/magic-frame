"""
Rotozoomer Effect - Classic demoscene rotating and zooming texture patterns.
Combines rotation and scaling transformations on repeating textures.
Creates hypnotic spinning and zooming visual effects.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin, ultra_cos, ultra_sqrt
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, ROTOZOOMER_MAX_FRAMES, CENTER_X, CENTER_Y, TRIG_LUT_SIZE


def rotozoomer(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=ROTOZOOMER_MAX_FRAMES):
    """
    Generate rotozoomer effect with rotating and zooming textures.
    Classic demoscene effect with mathematical texture transformations.
    """
    log_module_start("rotozoomer", max_frames=max_frames)
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
    def fast_sin(angle):
        return ultra_sin(angle)
    
    def fast_cos(angle):
        return ultra_cos(angle)
    
    # Texture generation functions
    def checkerboard_texture(u, v):
        """Classic checkerboard pattern"""
        check_size = 4
        return int((int(u * check_size) + int(v * check_size)) % 2)
    
    def rings_texture(u, v):
        """Concentric rings pattern"""
        distance = ultra_sqrt((u - 0.5)**2 + (v - 0.5)**2)
        return int(ultra_sin(distance * 20) > 0)
    
    def spiral_texture(u, v):
        """Spiral pattern"""
        angle = math.atan2(v - 0.5, u - 0.5)
        distance = ultra_sqrt((u - 0.5)**2 + (v - 0.5)**2)
        spiral_value = ultra_sin(angle * 4 + distance * 30)
        return int(spiral_value > 0)
    
    def plasma_texture(u, v, t):
        """Plasma-like texture"""
        value = (ultra_sin(u * 10 + t) + 
                ultra_sin(v * 8 + t * 0.7) + 
                ultra_sin((u + v) * 6 + t * 0.5)) / 3.0
        return (value + 1.0) / 2.0  # Normalize to 0-1
    
    def mandala_texture(u, v):
        """Mandala-like radial pattern"""
        angle = math.atan2(v - 0.5, u - 0.5)
        distance = ultra_sqrt((u - 0.5)**2 + (v - 0.5)**2)
        pattern = ultra_sin(angle * 8) * ultra_cos(distance * 15)
        return int(pattern > 0)
    
    # Texture list for cycling
    textures = [
        ('checkerboard', checkerboard_texture),
        ('rings', rings_texture),
        ('spiral', spiral_texture),
        ('plasma', plasma_texture),
        ('mandala', mandala_texture),
    ]
    
    # Color schemes
    color_schemes = [
        # Psychedelic
        [(255, 0, 255), (0, 255, 255)],  # Magenta/Cyan
        # Fire
        [(255, 100, 0), (255, 255, 0)],  # Orange/Yellow
        # Ocean
        [(0, 100, 255), (0, 255, 100)],  # Blue/Green
        # Sunset
        [(255, 50, 150), (255, 200, 50)],  # Pink/Yellow
        # Matrix
        [(0, 255, 0), (0, 100, 0)],  # Bright/Dark Green
    ]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Cycle through textures every 8 seconds
        texture_index = int(t / 8) % len(textures)
        texture_name, texture_func = textures[texture_index]
        
        # Cycle through color schemes
        color_index = int(t / 12) % len(color_schemes)
        colors = color_schemes[color_index]
        
        # Animation parameters
        rotation_angle = t * 0.5  # Rotation speed
        zoom_factor = 1.0 + 0.5 * math.sin(t * 0.3)  # Zoom oscillation
        offset_x = 0.3 * math.sin(t * 0.2)  # X drift
        offset_y = 0.3 * math.cos(t * 0.15)  # Y drift
        
        # Additional rotation for more complex motion
        secondary_rotation = t * 0.3
        
        # Pre-calculate transformation matrix components
        cos_main = fast_cos(rotation_angle)
        sin_main = fast_sin(rotation_angle)
        cos_sec = fast_cos(secondary_rotation)
        sin_sec = fast_sin(secondary_rotation)
        
        # Process each pixel (no clear_pixels to avoid flicker)
        for y in range(height):
            for x in range(width):
                # Convert to centered coordinates
                px = (x - cx) / zoom_factor
                py = (y - cy) / zoom_factor
                
                # Apply primary rotation
                rx1 = px * cos_main - py * sin_main
                ry1 = px * sin_main + py * cos_main
                
                # Apply secondary rotation (for more complex motion)
                rx2 = rx1 * cos_sec - ry1 * sin_sec * 0.3
                ry2 = rx1 * sin_sec * 0.3 + ry1 * cos_sec
                
                # Convert to texture coordinates (0-1 range)
                u = (rx2 / (width/2)) + 0.5 + offset_x
                v = (ry2 / (height/2)) + 0.5 + offset_y
                
                # Make texture repeat by using fractional part
                u = u - math.floor(u)
                v = v - math.floor(v)
                
                # Sample texture
                if texture_name == 'plasma':
                    texture_value = texture_func(u, v, t)
                    # Smooth color interpolation for plasma
                    color1, color2 = colors
                    final_color = (
                        int(color1[0] * (1 - texture_value) + color2[0] * texture_value),
                        int(color1[1] * (1 - texture_value) + color2[1] * texture_value),
                        int(color1[2] * (1 - texture_value) + color2[2] * texture_value)
                    )
                else:
                    texture_value = texture_func(u, v)
                    # Binary color selection for other textures
                    final_color = colors[texture_value] if texture_value else colors[0]
                
                # Add some brightness variation based on distance from center
                distance_from_center = math.sqrt((x - cx)**2 + (y - cy)**2) / (width/2)
                brightness_mod = 0.7 + 0.3 * (1.0 - distance_from_center)
                
                # Apply brightness modification
                final_color = (
                    int(final_color[0] * brightness_mod),
                    int(final_color[1] * brightness_mod),
                    int(final_color[2] * brightness_mod)
                )
                
                # Set pixel
                pixel_idx = pixel_map[y * width + x]
                pixels[pixel_idx] = final_color
        
        # Removed central highlight effect to avoid flashing white diamond
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.04)  # 25 FPS for smooth rotation
    
    log_module_finish("rotozoomer", frame_count=frame, duration=time.monotonic() - start_time)