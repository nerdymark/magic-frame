"""
Lava Lamp Effect - Smooth, hypnotic blobs rising and falling.
Classic 1960s psychedelic lava lamp with glowing blobs that merge and split.
Creates a relaxing, meditative atmosphere with warm colors.
"""
import time
import random
import math
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish, ultra_sin, ultra_cos, ultra_sqrt
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY

def lava_lamp(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=1500):
    """
    Generate lava lamp effect with rising and falling blobs.
    Smooth, relaxing motion with warm psychedelic colors.
    """
    log_module_start("lava_lamp", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Lava blob class
    class LavaBlob:
        def __init__(self):
            self.x = random.uniform(2, width - 2)
            self.y = random.uniform(2, height - 2)
            self.radius = random.uniform(1.5, 2.5)  # SMALLER blobs
            self.dy = random.uniform(-0.15, 0.15)  # SLOWER vertical speed for smoothness
            self.dx = random.uniform(-0.05, 0.05)  # Very gentle horizontal drift
            self.phase = random.uniform(0, math.pi * 2)  # For undulation
            self.temp = random.uniform(0.7, 1.0)  # "Temperature" affects color
            self.rising = random.choice([True, False])  # Direction
            
        def update(self, t):
            # Undulating movement like real lava lamp
            self.phase += 0.05
            
            # Temperature changes affect buoyancy - MUCH SMOOTHER
            if self.rising:
                self.dy -= 0.003  # Very gentle upward acceleration
                self.temp = min(1.0, self.temp + 0.002)  # Slow heating
                if self.y < 4 or self.dy < -0.2:
                    self.rising = False  # Start cooling/falling
            else:
                self.dy += 0.002  # Very gentle downward acceleration
                self.temp = max(0.5, self.temp - 0.001)  # Slow cooling
                if self.y > height - 4 or self.dy > 0.15:
                    self.rising = True  # Start heating/rising
            
            # Apply movement with very subtle horizontal wobble
            self.y += self.dy
            self.x += self.dx + ultra_sin(self.phase) * 0.05  # Half the wobble
            
            # Boundary bouncing with damping
            if self.x < self.radius or self.x > width - self.radius:
                self.dx *= -0.8
                self.x = max(self.radius, min(width - self.radius, self.x))
            
            if self.y < self.radius:
                self.y = self.radius
                self.dy *= -0.5
                self.rising = False
            elif self.y > height - self.radius:
                self.y = height - self.radius
                self.dy *= -0.5
                self.rising = True
            
            # Size pulsing based on temperature - SMALLER
            self.radius = 1.8 + ultra_sin(self.phase * 0.5) * 0.2 + self.temp * 0.3
            
        def get_color(self):
            # Warm lava colors based on temperature
            if self.temp > 0.85:  # Very hot - bright orange/yellow
                r = 255
                g = int(180 + 75 * (self.temp - 0.85) / 0.15)
                b = int(50 * (1 - self.temp))
            elif self.temp > 0.7:  # Hot - orange
                r = 255
                g = int(120 + 60 * (self.temp - 0.7) / 0.15)
                b = int(30 + 20 * (1 - self.temp))
            else:  # Cooler - deep red/purple
                r = int(180 + 75 * self.temp)
                g = int(50 + 70 * self.temp)
                b = int(80 * (1 - self.temp) + 20)
            
            return (r, g, b)
    
    # Create initial blobs
    blobs = []
    for _ in range(7):  # More smaller blobs for better effect
        blob = LavaBlob()
        # Start some at top, some at bottom
        if random.random() > 0.5:
            blob.y = random.uniform(2, 5)
            blob.rising = False
        else:
            blob.y = random.uniform(height - 5, height - 2)
            blob.rising = True
        blobs.append(blob)
    
    # Background "heat" gradient
    def get_background_heat(y, t):
        # Subtle animated gradient
        heat_wave = ultra_sin(y * 0.3 + t * 0.5) * 0.1
        base_heat = (height - y) / height * 0.3  # Hotter at bottom
        return base_heat + heat_wave
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Update blobs
        for blob in blobs:
            blob.update(t)
        
        # Check for blob merging/splitting (simplified for performance)
        if frame % 30 == 0:  # Check every 30 frames
            for i, blob1 in enumerate(blobs):
                for j, blob2 in enumerate(blobs[i+1:], i+1):
                    dist = ultra_sqrt((blob1.x - blob2.x)**2 + (blob1.y - blob2.y)**2)
                    
                    # Merge if very close and similar temperature
                    if dist < 1.5 and abs(blob1.temp - blob2.temp) < 0.2 and len(blobs) > 4:
                        # Merge into blob1
                        blob1.radius = min(3, ultra_sqrt(blob1.radius**2 + blob2.radius**2))  # Smaller max size
                        blob1.temp = (blob1.temp + blob2.temp) / 2
                        blobs.remove(blob2)
                        break
            
            # Occasionally split large blobs
            for blob in blobs:
                if blob.radius > 2.5 and random.random() < 0.1 and len(blobs) < 10:
                    # Split into two
                    new_blob = LavaBlob()
                    new_blob.x = blob.x + random.uniform(-2, 2)
                    new_blob.y = blob.y + random.uniform(-2, 2)
                    new_blob.radius = blob.radius * 0.7
                    new_blob.temp = blob.temp
                    new_blob.rising = blob.rising
                    blob.radius *= 0.7
                    blobs.append(new_blob)
                    break
        
        # Render the lava lamp
        for y in range(height):
            for x in range(width):
                # Start with dark background with heat gradient
                heat = get_background_heat(y, t)
                r = int(20 + heat * 30)  # Dark red background
                g = int(5 + heat * 10)
                b = int(10 + heat * 5)
                
                # Add blob influences (metaball-style)
                total_influence = 0
                blob_r = blob_g = blob_b = 0
                
                for blob in blobs:
                    dx = x - blob.x
                    dy = y - blob.y
                    dist_sq = dx*dx + dy*dy
                    
                    if dist_sq < blob.radius * blob.radius * 6:  # Wider influence for smaller blobs
                        # Metaball influence calculation - adjusted for smaller blobs
                        influence = (blob.radius * blob.radius * 1.5) / max(0.5, dist_sq)
                        
                        if influence > 0.3:  # Threshold for visible blob
                            blob_color = blob.get_color()
                            weight = min(1.0, influence)
                            
                            blob_r += blob_color[0] * weight
                            blob_g += blob_color[1] * weight
                            blob_b += blob_color[2] * weight
                            total_influence += weight
                
                # Combine background and blobs
                if total_influence > 0.8:  # Higher threshold for smaller blobs
                    # Normalize and apply blob colors
                    final_r = min(255, int(blob_r / max(1, total_influence)))
                    final_g = min(255, int(blob_g / max(1, total_influence)))
                    final_b = min(255, int(blob_b / max(1, total_influence)))
                    
                    # Add glow effect for hot blobs
                    if total_influence > 1.2:
                        glow = (total_influence - 1.2) * 0.3
                        final_r = min(255, int(final_r * (1 + glow)))
                        final_g = min(255, int(final_g * (1 + glow)))
                        final_b = min(255, int(final_b * (1 + glow * 0.5)))
                else:
                    # Background with subtle blob influence
                    influence_factor = total_influence * 2
                    final_r = int(r + (blob_r - r) * influence_factor)
                    final_g = int(g + (blob_g - g) * influence_factor)
                    final_b = int(b + (blob_b - b) * influence_factor)
                
                pixel_idx = pixel_map[y * width + x]
                pixels[pixel_idx] = (final_r, final_g, final_b)
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.03)  # 33 FPS for smoother motion
    
    log_module_finish("lava_lamp", frame_count=frame, duration=time.monotonic() - start_time)