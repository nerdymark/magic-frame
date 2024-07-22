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
import board
import neopixel

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 324
DEFAULT_BRIGHTNESS = 0.05


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


def set_pixel(x, y, color, brightness=None):
    """
    Set the pixel at the given x, y coordinates to the given color.
    """
    if x < 0 or x >= 18 or y < 0 or y >= 18:
        return
    index = y * 18 + x
    pixels[index] = color
    if brightness is not None:
        pixels.brightness = brightness
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


def john_conways_game_of_life(
        delay=0.5,
        density=None,
        allow_mutations=False,
        allow_visitors=False,
        animations=True):
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

    width = 18
    height = 18
    for y in range(height):
        for x in range(width):
            # Randomly set the initial state of the cell.
            if random.random() < density:
                set_pixel(x, y, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
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
                        # Any live cell with fewer than two live neighbors dies,
                        # as if by underpopulation.
                        # Any live cell with more than three live neighbors dies,
                        # as if by overpopulation.
                        print(f"Cell at ({x}, {y}) died because it had {len(live_neighbors)} live neighbors.")
                        set_pixel(x, y, (255, 0, 0))
                        time.sleep(delay)
                        set_pixel(x, y, (0, 0, 0))
                        time.sleep(delay)
                    # else:
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
                        else:
                            print(f"Row {y} is odd, x is {x}")
                        if allow_mutations:
                            chance = random.random()
                            if chance < 0.1:
                                r = random.randint(0, 255)
                                g = random.randint(0, 255)
                                b = random.randint(0, 255)
                                print(f"Cell at ({x}, {y}) will be born as a mutant with color ({r}, {g}, {b})")
                        set_pixel(x, y, (r, g, b))
                        time.sleep(delay)
                        print(
                            f"Cell at ({x}, {y}) was born. Color: ({r}, {g}, {b})")
                        if animations:
                            for cell_neighbor in all_neighbors:
                                color = get_pixel(cell_neighbor[0],
                                                cell_neighbor[1])
                                set_pixel(
                                    cell_neighbor[0],
                                    cell_neighbor[1],
                                    (255, 255, 255))
                                set_pixel(
                                    cell_neighbor[0],
                                    cell_neighbor[1],
                                    color)
                                time.sleep(delay)
                        time.sleep(delay)
        # Count the number of live cells.
        live_cells = 0
        for y in range(18):
            for x in range(18):
                if get_pixel(x, y) != (0, 0, 0):
                    live_cells += 1
        # print(f"Number of live cells: {live_cells}")
        if live_cells == 0:
            print("All cells are dead. Stopping.")
            break
        if live_cells < 10 and not allow_visitors:
            print("Too few live cells. Stopping.")
            break
        elif live_cells < width and allow_visitors:
            # Add a random amount of visitors to the grid in a random spot, but with a limit.
            visitors = random.randint(0, 100)
            visitors_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            print(f"Adding {visitors} visitors to the grid with color {visitors_color}")
            for _ in range(visitors):
                x = random.randint(0, 17)
                y = random.randint(0, 17)
                set_pixel(x, y, visitors_color)
                time.sleep(delay)
        if live_cells == prev_cells:
            stale_generations += 1
        
        if stale_generations > 10:
            print("Too many stale generations. Stopping.")
            break
        print(f"Last generation had {prev_cells} live cells, this generation has {live_cells} live cells.")
        prev_cells = live_cells

        # Delay between generations.
        time.sleep(delay)


while True:
    john_conways_game_of_life(delay=0, allow_mutations=True, allow_visitors=True, animations=True)

