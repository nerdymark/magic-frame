"""
Sine Wave Scrollers - Classic demoscene bouncing text effect.
Text scrolls horizontally while bouncing vertically following sine waves.
Multiple text strings with different frequencies and amplitudes.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, ultra_sin, ultra_cos
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, SINE_SCROLLERS_MAX_FRAMES, CHAR_WIDTH, CHAR_HEIGHT, CHAR_SPACING


def sine_scrollers(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=SINE_SCROLLERS_MAX_FRAMES):
    """
    Generate sine wave text scrolling effect.
    Text moves horizontally while bouncing on sine wave patterns.
    """
    log_module_start("sine_scrollers", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Simple 3x5 bitmap font for text
    font = {
        'A': [0b111, 0b101, 0b111, 0b101, 0b101],
        'B': [0b110, 0b101, 0b110, 0b101, 0b110],
        'C': [0b111, 0b100, 0b100, 0b100, 0b111],
        'D': [0b110, 0b101, 0b101, 0b101, 0b110],
        'E': [0b111, 0b100, 0b111, 0b100, 0b111],
        'F': [0b111, 0b100, 0b111, 0b100, 0b100],
        'G': [0b111, 0b100, 0b101, 0b101, 0b111],
        'H': [0b101, 0b101, 0b111, 0b101, 0b101],
        'I': [0b111, 0b010, 0b010, 0b010, 0b111],
        'J': [0b111, 0b001, 0b001, 0b101, 0b111],
        'K': [0b101, 0b110, 0b100, 0b110, 0b101],
        'L': [0b100, 0b100, 0b100, 0b100, 0b111],
        'M': [0b101, 0b111, 0b111, 0b101, 0b101],
        'N': [0b101, 0b111, 0b111, 0b111, 0b101],
        'O': [0b111, 0b101, 0b101, 0b101, 0b111],
        'P': [0b111, 0b101, 0b111, 0b100, 0b100],
        'Q': [0b111, 0b101, 0b101, 0b111, 0b001],
        'R': [0b111, 0b101, 0b111, 0b110, 0b101],
        'S': [0b111, 0b100, 0b111, 0b001, 0b111],
        'T': [0b111, 0b010, 0b010, 0b010, 0b010],
        'U': [0b101, 0b101, 0b101, 0b101, 0b111],
        'V': [0b101, 0b101, 0b101, 0b111, 0b010],
        'W': [0b101, 0b101, 0b111, 0b111, 0b101],
        'X': [0b101, 0b101, 0b010, 0b101, 0b101],
        'Y': [0b101, 0b101, 0b111, 0b010, 0b010],
        'Z': [0b111, 0b001, 0b010, 0b100, 0b111],
        '0': [0b111, 0b101, 0b101, 0b101, 0b111],
        '1': [0b010, 0b110, 0b010, 0b010, 0b111],
        '2': [0b111, 0b001, 0b111, 0b100, 0b111],
        '3': [0b111, 0b001, 0b111, 0b001, 0b111],
        '4': [0b101, 0b101, 0b111, 0b001, 0b001],
        '5': [0b111, 0b100, 0b111, 0b001, 0b111],
        '6': [0b111, 0b100, 0b111, 0b101, 0b111],
        '7': [0b111, 0b001, 0b001, 0b001, 0b001],
        '8': [0b111, 0b101, 0b111, 0b101, 0b111],
        '9': [0b111, 0b101, 0b111, 0b001, 0b111],
        ' ': [0b000, 0b000, 0b000, 0b000, 0b000],
        '!': [0b010, 0b010, 0b010, 0b000, 0b010],
        '?': [0b111, 0b001, 0b010, 0b000, 0b010],
        '.': [0b000, 0b000, 0b000, 0b000, 0b010],
        '-': [0b000, 0b000, 0b111, 0b000, 0b000],
        '=': [0b000, 0b111, 0b000, 0b111, 0b000],
    }
    
    # Text messages to scroll
    messages = [
        "HELLO WORLD!",
        "HELLO APPLE!",
        "OH HI MARK!"
    ]
    
    def get_text_width(text):
        """Calculate total width of text in pixels"""
        return len(text) * 4  # 3 pixels per char + 1 space
    
    def draw_char(char, start_x, base_y, color):
        """Draw a single character at given position"""
        if char not in font:
            return
        
        char_pattern = font[char]
        for row in range(5):  # Character height
            for col in range(3):  # Character width
                if char_pattern[row] & (1 << (2 - col)):  # Check bit
                    pixel_x = start_x + col
                    pixel_y = base_y + row
                    
                    if 0 <= pixel_x < width and 0 <= pixel_y < height:
                        pixel_idx = pixel_map[pixel_y * width + pixel_x]
                        pixels[pixel_idx] = color
    
    def draw_text(text, start_x, base_y, color):
        """Draw entire text string"""
        x_pos = start_x
        for char in text:
            draw_char(char, x_pos, base_y, color)
            x_pos += 4  # Move to next character position
    
    # Sine wave parameters for different scrollers
    scrollers = [
        {
            'message': 0,
            'x_pos': width,
            'amplitude': 3,
            'frequency': 0.2,
            'speed': 0.8,
            'base_y': height // 2 - 6,
            'color': (255, 100, 100)  # Red
        },
        {
            'message': 1,
            'x_pos': width + 40,
            'amplitude': 4,
            'frequency': 0.15,
            'speed': 0.6,
            'base_y': height // 2 - 2,
            'color': (100, 255, 100)  # Green
        },
        {
            'message': 2,
            'x_pos': width + 80,
            'amplitude': 2,
            'frequency': 0.3,
            'speed': 1.0,
            'base_y': height // 2 + 2,
            'color': (100, 100, 255)  # Blue
        }
    ]
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Initialize all pixels to black to avoid flicker  
        for y in range(height):
            for x in range(width):
                pixels[pixel_map[y * width + x]] = (0, 0, 0)
        
        # Update and draw each scroller
        for scroller in scrollers:
            # Get current message
            msg_idx = (scroller['message'] + int(t / 15)) % len(messages)
            current_message = messages[msg_idx]
            text_width = get_text_width(current_message)
            
            # Update horizontal position
            scroller['x_pos'] -= scroller['speed']
            
            # Reset position when text completely scrolled off screen
            if scroller['x_pos'] < -text_width:
                scroller['x_pos'] = width + 20
                scroller['message'] = (scroller['message'] + 1) % len(messages)
            
            # Calculate vertical position using sine wave
            sine_offset = scroller['amplitude'] * ultra_sin(
                (scroller['x_pos'] + t * 10) * scroller['frequency']
            )
            
            # Add secondary sine wave for more complex motion
            sine_offset += scroller['amplitude'] * 0.3 * ultra_sin(
                (scroller['x_pos'] + t * 5) * scroller['frequency'] * 2.3
            )
            
            final_y = int(scroller['base_y'] + sine_offset)
            
            # Draw the text
            draw_text(current_message, int(scroller['x_pos']), final_y, scroller['color'])
            
            # Add glowing effect
            if frame % 20 < 10:  # Periodic glow
                glow_color = (
                    scroller['color'][0] // 3,
                    scroller['color'][1] // 3, 
                    scroller['color'][2] // 3
                )
                draw_text(current_message, int(scroller['x_pos']), final_y + 1, glow_color)
                draw_text(current_message, int(scroller['x_pos']), final_y - 1, glow_color)
        
        # Add background starfield effect
        if frame % 5 == 0:
            for _ in range(3):
                star_x = int((t * 20 + frame * 7) % width)
                star_y = int((t * 15 + frame * 11) % height)
                if 0 <= star_x < width and 0 <= star_y < height:
                    pixel_idx = pixel_map[star_y * width + star_x]
                    current = pixels[pixel_idx]
                    if current == (0, 0, 0):  # Only draw on empty pixels
                        pixels[pixel_idx] = (30, 30, 30)  # Dim stars
        
        # Add border effect
        border_color = (50, 50, 50)
        border_flash = int(50 + 50 * ultra_sin(t * 3))
        flash_color = (border_flash, border_flash, 0)
        
        # Top and bottom borders
        for x in range(width):
            if frame % 100 < 20:  # Periodic flash
                pixels[pixel_map[0 * width + x]] = flash_color
                pixels[pixel_map[(height-1) * width + x]] = flash_color
            else:
                pixels[pixel_map[0 * width + x]] = border_color
                pixels[pixel_map[(height-1) * width + x]] = border_color
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.05)  # 20 FPS for readable text scrolling
    
    log_module_finish("sine_scrollers", frame_count=frame, duration=time.monotonic() - start_time)