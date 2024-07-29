"""
nerdymark's magic NeoPixel Picture Frame
REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP1.
* A power source for the NeoPixels.
* A CircuitPython (or MicroPython) board. 
  * This example uses the Raspberry Pi Pico W

The LED strip is arranged in a 18x18 grid.
The first 18 LEDs is the first row,
the next 18 LEDs is the second row, and so on.

Odd rows are arranged from left to right,
and even rows are arranged from right to left.
"""
import time
import random
import board  # pylint: disable=import-error
import neopixel  # pylint: disable=import-error

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 324
WIDTH = 18
HEIGHT = 18
DEFAULT_BRIGHTNESS = 0.1


pixels = neopixel.NeoPixel(
    board.GP1,
    NUM_PIXELS,
    brightness=DEFAULT_BRIGHTNESS,
    auto_write=False)


def test_pixels():
    """
    Test the pixels by turning them all red for 1 second.
    """
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()


def set_pixel(x, y, color, brightness=None, auto_write=True):
    """
    Set the pixel at the given x, y coordinates to the given color.
    """
    if x < 0 or x >= 18 or y < 0 or y >= 18:
        return
    index = y * 18 + x
    pixels[index] = color
    if brightness is not None:
        pixels[index].brightness = brightness
    if auto_write:
        pixels.show()


def clear_pixels():
    """
    Clear all the pixels.
    """
    pixels.fill((0, 0, 0))
    pixels.show()


def set_all_pixels(color):
    """
    Set all the pixels to the given color.
    """
    pixels.fill(color)
    pixels.show()


def set_row(y, color):
    """
    Set all the pixels in the given row to the given color.
    """
    for x in range(18):
        set_pixel(x, y, color)


def set_column(x, color):
    """
    Set all the pixels in the given column to the given color.
    """
    for y in range(18):
        set_pixel(x, y, color)


def get_pixel(x, y):
    """
    Get the color of the pixel at the given x, y coordinates.
    """
    if x < 0 or x >= 18 or y < 0 or y >= 18:
        return None
    index = y * 18 + x
    return pixels[index]


def game_over(delay=0.5):
    """
    Flash the pixels red 3 times and then turn them off.
    """
    for _ in range(3):
        set_all_pixels((255, 0, 0))
        pixels.show()
        time.sleep(delay)
        clear_pixels()
        pixels.show()
        time.sleep(delay)
    clear_pixels()
    pixels.show()


