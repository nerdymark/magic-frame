"""
nerdymark's magic NeoPixel Picture Frame
REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP1.
* A power source for the NeoPixels.
* A CircuitPython (or MicroPython) board. This example uses the Raspberry Pi Pico W

The LED strip is arranged in a 18x18 grid. The first 18 LEDs is the first row, the next 18 LEDs is the second row, and so on.
"""
import time
import random
import board
import neopixel

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 324
DEFAULT_BRIGHTNESS = 0.01


pixels = neopixel.NeoPixel(board.GP1, NUM_PIXELS, brightness=DEFAULT_BRIGHTNESS, auto_write=False)


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


def john_conways_game_of_life(speed=0.1):
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
    density = 0.15
    grid = [[0 for _ in range(18)] for _ in range(18)]
    for y in range(18):
        for x in range(18):
            # Randomly set the initial state of the cell.
            grid[y][x] = 1 if random.random() < density else 0

    # Run the game of life.
    while True:
        # Display the grid.
        for y in range(18):
            for x in range(18):
                if grid[y][x] == 1:
                    set_pixel(x, y, (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)))
                else:
                    set_pixel(x, y, (0, 0, 0))

        # Create the next generation of the grid.
        new_grid = [[0 for _ in range(18)] for _ in range(18)]
        for y in range(18):
            for x in range(18):
                # Count the number of live neighbors.
                live_neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0:
                            continue
                        if y + dy < 0 or y + dy >= 18 or x + dx < 0 or x + dx >= 18:
                            continue
                        if grid[y + dy][x + dx] == 1:
                            live_neighbors += 1

                # Apply the rules of the game of life.
                if grid[y][x] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[y][x] = 0
                    else:
                        new_grid[y][x] = 1
                else:
                    if live_neighbors == 3:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0

        # Update the grid.
        grid = new_grid

        # If the grid is empty, flash red 3 times and then restart.
        if sum(sum(row) for row in grid) == 0:
            for _ in range(3):
                set_all_pixels((255, 0, 0))
                time.sleep(0.5)
                clear_pixels()
                time.sleep(0.5)
            break

        # Wait before updating the grid.
        time.sleep(speed)


while True:
    john_conways_game_of_life()
