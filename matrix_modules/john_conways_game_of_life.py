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
from matrix_modules.utils import set_pixel, clear_pixels, get_pixel, game_over

def john_conways_game_of_life(
        pixels,
        width,
        height,
        delay=0.5,
        density=None,
        allow_mutations=False,
        allow_visitors=False,
        show_log=True,
        animations=True,
        max_generations=0):
    """
    Display John Conway's Game of Life on the given pixels.
    """
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

    def find_live_neighbors(x, y, live_only=True):
        # print(f"Finding live neighbors for cell at ({x}, {y})")
        cell_neighbors = []
        max_index = width - 1

        # Define the neighbors of the cell.
        neighbors = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        ]

        for nx, ny in neighbors:
            if ny % 2 == 0:
                # Adjust for odd rows.
                nx = abs(nx - width + 1)
            # Ensure nx is within bounds after adjustment for odd rows
            if 0 <= nx <= max_index and 0 <= ny <= max_index:
                if get_pixel(pixels, nx, ny) != (0, 0, 0) and live_only:
                    cell_neighbors.append((nx, ny))
                elif not live_only:
                    cell_neighbors.append((nx, ny))
        return cell_neighbors

    # Run the game of life.
    prev_cells = 0
    stale_generations = 0
    generations_table = {}
    while True:
        # Update each cell in the grid.
        for y in range(18):
            for x in sorted(range(18), reverse=True) if y % 2 == 0 else \
                    range(18):
                # print(f"Checking cell at ({x}, {y})")
                live_neighbors = find_live_neighbors(x, y)
                all_neighbors = find_live_neighbors(x, y, live_only=False)

                # Apply the rules of the game of life.
                if get_pixel(pixels, x, y) != (0, 0, 0):
                    if len(live_neighbors) < 2 or len(live_neighbors) > 3:
                        if show_log:
                            print(f"Cell at ({x}, {y}) died because it had {len(live_neighbors)} live neighbors.")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            set_pixel(pixels, x, y, (255, 0, 0))
                            time.sleep(delay)
                            set_pixel(pixels, x, y, (0, 0, 0))
                            time.sleep(delay)
                        else:
                            set_pixel(pixels, x, y, (0, 0, 0), auto_write=False)
                    if max_generations > 0:
                        if x in generations_table and \
                                y in generations_table[x]:
                            generations_table[x][y] += 1
                        else:
                            generations_table[x] = {y: 1}

                        # Adjust the color value to appear dimmer.
                        # We can't control the brightness directly.
                        prev_color = get_pixel(pixels, x, y)
                        # Find next_brightness with prev_brightness,
                        # max_generations, and min_brightness.
                        next_factor = 1 - (1 / max_generations)
                        # next_colors is a tuple of the next color values.
                        next_colors = tuple(
                            int(prev_color[i] * next_factor) for i in range(3))
                        set_pixel(pixels, x, y, next_colors, auto_write=False)
                    if max_generations > 0 and \
                            generations_table[x][y] >= max_generations:
                        if show_log:
                            print(f"Cell at ({x}, {y}) died because it reached the maximum number of generations.")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            set_pixel(pixels, x, y, (255, 0, 0))
                            time.sleep(delay)
                            set_pixel(pixels, x, y, (0, 0, 0))
                            time.sleep(delay)
                        else:
                            set_pixel(pixels, x, y, (0, 0, 0), auto_write=False)
                    # elif show_log:
                    #     print(f"Cell at ({x}, {y}) survived.")
                else:
                    if animations:
                        # Blink the cell for visibility.
                        set_pixel(pixels, x, y, (255, 255, 255))
                        set_pixel(pixels, x, y, (0, 0, 0))
                    if len(live_neighbors) == 3:
                        colors = [
                            get_pixel(pixels, nx, ny) for nx, ny in live_neighbors if
                            get_pixel(pixels, nx, ny) != (0, 0, 0)]

                        # Remove any None values from the list of colors.
                        colors = [
                            color for color in colors if color is not None]
                        r = sum([color[0] for color in colors]) // len(colors)
                        g = sum([color[1] for color in colors]) // len(colors)
                        b = sum([color[2] for color in colors]) // len(colors)
                        if y % 2 == 0:
                            x = abs(x - width)
                        if allow_mutations:
                            chance = random.random()
                            if chance < 0.1:
                                r = random.randint(0, 255)
                                g = random.randint(0, 255)
                                b = random.randint(0, 255)
                                if show_log:
                                    print(f"Cell at ({x}, {y}) will be born as a mutant with color ({r}, {g}, {b})")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            set_pixel(pixels, x, y, (r, g, b))
                            time.sleep(delay)
                        else:
                            set_pixel(pixels, x, y, (r, g, b), auto_write=False)
                        if show_log:
                            print(
                                f"Cell at ({x}, {y}) was born. Color: ({r}, {g}, {b})")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            temp_colors = []
                            for cell_neighbor in all_neighbors:
                                color = get_pixel(pixels,
                                                  cell_neighbor[0],
                                                  cell_neighbor[1])
                                temp_colors.append(color)
                                set_pixel(
                                    pixels,
                                    cell_neighbor[0],
                                    cell_neighbor[1],
                                    (255, 255, 255), auto_write=False)
                            pixels.show()
                            time.sleep(delay * 4)

                            for cell_neighbor, color in zip(
                                    all_neighbors, temp_colors):
                                set_pixel(
                                    pixels,
                                    cell_neighbor[0],
                                    cell_neighbor[1],
                                    color,
                                    auto_write=False)
                            pixels.show()
                            time.sleep(delay)
        # Count the number of live cells.
        live_cells = 0
        for y in range(18):
            for x in range(18):
                if get_pixel(pixels, x, y) != (0, 0, 0):
                    live_cells += 1
        # print(f"Number of live cells: {live_cells}")
        if live_cells == 0:
            if show_log:
                print("All cells are dead. Stopping.")
            game_over(pixels, delay=delay)
            break
        if live_cells < 10 and not allow_visitors:
            if show_log:
                print("Too few live cells. Stopping.")
            game_over(pixels, delay=delay)
            break
        # Add visitors to the grid if the number of live cells is less than
        # the width of the grid or if the grid has stabilized.
        elif live_cells < width and allow_visitors or \
                stale_generations > 10 and allow_visitors:
            # Add a random amount of visitors to the grid in a random spot,
            # but with a limit.
            visitors = random.randint(0, num_pixels // 2)
            visitors_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
            if show_log:
                print(f"Adding {visitors} visitors to the grid with color {visitors_color}")  # noqa: E501  # pylint: disable=line-too-long
            for _ in range(visitors):
                x = random.randint(0, 17)
                y = random.randint(0, 17)
                if get_pixel(pixels, x, y) != (0, 0, 0):
                    pass
                else:
                    set_pixel(pixels, x, y, visitors_color)
                    if animations:
                        time.sleep(delay)
        # Check if the grid has stabilized - Either the same number of live
        # cells or within a margin of error.
        if live_cells == prev_cells or abs(live_cells - prev_cells) < 2:
            stale_generations += 1
        else:
            stale_generations = 0

        if stale_generations > 10:
            if show_log:
                print("Too many stale generations. Stopping.")
            game_over(pixels, delay=delay)
            break
        if show_log:
            print(f"Last generation had {prev_cells} live cells, this generation has {live_cells} live cells.")  # noqa: E501  # pylint: disable=line-too-long
        prev_cells = live_cells

        pixels.show()

        # Delay between generations.
        time.sleep(delay)
    clear_pixels(pixels)
