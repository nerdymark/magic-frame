"""
Soothing water ripples animation.
Simulates slowly moving water with gentle waves and ripple effects.
"""
import math
import random
import time
from matrix_modules.utils import set_pixel


def water_ripples(pixels, width, height, delay=0.1, max_frames=150):
    """
    Create a soothing water ripple animation with gentle waves.
    """
    
    class Ripple:
        def __init__(self, x, y, max_radius, speed, intensity):
            self.center_x = x
            self.center_y = y
            self.radius = 0.0
            self.max_radius = max_radius
            self.speed = speed
            self.intensity = intensity
            self.active = True
        
        def update(self):
            self.radius += self.speed
            if self.radius > self.max_radius:
                self.active = False
        
        def get_intensity_at(self, x, y):
            if not self.active:
                return 0.0
            
            distance = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
            
            # Create ripple ring effect
            if self.radius > 0:
                ring_distance = abs(distance - self.radius)
                if ring_distance < 3.0:  # Thicker ring for more visibility
                    # Fade out as ripple expands
                    fade = max(0, 1.0 - (self.radius / self.max_radius))
                    # Ring intensity based on distance from ring edge
                    ring_intensity = max(0, 1.0 - (ring_distance / 3.0))
                    return self.intensity * fade * ring_intensity
            
            return 0.0
    
    # Initialize ripples list
    ripples = []
    
    # Base water colors with independent shifting animation
    def get_base_water_color(x, y, time_offset):
        # Multiple independent wave patterns for shifting colors
        wave1 = math.sin((x + time_offset * 0.5) / 3.0)
        wave2 = math.cos((y + time_offset * 0.4) / 4.0)
        wave3 = math.sin((x + y + time_offset * 0.3) / 5.0)
        
        # Independent color shifting waves
        red_shift = math.sin(time_offset * 0.15 + x * 0.1)
        green_shift = math.cos(time_offset * 0.12 + y * 0.08)
        blue_shift = math.sin(time_offset * 0.18 + (x + y) * 0.05)
        
        # Create depth variation with fewer calculations
        depth = (wave1 + wave2 + 2) / 4  # Normalized to 0-1 range
        current = wave3
        
        # Water colors with independent shifting
        current_normalized = (current + 1) / 2  # Normalize to 0-1
        
        if depth < 0.4:  # Deep water
            base_r = int(8 + depth * 30 + red_shift * 15)
            base_g = int(15 + depth * 50 + green_shift * 20) 
            base_b = int(60 + depth * 70 + blue_shift * 25)
        else:  # Shallow water
            base_r = int(15 + current_normalized * 40 + red_shift * 20)
            base_g = int(50 + current_normalized * 80 + green_shift * 30)
            base_b = int(90 + current_normalized * 60 + blue_shift * 25)
        
        # Ensure colors stay within bounds
        base_r = max(0, min(255, base_r))
        base_g = max(0, min(255, base_g))
        base_b = max(0, min(255, base_b))
        
        return (base_r, base_g, base_b)
    
    frame = 0
    ripple_spawn_timer = 0
    
    while frame < max_frames:
        current_time = frame * delay
        
        # Spawn new ripples occasionally
        ripple_spawn_timer += 1
        if ripple_spawn_timer > random.randint(20, 60):  # Every 2-6 seconds at 0.1 delay
            # Random ripple location - allow edge spawning
            ripple_x = random.uniform(0, width - 1)
            ripple_y = random.uniform(0, height - 1)
            # Calculate max radius to reach screen edges from spawn point
            max_dist_to_edge = max(
                ripple_x, width - 1 - ripple_x,
                ripple_y, height - 1 - ripple_y
            )
            ripple_max_radius = random.uniform(max_dist_to_edge + 2, max_dist_to_edge + 6)
            ripple_speed = random.uniform(0.2, 0.4)  # Moderate expansion
            ripple_intensity = random.uniform(0.8, 1.2)  # More visible intensity
            
            ripples.append(Ripple(ripple_x, ripple_y, ripple_max_radius, ripple_speed, ripple_intensity))
            ripple_spawn_timer = 0
        
        # Update ripples
        for ripple in ripples[:]:  # Use slice to avoid modification during iteration
            ripple.update()
            if not ripple.active:
                ripples.remove(ripple)
        
        # Draw water surface
        for y in range(height):
            for x in range(width):
                # Get base water color
                base_r, base_g, base_b = get_base_water_color(x, y, current_time)
                
                # Add ripple effects
                ripple_effect = 0.0
                for ripple in ripples:
                    ripple_effect += ripple.get_intensity_at(x, y)
                
                # Combine base water with ripple highlights
                if ripple_effect > 0:
                    # Ripples create varied highlights based on base color
                    if base_b > base_g and base_b > base_r:  # Blue-dominant areas
                        # Add white highlights with blue tint
                        ripple_r = int(base_r + ripple_effect * 80)
                        ripple_g = int(base_g + ripple_effect * 100) 
                        ripple_b = int(base_b + ripple_effect * 120)
                    elif base_g > base_r:  # Green-dominant areas  
                        # Add bright aqua highlights
                        ripple_r = int(base_r + ripple_effect * 40)
                        ripple_g = int(base_g + ripple_effect * 120)
                        ripple_b = int(base_b + ripple_effect * 90)
                    else:  # Red-dominant areas (warm shallow water)
                        # Add golden highlights
                        ripple_r = int(base_r + ripple_effect * 100)
                        ripple_g = int(base_g + ripple_effect * 80)
                        ripple_b = int(base_b + ripple_effect * 60)
                    
                    final_r = min(255, ripple_r)
                    final_g = min(255, ripple_g)
                    final_b = min(255, ripple_b)
                else:
                    final_r = base_r
                    final_g = base_g
                    final_b = base_b
                
                # Handle serpentine wiring
                display_x = x
                if y % 2 == 0:
                    display_x = width - 1 - x
                
                set_pixel(pixels, display_x, y, (final_r, final_g, final_b), auto_write=False)
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)