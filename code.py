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
import random
import board  # pylint: disable=import-error
import neopixel  # pylint: disable=import-error
from matrix_modules import snake_game, john_conways_game_of_life, flag_wave, dvd_screen_saver, \
    the_matrix, blizzard

# Update this to match the number of NeoPixel LEDs connected to your board.
NUM_PIXELS = 324
WIDTH = 18
HEIGHT = 18
DEFAULT_BRIGHTNESS = 0.05


pixels = neopixel.NeoPixel(
    board.GP1,
    NUM_PIXELS,
    brightness=DEFAULT_BRIGHTNESS,
    auto_write=False)


while True:
    blizzard.blizzard(pixels, WIDTH, HEIGHT, delay=0.01, max_frames=1000)
    the_matrix.the_matrix(pixels, WIDTH, HEIGHT, delay=0.01, max_frames=1000)
    flag_wave.flag_wave(pixels, WIDTH, HEIGHT, delay=0.01, mode="trans", duration=10)
    snake_game.snake_game(pixels, WIDTH, HEIGHT, delay=0.0, show_log=False)
    flag_wave.flag_wave(pixels, WIDTH, HEIGHT, delay=0.01, mode="usa", duration=10)
    flag_wave.flag_wave(pixels, WIDTH, HEIGHT, delay=0.01, mode="pride", duration=10)
    dvd_screen_saver.dvd_screen_saver(pixels, WIDTH, HEIGHT, delay=0.01)
    john_conways_game_of_life.john_conways_game_of_life(pixels,
                                                        WIDTH,
                                                        HEIGHT,
                                                        delay=0.01,
                                                        allow_mutations=True,
                                                        allow_visitors=True,
                                                        show_log=False,
                                                        animations=False,
                                                        max_generations=10)

