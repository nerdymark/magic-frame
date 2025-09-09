"""
Fishtank Effect - Peaceful underwater scene with swimming fish.
Features sandy bottom, shimmering blue water, rising bubbles, and various fish.
Creates a calming aquarium atmosphere with natural movement.
"""
import time
import random
import math
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY

def fishtank(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=2000):
    """
    Generate a peaceful fishtank scene with fish, bubbles, and shimmering water.
    Complete underwater ecosystem simulation.
    """
    log_module_start("fishtank", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Fish class - non-uniform dot patterns
    class Fish:
        def __init__(self):
            self.x = random.uniform(-5, width + 5)  # Can start off-screen
            self.y = random.uniform(2, height - 4)  # Avoid sand and surface
            self.speed = random.uniform(0.3, 0.8)
            self.direction = random.choice([-1, 1])  # Left or right
            self.size = random.choice(['small', 'medium', 'large'])
            self.color_type = random.choice(['tropical', 'gold', 'blue', 'neon'])
            self.swim_phase = random.uniform(0, math.pi * 2)
            self.vertical_amplitude = random.uniform(0.2, 0.5)
            
            # Define fish patterns (non-uniform dots)
            if self.size == 'small':
                # 2-3 pixel fish
                self.pattern = [(0, 0), (1, 0)]
                if random.random() > 0.5:
                    self.pattern.append((0, 1))
            elif self.size == 'medium':
                # 4-5 pixel fish
                self.pattern = [(0, 0), (1, 0), (-1, 0)]
                if random.random() > 0.5:
                    self.pattern.append((0, -1))
                if random.random() > 0.5:
                    self.pattern.append((2, 0))
            else:  # large
                # 6-8 pixel fish
                self.pattern = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
                if random.random() > 0.5:
                    self.pattern.extend([(2, 0), (-2, 0)])
                if random.random() > 0.5:
                    self.pattern.append((1, 1))
            
            # Set colors based on type
            if self.color_type == 'tropical':
                self.colors = [(255, 100, 0), (255, 150, 0), (255, 200, 50)]
            elif self.color_type == 'gold':
                self.colors = [(255, 180, 0), (255, 200, 50), (255, 220, 100)]
            elif self.color_type == 'blue':
                self.colors = [(0, 100, 255), (50, 150, 255), (100, 200, 255)]
            else:  # neon
                self.colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
        
        def update(self, t):
            # Horizontal movement
            self.x += self.speed * self.direction
            
            # Sinusoidal vertical movement for natural swimming
            self.swim_phase += 0.1
            self.y += ultra_sin(self.swim_phase) * self.vertical_amplitude
            
            # Keep fish in water area
            self.y = max(2, min(height - 4, self.y))
            
            # Wrap around or respawn
            if self.direction > 0 and self.x > width + 5:
                self.x = -5
                self.y = random.uniform(2, height - 4)
            elif self.direction < 0 and self.x < -5:
                self.x = width + 5
                self.y = random.uniform(2, height - 4)
        
        def draw(self, pixels, pixel_map):
            for i, (dx, dy) in enumerate(self.pattern):
                # Flip pattern if swimming left
                if self.direction < 0:
                    dx = -dx
                
                draw_x = int(self.x + dx)
                draw_y = int(self.y + dy)
                
                if 0 <= draw_x < width and 0 <= draw_y < height:
                    color = self.colors[i % len(self.colors)]
                    # Slightly dim based on depth for perspective
                    depth_factor = 0.7 + 0.3 * (1 - draw_y / height)
                    dimmed_color = (
                        int(color[0] * depth_factor),
                        int(color[1] * depth_factor),
                        int(color[2] * depth_factor)
                    )
                    pixel_idx = pixel_map[draw_y * width + draw_x]
                    pixels[pixel_idx] = dimmed_color
    
    # Bubble class
    class Bubble:
        def __init__(self):
            self.x = random.uniform(1, width - 1)
            self.y = height - 1  # Start at bottom
            self.speed = random.uniform(0.2, 0.4)
            self.wobble = random.uniform(0, math.pi * 2)
            self.size = random.choice([1, 1, 2])  # Mostly small
        
        def update(self, t):
            # Rise upward with slight wobble
            self.y -= self.speed
            self.wobble += 0.2
            self.x += ultra_sin(self.wobble) * 0.1
            
            # Reset when reaching surface
            if self.y < 1:
                self.x = random.uniform(1, width - 1)
                self.y = height - 1
        
        def draw(self, pixels, pixel_map):
            draw_x = int(self.x)
            draw_y = int(self.y)
            
            if 0 <= draw_x < width and 0 <= draw_y < height:
                # Bubble color - light blue/white
                bubble_color = (150, 200, 255)
                pixel_idx = pixel_map[draw_y * width + draw_x]
                pixels[pixel_idx] = bubble_color
                
                # Larger bubbles have a highlight
                if self.size == 2 and draw_x > 0:
                    pixel_idx = pixel_map[draw_y * width + (draw_x - 1)]
                    pixels[pixel_idx] = (200, 230, 255)
    
    # Create fish population
    fish_list = []
    for _ in range(6):  # 6 fish swimming around
        fish = Fish()
        # Stagger their positions
        fish.x = random.uniform(0, width)
        fish_list.append(fish)
    
    # Create occasional bubbles
    bubbles = []
    for _ in range(3):  # 3 bubble streams
        bubble = Bubble()
        bubble.y = random.uniform(height // 2, height - 1)  # Start at different heights
        bubbles.append(bubble)
    
    # Water shimmer effect parameters
    shimmer_phase = 0
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        shimmer_phase += 0.05
        
        # Draw the scene from bottom to top
        for y in range(height):
            for x in range(width):
                # Sandy bottom (bottom 2 rows)
                if y >= height - 2:
                    # Sand color with slight variation
                    sand_variation = random.randint(-10, 10)
                    sand_r = min(255, max(0, 200 + sand_variation))
                    sand_g = min(255, max(0, 180 + sand_variation))
                    sand_b = min(255, max(0, 120 + sand_variation))
                    color = (sand_r, sand_g, sand_b)
                
                # Water area
                else:
                    # Base water color with depth gradient
                    depth = y / height
                    
                    # Shimmering water effect
                    shimmer = ultra_sin(x * 0.5 + y * 0.3 + shimmer_phase) * 15
                    shimmer += ultra_cos(x * 0.3 - y * 0.4 + shimmer_phase * 1.5) * 10
                    
                    # Deeper blue as you go down
                    base_r = int(0 + depth * 20)
                    base_g = int(50 + depth * 50 + shimmer)
                    base_b = int(150 + depth * 50 - shimmer * 0.5)
                    
                    # Caustic light patterns near surface
                    if y < 4:
                        caustic = ultra_sin(x * 0.8 + shimmer_phase * 2) * 30
                        base_g = min(255, base_g + int(caustic))
                        base_b = min(255, base_b + int(caustic * 0.7))
                    
                    # Clamp values
                    color = (
                        max(0, min(255, base_r)),
                        max(0, min(255, base_g)),
                        max(0, min(255, base_b))
                    )
                
                pixel_idx = pixel_map[y * width + x]
                pixels[pixel_idx] = color
        
        # Add seaweed/plants at bottom (simple dark green lines)
        if frame % 2 == 0:  # Animate every other frame
            for i in range(3):  # 3 plants
                plant_x = 3 + i * 6
                plant_height = 4 + int(ultra_sin(t + i) * 2)
                for py in range(plant_height):
                    plant_y = height - 3 - py
                    if 0 <= plant_x < width and 0 <= plant_y < height:
                        # Dark green with slight variation
                        plant_color = (0, 80 + py * 10, 20)
                        pixel_idx = pixel_map[plant_y * width + plant_x]
                        pixels[pixel_idx] = plant_color
        
        # Update and draw bubbles
        for bubble in bubbles:
            bubble.update(t)
            bubble.draw(pixels, pixel_map)
        
        # Occasionally add new bubble
        if random.random() < 0.05:  # 5% chance per frame
            new_bubble = Bubble()
            bubbles.append(new_bubble)
            # Remove oldest bubble if too many
            if len(bubbles) > 8:
                bubbles.pop(0)
        
        # Update and draw fish
        for fish in fish_list:
            fish.update(t)
            fish.draw(pixels, pixel_map)
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.04)  # 25 FPS for smooth fish movement
    
    log_module_finish("fishtank", frame_count=frame, duration=time.monotonic() - start_time)