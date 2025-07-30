"""
Search Light animation - Three circular searchlights hunt for a hidden 2x2 target block.
When found, the target changes color and searchlights lock onto it.
When all three lights find it, the screen fills with a flashing rainbow pattern.
"""
import math
import random
import time
from matrix_modules.utils import set_pixel


def search_light(pixels, width, height, delay=0.05, max_cycles=5):
    """
    Display searchlights hunting for a hidden target block.
    """
    
    class Target:
        def __init__(self):
            self.found_by = set()  # Track which searchlights have found it
            self.color_index = 0
            self.colors = [
                (255, 0, 0),    # Red
                (0, 255, 0),    # Green
                (0, 0, 255),    # Blue
                (255, 255, 0),  # Yellow
                (255, 0, 255),  # Magenta
                (0, 255, 255),  # Cyan
            ]
            self.reset_position()
        
        def reset_position(self):
            # Place 2x2 block with room for full block
            self.x = random.randint(0, width - 2)
            self.y = random.randint(0, height - 2)
            self.found_by.clear()
        
        def get_positions(self):
            """Return all 4 positions of the 2x2 block"""
            return [
                (self.x, self.y),
                (self.x + 1, self.y),
                (self.x, self.y + 1),
                (self.x + 1, self.y + 1)
            ]
        
        def is_found_by_all(self, num_searchlights):
            return len(self.found_by) >= num_searchlights
        
        def change_color(self):
            self.color_index = (self.color_index + 1) % len(self.colors)
        
        def get_color(self):
            return self.colors[self.color_index]
    
    class Searchlight:
        def __init__(self, light_id, start_x, start_y, color):
            self.id = light_id
            self.x = float(start_x)
            self.y = float(start_y)
            self.color = color
            self.radius = 2.5
            self.speed = random.uniform(0.3, 0.6)
            self.direction = random.uniform(0, 2 * math.pi)
            self.direction_change_timer = 0
            self.found_target = False
            self.locked_target = None
        
        def update(self, target):
            if self.found_target and self.locked_target:
                # Stay locked on target
                target_center_x = self.locked_target.x + 0.5
                target_center_y = self.locked_target.y + 0.5
                self.x = target_center_x
                self.y = target_center_y
                return
            
            # Normal movement pattern
            self.direction_change_timer += 1
            
            # Occasionally change direction
            if self.direction_change_timer > random.randint(30, 80):
                self.direction += random.uniform(-0.8, 0.8)
                self.direction_change_timer = 0
            
            # Move in current direction
            dx = math.cos(self.direction) * self.speed
            dy = math.sin(self.direction) * self.speed
            
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Bounce off walls
            if new_x < self.radius or new_x >= width - self.radius:
                self.direction = math.pi - self.direction
                new_x = max(self.radius, min(width - self.radius - 1, new_x))
            
            if new_y < self.radius or new_y >= height - self.radius:
                self.direction = -self.direction
                new_y = max(self.radius, min(height - self.radius - 1, new_y))
            
            self.x = new_x
            self.y = new_y
            
            # Check if we found the target
            self.check_target_collision(target)
        
        def check_target_collision(self, target):
            # Check if searchlight overlaps with any part of the 2x2 target
            for tx, ty in target.get_positions():
                distance = math.sqrt((self.x - tx)**2 + (self.y - ty)**2)
                if distance <= self.radius:
                    if self.id not in target.found_by:
                        target.found_by.add(self.id)
                        target.change_color()
                        self.found_target = True
                        self.locked_target = target
                    return True
            return False
        
        def draw_circle(self, background):
            # Draw circular searchlight
            center_x, center_y = int(self.x), int(self.y)
            
            for y in range(max(0, center_y - int(self.radius) - 1), 
                          min(height, center_y + int(self.radius) + 2)):
                for x in range(max(0, center_x - int(self.radius) - 1), 
                              min(width, center_x + int(self.radius) + 2)):
                    distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
                    
                    if distance <= self.radius:
                        # Calculate intensity based on distance from center
                        intensity = max(0, 1.0 - (distance / self.radius))
                        
                        # Apply color with intensity
                        old_r, old_g, old_b = background[y][x]
                        new_r = min(255, old_r + int(self.color[0] * intensity * 0.6))
                        new_g = min(255, old_g + int(self.color[1] * intensity * 0.6))
                        new_b = min(255, old_b + int(self.color[2] * intensity * 0.6))
                        background[y][x] = (new_r, new_g, new_b)
    
    def growing_rainbow_block(pixels, width, height, target, duration=4.0):
        """Animate the target block growing to fill screen with rainbow pattern"""
        start_time = time.monotonic()
        rainbow_colors = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0),
            (0, 255, 0), (0, 255, 127), (0, 255, 255), (0, 127, 255),
            (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127)
        ]
        
        # Calculate center of target block
        center_x = target.x + 0.5
        center_y = target.y + 0.5
        
        # Maximum distance from center to any corner of screen
        max_distance = max(
            math.sqrt(center_x**2 + center_y**2),
            math.sqrt((width - center_x)**2 + center_y**2),
            math.sqrt(center_x**2 + (height - center_y)**2),
            math.sqrt((width - center_x)**2 + (height - center_y)**2)
        )
        
        while time.monotonic() - start_time < duration:
            elapsed = time.monotonic() - start_time
            progress = min(1.0, elapsed / duration)
            
            # Current radius of the growing block
            current_radius = progress * max_distance
            
            # Initialize background
            background = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
            
            for y in range(height):
                for x in range(width):
                    # Distance from target center
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    
                    if distance <= current_radius:
                        # Inside the growing block - apply rainbow pattern
                        wave = math.sin((x + y + elapsed * 8) * 0.4)
                        color_index = int((wave + 1) * 6) % len(rainbow_colors)
                        color = rainbow_colors[color_index]
                        
                        # Add some pulsing effect at the edge
                        edge_distance = current_radius - distance
                        if edge_distance < 2.0:
                            pulse = math.sin(elapsed * 12) * 0.3 + 0.7
                            color = (
                                int(color[0] * pulse),
                                int(color[1] * pulse),
                                int(color[2] * pulse)
                            )
                        
                        background[y][x] = color
            
            # Apply to display with serpentine wiring
            for y in range(height):
                for x in range(width):
                    display_x = x
                    if y % 2 == 0:
                        display_x = width - 1 - x
                    
                    set_pixel(pixels, display_x, y, background[y][x], auto_write=False)
            
            pixels.show()
            time.sleep(0.05)
    
    # Initialize target and searchlights
    target = Target()
    searchlights = [
        Searchlight(0, width * 0.2, height * 0.2, (255, 255, 255)),  # White
        Searchlight(1, width * 0.8, height * 0.2, (255, 255, 0)),   # Yellow  
        Searchlight(2, width * 0.5, height * 0.8, (0, 255, 255))    # Cyan
    ]
    
    cycles_completed = 0
    frame = 0
    
    while cycles_completed < max_cycles:
        # Initialize background
        background = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        
        # Update searchlights
        for searchlight in searchlights:
            searchlight.update(target)
        
        # Draw searchlights
        for searchlight in searchlights:
            searchlight.draw_circle(background)
        
        # Draw target if any searchlight has found it
        if target.found_by:
            target_color = target.get_color()
            for tx, ty in target.get_positions():
                if 0 <= tx < width and 0 <= ty < height:
                    old_r, old_g, old_b = background[ty][tx]
                    background[ty][tx] = (
                        min(255, old_r + target_color[0]),
                        min(255, old_g + target_color[1]),
                        min(255, old_b + target_color[2])
                    )
        
        # Check if all searchlights found the target
        if target.is_found_by_all(len(searchlights)):
            growing_rainbow_block(pixels, width, height, target)
            
            # Reset for next cycle
            target.reset_position()
            for searchlight in searchlights:
                searchlight.found_target = False
                searchlight.locked_target = None
                # Reset positions
                searchlight.x = random.uniform(1, width - 1)
                searchlight.y = random.uniform(1, height - 1)
                searchlight.direction = random.uniform(0, 2 * math.pi)
            
            cycles_completed += 1
        
        # Apply background to display with serpentine wiring
        for y in range(height):
            for x in range(width):
                display_x = x
                if y % 2 == 0:
                    display_x = width - 1 - x
                
                set_pixel(pixels, display_x, y, background[y][x], auto_write=False)
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)