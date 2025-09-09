"""
Lens Flare Effect - Bright light source with radiating beams and artifacts.
Classic 90s demo effect with bright central light and optical artifacts.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, LENS_FLARE_MAX_FRAMES, CENTER_X, CENTER_Y


def lens_flare(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=LENS_FLARE_MAX_FRAMES):
    """
    Generate lens flare effect with moving light source and artifacts.
    """
    log_module_start("lens_flare", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate coordinate arrays for performance
    coord_x = [x for x in range(width)]
    coord_y = [y for y in range(height)]
    
    # Sine lookup table for smooth animation
    SINE_SIZE = 256
    sine_lut = [math.sin(i * 2 * math.pi / SINE_SIZE) for i in range(SINE_SIZE)]
    cos_lut = [math.cos(i * 2 * math.pi / SINE_SIZE) for i in range(SINE_SIZE)]
    
    def fast_sin(angle):
        return sine_lut[int(angle * SINE_SIZE / (2 * math.pi)) % SINE_SIZE]
    
    def fast_cos(angle):
        return cos_lut[int(angle * SINE_SIZE / (2 * math.pi)) % SINE_SIZE]
    
    # Pre-calculate ray directions for smooth rays
    RAY_COUNT = 8
    ray_angles = [i * 2 * math.pi / RAY_COUNT for i in range(RAY_COUNT)]
    
    # Frame buffer for temporal smoothing
    previous_frame = [(0, 0, 0) for _ in range(len(pixels))]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Smooth moving light source using lookup tables
        light_x = CENTER_X + 6 * fast_sin(t * 0.3)
        light_y = CENTER_Y + 4 * fast_cos(t * 0.5)
        
        # Start with black frame
        current_frame = [(0, 0, 0) for _ in range(len(pixels))]
        
        # Draw main light source with pre-calculated distances
        light_radius = 8.0
        for y in range(int(max(0, light_y - light_radius)), int(min(height, light_y + light_radius + 1))):
            for x in range(int(max(0, light_x - light_radius)), int(min(width, light_x + light_radius + 1))):
                dx = x - light_x
                dy = y - light_y
                distance_sq = dx*dx + dy*dy
                
                if distance_sq < light_radius * light_radius:
                    # Bright core with smooth falloff
                    distance = math.sqrt(distance_sq)
                    intensity = max(0, 1 - distance / light_radius)
                    brightness = int(255 * intensity * intensity)
                    
                    pixel_idx = pixel_map[y * width + x]
                    current_frame[pixel_idx] = (brightness, brightness, brightness)
        
        # Draw smooth rays using pre-calculated directions
        ray_length = 12
        ray_base_intensity = 0.8
        
        for angle in ray_angles:
            cos_a = fast_cos(angle + t * 0.5)  # Slowly rotating rays
            sin_a = fast_sin(angle + t * 0.5)
            
            for step in range(1, ray_length):
                ray_x = light_x + step * cos_a
                ray_y = light_y + step * sin_a
                
                if 0 <= ray_x < width and 0 <= ray_y < height:
                    # Ray intensity falls off with distance
                    intensity = ray_base_intensity * (1 - step / ray_length)
                    ray_brightness = int(255 * intensity * 0.4)
                    
                    pixel_idx = pixel_map[int(ray_y) * width + int(ray_x)]
                    current = current_frame[pixel_idx]
                    current_frame[pixel_idx] = (
                        min(255, current[0] + ray_brightness),
                        min(255, current[1] + ray_brightness // 2),
                        current[2]
                    )
        
        # Lens artifacts with smoother positioning
        artifact_colors = [(200, 80, 80), (80, 200, 80), (80, 80, 200)]
        for i in range(3):
            artifact_factor = 0.4 + i * 0.2
            artifact_x = CENTER_X + (light_x - CENTER_X) * artifact_factor
            artifact_y = CENTER_Y + (light_y - CENTER_Y) * artifact_factor
            
            artifact_size = 2.5 + i * 0.5
            
            for y in range(int(artifact_y - artifact_size), int(artifact_y + artifact_size + 1)):
                for x in range(int(artifact_x - artifact_size), int(artifact_x + artifact_size + 1)):
                    if 0 <= x < width and 0 <= y < height:
                        dx = x - artifact_x
                        dy = y - artifact_y
                        distance_sq = dx*dx + dy*dy
                        
                        if distance_sq <= artifact_size*artifact_size:
                            # Smooth artifact with distance falloff
                            distance = math.sqrt(distance_sq)
                            intensity = max(0, 1 - distance / artifact_size)
                            
                            pixel_idx = pixel_map[y * width + x]
                            current = current_frame[pixel_idx]
                            artifact_color = artifact_colors[i]
                            
                            blend_factor = intensity * 0.4
                            current_frame[pixel_idx] = (
                                min(255, int(current[0] + artifact_color[0] * blend_factor)),
                                min(255, int(current[1] + artifact_color[1] * blend_factor)),
                                min(255, int(current[2] + artifact_color[2] * blend_factor))
                            )
        
        # Temporal smoothing to reduce flickering
        smoothing_factor = 0.15  # How much to blend with previous frame
        for i in range(len(pixels)):
            prev = previous_frame[i]
            curr = current_frame[i]
            
            # Blend current frame with previous frame
            pixels[i] = (
                int(prev[0] * smoothing_factor + curr[0] * (1 - smoothing_factor)),
                int(prev[1] * smoothing_factor + curr[1] * (1 - smoothing_factor)),
                int(prev[2] * smoothing_factor + curr[2] * (1 - smoothing_factor))
            )
            
            # Store current frame for next iteration
            previous_frame[i] = pixels[i]
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.06)  # 16-17 FPS for smoother, less flickery animation
    
    log_module_finish("lens_flare", frame_count=frame, duration=time.monotonic() - start_time)