"""
Common utility functions for the LED matrix.
"""
import time

def test_pixels(pixels):
    """
    Test the pixels by turning them all red for 1 second.
    """
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()


def set_pixel(pixels, x, y, color, brightness=None, auto_write=True):
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


def clear_pixels(pixels):
    """
    Clear all the pixels.
    """
    pixels.fill((0, 0, 0))
    pixels.show()


def set_all_pixels(pixels, color):
    """
    Set all the pixels to the given color.
    """
    pixels.fill(color)
    pixels.show()


def set_row(pixels, y, color):
    """
    Set all the pixels in the given row to the given color.
    """
    for x in range(18):
        set_pixel(pixels, x, y, color)


def set_column(pixels, x, color):
    """
    Set all the pixels in the given column to the given color.
    """
    for y in range(18):
        set_pixel(pixels, x, y, color)


def get_pixel(pixels, x, y):
    """
    Get the color of the pixel at the given x, y coordinates.
    """
    if x < 0 or x >= 18 or y < 0 or y >= 18:
        return None
    index = y * 18 + x
    return pixels[index]


def game_over(pixels, delay=0.5):
    """
    Flash the pixels red 3 times and then turn them off.
    """
    for _ in range(3):
        # set_all_pixels((255, 0, 0))
        pixels.show()
        time.sleep(delay)
        clear_pixels(pixels)
        pixels.show()
        time.sleep(delay)
    clear_pixels(pixels)
    pixels.show()