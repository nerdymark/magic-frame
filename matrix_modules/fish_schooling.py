"""
Fish schooling animation implementing boids algorithm.
Features separation, alignment, and cohesion behaviors for realistic schooling.
"""
import math
import random
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def fish_schooling(pixels, width=WIDTH, height=HEIGHT, delay=0.08, max_frames=1000):
    """
    Simulate fish schooling behavior using boids algorithm.
    """
    log_module_start("fish_schooling", max_frames=max_frames)
    start_time = time.monotonic()
    
    class Fish:
        def __init__(self, x, y):
            self.x = float(x)
            self.y = float(y)
            self.vx = random.uniform(-0.5, 0.5)  # Slower initial velocities
            self.vy = random.uniform(-0.5, 0.5)
            self.max_speed = random.uniform(0.4, 0.7)  # Much slower max speeds
            self.perception_radius = random.uniform(2.5, 3.5)
            self.color_hue = random.uniform(0, 1)  # For color variation
            self.size = random.choice([1, 2])  # Some fish are slightly bigger
            self.trail = []  # Store trail positions for fading effect
            
            # Normalize initial velocity (slower)
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > 0:
                self.vx = (self.vx / speed) * self.max_speed * 0.3
                self.vy = (self.vy / speed) * self.max_speed * 0.3
        
        def get_color(self):
            # Enhanced fish colors with more variety
            if self.color_hue < 0.5:
                # Deep blue fish
                r = int(10 + self.color_hue * 40)
                g = int(80 + self.color_hue * 120) 
                b = int(180 + self.color_hue * 75)
            elif self.color_hue < 0.8:
                # Teal/cyan fish
                r = int(20 + self.color_hue * 60)
                g = int(150 + self.color_hue * 80)
                b = int(120 + self.color_hue * 90)
            else:
                # Tropical accent fish (orange/yellow)
                r = int(220 + self.color_hue * 35)
                g = int(140 + self.color_hue * 70)
                b = int(30 + self.color_hue * 40)
            
            return (min(255, r), min(255, g), min(255, b))
        
        def separation(self, neighbors):
            # Avoid crowding - steer away from nearby fish (slower)
            steer_x = 0
            steer_y = 0
            count = 0
            
            for other in neighbors:
                distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                if distance > 0 and distance < 1.5:  # Close neighbors
                    # Calculate steering force away from neighbor
                    diff_x = self.x - other.x
                    diff_y = self.y - other.y
                    # Weight by distance (closer = stronger repulsion)
                    diff_x /= distance
                    diff_y /= distance
                    steer_x += diff_x
                    steer_y += diff_y
                    count += 1
            
            if count > 0:
                steer_x /= count
                steer_y /= count
                # Normalize and scale (slower response)
                length = math.sqrt(steer_x**2 + steer_y**2)
                if length > 0:
                    steer_x = (steer_x / length) * 0.2  # Reduced from 0.5
                    steer_y = (steer_y / length) * 0.2
            
            return steer_x, steer_y
        
        def alignment(self, neighbors):
            # Align with average heading of neighbors
            avg_vx = 0
            avg_vy = 0
            count = 0
            
            for other in neighbors:
                distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                if distance > 0 and distance < self.perception_radius:
                    avg_vx += other.vx
                    avg_vy += other.vy
                    count += 1
            
            if count > 0:
                avg_vx /= count
                avg_vy /= count
                
                # Normalize and scale (slower alignment)
                length = math.sqrt(avg_vx**2 + avg_vy**2)
                if length > 0:
                    avg_vx = (avg_vx / length) * 0.15  # Reduced from 0.3
                    avg_vy = (avg_vy / length) * 0.15
                
                return avg_vx, avg_vy
            
            return 0, 0
        
        def cohesion(self, neighbors):
            # Steer towards average position of neighbors
            center_x = 0
            center_y = 0
            count = 0
            
            for other in neighbors:
                distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                if distance > 0 and distance < self.perception_radius:
                    center_x += other.x
                    center_y += other.y
                    count += 1
            
            if count > 0:
                center_x /= count
                center_y /= count
                
                # Steer towards center
                steer_x = center_x - self.x
                steer_y = center_y - self.y
                
                # Normalize and scale (slower cohesion)
                length = math.sqrt(steer_x**2 + steer_y**2)
                if length > 0:
                    steer_x = (steer_x / length) * 0.1  # Reduced from 0.2
                    steer_y = (steer_y / length) * 0.1
                
                return steer_x, steer_y
            
            return 0, 0
        
        def avoid_edges(self):
            # Gentle edge avoidance to keep school visible
            steer_x = 0
            steer_y = 0
            edge_distance = 2.0
            
            if self.x < edge_distance:
                steer_x = 0.2  # Gentler edge avoidance
            elif self.x > width - edge_distance:
                steer_x = -0.2
                
            if self.y < edge_distance:
                steer_y = 0.2
            elif self.y > height - edge_distance:
                steer_y = -0.2
            
            return steer_x, steer_y
        
        def update(self, school):
            # Store current position in trail
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > 4:  # Keep 4 trail positions for smoother effect
                self.trail.pop(0)
            
            # Get neighbors within perception
            neighbors = [fish for fish in school if fish != self]
            
            # Apply boids rules (all reduced for underwater feel)
            sep_x, sep_y = self.separation(neighbors)
            align_x, align_y = self.alignment(neighbors)  
            coh_x, coh_y = self.cohesion(neighbors)
            edge_x, edge_y = self.avoid_edges()
            
            # Combine forces with damping for underwater feel
            self.vx += (sep_x + align_x + coh_x + edge_x) * 0.8
            self.vy += (sep_y + align_y + coh_y + edge_y) * 0.8
            
            # Apply underwater drag
            self.vx *= 0.95
            self.vy *= 0.95
            
            # Limit speed
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > self.max_speed:
                self.vx = (self.vx / speed) * self.max_speed
                self.vy = (self.vy / speed) * self.max_speed
            
            # Update position
            self.x += self.vx
            self.y += self.vy
            
            # Wrap around edges with some randomness (gentler)
            if self.x < 0:
                self.x = width - 1
                self.vx += random.uniform(-0.1, 0.1)
            elif self.x >= width:
                self.x = 0
                self.vx += random.uniform(-0.1, 0.1)
                
            if self.y < 0:
                self.y = height - 1
                self.vy += random.uniform(-0.1, 0.1)
            elif self.y >= height:
                self.y = 0
                self.vy += random.uniform(-0.1, 0.1)
    
    # Create school of fish
    num_fish = random.randint(15, 22)
    school = []
    
    # Start fish in a loose cluster
    center_x = width // 2
    center_y = height // 2
    
    for _ in range(num_fish):
        # Random position around center with some spread
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(1, 4)
        x = center_x + math.cos(angle) * distance
        y = center_y + math.sin(angle) * distance
        
        # Keep in bounds
        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))
        
        school.append(Fish(x, y))
    
    frame = 0
    # Initialize background for smoother fading
    background = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    
    while frame < max_frames:
        # Fade background gradually instead of clearing
        for y in range(height):
            for x in range(width):
                r, g, b = background[y][x]
                # Slower fade for underwater effect
                background[y][x] = (max(0, r - 12), max(0, g - 12), max(0, b - 12))
                
                # Apply faded background
                set_pixel(pixels, x, y, background[y][x], auto_write=False)
        
        # Update all fish
        for fish in school:
            fish.update(school)
        
        # Draw fish with enhanced visual effects
        for fish in school:
            color = fish.get_color()
            
            # Draw enhanced trails with background blending
            for i, (trail_x, trail_y) in enumerate(fish.trail):
                if 0 <= trail_x < width and 0 <= trail_y < height:
                    # Calculate fade intensity (newest = brightest)
                    fade_factor = (i + 1) / len(fish.trail)
                    
                    if i == len(fish.trail) - 1:  # Current position (brightest)
                        # Enhanced current position with slight glow
                        enhanced_color = (
                            min(255, int(color[0] * 1.1)),
                            min(255, int(color[1] * 1.1)),
                            min(255, int(color[2] * 1.1))
                        )
                        background[trail_y][trail_x] = enhanced_color
                    else:  # Fading trail positions
                        trail_color = (
                            int(color[0] * fade_factor * 0.5),
                            int(color[1] * fade_factor * 0.5), 
                            int(color[2] * fade_factor * 0.5)
                        )
                        # Blend with existing background
                        old_r, old_g, old_b = background[trail_y][trail_x]
                        background[trail_y][trail_x] = (
                            min(255, old_r + trail_color[0]),
                            min(255, old_g + trail_color[1]),
                            min(255, old_b + trail_color[2])
                        )
                    
                    set_pixel(pixels, trail_x, trail_y, background[trail_y][trail_x], auto_write=False)
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
    
    duration = time.monotonic() - start_time
    log_module_finish("fish_schooling", frame_count=frame, duration=duration)