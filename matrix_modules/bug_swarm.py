"""
Bug swarm animation - A leading bug flies around with a swarm following.
The lead bug moves in organic patterns while followers trail behind with slight randomness.
"""
import math
import random
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def bug_swarm(pixels, width=WIDTH, height=HEIGHT, delay=0.05, max_frames=1000):
    """
    Simulate a bug flying with a swarm following behind.
    """
    log_module_start("bug_swarm", max_frames=max_frames)
    start_time = time.monotonic()
    
    class Bug:
        def __init__(self, x, y, is_leader=False):
            self.x = float(x)
            self.y = float(y)
            self.target_x = x
            self.target_y = y
            self.is_leader = is_leader
            self.speed = 0.6 if is_leader else 0.4
            self.trail = []  # Store recent positions for followers
            # Smaller, dimmer bugs
            if is_leader:
                self.color = (150, 150, 0)  # Dimmer yellow leader
            else:
                # Variety of small bug colors - greens and some browns
                if random.random() < 0.8:
                    self.color = (0, random.randint(80, 120), 0)  # Various green intensities
                else:
                    self.color = (random.randint(60, 100), random.randint(40, 80), 0)  # Brown bugs
            
            if is_leader:
                # Leader has more erratic movement
                self.direction_change_timer = 0
                self.direction = random.uniform(0, 2 * math.pi)
                self.turn_rate = 0.1
            else:
                # Followers have more varied following behavior for spread
                self.follow_distance = random.uniform(2.0, 6.0)  # Much wider range
                self.randomness = random.uniform(0.5, 1.2)  # More randomness
                self.spread_factor = random.uniform(1.0, 2.5)  # Individual spread preference
        
        def update_leader(self, frame):
            # Leader flies in organic patterns with occasional direction changes
            self.direction_change_timer += 1
            
            # Smooth curving flight with occasional random turns
            if self.direction_change_timer > random.randint(20, 60):
                self.direction += random.uniform(-0.8, 0.8)
                self.direction_change_timer = 0
            
            # Add some sine wave motion for organic feel
            wave_offset = math.sin(frame * 0.1) * 0.3
            self.direction += wave_offset * 0.1
            
            # Calculate movement
            dx = math.cos(self.direction) * self.speed
            dy = math.sin(self.direction) * self.speed
            
            # Update position with boundary bouncing
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Bounce off walls with direction change
            if new_x < 1 or new_x >= width - 1:
                self.direction = math.pi - self.direction + random.uniform(-0.5, 0.5)
                new_x = max(1, min(width - 2, new_x))
            
            if new_y < 1 or new_y >= height - 1:
                self.direction = -self.direction + random.uniform(-0.5, 0.5)
                new_y = max(1, min(height - 2, new_y))
            
            # Store trail for followers
            self.trail.append((self.x, self.y))
            if len(self.trail) > 8:  # Keep last 8 positions for smoother trails
                self.trail.pop(0)
            
            self.x = new_x
            self.y = new_y
        
        def update_follower(self, leader, other_followers):
            # Follow the leader's trail with varied delays and more spread
            if len(leader.trail) > 2:
                # Pick a trail position based on follow distance (more varied)
                trail_index = min(int(self.follow_distance * 1.5), len(leader.trail) - 1)
                target_pos = leader.trail[-(trail_index + 1)]
                
                self.target_x = target_pos[0]
                self.target_y = target_pos[1]
                
                # Add much more randomness for spread
                self.target_x += random.uniform(-2, 2) * self.randomness * self.spread_factor
                self.target_y += random.uniform(-2, 2) * self.randomness * self.spread_factor
                
                # Stronger separation from other followers
                separation_force_x = 0
                separation_force_y = 0
                for other in other_followers:
                    if other != self:
                        dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                        if dist < 2.5 and dist > 0:  # Larger separation distance
                            # Push away more strongly
                            push_x = (self.x - other.x) / dist * 0.8
                            push_y = (self.y - other.y) / dist * 0.8
                            separation_force_x += push_x
                            separation_force_y += push_y
                
                self.target_x += separation_force_x
                self.target_y += separation_force_y
            
            # Move towards target with more varied speeds
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            # More varied following movement
            follow_strength = 0.2 + (1.0 / self.follow_distance) * 0.1  # Closer followers move faster
            self.x += dx * self.speed * follow_strength
            self.y += dy * self.speed * follow_strength
            
            # Keep in bounds
            self.x = max(0, min(width - 1, self.x))
            self.y = max(0, min(height - 1, self.y))
    
    # Create bugs - 1 leader and 18-25 followers (more bugs)
    num_followers = random.randint(18, 25)
    leader = Bug(width // 2, height // 2, is_leader=True)
    followers = []
    
    for i in range(num_followers):
        # Start followers more spread out around leader
        angle = (i / num_followers) * 2 * math.pi + random.uniform(-0.5, 0.5)  # Add angle randomness
        distance = random.uniform(3.0, 7.0)  # Much wider initial spread
        start_x = leader.x + math.cos(angle) * distance
        start_y = leader.y + math.sin(angle) * distance
        start_x = max(0, min(width - 1, start_x))
        start_y = max(0, min(height - 1, start_y))
        followers.append(Bug(start_x, start_y, is_leader=False))
    
    frame = 0
    # Initialize background fade array for smoother animation
    background = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    
    while frame < max_frames:
        # Fade background instead of clearing for smoother animation
        for y in range(height):
            for x in range(width):
                r, g, b = background[y][x]
                # Fade to black gradually
                background[y][x] = (max(0, r - 25), max(0, g - 25), max(0, b - 25))
                
                # Apply faded background
                set_pixel(pixels, x, y, background[y][x], auto_write=False)
        
        # Update leader
        leader.update_leader(frame)
        
        # Update followers
        for follower in followers:
            follower.update_follower(leader, followers)
        
        # Draw leader with trail effect
        leader_x = int(leader.x)
        leader_y = int(leader.y)
        
        if 0 <= leader_x < width and 0 <= leader_y < height:
            # Add leader to background with enhanced brightness
            bright_leader_color = (
                min(255, int(leader.color[0] * 1.3)),
                min(255, int(leader.color[1] * 1.3)),
                min(255, int(leader.color[2] * 1.3))
            )
            background[leader_y][leader_x] = bright_leader_color
            
            set_pixel(pixels, leader_x, leader_y, bright_leader_color, auto_write=False)
        
        # Draw followers with trail blending
        for follower in followers:
            follower_x = int(follower.x)
            follower_y = int(follower.y)
            
            if 0 <= follower_x < width and 0 <= follower_y < height:
                # Blend follower color with background
                old_r, old_g, old_b = background[follower_y][follower_x]
                new_color = (
                    min(255, old_r + follower.color[0]),
                    min(255, old_g + follower.color[1]),
                    min(255, old_b + follower.color[2])
                )
                background[follower_y][follower_x] = new_color
                
                set_pixel(pixels, follower_x, follower_y, new_color, auto_write=False)
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
    
    duration = time.monotonic() - start_time
    log_module_finish("bug_swarm", frame_count=frame, duration=duration)