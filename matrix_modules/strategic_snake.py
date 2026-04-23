"""
Strategic Snake Game - Enhanced AI Version
Uses greedy pathfinding with escape-route awareness for fast, smart play.
"""
import random
import time
from matrix_modules.utils import set_pixel, clear_pixels, game_over, log_module_start, log_module_finish


def strategic_snake(pixels, width, height, delay=0.02, max_games=5, show_log=True):
    """
    Strategic snake game optimized for microcontroller performance.
    Greedy AI with escape-route counting — no BFS/flood fill.
    """
    log_module_start("strategic_snake", max_games=max_games)
    start_time = time.monotonic()
    total_frames = 0

    # Directions as tuples
    DIRS = ((0, -1), (0, 1), (-1, 0), (1, 0))

    # 3x5 digit bitmaps (each digit is 3 wide, 5 tall)
    # Each entry is 5 rows of 3-bit patterns
    DIGITS = (
        (0b111, 0b101, 0b101, 0b101, 0b111),  # 0
        (0b010, 0b110, 0b010, 0b010, 0b111),  # 1
        (0b111, 0b001, 0b111, 0b100, 0b111),  # 2
        (0b111, 0b001, 0b111, 0b001, 0b111),  # 3
        (0b101, 0b101, 0b111, 0b001, 0b001),  # 4
        (0b111, 0b100, 0b111, 0b001, 0b111),  # 5
        (0b111, 0b100, 0b111, 0b101, 0b111),  # 6
        (0b111, 0b001, 0b010, 0b010, 0b010),  # 7
        (0b111, 0b101, 0b111, 0b101, 0b111),  # 8
        (0b111, 0b101, 0b111, 0b001, 0b111),  # 9
    )
    SCORE_COLOR = (60, 50, 0)  # Dim yellow

    def get_score_pixels(score_val):
        """Return set of (x,y) positions for the score, centered at bottom."""
        digits = str(score_val)
        total_w = len(digits) * 4 - 1  # 3px each + 1px gap
        sx = (width - total_w) // 2
        sy = height - 6  # 1px from bottom
        pts = set()
        for i, ch in enumerate(digits):
            d = int(ch)
            bx = sx + i * 4
            for row in range(5):
                bits = DIGITS[d][row]
                for col in range(3):
                    if bits & (1 << (2 - col)):
                        px, py = bx + col, sy + row
                        if 0 <= px < width and 0 <= py < height:
                            pts.add((px, py))
        return pts

    def draw_score_layer(score_val, snake_set, food_pos):
        """Draw score digits in yellow where not covered by snake or food."""
        pts = get_score_pixels(score_val)
        for x, y in pts:
            if (x, y) not in snake_set and (x, y) != food_pos:
                set_pixel(pixels, x, y, SCORE_COLOR, auto_write=False)

    def get_ring_pixels(rx, ry, radius):
        """Get the set of pixels for a diamond ring at given radius."""
        pts = set()
        for d in range(-radius, radius + 1):
            r2 = radius - abs(d)
            for px, py in ((rx + d, ry + r2), (rx + d, ry - r2)):
                if 0 <= px < width and 0 <= py < height:
                    pts.add((px, py))
        return pts

    def draw_ripple(rings, snake_set, food_pos, score_pts):
        """Clear old ring, draw new ring, fade out. Returns updated rings list."""
        alive = []
        for rx, ry, radius, brightness in rings:
            # Erase previous ring (radius - 1)
            if radius > 1:
                for px, py in get_ring_pixels(rx, ry, radius - 1):
                    if (px, py) not in snake_set and (px, py) != food_pos:
                        if (px, py) in score_pts:
                            set_pixel(pixels, px, py, SCORE_COLOR, auto_write=False)
                        else:
                            set_pixel(pixels, px, py, (0, 0, 0), auto_write=False)
            if brightness <= 0:
                continue
            # Draw current ring
            for px, py in get_ring_pixels(rx, ry, radius):
                if (px, py) not in snake_set and (px, py) != food_pos:
                    c = int(brightness)
                    set_pixel(pixels, px, py, (c, c // 3, 0), auto_write=False)
            alive.append((rx, ry, radius + 1, brightness - 40))
        return alive

    def pick_direction(head, food, snake_set, cur_dir):
        """Fast greedy direction picker with escape-route safety."""
        hx, hy = head
        fx, fy = food
        cur_dist = abs(hx - fx) + abs(hy - fy)

        best_dir = None
        best_score = -9999

        for dx, dy in DIRS:
            nx, ny = hx + dx, hy + dy

            # Bounds + collision
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue
            if (nx, ny) in snake_set:
                continue

            # Count escape routes from this position
            escapes = 0
            for ddx, ddy in DIRS:
                ex, ey = nx + ddx, ny + ddy
                if (0 <= ex < width and 0 <= ey < height and
                        (ex, ey) not in snake_set):
                    escapes += 1

            lands_on_food = (nx == fx and ny == fy)

            # Dead end — avoid unless it's the food
            if escapes == 0 and not lands_on_food:
                score = -200
            else:
                # Immediate food capture — always best
                if lands_on_food:
                    score = 500
                else:
                    # Distance improvement toward food
                    new_dist = abs(nx - fx) + abs(ny - fy)
                    score = (cur_dist - new_dist) * 10

                    # Escape route bonus
                    score += escapes * 5

                    # Prefer continuing straight
                    if (dx, dy) == cur_dir:
                        score += 2

                    # Penalize 180-degree reversal
                    if (dx, dy) == (-cur_dir[0], -cur_dir[1]):
                        score -= 50

                    # Penalty for few escapes (potential trap)
                    if escapes < 2:
                        score -= 30

            if score > best_score:
                best_score = score
                best_dir = (dx, dy)

        return best_dir if best_dir else cur_dir

    games_played = 0
    total_score = 0
    best_score = 0

    while games_played < max_games:
        if show_log:
            print(f"Strategic snake game {games_played + 1}/{max_games}")

        # Initialize game state
        snake_body = [(width // 2, height // 2)]
        snake_set = set(snake_body)
        direction = (1, 0)  # RIGHT
        score = 0
        moves_without_food = 0
        max_moves = width * height

        # Place initial food
        food_pos = None
        while food_pos is None or food_pos in snake_set:
            food_pos = (random.randint(1, width - 2), random.randint(1, height - 2))

        ripples = []
        prev_score_pts = set()

        # Initial draw
        clear_pixels(pixels)
        prev_score_pts = get_score_pixels(score)
        draw_score_layer(score, snake_set, food_pos)
        hx, hy = snake_body[0]
        set_pixel(pixels, hx, hy, (0, 255, 0), auto_write=False)
        fx, fy = food_pos
        set_pixel(pixels, fx, fy, (255, 0, 0), auto_write=False)
        pixels.show()

        game_running = True
        while game_running:
            # Pick direction
            direction = pick_direction(
                snake_body[0], food_pos, snake_set, direction
            )

            # Move snake
            head_x, head_y = snake_body[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Check collisions
            if (new_head[0] < 0 or new_head[0] >= width or
                    new_head[1] < 0 or new_head[1] >= height or
                    new_head in snake_set):
                game_running = False
                break

            # Add new head
            snake_body.insert(0, new_head)
            snake_set.add(new_head)
            moves_without_food += 1

            # Draw new head
            set_pixel(pixels, new_head[0], new_head[1], (0, 255, 0), auto_write=False)

            # Recolor old head as body
            if len(snake_body) > 1:
                ox, oy = snake_body[1]
                set_pixel(pixels, ox, oy, (0, 150, 0), auto_write=False)

            if new_head == food_pos:
                score += 1
                moves_without_food = 0

                # Spawn ripple from eaten food position
                ripples.append((new_head[0], new_head[1], 1, 160))

                # Place new food
                attempts = 0
                while attempts < 100:
                    if attempts < 30 and random.random() < 0.6:
                        edge = random.randint(0, 3)
                        if edge == 0:
                            food_pos = (random.randint(0, width - 1), 0)
                        elif edge == 1:
                            food_pos = (random.randint(0, width - 1), height - 1)
                        elif edge == 2:
                            food_pos = (0, random.randint(0, height - 1))
                        else:
                            food_pos = (width - 1, random.randint(0, height - 1))
                    else:
                        food_pos = (random.randint(0, width - 1), random.randint(0, height - 1))

                    if food_pos not in snake_set:
                        break
                    attempts += 1

                # Draw new food
                set_pixel(pixels, food_pos[0], food_pos[1], (255, 0, 0), auto_write=False)

                if show_log:
                    print(f"  score:{score} len:{len(snake_body)}")
            else:
                # Erase old tail, remove from tracking
                tail = snake_body.pop()
                snake_set.discard(tail)
                set_pixel(pixels, tail[0], tail[1], (0, 0, 0), auto_write=False)

            # Draw background layers (ripples + score) on uncovered pixels
            score_pts = get_score_pixels(score)

            # Erase pixels from old score that aren't in new score
            stale = prev_score_pts - score_pts
            for sx, sy in stale:
                if (sx, sy) not in snake_set and (sx, sy) != food_pos:
                    set_pixel(pixels, sx, sy, (0, 0, 0), auto_write=False)
            prev_score_pts = score_pts

            ripples = draw_ripple(ripples, snake_set, food_pos, score_pts)
            draw_score_layer(score, snake_set, food_pos)

            # Single show per frame
            pixels.show()
            total_frames += 1

            if moves_without_food > max_moves:
                if show_log:
                    print("  ended - stuck")
                game_running = False
                break

            if delay > 0:
                time.sleep(delay)

        # Game over
        total_score += score
        best_score = max(best_score, score)
        games_played += 1

        if show_log:
            print(f"  game {games_played} done: score={score} len={len(snake_body)}")

        game_over(pixels, delay=delay)
        time.sleep(0.5)

    if show_log:
        avg = total_score / max_games if max_games > 0 else 0
        print(f"Strategic Snake: best={best_score} avg={avg:.1f}")

    clear_pixels(pixels)
    pixels.show()

    duration = time.monotonic() - start_time
    log_module_finish("strategic_snake", frame_count=total_frames, duration=duration)
