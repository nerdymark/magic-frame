"""
Strategic Snake Game - Enhanced AI Version
Inspired by GeeksforGeeks implementation but optimized for maximum tail length.
Uses edge-following pathfinding and strategic movement to build the longest possible snake.
"""
import random
import time
from collections import deque
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish


def strategic_snake(pixels, width, height, delay=0.0, max_games=5, show_log=True):
    """
    Strategic snake game that prioritizes building the longest tail possible.
    Uses advanced pathfinding along edges and avoids traps.
    """
    log_module_start("strategic_snake", max_games=max_games)
    start_time = time.monotonic()
    total_frames = 0
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Color schemes for different game elements
    SNAKE_HEAD = (0, 255, 0)      # Bright green head
    SNAKE_BODY = (0, 180, 0)      # Medium green body
    SNAKE_TAIL = (0, 120, 0)      # Dark green tail
    FOOD = (255, 50, 0)           # Red food
    BACKGROUND = (0, 0, 0)        # Black background
    WALL_WARNING = (100, 100, 0)  # Yellow warning for danger zones
    
    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    
    def get_pixel_index(x, y):
        """Convert x,y coordinates to pixel index"""
        if 0 <= y < height and 0 <= x < width:
            return pixel_map[y * width + x]
        return None
    
    def is_valid_position(x, y, snake_body):
        """Check if position is valid (in bounds and not occupied by snake)"""
        if x < 0 or x >= width or y < 0 or y >= height:
            return False
        return (x, y) not in snake_body
    
    def manhattan_distance(pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def is_edge_position(x, y):
        """Check if position is on the edge of the game area"""
        return x == 0 or x == width - 1 or y == 0 or y == height - 1
    
    def count_reachable_cells(start, snake_body):
        """Count how many cells are reachable from start position using BFS"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        count = 0
        
        while queue:
            x, y = queue.popleft()
            count += 1
            
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and is_valid_position(nx, ny, snake_body):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        
        return count
    
    def find_edge_path_to_food(head, food, snake_body):
        """Find path to food that prefers edges and avoids creating traps"""
        # Use A* pathfinding with edge preference
        from heapq import heappush, heappop
        
        def heuristic(pos):
            """Heuristic function: Manhattan distance + edge bonus"""
            h = manhattan_distance(pos, food)
            # Bonus for edge positions (lower is better)
            if is_edge_position(pos[0], pos[1]):
                h -= 2
            return h
        
        def get_neighbors(pos):
            x, y = pos
            neighbors = []
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if is_valid_position(nx, ny, snake_body):
                    neighbors.append((nx, ny))
            return neighbors
        
        # A* algorithm
        open_set = [(heuristic(head), 0, head, [head])]
        closed_set = set()
        
        while open_set:
            f_score, g_score, current, path = heappop(open_set)
            
            if current in closed_set:
                continue
                
            closed_set.add(current)
            
            if current == food:
                return path[1:] if len(path) > 1 else []
            
            for neighbor in get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                new_g_score = g_score + 1
                new_path = path + [neighbor]
                
                # Check if this move would create a trap
                temp_snake = snake_body + [neighbor]
                reachable_after = count_reachable_cells(neighbor, temp_snake)
                
                # Avoid moves that dramatically reduce reachable space
                if reachable_after < len(snake_body) + 10:
                    continue
                
                new_f_score = new_g_score + heuristic(neighbor)
                heappush(open_set, (new_f_score, new_g_score, neighbor, new_path))
        
        return []  # No path found
    
    def get_strategic_direction(head, food, snake_body, current_direction):
        """Get the best strategic direction for maximum tail growth"""
        path = find_edge_path_to_food(head, food, snake_body)
        
        if path:
            # Follow the calculated path
            next_pos = path[0]
            dx = next_pos[0] - head[0]
            dy = next_pos[1] - head[1]
            return (dx, dy)
        
        # If no path to food, find safe direction that maximizes space
        best_direction = None
        best_score = -1
        
        for direction in DIRECTIONS:
            dx, dy = direction
            new_head = (head[0] + dx, head[1] + dy)
            
            if not is_valid_position(new_head[0], new_head[1], snake_body):
                continue
            
            # Score this direction
            score = 0
            
            # Prefer directions that keep us on edges
            if is_edge_position(new_head[0], new_head[1]):
                score += 20
            
            # Prefer directions that maintain maximum reachable space
            temp_snake = snake_body + [new_head]
            reachable = count_reachable_cells(new_head, temp_snake)
            score += reachable
            
            # Avoid 180-degree turns
            if (dx, dy) == (-current_direction[0], -current_direction[1]):
                score -= 100
            
            # Prefer continuing in same direction when safe
            if direction == current_direction:
                score += 5
            
            if score > best_score:
                best_score = score
                best_direction = direction
        
        return best_direction if best_direction else current_direction
    
    def draw_game_state(snake_body, food_pos, score):
        """Draw the current game state"""
        clear_pixels(pixels)
        
        # Draw snake body with gradient effect
        for i, (x, y) in enumerate(snake_body):
            pixel_idx = get_pixel_index(x, y)
            if pixel_idx is not None:
                if i == 0:  # Head
                    pixels[pixel_idx] = SNAKE_HEAD
                elif i == len(snake_body) - 1:  # Tail
                    pixels[pixel_idx] = SNAKE_TAIL
                else:  # Body - gradient from head to tail
                    intensity = 180 - (i * 40 // len(snake_body))
                    intensity = max(80, intensity)
                    pixels[pixel_idx] = (0, intensity, 0)
        
        # Draw food with pulsing effect
        food_x, food_y = food_pos
        food_idx = get_pixel_index(food_x, food_y)
        if food_idx is not None:
            pulse = int(50 + 50 * abs(time.monotonic() % 2 - 1))
            pixels[food_idx] = (255, pulse, 0)
        
        # Show danger zones (positions that would cause collision)
        head_x, head_y = snake_body[0]
        for dx, dy in DIRECTIONS:
            warn_x, warn_y = head_x + dx, head_y + dy
            if (warn_x < 0 or warn_x >= width or warn_y < 0 or warn_y >= height or 
                (warn_x, warn_y) in snake_body):
                # This would be a collision - show warning if adjacent
                for ddx, ddy in DIRECTIONS:
                    warn2_x, warn2_y = warn_x + ddx, warn_y + ddy
                    warn_idx = get_pixel_index(warn2_x, warn2_y)
                    if (warn_idx is not None and 
                        is_valid_position(warn2_x, warn2_y, snake_body) and
                        (warn2_x, warn2_y) != food_pos):
                        current_color = pixels[warn_idx]
                        if current_color == BACKGROUND:
                            pixels[warn_idx] = WALL_WARNING
        
        pixels.show()
    
    games_played = 0
    total_score = 0
    best_score = 0
    
    while games_played < max_games:
        if show_log:
            print(f"Starting strategic snake game {games_played + 1}/{max_games}")
        
        # Initialize game state
        snake_body = [(width // 2, height // 2)]  # Start in center
        direction = RIGHT
        food_pos = None
        score = 0
        moves_without_food = 0
        max_moves_without_food = width * height  # Prevent infinite loops
        
        # Place initial food
        while food_pos is None or food_pos in snake_body:
            food_pos = (random.randint(1, width - 2), random.randint(1, height - 2))
        
        game_running = True
        while game_running:
            # Get strategic direction
            new_direction = get_strategic_direction(
                snake_body[0], food_pos, snake_body, direction
            )
            
            if new_direction is not None:
                direction = new_direction
            
            # Move snake
            head_x, head_y = snake_body[0]
            new_head = (head_x + direction[0], head_y + direction[1])
            
            # Check collisions
            if not is_valid_position(new_head[0], new_head[1], snake_body):
                game_running = False
                break
            
            # Add new head
            snake_body.insert(0, new_head)
            moves_without_food += 1
            
            # Check if food eaten
            if new_head == food_pos:
                score += 1
                moves_without_food = 0
                
                # Don't remove tail (snake grows)
                
                # Place new food strategically (prefer edges)
                attempts = 0
                while attempts < 100:
                    if attempts < 50:
                        # Prefer edges for first 50 attempts
                        if random.random() < 0.7:  # 70% chance for edge
                            edge = random.choice(['top', 'bottom', 'left', 'right'])
                            if edge == 'top':
                                food_pos = (random.randint(0, width-1), 0)
                            elif edge == 'bottom':
                                food_pos = (random.randint(0, width-1), height-1)
                            elif edge == 'left':
                                food_pos = (0, random.randint(0, height-1))
                            else:  # right
                                food_pos = (width-1, random.randint(0, height-1))
                        else:
                            food_pos = (random.randint(1, width-2), random.randint(1, height-2))
                    else:
                        # Random placement as fallback
                        food_pos = (random.randint(0, width-1), random.randint(0, height-1))
                    
                    if food_pos not in snake_body:
                        break
                    attempts += 1
                
                if show_log:
                    print(f"Score: {score}, Snake length: {len(snake_body)}")
            else:
                # Remove tail (normal movement)
                snake_body.pop()
            
            # Check for stuck situation
            if moves_without_food > max_moves_without_food:
                if show_log:
                    print("Game ended - too many moves without food")
                game_running = False
                break
            
            # Draw current state
            draw_game_state(snake_body, food_pos, score)
            total_frames += 1
            
            # Control game speed
            if delay > 0:
                time.sleep(delay)
            else:
                time.sleep(0.15)  # Default speed for strategic play
        
        # Game over
        total_score += score
        best_score = max(best_score, score)
        games_played += 1
        
        if show_log:
            print(f"Game {games_played} ended. Final score: {score}, Snake length: {len(snake_body)}")
            print(f"Best score so far: {best_score}")
        
        # Show game over effect
        for flash in range(3):
            # Flash the snake red
            for x, y in snake_body:
                pixel_idx = get_pixel_index(x, y)
                if pixel_idx is not None:
                    pixels[pixel_idx] = (255, 0, 0)
            pixels.show()
            time.sleep(0.3)
            
            # Flash off
            clear_pixels(pixels)
            pixels.show()
            time.sleep(0.2)
        
        # Brief pause between games
        time.sleep(1.0)
    
    # Final statistics
    if show_log:
        avg_score = total_score / max_games if max_games > 0 else 0
        print(f"Strategic Snake completed!")
        print(f"Games played: {max_games}")
        print(f"Best score: {best_score}")
        print(f"Average score: {avg_score:.1f}")
        print(f"Total playing time: {time.monotonic() - start_time:.1f}s")
    
    # Clear display
    clear_pixels(pixels)
    pixels.show()
    
    duration = time.monotonic() - start_time
    log_module_finish("strategic_snake", frame_count=total_frames, duration=duration)