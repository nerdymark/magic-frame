"""
Vector Balls (Metaballs) - Classic demoscene organic blob effects.
Smooth organic shapes that merge and separate based on distance fields.
Creates fluid, liquid-like animations with gradient shading.
ENHANCED FOR MAXIMUM VISIBILITY!
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, VECTOR_BALLS_MAX_FRAMES, CENTER_X, CENTER_Y


def vector_balls(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=VECTOR_BALLS_MAX_FRAMES):
    """
    Generate vector balls (metaballs) effect with organic blob shapes.
    ENHANCED VERSION - much more visible and clear!
    """
    log_module_start("vector_balls", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Simple Metaball class - using screen coordinates directly!
    class MetaBall:
        def __init__(self, start_x, start_y, radius):
            self.base_x = start_x
            self.base_y = start_y
            self.radius = radius
            self.angle = 0
            self.orbit_radius = 3 + radius / 4  # Orbit distance based on size
            
        def get_position(self, t):
            # Simple circular motion around base position
            self.angle = t * 0.5  # Slow rotation
            x = self.base_x + ultra_cos(self.angle) * self.orbit_radius
            y = self.base_y + ultra_sin(self.angle) * self.orbit_radius
            return x, y
    
    # Create 3-4 BIG, VISIBLE metaballs positioned on screen
    metaballs = [
        MetaBall(width // 2, height // 2, 5),      # Large center ball
        MetaBall(width // 3, height // 3, 4),      # Top-left ball
        MetaBall(2 * width // 3, 2 * height // 3, 4),  # Bottom-right ball
        MetaBall(2 * width // 3, height // 3, 3.5),    # Top-right ball
    ]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Clear all pixels first
        for i in range(len(pixels)):
            pixels[i] = (0, 0, 0)
        
        # Calculate metaball field for each pixel
        for y in range(height):
            for x in range(width):
                # Calculate total influence from all metaballs
                total_influence = 0
                
                for ball in metaballs:
                    ball_x, ball_y = ball.get_position(t)
                    
                    # Distance from this pixel to ball center
                    dx = x - ball_x
                    dy = y - ball_y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    # Metaball influence formula - STRONGER for visibility!
                    if distance < 0.1:
                        influence = 10.0  # Very high at center
                    else:
                        # Stronger influence with larger radius effect
                        influence = (ball.radius * ball.radius) / (distance * distance)
                    
                    total_influence += influence
                
                # Convert influence to bright, visible colors!
                if total_influence > 1.0:  # Inside a metaball - BRIGHT!
                    # Bright white core
                    intensity = min(255, int(200 + total_influence * 20))
                    color = (intensity, intensity, intensity)
                elif total_influence > 0.5:  # Edge of metaball - colored
                    # Colorful edge based on position and time
                    hue_shift = t * 30 + x * 10 + y * 10
                    r = int(128 + 127 * ultra_sin(hue_shift * 0.01))
                    g = int(128 + 127 * ultra_sin(hue_shift * 0.011 + 2))
                    b = int(128 + 127 * ultra_sin(hue_shift * 0.012 + 4))
                    
                    # Scale by influence
                    factor = (total_influence - 0.5) * 2
                    color = (
                        int(r * factor),
                        int(g * factor),
                        int(b * factor)
                    )
                elif total_influence > 0.2:  # Outer glow
                    # Dim colored glow
                    intensity = int(total_influence * 100)
                    color = (intensity // 2, intensity // 3, intensity)
                else:
                    # Background
                    color = (0, 0, 5)  # Very dark blue background
                
                pixel_idx = pixel_map[y * width + x]
                pixels[pixel_idx] = color
        
        # Add some visible debug points at metaball centers
        for ball in metaballs:
            ball_x, ball_y = ball.get_position(t)
            center_x = int(ball_x)
            center_y = int(ball_y)
            
            # Draw bright center point if on screen
            if 0 <= center_x < width and 0 <= center_y < height:
                pixel_idx = pixel_map[center_y * width + center_x]
                pixels[pixel_idx] = (255, 0, 0)  # Red center markers
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.04)  # 25 FPS for smooth motion
    
    log_module_finish("vector_balls", frame_count=frame, duration=time.monotonic() - start_time)