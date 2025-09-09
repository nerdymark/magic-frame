"""
Snake Game like from the original Snake game on Nokia phones.
"""
import time
import random
from matrix_modules.utils import set_pixel, clear_pixels, game_over, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def snake_game(pixels, width=WIDTH, height=HEIGHT, delay=0.02, show_log=False):
    """
    Play the snake game on the given pixels.
    """
    log_module_start("snake_game")
    start_time = time.monotonic()
    frame_count = 0
    snake = [(9, 9)]
    directions = ["up", "down", "left", "right"]
    direction = random.choice(directions)
    dot = (random.randint(0, 17), random.randint(0, 17))
    last_moves = []
    last_dot_pos = None

    def manhattan_distance(pos1, pos2):
        """Calculate Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def is_valid_position(pos):
        """Helper function to check if a position is valid"""
        return (0 <= pos[0] < width and 0 <= pos[1] < height and pos not in snake)

    def evaluate_move(pos):
        """Improved move evaluation"""
        if not is_valid_position(pos):
            return float('-inf')

        dist_to_dot = manhattan_distance(pos, dot)
        if dist_to_dot == 0:  # Immediate dot capture
            return float('inf')

        # Enhanced space check - look ahead for escape routes
        escape_dirs = 0
        wall_penalty = 0
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (pos[0] + dx, pos[1] + dy)
            if is_valid_position(next_pos):
                escape_dirs += 1
                # Penalty for being near walls
                if (next_pos[0] <= 1 or next_pos[0] >= width-2 or 
                    next_pos[1] <= 1 or next_pos[1] >= height-2):
                    wall_penalty += 10
        
        if escape_dirs < 2:
            return float('-inf')
        
        # Penalize positions near walls/corners
        if (pos[0] <= 1 or pos[0] >= width-2 or 
            pos[1] <= 1 or pos[1] >= height-2):
            wall_penalty += 20

        # Prioritize dot-seeking with wall avoidance
        return (75 * (1.0 / (dist_to_dot + 1)) + 5 * escape_dirs - wall_penalty)

    def place_new_dot():
        """Place a new dot with improved randomization"""
        MIN_DISTANCE = 3  # Minimum distance from previous dot
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            # Use actual width/height parameters
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            new_pos = (x, y)
            
            # Check if position is valid
            if new_pos not in snake:
                # If this is not the first dot, ensure minimum distance
                if last_dot_pos:
                    if manhattan_distance(new_pos, last_dot_pos) >= MIN_DISTANCE:
                        return new_pos
                else:
                    return new_pos
            attempts += 1
        
        # Fallback to simple placement if no good position found
        while True:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if (x, y) not in snake:
                return (x, y)

    # Initialize first dot and clear any previous dots
    dot = place_new_dot()
    pixels.fill((0, 0, 0))  # Clear screen at start

    # Main game loop optimizations
    while True:
        frame_count += 1
        # Batch clear previous snake position
        for x, y in snake:
            set_pixel(pixels, x, y, (0, 0, 0), auto_write=False)

        # Move the snake.
        head = snake[-1]

        # First check if moving in current direction would hit snake body or wall
        next_pos = {
            "up": (head[0], head[1] - 1),
            "down": (head[0], head[1] + 1),
            "left": (head[0] - 1, head[1]),
            "right": (head[0] + 1, head[1])
        }

        # Score all possible moves with dot-seeking priority
        move_scores = {}
        for d, pos in next_pos.items():
            base_score = evaluate_move(pos)
            if base_score > float('-inf'):
                # Add strong weight for moves that get closer to dot
                dist_to_dot = manhattan_distance(pos, dot)
                current_dist = manhattan_distance(head, dot)
                
                # Extra score for moves that decrease distance to dot
                if dist_to_dot < current_dist:
                    move_scores[d] = base_score + 100  # Strong preference for approaching dot
                else:
                    move_scores[d] = base_score
            else:
                move_scores[d] = float('-inf')

        # Choose best valid move
        best_score = float('-inf')
        best_dir = None
        for d, score in move_scores.items():
            if score > best_score and is_valid_position(next_pos[d]):
                best_score = score
                best_dir = d

        if best_dir:
            direction = best_dir
        else:
            if show_log:
                print("No safe direction available. Game over.")
            game_over(pixels, delay=delay)
            break

        # Move in the direction, but avoid hitting the wall or itself.
        if direction == "up":
            new_head = (head[0], head[1] - 1)
        elif direction == "down":
            new_head = (head[0], head[1] + 1)
        elif direction == "left":
            new_head = (head[0] - 1, head[1])
        elif direction == "right":
            new_head = (head[0] + 1, head[1])
        else:
            if show_log:
                print("Invalid direction. Game over.")
            game_over(pixels, delay=delay)
            break

        # Check if the snake has hit the wall.
        if new_head[0] < 0 or new_head[0] >= width or \
                new_head[1] < 0 or new_head[1] >= height:
            if show_log:
                print("Snake hit the wall. Game over.")
            # Clear the screen.
            game_over(pixels, delay=delay)
            break
        # Check if the snake has hit itself.
        if new_head in snake:
            if show_log:
                print("Snake hit itself. Game over.")
            # Clear the screen.
            game_over(pixels, delay=delay)
            break
        snake.append(new_head)
        # Clear the previous dot if it exists
        if last_dot_pos:
            x, y = last_dot_pos
            set_pixel(pixels, x, y, (0, 0, 0), auto_write=False)
            last_dot_pos = None  # Reset after clearing

        # Handle dot eating and placement
        if new_head == dot:
            if show_log:
                print("Snake ate the dot.")
            last_dot_pos = dot  # Store previous dot position
            dot = place_new_dot()
        else:
            snake.pop(0)

        # Batch update snake and dot positions
        if dot:
            x, y = dot
            set_pixel(pixels, x, y, (255, 0, 0), auto_write=False)

        for x, y in snake:
            set_pixel(pixels, x, y, (0, 255, 0), auto_write=False)

        # Single screen update per frame
        pixels.show()
        time.sleep(delay)

        # Track the last few moves to detect oscillation
        last_moves.append(new_head)
        if len(last_moves) > 4:
            last_moves.pop(0)

        # Only use pattern breaking if not making progress toward the dot
        current_dist = manhattan_distance(new_head, dot)
        last_few_dists = [manhattan_distance(pos, dot) for pos in last_moves[-4:]] if len(last_moves) >= 4 else []

        # Only break patterns if we're not approaching the dot
        if len(last_moves) >= 4 and min(last_few_dists) >= current_dist:
            # Oscillation detection (simplified)
            if last_moves[0] == last_moves[2] and last_moves[1] == last_moves[3]:
                # Get directions that would get us closer to the dot
                safe_dirs = [d for d in directions if is_valid_position(next_pos[d])]
                if safe_dirs:
                    direction = random.choice(safe_dirs)

        # Enhanced wall avoidance - check proximity to walls
        near_wall = (new_head[0] <= 1 or new_head[0] >= width-2 or 
                     new_head[1] <= 1 or new_head[1] >= height-2)
        
        if near_wall:
            # Prioritize moves away from walls
            away_from_wall = []
            for d in directions:
                test_pos = next_pos[d]
                if is_valid_position(test_pos):
                    # Check if this move takes us away from walls
                    wall_dist = min(test_pos[0], width-1-test_pos[0], 
                                   test_pos[1], height-1-test_pos[1])
                    current_wall_dist = min(new_head[0], width-1-new_head[0], 
                                           new_head[1], height-1-new_head[1])
                    if wall_dist >= current_wall_dist:
                        away_from_wall.append(d)
            
            if away_from_wall:
                direction = random.choice(away_from_wall)

        # Simplified loop detection - only break loops if not approaching dot
        if len(last_moves) >= 6:
            # Check for simple back-and-forth pattern
            if (last_moves[-1] == last_moves[-3] == last_moves[-5] and 
                last_moves[-2] == last_moves[-4]):
                safe_dirs = [d for d in directions if is_valid_position(next_pos[d])]
                if safe_dirs:
                    direction = random.choice(safe_dirs)

    clear_pixels(pixels)
    
    duration = time.monotonic() - start_time
    log_module_finish("snake_game", frame_count=frame_count, duration=duration)

