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
    Optimized for low memory usage.
    """
    log_module_start("tunnel", max_frames=max_frames)
    start_time = time.monotonic()

    # Center of screen
    cx = width / 2.0
    cy = height / 2.0

    # Ratio for tunnel depth
    ratio = 32.0

    # Helper functions for on-the-fly calculation
    def get_distance_angle(x, y):
        """Calculate distance and angle on-the-fly to save memory"""
        dx = x - cx
        dy = y - cy
        dist_from_center = math.sqrt(dx * dx + dy * dy)
        if dist_from_center < 0.5:
            dist_from_center = 0.5
        distance = int(ratio * 8.0 / dist_from_center) & 255
        angle = int(math.atan2(dy, dx) * 128.0 / math.pi) & 255
        return distance, angle

    def get_texture_value(tx, ty):
        """Calculate texture value on-the-fly"""
        ring = (tx // 16) % 16
        segment = (ty // 16) % 16
        return (ring * 16 + segment * 8) % 256

    def hsv_to_rgb_fast(h):
        """Fast HSV to RGB for rainbow colors - simplified for memory"""
        h = (h * 360 // 256) % 360
        # Simplified color calculation
        if h < 60:
            return (204, int(h * 204 / 60), 0)
        elif h < 120:
            return (int((120 - h) * 204 / 60), 204, 0)
        elif h < 180:
            return (0, 204, int((h - 120) * 204 / 60))
        elif h < 240:
            return (0, int((240 - h) * 204 / 60), 204)
        elif h < 300:
            return (int((h - 240) * 204 / 60), 0, 204)
        else:
            return (204, 0, int((360 - h) * 204 / 60))
    
    frame = 0

    while frame < max_frames:
        current_time = time.monotonic() - start_time

        # Animation parameters
        shift_distance = int(current_time * 40.0) & 255
        shift_angle = int(current_time * 30.0) & 255
        color_shift = int(current_time * 60.0) & 255
        wobble_x = math.sin(current_time * 1.5) * 8
        wobble_y = math.cos(current_time * 1.2) * 8
        pulse = 0.9 + 0.1 * math.sin(current_time * 3.0)

        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                # Calculate distance and angle on-the-fly
                dist, angle = get_distance_angle(x, y)

                # Apply animation shifts
                texture_x = (dist + shift_distance) & 255
                texture_y = (angle + shift_angle) & 255

                # Add wobble to center pixels
                if abs(x - cx) < 6 and abs(y - cy) < 6:
                    wobble_factor = 1.0 - (abs(x - cx) + abs(y - cy)) / 12.0
                    texture_x = (texture_x + int(wobble_x * wobble_factor)) & 255
                    texture_y = (texture_y + int(wobble_y * wobble_factor)) & 255

                # Get texture value on-the-fly
                tex_val = get_texture_value(texture_x, texture_y)

                # Calculate rainbow color index
                rainbow_index = (tex_val + color_shift + int(dist * 0.5)) & 255

                # Apply distance-based shading
                edge_dist = math.sqrt((x - cx)**2 + (y - cy)**2) / (width/2)
                shade = max(0.4, 1.0 - edge_dist * 0.4) * pulse

                # Get rainbow color and apply shading
                base_color = hsv_to_rgb_fast(rainbow_index)
                color = (
                    int(base_color[0] * shade),
                    int(base_color[1] * shade),
                    int(base_color[2] * shade)
                )

                # Serpentine LED mapping on-the-fly
                if y % 2 == 0:
                    led_index = y * width + (width - 1 - x)
                else:
                    led_index = y * width + x

                # Set pixel
                pixels[led_index] = color
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        # Control frame rate
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.02)  # 50 FPS for smooth rainbow movement
    
    log_module_finish("tunnel", frame_count=frame, duration=time.monotonic() - start_time)