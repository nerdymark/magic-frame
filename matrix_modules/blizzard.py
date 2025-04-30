"""
Display a snowstorm on the LED matrix.
"""
import time
import random
from matrix_modules.utils import set_pixel, clear_pixels


def blizzard(pixels, width, height, delay=0.01, max_frames=1000):
    """
    Display a snowstorm on the LED matrix with wind effect and varied flake patterns.
    """
    # Create pixel mapping to handle zigzag wiring pattern
    pixel_map = {}
    for y in range(height):
        for x in range(width):
            # Handle zigzag pattern - odd rows are right to left
            adjusted_x = (width - 1 - x) if y % 2 == 1 else x
            pixel_map[(x, y)] = y * width + adjusted_x
            
    flakes = []  # Each flake is [x, y, intensity, drift, shape]
    
    # Wind effect variables
    wind = 0  # Current wind strength (-1 to 1)
    target_wind = 0  # Target wind strength
    wind_change_delay = 0  # Counter for wind changes
    
    # Function to draw a flake with given shape
    def draw_flake(x, y, intensity, shape):
        if not (0 <= x < width and 0 <= y < height):
            return
            
        # Different snowflake patterns
        if shape == 0:  # Single pixel
            pixels[pixel_map[(x, y)]] = (intensity, intensity, intensity)
        elif shape == 1:  # Small square (if possible)
            pixels[pixel_map[(x, y)]] = (intensity, intensity, intensity)
            if x+1 < width and y+1 < height:
                pixels[pixel_map[(x+1, y)]] = (intensity//2, intensity//2, intensity//2)
                pixels[pixel_map[(x, y+1)]] = (intensity//2, intensity//2, intensity//2)
                pixels[pixel_map[(x+1, y+1)]] = (intensity//2, intensity//2, intensity//2)
        elif shape == 2:  # Diamond/rhombus
            pixels[pixel_map[(x, y)]] = (intensity, intensity, intensity)
            if y > 0:
                pixels[pixel_map[(x, y-1)]] = (intensity//2, intensity//2, intensity//2)
            if x > 0:
                pixels[pixel_map[(x-1, y)]] = (intensity//2, intensity//2, intensity//2)
            if x+1 < width:
                pixels[pixel_map[(x+1, y)]] = (intensity//2, intensity//2, intensity//2)
            if y+1 < height:
                pixels[pixel_map[(x, y+1)]] = (intensity//2, intensity//2, intensity//2)
    
    frame_number = 0
    while frame_number < max_frames:
        clear_pixels(pixels)

        # Wind effect logic
        wind_change_delay -= 1
        if wind_change_delay <= 0:
            target_wind = random.uniform(-0.8, 0.8)
            wind_change_delay = random.randint(30, 100)
        
        wind += (target_wind - wind) * 0.05

        # Add new flakes
        if random.random() < 0.3:
            x = random.randint(0, width-1)
            drift = random.choice([-0.2, 0, 0, 0.2]) + (wind * 0.5)
            intensity = random.randint(100, 255)  # Vary brightness for size impression
            shape = random.randint(0, 2)  # 0=single pixel, 1=square, 2=diamond
            flakes.append([float(x), 0, intensity, drift, shape])

        new_flakes = []
        for flake in flakes:
            x, y, intensity, drift, shape = flake
            
            # Convert to int for display
            int_x = int(x) % width
            int_y = int(y)
            
            # Draw the flake with its shape
            draw_flake(int_x, int_y, intensity, shape)

            # Move flake down and apply drift
            new_drift = drift + (wind * 0.1)
            new_x = x + new_drift
            new_y = y + 1
            
            # Wrap horizontally
            if new_x < 0:
                new_x = width - 1
            elif new_x >= width:
                new_x = 0
                
            # Keep only flakes still on screen
            if new_y < height:
                new_flakes.append([new_x, new_y, intensity, new_drift, shape])

        flakes = new_flakes
        pixels.show()
        time.sleep(delay)
        frame_number += 1
