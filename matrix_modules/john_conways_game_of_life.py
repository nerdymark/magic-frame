"""
    Run John Conway's Game of Life.

    The Game of Life, also known simply as Life, is a cellular automaton
    devised by the British mathematician John Horton Conway in 1970. It is a
    zero-player game, meaning that its evolution is determined by its initial
    state, requiring no further input. One interacts with the Game of Life by
    creating an initial configuration and observing how it evolves. It is
    Turing complete and can simulate a universal constructor or any other
    Turing machine.

    Rules
    The universe of the Game of Life is an infinite, two-dimensional orthogonal
    grid of square cells, each of which is in one of two possible states, live
    or dead (or populated and unpopulated, respectively). Every cell interacts
    with its eight neighbors, which are the cells that are horizontally,
    vertically, or diagonally adjacent. At each step in time, the following
    transitions occur:

    Any live cell with fewer than two live neighbours dies, as if by
    underpopulation.

    Any live cell with two or three live neighbours lives on to the next
    generation.

    Any live cell with more than three live neighbours dies, as if by
    overpopulation.

    Any dead cell with exactly three live neighbours becomes a live cell,
      as if by reproduction.

    The initial pattern constitutes the seed of the system. The first
    generation is created by applying the above rules simultaneously to every
    cell in the seed, live or dead; births and deaths occur simultaneously,
    and the discrete moment at which this happens is sometimes called a tick.

    Each generation is a pure function of the preceding one. The rules
    continue to be applied repeatedly to create further generations.

    Initially, the color of the cell is randomly chosen from any RGB color.
    The reproductive cells are a combination of the colors of the parent cells.
    """
import time
import random
from matrix_modules.utils import set_pixel, clear_pixels, get_pixel, game_over, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT

