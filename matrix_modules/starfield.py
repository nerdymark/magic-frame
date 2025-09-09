"""
Starfield Effect - 3D stars rushing toward the viewer.
Classic screensaver and demo effect with depth and perspective.
Creates the illusion of traveling through space at warp speed.
ULTRA-OPTIMIZED FOR MAXIMUM PERFORMANCE!
"""
import random
import time
import math
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, STARFIELD_MAX_FRAMES, CENTER_X, CENTER_Y, STARFIELD_NUM_STARS


def starfield(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=STARFIELD_MAX_FRAMES):
    """
    Generate 3D starfield effect with stars moving toward the viewer.
    ULTRA-OPTIMIZED VERSION - maximum performance!
    """
    log_module_start("starfield", max_frames=max_frames)
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
    
    # OPTIMIZED Star class
    class Star:
        def __init__(self):
            self.reset()
        
        def reset(self):
            # Random position in 3D space
            self.x = (random.random() - 0.5) * 100  # -50 to 50
            self.y = (random.random() - 0.5) * 100  # -50 to 50
            self.z = random.random() * 50 + 10      # 10 to 60 (distance)
            
        def update(self, speed):
            # Move star toward viewer
            self.z -= speed
            
            # Reset star if it's too close
            if self.z <= 0.1:
                self.reset()
        
        def project(self):
            # 3D to 2D projection with perspective
            if self.z > 0.1:  # Avoid division by zero
                # Perspective projection
                screen_x = cx + (self.x * 20) / self.z
                screen_y = cy + (self.y * 20) / self.z
                
                # Brightness based on distance - SIMPLIFIED!
                if self.z < 10:
                    brightness = 255  # Very bright when close
                elif self.z < 20:
                    brightness = 200  # Bright
                elif self.z < 30:
                    brightness = 150  # Medium
                else:
                    brightness = 100  # Dim when far
                
                return int(screen_x), int(screen_y), brightness
            
            return None, None, 0
    
    # Create star field - OPTIMIZED COUNT!
    num_stars = 35  # Further reduced for maximum speed
    stars = [Star() for _ in range(num_stars)]
    
    frame = 0
    base_speed = 1.2  # Fast base speed
    
    # Pre-calculate black for clearing
    black = (0, 0, 0)
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Simple speed variation
        current_speed = base_speed * (1.2 + 0.5 * ultra_sin(t * 0.5))
        
        # ULTRA-FAST pixel clearing
        for i in range(len(pixels)):
            pixels[i] = black
        
        # Update and draw each star - SIMPLIFIED!
        for star in stars:
            star.update(current_speed)
            screen_x, screen_y, brightness = star.project()
            
            if (screen_x is not None and 
                0 <= screen_x < width and 0 <= screen_y < height):
                
                # SIMPLE color based on speed
                if current_speed > base_speed * 1.4:  # Fast - bluish
                    color = (brightness - 50, brightness - 20, brightness)
                else:  # Normal - white
                    color = (brightness, brightness, brightness)
                
                # Single pixel per star - MAXIMUM SPEED!
                pixel_idx = pixel_map[screen_y * width + screen_x]
                pixels[pixel_idx] = color
                
                # Add cross pattern ONLY for very close stars
                if star.z < 5:
                    # Just 4 pixels in cross
                    half_bright = brightness // 2
                    cross_color = (half_bright, half_bright, half_bright)
                    
                    # Top
                    if screen_y > 0:
                        pixels[pixel_map[(screen_y - 1) * width + screen_x]] = cross_color
                    # Bottom
                    if screen_y < height - 1:
                        pixels[pixel_map[(screen_y + 1) * width + screen_x]] = cross_color
                    # Left
                    if screen_x > 0:
                        pixels[pixel_map[screen_y * width + (screen_x - 1)]] = cross_color
                    # Right
                    if screen_x < width - 1:
                        pixels[pixel_map[screen_y * width + (screen_x + 1)]] = cross_color
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.02)  # 50 FPS target
    
    log_module_finish("starfield", frame_count=frame, duration=time.monotonic() - start_time)