def john_conways_game_of_life(
        delay=0.5,
        density=None,
        allow_mutations=False,
        allow_visitors=False,
        show_log=True,
        animations=True,
        max_generations=0):
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
    # Create a 18x18 grid of cells.
    if density is None:
        # Random float between 0 and 1.
        density = random.random()

    width = WIDTH
    height = HEIGHT
    for y in range(height):
        for x in range(width):
            # Randomly set the initial state of the cell.
            if random.random() < density:
                set_pixel(x, y, (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)))
            else:
                set_pixel(x, y, (0, 0, 0))

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
                if get_pixel(nx, ny) != (0, 0, 0) and live_only:
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
                if get_pixel(x, y) != (0, 0, 0):
                    if len(live_neighbors) < 2 or len(live_neighbors) > 3:
                        if show_log:
                            print(f"Cell at ({x}, {y}) died because it had {len(live_neighbors)} live neighbors.")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            set_pixel(x, y, (255, 0, 0))
                            time.sleep(delay)
                            set_pixel(x, y, (0, 0, 0))
                            time.sleep(delay)
                        else:
                            set_pixel(x, y, (0, 0, 0), auto_write=False)
                    if max_generations > 0:
                        if x in generations_table and \
                                y in generations_table[x]:
                            generations_table[x][y] += 1
                        else:
                            generations_table[x] = {y: 1}

                        # Adjust the color value to appear dimmer.
                        # We can't control the brightness directly.
                        prev_color = get_pixel(x, y)
                        # Find next_brightness with prev_brightness,
                        # max_generations, and min_brightness.
                        next_factor = 1 - (1 / max_generations)
                        # next_colors is a tuple of the next color values.
                        next_colors = tuple(
                            int(prev_color[i] * next_factor) for i in range(3))
                        set_pixel(x, y, next_colors, auto_write=False)
                    if max_generations > 0 and \
                            generations_table[x][y] >= max_generations:
                        if show_log:
                            print(f"Cell at ({x}, {y}) died because it reached the maximum number of generations.")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            set_pixel(x, y, (255, 0, 0))
                            time.sleep(delay)
                            set_pixel(x, y, (0, 0, 0))
                            time.sleep(delay)
                        else:
                            set_pixel(x, y, (0, 0, 0), auto_write=False)
                    # elif show_log:
                    #     print(f"Cell at ({x}, {y}) survived.")
                else:
                    if animations:
                        # Blink the cell for visibility.
                        set_pixel(x, y, (255, 255, 255))
                        set_pixel(x, y, (0, 0, 0))
                    if len(live_neighbors) == 3:
                        colors = [
                            get_pixel(nx, ny) for nx, ny in live_neighbors if
                            get_pixel(nx, ny) != (0, 0, 0)]

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
                            set_pixel(x, y, (r, g, b))
                            time.sleep(delay)
                        else:
                            set_pixel(x, y, (r, g, b), auto_write=False)
                        if show_log:
                            print(
                                f"Cell at ({x}, {y}) was born. Color: ({r}, {g}, {b})")  # noqa: E501  # pylint: disable=line-too-long
                        if animations:
                            temp_colors = []
                            for cell_neighbor in all_neighbors:
                                color = get_pixel(cell_neighbor[0],
                                                  cell_neighbor[1])
                                temp_colors.append(color)
                                set_pixel(
                                    cell_neighbor[0],
                                    cell_neighbor[1],
                                    (255, 255, 255), auto_write=False)
                            pixels.show()
                            time.sleep(delay * 4)

                            for cell_neighbor, color in zip(
                                    all_neighbors, temp_colors):
                                set_pixel(
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
                if get_pixel(x, y) != (0, 0, 0):
                    live_cells += 1
        # print(f"Number of live cells: {live_cells}")
        if live_cells == 0:
            if show_log:
                print("All cells are dead. Stopping.")
            game_over(delay=delay)
            break
        if live_cells < 10 and not allow_visitors:
            if show_log:
                print("Too few live cells. Stopping.")
            game_over(delay=delay)
            break
        # Add visitors to the grid if the number of live cells is less than
        # the width of the grid or if the grid has stabilized.
        elif live_cells < width and allow_visitors or \
                stale_generations > 10 and allow_visitors:
            # Add a random amount of visitors to the grid in a random spot,
            # but with a limit.
            visitors = random.randint(0, NUM_PIXELS // 2)
            visitors_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
            if show_log:
                print(f"Adding {visitors} visitors to the grid with color {visitors_color}")  # noqa: E501  # pylint: disable=line-too-long
            for _ in range(visitors):
                x = random.randint(0, 17)
                y = random.randint(0, 17)
                if get_pixel(x, y) != (0, 0, 0):
                    pass
                else:
                    set_pixel(x, y, visitors_color)
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
            game_over(delay=delay)
            break
        if show_log:
            print(f"Last generation had {prev_cells} live cells, this generation has {live_cells} live cells.")  # noqa: E501  # pylint: disable=line-too-long
        prev_cells = live_cells

        pixels.show()

        # Delay between generations.
        time.sleep(delay)
    clear_pixels()


def snake_game(delay=0.5, show_log=True):
    """
    Snake game like from the old Nokia phones.
    Place a dot on the screen. The snake moves around the screen.

    The snake can move up, down, left, or right. The snake grows when it eats
    the dot. The game ends when the snake runs into the wall or itself.
    """
    # Create a 18x18 grid of cells.
    width = WIDTH
    height = HEIGHT
    snake = [(9, 9)]
    directions = ["up", "down", "left", "right"]
    direction = random.choice(directions)
    dot = (random.randint(0, 17), random.randint(0, 17))
    # Odd rows are arranged from left to right,
    # and even rows are arranged from right to left.
    while True:
        # Clear the previous position of the snake, but keep the tail.
        if len(snake) > 1:
            for x, y in snake[:-1]:
                if y % 2 == 0:
                    x = abs(x - width + 1)
                set_pixel(x, y, (0, 0, 0), auto_write=False)
        else:
            for x, y in snake:
                if y % 2 == 0:
                    x = abs(x - width + 1)
                set_pixel(x, y, (0, 0, 0), auto_write=False)

        # Move the snake.
        head = snake[-1]

        # Move towards the dot.
        if dot[1] % 2 == 0:
            dot = (abs(dot[0] - width + 1), dot[1])

        if head[0] < dot[0]:
            direction = "right"
        elif head[0] > dot[0]:
            direction = "left"
        elif head[1] < dot[1]:
            direction = "down"
        elif head[1] > dot[1]:
            direction = "up"
        if show_log:
            print(f"Snake is moving {direction}")

        # Move in the direction, but avoid hitting the wall or itself.
        if direction == "up":
            # Check pixels above the head for snake body.
            if (head[0], head[1] - 1) in snake:
                # Check if the snake can move left or right.
                if head[0] > 0 and (head[0] - 1, head[1]) not in snake:
                    if head[1] % 2 == 0:
                        direction = "left"
                    else:
                        direction = "right"
                elif head[0] < width - 1 and \
                        (head[0] + 1, head[1]) not in snake:
                    if head[1] % 2 == 0:
                        direction = "right"
                    else:
                        direction = "left"
                else:
                    if show_log:
                        print("Snake hit the wall. Game over.")
                    # Clear the screen.
                    game_over(delay=delay)
                    break
        elif direction == "down":
            # Check pixels below the head for snake body.
            if (head[0], head[1] + 1) in snake:
                # Check if the snake can move left or right.
                if head[0] > 0 and (head[0] - 1, head[1]) not in snake:
                    direction = "left"
                elif head[0] < width - 1 and \
                        (head[0] + 1, head[1]) not in snake:
                    direction = "right"
                else:
                    if show_log:
                        print("Snake hit the wall. Game over.")
                    # Clear the screen.
                    game_over(delay=delay)
                    break
        elif direction == "left":
            # Check pixels to the left of the head for snake body.
            if (head[0] - 1, head[1]) in snake:
                # Check if the snake can move up or down.
                if head[1] > 0 and (head[0], head[1] - 1) not in snake:
                    if head[1] % 2 == 0:
                        direction = "up"
                    else:
                        direction = "down"
                elif head[1] < height - 1 and \
                        (head[0], head[1] + 1) not in snake:
                    if head[1] % 2 == 0:
                        direction = "down"
                    else:
                        direction = "up"
                else:
                    if show_log:
                        print("Snake hit the wall. Game over.")
                    # Clear the screen.
                    game_over(delay=delay)
                    break
        elif direction == "right":
            # Check pixels to the right of the head for snake body.
            if (head[0] + 1, head[1]) in snake:
                # Check if the snake can move up or down.
                if head[1] > 0 and (head[0], head[1] - 1) not in snake:
                    direction = "up"
                elif head[1] < height - 1 and \
                        (head[0], head[1] + 1) not in snake:
                    direction = "down"
                else:
                    if show_log:
                        print("Snake hit the wall. Game over.")
                    # Clear the screen.
                    game_over(delay=delay)
                    break

        if direction == "up":
            new_head = (head[0], head[1] - 1)
        elif direction == "down":
            new_head = (head[0], head[1] + 1)
        elif direction == "left":
            new_head = (head[0] - 1, head[1])
        elif direction == "right":
            new_head = (head[0] + 1, head[1])
        # Check if the snake has hit the wall.
        if new_head[0] < 0 or new_head[0] >= width or \
                new_head[1] < 0 or new_head[1] >= height:
            if show_log:
                print("Snake hit the wall. Game over.")
            # Clear the screen.
            game_over(delay=delay)
            break
        # Check if the snake has hit itself.
        if new_head in snake:
            if show_log:
                print("Snake hit itself. Game over.")
            # Clear the screen.
            game_over(delay=delay)
            break
        snake.append(new_head)
        # Check if the snake has eaten the dot.
        if new_head == dot:
            if show_log:
                print("Snake ate the dot.")
            dot = None
        else:
            snake.pop(0)
        # Place the dot on the screen.
        if dot is None:
            dot = (random.randint(0, 17), random.randint(0, 17))
            while dot in snake:
                dot = (random.randint(0, 17), random.randint(0, 17))
        if dot[1] % 2 == 0:
            dot = (abs(dot[0] - width + 1), dot[1])
        set_pixel(dot[0], dot[1], (255, 0, 0), auto_write=False)
        # Place the snake on the screen.
        for x, y in snake:
            if y % 2 == 0:
                x = abs(x - width + 1)
            set_pixel(x, y, (0, 255, 0), auto_write=False)
        pixels.show()
        time.sleep(delay)
    clear_pixels()


def dvd_screen_saver(width=WIDTH, height=HEIGHT, show_log=False, delay=0.5, max_frames=1000):
    """
    TODO: This doesn't work yet
    """
    # Initialize square position and direction
    directions = [
        "down-right", "down-right-right", "down-down-right",
        "down-left", "down-left-left", "down-down-left",
        "up-right", "up-right-right", "up-up-right",
        "up-left", "up-left-left", "up-up-left"
    ]
    square = [(1, 1), (2, 1), (1, 2), (2, 2)]  # Starting position of the square
    # Move the square in a random direction on the x and y axis
    random_offset = (random.randint(0, width - 1), random.randint(0, height - 1))
    square = [(x + random_offset[0], y + random_offset[1]) for x, y in square]

    direction = random.choice(directions)  # Direction of the square
    start_color = (255, 0, 0)  # Color of the square
    frame_number = 0

    while frame_number < max_frames:
        # Clear the screen
        clear_pixels()

        new_square = []
        for x, y in square:
            # if y % 2 == 0:
            #     x = abs(x - width + 1)
            # Move square based on direction
            if direction == "down-right":
                new_square.append((x + 1, y + 1))
            elif direction == "down-right-right":
                new_square.append((x + 2, y + 1))
            elif direction == "down-down-right":
                new_square.append((x + 1, y + 2))
            elif direction == "down-left":
                new_square.append((x - 1, y + 1))
            elif direction == "down-left-left":
                new_square.append((x - 2, y + 1))
            elif direction == "down-down-left":
                new_square.append((x - 1, y + 2))
            elif direction == "up-right":
                new_square.append((x + 1, y - 1))
            elif direction == "up-right-right":
                new_square.append((x + 2, y - 1))
            elif direction == "up-up-right":
                new_square.append((x + 1, y - 2))
            elif direction == "up-left":
                new_square.append((x - 1, y - 1))
            elif direction == "up-left-left":
                new_square.append((x - 2, y - 1))
            elif direction == "up-up-left":
                new_square.append((x - 1, y - 2))

        # Check for wall collisions and adjust direction
        hit_wall = False
        for x, y in new_square:
            # if y % 2 == 0:
            #    x = abs(x - width + 1)
            if x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1:
                hit_wall = True
                break

        # Reflect the square if it hits a wall, but not the corners
        # If direction is in a double direction, reflect the square in a single direction (e.g. down-right-right -> down-left)
        # If direction is in a single direction, reflect the square in a double direction (e.g. down-right -> down-down-left)
        if hit_wall:
            if direction == "down-right":
                direction = "up-up-right"
            elif direction == "down-right-right":
                direction = "up-right-right"
            elif direction == "down-down-right":
                direction = "up-right"
            elif direction == "down-left":
                direction = "up-up-left"
            elif direction == "down-left-left":
                direction = "up-left-left"
            elif direction == "down-down-left":
                direction = "up-left"
            elif direction == "up-right":
                direction = "down-down-right"
            elif direction == "up-right-right":
                direction = "down-right-right"
            elif direction == "up-up-right":
                direction = "down-right"
            elif direction == "up-left":
                direction = "down-down-left"
            elif direction == "up-left-left":
                direction = "down-left-left"
            elif direction == "up-up-left":
                direction = "down-left"

            if show_log:
                print(f"Square hit the wall. New direction: {direction}")

        # Update square position
        square = new_square

        # Break condition for demonstration purposes (replace with actual loop control)
        # break  # Remove or replace with actual condition

        # Display square on screen
        for x, y in square:
            if y % 2 == 0:
                x = abs(x - width + 1)
            set_pixel(x, y, start_color, auto_write=False)

        # Shift rgb along the color wheel,
        # just a little bit for the next square
        # Max value is 255, min value is 0
        # We want to go from Red, Orange, Yellow, Green, Blue, Indigo, Violet
        # red: (255, 0, 0) -> orange: (255, 165, 0) -> yellow: (255, 255, 0) -> green: (0, 128, 0) -> blue: (0, 0, 255) -> indigo: (75, 0, 130) -> violet: (238, 130, 238)

        
        if show_log:
            print(f"start_color: {start_color}, next_color: {next_color}")
        pixels.show()
        frame_number += 1
        time.sleep(delay)


def flag_wave(mode="pride", delay=0.1):
    """
    TODO: This doesn't work yet
    Display a waving flag on the screen.
    """
    width = 18
    height = 18
    if mode == "pride":
        stripes = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
        extras = None
    elif mode == "trans":
        stripes = [(91, 206, 250), (245, 169, 184), (255, 255, 255)]
        extras = None
    elif mode == "usa":
        stripes = [(255, 0, 0), (255, 255, 255)]
        extras = [(0, 0, 255), (255, 255, 255)]

    def wave_flag_pixels(pixels, delay=0.1):
        """
        Wave the flag on the screen. Simulate the flag waving in the wind by taking groups of 3 rows and moving them up and down.
        """
        for row in range(0, height - 2, 3):
            for _ in range(3):
                for y in range(row, row + 3):
                    for x in range(width):
                        if y % 2 == 0:
                            x = abs(x - width + 1)
                        set_pixel(x, y, get_pixel(x, y + 1), auto_write=False)
                pixels.show()
                time.sleep(delay)
            for y in range(row, row + 3):
                for x in range(width):
                    if y % 2 == 0:
                        x = abs(x - width + 1)
                    set_pixel(x, y, (0, 0, 0), auto_write=False)
            pixels.show()


    for stripe in stripes:
        for row in range(height - 1):
            set_row(row, stripe)
            pixels.show()

    if extras is not None:
        if mode == "usa":
            for row in range(0, 9, 2):
                set_row(row, extras[0])
                set_row(row + 1, extras[1])
                pixels.show()

    # Wave the flag.
    while True:
        wave_flag_pixels(pixels, delay=delay)


while True:
    # dvd_screen_saver(delay=0.05, show_log=False, max_frames=1000)
    # flag_wave(mode="pride", delay=0.1)
    snake_game(delay=0.05, show_log=False)
    john_conways_game_of_life(delay=0.05,
                              allow_mutations=True,
                              allow_visitors=True,
                              show_log=False,
                              animations=False,
                              max_generations=10)
