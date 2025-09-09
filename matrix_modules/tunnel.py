"""
Tunnel effect based on classic algorithm from lodev.org.
Creates 3D tunnel illusion with texture mapping and rainbow colors.
Optimized for LED matrix display.
"""
import math
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def tunnel(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate tunnel effect with smooth rainbow color transitions.
    Creates illusion of moving through a colorful 3D tunnel.
    """
    log_module_start("tunnel", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate distance and angle tables for tunnel transformation
    distance_table = []
    angle_table = []
    
    # Center of screen
    cx = width / 2.0
    cy = height / 2.0
    
    # Ratio for tunnel depth
    ratio = 32.0
    
    for y in range(height):
        row_dist = []
        row_angle = []
        for x in range(width):
            # Calculate distance from center
            dx = x - cx
            dy = y - cy
            dist_from_center = math.sqrt(dx * dx + dy * dy)
            
            # Avoid division by zero
            if dist_from_center < 0.5:
                dist_from_center = 0.5
            
            # Inverse distance for tunnel effect
            distance = int(ratio * 8.0 / dist_from_center) & 255
            
            # Calculate angle
            angle = int(math.atan2(dy, dx) * 128.0 / math.pi) & 255
            
            row_dist.append(distance)
            row_angle.append(angle)
        
        distance_table.append(row_dist)
        angle_table.append(row_angle)
    
    # Generate texture pattern (rings and segments for rainbow effect)
    TEXTURE_SIZE = 256
    texture = []
    for ty in range(TEXTURE_SIZE):
        row = []
        for tx in range(TEXTURE_SIZE):
            # Create ring pattern for smooth color transitions
            ring = (tx // 16) % 16
            segment = (ty // 16) % 16
            val = (ring * 16 + segment * 8) % 256
            row.append(val)
        texture.append(row)
    
    # Generate smooth rainbow palette
    def hsv_to_rgb(h, s, v):
        """Convert HSV to RGB for rainbow colors"""
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
    
    # Create smooth rainbow palette
    rainbow_palette = []
    for i in range(256):
        # Full spectrum rainbow
        hue = (i * 360 / 256)
        saturation = 0.9  # High saturation for vibrant colors
        value = 0.8 + 0.2 * math.sin(i * math.pi / 128)  # Subtle brightness variation
        r, g, b = hsv_to_rgb(hue, saturation, value)
        rainbow_palette.append((r, g, b))
    
    frame = 0
    
    while frame < max_frames:
        current_time = time.monotonic() - start_time
        
        # Animation parameters
        # Move through tunnel
        shift_distance = int(current_time * 40.0) & 255
        # Rotate around tunnel with rainbow cycling
        shift_angle = int(current_time * 30.0) & 255
        # Color cycling for rainbow effect
        color_shift = int(current_time * 60.0) & 255
        
        # Add smooth wobble effect
        wobble_x = math.sin(current_time * 1.5) * 8
        wobble_y = math.cos(current_time * 1.2) * 8
        
        # Pulsing effect for tunnel
        pulse = 0.9 + 0.1 * math.sin(current_time * 3.0)
        
        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                # Get pre-calculated distance and angle
                dist = distance_table[y][x]
                angle = angle_table[y][x]
                
                # Apply animation shifts
                texture_x = (dist + shift_distance) & 255
                texture_y = (angle + shift_angle) & 255
                
                # Add wobble to center pixels
                if abs(x - width/2) < 6 and abs(y - height/2) < 6:
                    wobble_factor = 1.0 - (abs(x - width/2) + abs(y - height/2)) / 12.0
                    texture_x = (texture_x + int(wobble_x * wobble_factor)) & 255
                    texture_y = (texture_y + int(wobble_y * wobble_factor)) & 255
                
                # Get texture value
                tex_val = texture[texture_y][texture_x]
                
                # Calculate rainbow color with smooth transitions
                # Combine texture value with color shift for animated rainbow
                rainbow_index = (tex_val + color_shift + int(dist * 0.5)) & 255
                
                # Apply distance-based shading for depth
                edge_dist = math.sqrt((x - width/2)**2 + (y - height/2)**2) / (width/2)
                shade = max(0.4, 1.0 - edge_dist * 0.4) * pulse
                
                # Get rainbow color and apply shading
                base_color = rainbow_palette[rainbow_index]
                color = (
                    int(base_color[0] * shade),
                    int(base_color[1] * shade),
                    int(base_color[2] * shade)
                )
                
                # Add sparkle effect on certain pixels
                if (frame + x + y) % 60 == 0 and tex_val > 128:
                    sparkle = 0.3 * math.sin(current_time * 10.0 + x + y)
                    color = (
                        min(255, int(color[0] * (1 + sparkle))),
                        min(255, int(color[1] * (1 + sparkle))),
                        min(255, int(color[2] * (1 + sparkle)))
                    )
                
                # Set pixel
                pixels[pixel_map[pixel_idx]] = color
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        # Control frame rate
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.02)  # 50 FPS for smooth rainbow movement
    
    log_module_finish("tunnel", frame_count=frame, duration=time.monotonic() - start_time)