def john_conways_game_of_life(
        pixels,
        width=WIDTH,
        height=HEIGHT,
        delay=0.08,  # Much faster - ~12 FPS for smooth gameplay
        density=None,
        allow_mutations=False,
        allow_visitors=False,
        show_log=True,
        animations=True,
        max_generations=0,
        max_frames=300):
    """
    Display John Conway's Game of Life on the given pixels.
    """
    log_module_start("john_conways_game_of_life", allow_mutations=allow_mutations, allow_visitors=allow_visitors)
    start_time = time.monotonic()
    generation_count = 0
    num_pixels = width * height
    # Create a 18x18 grid of cells.
    if density is None:
        # Random float between 0 and 1.
        density = random.random()

    for y in range(height):
        for x in range(width):
            # Randomly set the initial state of the cell.
            if random.random() < density:
                set_pixel(pixels, x, y, (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)))
            else:
                set_pixel(pixels, x, y, (0, 0, 0))

    def get_neighbors_info(x, y):
        """Get both live and all neighbors in one pass for efficiency"""
        live_neighbors = []
        all_neighbors = []
        
        # Define the neighbors of the cell.
        neighbors = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        ]

        for nx, ny in neighbors:
            # Ensure coordinates are within bounds
            if 0 <= nx < width and 0 <= ny < height:
                all_neighbors.append((nx, ny))
                if get_pixel(pixels, nx, ny) != (0, 0, 0):
                    live_neighbors.append((nx, ny))
        
        return live_neighbors, all_neighbors

    # Run the game of life.
    prev_cells = 0
    stale_generations = 0
    generations_table = {}
    while True:
        generation_count += 1

        # Check if we've hit the max frame limit
        if max_frames > 0 and generation_count > max_frames:
            if show_log:
                print(f"Reached maximum frame limit ({max_frames}). Stopping.")
            break

        # Create a copy of the current state to apply rules simultaneously
        next_state = [[None for _ in range(width)] for _ in range(height)]

        # Calculate next state for all cells
        for y in range(height):
            for x in range(width):
                # Get neighbor info in single pass
                live_neighbors, all_neighbors = get_neighbors_info(x, y)

                # Apply the rules of the game of life.
                current_color = get_pixel(pixels, x, y)
                is_alive = current_color != (0, 0, 0)

                if is_alive:
                    if len(live_neighbors) < 2 or len(live_neighbors) > 3:
                        # Cell dies
                        next_state[y][x] = (0, 0, 0)
                        if show_log and generation_count <= 2:  # Only log first 2 generations
                            print(f"Cell at ({x}, {y}) will die ({len(live_neighbors)} neighbors)")
                    else:
                        # Cell survives - keep same color but maybe dim it
                        next_state[y][x] = current_color

                        if max_generations > 0:
                            # Track generations
                            if x not in generations_table:
                                generations_table[x] = {}
                            generations_table[x][y] = generations_table[x].get(y, 0) + 1

                            # Check if cell is too old
                            if generations_table[x][y] >= max_generations:
                                next_state[y][x] = (0, 0, 0)  # Die of old age
                                if show_log:
                                    print(f"Cell at ({x}, {y}) died of old age")
                            else:
                                # Dim color over time
                                next_factor = 1 - (generations_table[x][y] / (max_generations * 2))
                                next_state[y][x] = (
                                    int(current_color[0] * next_factor),
                                    int(current_color[1] * next_factor),
                                    int(current_color[2] * next_factor)
                                )
                else:
                    # Dead cell - check if it should be born
                    if len(live_neighbors) == 3:
                        # Calculate color from parent cells
                        colors = []
                        for nx, ny in live_neighbors:
                            color = get_pixel(pixels, nx, ny)
                            if color != (0, 0, 0) and color is not None:
                                colors.append(color)

                        if colors:
                            r = sum(color[0] for color in colors) // len(colors)
                            g = sum(color[1] for color in colors) // len(colors)
                            b = sum(color[2] for color in colors) // len(colors)
                        else:
                            r, g, b = 255, 255, 255  # Default white

                        # Apply mutation if enabled
                        if allow_mutations and random.random() < 0.15:  # 15% mutation chance
                            # Create vibrant mutation colors
                            mutation_type = random.randint(0, 2)
                            if mutation_type == 0:  # Full random
                                r = random.randint(100, 255)
                                g = random.randint(100, 255)
                                b = random.randint(100, 255)
                            elif mutation_type == 1:  # Boost one channel
                                channel = random.randint(0, 2)
                                if channel == 0:
                                    r = min(255, r + random.randint(50, 150))
                                elif channel == 1:
                                    g = min(255, g + random.randint(50, 150))
                                else:
                                    b = min(255, b + random.randint(50, 150))
                            else:  # Invert colors
                                r = 255 - r
                                g = 255 - g
                                b = 255 - b

                            if show_log and generation_count <= 5:
                                print(f"MUTATION at ({x}, {y}): RGB({r}, {g}, {b})")

                        next_state[y][x] = (r, g, b)
                        if show_log and generation_count <= 2:
                            print(f"Cell born at ({x}, {y}) with color ({r}, {g}, {b})")
                    else:
                        # Cell stays dead
                        next_state[y][x] = (0, 0, 0)
        # Apply the next state to the display with animation effects
        for y in range(height):
            for x in range(width):
                old_color = get_pixel(pixels, x, y)
                new_color = next_state[y][x]

                if old_color != new_color:
                    if animations and new_color == (0, 0, 0) and old_color != (0, 0, 0):
                        # Death animation - flash red
                        set_pixel(pixels, x, y, (255, 0, 0), auto_write=False)
                    elif animations and new_color != (0, 0, 0) and old_color == (0, 0, 0):
                        # Birth animation - flash white
                        set_pixel(pixels, x, y, (255, 255, 255), auto_write=False)
                    else:
                        set_pixel(pixels, x, y, new_color, auto_write=False)

        if animations:
            pixels.show()
            time.sleep(delay / 2)

        # Now set final colors
        for y in range(height):
            for x in range(width):
                set_pixel(pixels, x, y, next_state[y][x], auto_write=False)

        # Count live cells in the new state
        live_cells = sum(1 for y in range(height) for x in range(width)
                        if next_state[y][x] != (0, 0, 0))

        # Check for visitors condition BEFORE showing the frame
        add_visitors = False
        if allow_visitors:
            if live_cells < width and generation_count > 5:
                add_visitors = True
                visitor_count = random.randint(3, 8)
            elif stale_generations > 3:
                add_visitors = True
                visitor_count = random.randint(5, 12)
            elif live_cells < 10 and generation_count > 10:
                add_visitors = True
                visitor_count = random.randint(8, 15)

            if add_visitors:
                # Create vibrant visitor patterns
                visitor_colors = [
                    (255, 0, 100),   # Hot pink
                    (0, 255, 200),   # Cyan
                    (255, 200, 0),   # Gold
                    (150, 0, 255),   # Purple
                    (0, 255, 0),     # Green
                    (255, 100, 0),   # Orange
                ]
                visitor_color = random.choice(visitor_colors)

                if show_log:
                    print(f"VISITORS: Adding {visitor_count} visitors (color: {visitor_color})")

                # Add visitors in patterns for visibility
                pattern = random.choice(["scatter", "glider", "block", "line"])

                if pattern == "glider":
                    # Add a glider pattern
                    start_x = random.randint(1, width - 4)
                    start_y = random.randint(1, height - 4)
                    glider_cells = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
                    for dx, dy in glider_cells:
                        if start_x + dx < width and start_y + dy < height:
                            set_pixel(pixels, start_x + dx, start_y + dy, visitor_color, auto_write=False)
                elif pattern == "block":
                    # Add a 2x2 block
                    start_x = random.randint(0, width - 2)
                    start_y = random.randint(0, height - 2)
                    for dx in range(2):
                        for dy in range(2):
                            set_pixel(pixels, start_x + dx, start_y + dy, visitor_color, auto_write=False)
                elif pattern == "line":
                    # Add a line of cells
                    if random.random() < 0.5:
                        # Horizontal line
                        y = random.randint(0, height - 1)
                        start_x = random.randint(0, width - visitor_count)
                        for i in range(min(visitor_count, width - start_x)):
                            set_pixel(pixels, start_x + i, y, visitor_color, auto_write=False)
                    else:
                        # Vertical line
                        x = random.randint(0, width - 1)
                        start_y = random.randint(0, height - visitor_count)
                        for i in range(min(visitor_count, height - start_y)):
                            set_pixel(pixels, x, start_y + i, visitor_color, auto_write=False)
                else:  # scatter
                    for _ in range(visitor_count):
                        x = random.randint(0, width - 1)
                        y = random.randint(0, height - 1)
                        if get_pixel(pixels, x, y) == (0, 0, 0):
                            set_pixel(pixels, x, y, visitor_color, auto_write=False)

                # Flash animation for visitors
                if animations:
                    pixels.show()
                    time.sleep(delay * 2)
        # Early termination checks
        if live_cells == 0:
            if show_log:
                print("All cells are dead. Stopping.")
            game_over(pixels, delay=delay)
            break
        elif live_cells < 3 and not allow_visitors and generation_count > 10:
            if show_log:
                print("Too few live cells. Stopping.")
            game_over(pixels, delay=delay)
            break

        # Check if the grid has stabilized
        if live_cells == prev_cells or abs(live_cells - prev_cells) < 2:
            stale_generations += 1
        else:
            stale_generations = 0

        if stale_generations > 15:
            if show_log:
                print("Pattern stabilized. Stopping.")
            game_over(pixels, delay=delay)
            break

        if show_log and generation_count <= 10:
            print(f"Gen {generation_count}: {live_cells} cells (prev: {prev_cells})")

        prev_cells = live_cells

        pixels.show()
        time.sleep(delay)
    clear_pixels(pixels)
    
    duration = time.monotonic() - start_time
    log_module_finish("john_conways_game_of_life", frame_count=generation_count, duration=duration)
