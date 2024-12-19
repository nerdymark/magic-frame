"""
Snake Game like from the original Snake game on Nokia phones.
"""
import time
import random
from matrix_modules.utils import set_pixel, clear_pixels, game_over


def snake_game(pixels, width, height, delay=0.02, show_log=False):
    """
    Play the snake game on the given pixels.
    """
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
        """Simplified move evaluation"""
        if not is_valid_position(pos):
            return float('-inf')

        dist_to_dot = manhattan_distance(pos, dot)
        if dist_to_dot == 0:  # Immediate dot capture
            return float('inf')

        # Quick space check
        escape_dirs = sum(1 for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                          if is_valid_position((pos[0] + dx, pos[1] + dy)))
        if escape_dirs < 2:
            return float('-inf')

        # Basic scoring
        return (50 * (1.0 / (dist_to_dot + 1)) + 10 * escape_dirs)  # Distance score + Available moves score

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
        # Batch clear previous snake position
        for x, y in snake:
            if y % 2 == 0:
                x = abs(x - width + 1)
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
                dot_score = 50 * (1.0 / (dist_to_dot + 1))  # Avoid division by zero

                # Add extra score for moves directly towards dot
                if (d == "right" and dot[0] > head[0]) or \
                   (d == "left" and dot[0] < head[0]) or \
                   (d == "down" and dot[1] > head[1]) or \
                   (d == "up" and dot[1] < head[1]):
                    dot_score *= 2

                move_scores[d] = base_score + dot_score
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
            if y % 2 == 0:
                x = abs(x - width + 1)
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
            if y % 2 == 0:
                x = abs(x - width + 1)
            set_pixel(pixels, x, y, (255, 0, 0), auto_write=False)

        for x, y in snake:
            if y % 2 == 0:
                x = abs(x - width + 1)
            set_pixel(pixels, x, y, (0, 255, 0), auto_write=False)

        # Single screen update per frame
        pixels.show()
        time.sleep(delay)

        # Track the last few moves to detect oscillation
        last_moves.append(new_head)
        if len(last_moves) > 4:
            last_moves.pop(0)
        if len(last_moves) == 4 and \
                last_moves[0] == last_moves[2] and \
                last_moves[1] == last_moves[3]:
            # Force change direction if oscillating
            direction = random.choice([d for d in directions if d != direction])

        # Check if the snake is about to hit the wall and force a change in direction
        if new_head[0] == 0 or \
                new_head[0] == width - 1 or \
                new_head[1] == 0 or \
                new_head[1] == height - 1:
            safe_directions = [d for d in directions if is_valid_position(next_pos[d])]
            if safe_directions:
                direction = random.choice(safe_directions)

        # Check if the snake is stuck in a corner and force a change in direction
        if (new_head[0] == 0 or \
                new_head[0] == width - 1) and \
                (new_head[1] == 0 or \
                 new_head[1] == height - 1):
            safe_directions = [d for d in directions if is_valid_position(next_pos[d])]
            if safe_directions:
                direction = random.choice(safe_directions)

        # Detect if the snake is stuck in a loop and force a change in direction
        if len(last_moves) >= 8 and \
                last_moves[-1] == last_moves[-3] and \
                last_moves[-2] == last_moves[-4]:
            direction = random.choice([d for d in directions if d != direction])

        # Additional check to break out of circular patterns
        if len(last_moves) >= 12 and \
                last_moves[-1] == last_moves[-4] and \
                last_moves[-2] == last_moves[-5] and \
                last_moves[-3] == last_moves[-6]:
            direction = random.choice([d for d in directions if d != direction])

        # Additional check to break out of circular patterns when the dot is in a corner
        if dot in [(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)]:
            if len(last_moves) >= 4 and \
                    last_moves[-1] == last_moves[-3] and \
                    last_moves[-2] == last_moves[-4]:
                direction = random.choice([d for d in directions if d != direction])

    clear_pixels(pixels)
