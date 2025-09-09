"""
C64 Demoscene Effect - Authentic 80s computer demo with classic effects.
Features scrolling text, plasma fields, bouncing sprites, raster bars, and sine waves.
Inspired by legendary Commodore 64 demoscene productions with authentic styling.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_DELAY, VERY_LONG_MAX_FRAMES


def c64_demoscene(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=VERY_LONG_MAX_FRAMES):
    """
    Generate authentic C64-style demoscene with classic effects:
    - Scrolling text with sine wave motion
    - Multi-layer raster bars  
    - Bouncing C64 logo sprites
    - Plasma field backgrounds
    - Scene transitions with authentic C64 colors
    """
    log_module_start("c64_demoscene", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate coordinate system  
    cx = width / 2.0
    cy = height / 2.0
    
    # Authentic C64 color palette (classic demoscene colors)
    c64_colors = {
        'black': (0, 0, 0),
        'white': (255, 255, 255), 
        'red': (136, 57, 50),
        'cyan': (103, 182, 189),
        'purple': (139, 63, 150),
        'green': (85, 160, 73),
        'blue': (64, 49, 141),
        'yellow': (191, 206, 114),
        'orange': (139, 84, 41),
        'brown': (87, 66, 0),
        'lightred': (184, 105, 98),
        'darkgrey': (80, 80, 80),
        'grey': (120, 120, 120),
        'lightgreen': (148, 224, 137),
        'lightblue': (120, 105, 196),
        'lightgrey': (159, 159, 159)
    }
    
    # Sine lookup table for smooth animations
    sine_lut = [math.sin(i * 2 * math.pi / 256) for i in range(256)]
    
    def fast_sin(x):
        return sine_lut[int(x * 40) % 256]
    
    # 3x3 bitmap font for scrolling text
    font = {
        'C': [0b111, 0b100, 0b111],
        '6': [0b111, 0b101, 0b111], 
        '4': [0b101, 0b111, 0b001],
        ' ': [0b000, 0b000, 0b000],
        'D': [0b110, 0b101, 0b110],
        'E': [0b111, 0b110, 0b111],
        'M': [0b111, 0b111, 0b101],
        'O': [0b111, 0b101, 0b111],
        'S': [0b111, 0b110, 0b111],
        'N': [0b111, 0b111, 0b111],
    }
    
    # Different scenes with timing
    scenes = [
        {'name': 'raster_bars', 'duration': 8, 'colors': ['red', 'yellow', 'green', 'cyan']},
        {'name': 'plasma', 'duration': 10, 'colors': ['blue', 'purple', 'lightblue', 'white']}, 
        {'name': 'bouncing_logo', 'duration': 8, 'colors': ['cyan', 'lightblue', 'white']},
        {'name': 'scrolling_text', 'duration': 12, 'colors': ['lightgreen', 'green', 'yellow']},
    ]
    
    # Scene functions
    def draw_raster_bars(t, colors):
        """Classic demoscene raster bars moving up/down screen"""
        # Multiple colored bars with sine wave motion
        for i, color_name in enumerate(colors):
            color = c64_colors[color_name]
            bar_y = int(cy + 6 * fast_sin(t * 0.7 + i * 2))
            bar_height = 2
            
            for dy in range(-bar_height, bar_height + 1):
                y_pos = bar_y + dy
                if 0 <= y_pos < height:
                    # Intensity based on distance from center
                    intensity = max(0, 1.0 - abs(dy) / bar_height)
                    bar_color = (
                        int(color[0] * intensity),
                        int(color[1] * intensity), 
                        int(color[2] * intensity)
                    )
                    
                    for x in range(width):
                        pixel_idx = pixel_map[y_pos * width + x]
                        current = pixels[pixel_idx]
                        pixels[pixel_idx] = (
                            min(255, current[0] + bar_color[0]),
                            min(255, current[1] + bar_color[1]),
                            min(255, current[2] + bar_color[2])
                        )
    
    def draw_plasma(t, colors):
        """Classic plasma field effect"""
        for y in range(height):
            for x in range(width):
                # Multiple sine waves create plasma field
                val1 = fast_sin(x * 0.5 + t * 2)
                val2 = fast_sin(y * 0.3 + t * 1.5) 
                val3 = fast_sin((x + y) * 0.25 + t)
                val4 = fast_sin(math.sqrt(x*x + y*y) * 0.4 + t * 0.8)
                
                plasma_val = (val1 + val2 + val3 + val4) / 4.0
                
                # Map to colors
                color_idx = int((plasma_val + 1) * len(colors) / 2) % len(colors)
                color = c64_colors[colors[color_idx]]
                
                # Add some intensity variation
                intensity = (plasma_val + 1) / 2.0
                final_color = (
                    int(color[0] * intensity),
                    int(color[1] * intensity),
                    int(color[2] * intensity)
                )
                
                pixel_idx = pixel_map[y * width + x]
                pixels[pixel_idx] = final_color
    
    def draw_bouncing_logo(t, colors):
        """Bouncing C64 logo sprites"""
        # Two bouncing C64 logos
        for i in range(2):
            # Bouncing motion
            logo_x = int(cx + 6 * fast_sin(t * 1.2 + i * 3))
            logo_y = int(cy + 4 * fast_sin(t * 0.8 + i * 2))
            
            color = c64_colors[colors[i % len(colors)]]
            
            # Draw simple "64" sprite (2x3 pixels)
            sprite_64 = [
                [1, 0, 1],  # 6  4
                [1, 1, 1],  # 64 64
            ]
            
            for dy in range(len(sprite_64)):
                for dx in range(len(sprite_64[0])):
                    if sprite_64[dy][dx]:
                        sprite_x = logo_x + dx - 1
                        sprite_y = logo_y + dy - 1
                        
                        if 0 <= sprite_x < width and 0 <= sprite_y < height:
                            pixel_idx = pixel_map[sprite_y * width + sprite_x]
                            pixels[pixel_idx] = color
    
    def draw_scrolling_text(t, colors):
        """Classic scrolling text with sine wave"""
        text = "C64 DEMO"
        scroll_x = int(t * 8) % (len(text) * 4 + width)  # Scroll speed
        
        color = c64_colors[colors[0]]
        
        for i, char in enumerate(text):
            if char in font:
                char_x = width - scroll_x + i * 4
                
                # Sine wave motion for text
                wave_y = int(cy + 3 * fast_sin(t * 2 + i * 0.5))
                
                char_pattern = font[char]
                for row in range(3):
                    for col in range(3):
                        if char_pattern[row] & (1 << (2 - col)):
                            text_x = char_x + col
                            text_y = wave_y + row - 1
                            
                            if 0 <= text_x < width and 0 <= text_y < height:
                                pixel_idx = pixel_map[text_y * width + text_x]
                                pixels[pixel_idx] = color
    
    frame = 0
    scene_start_time = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Determine current scene
        scene_time = t - scene_start_time
        current_scene_idx = 0
        temp_time = 0
        
        for i, scene in enumerate(scenes):
            if temp_time + scene['duration'] > t:
                current_scene_idx = i
                break
            temp_time += scene['duration']
        else:
            # Loop scenes
            current_scene_idx = 0
            scene_start_time = t
            scene_time = 0
        
        scene = scenes[current_scene_idx]
        
        # Clear background to black
        for i in range(len(pixels)):
            pixels[i] = c64_colors['black']
        
        # Draw current scene
        if scene['name'] == 'raster_bars':
            draw_raster_bars(scene_time, scene['colors'])
        elif scene['name'] == 'plasma':
            draw_plasma(scene_time, scene['colors'])
        elif scene['name'] == 'bouncing_logo':
            draw_plasma(scene_time, ['blue', 'darkgrey'])  # Background plasma
            draw_bouncing_logo(scene_time, scene['colors'])  # Logos on top
        elif scene['name'] == 'scrolling_text':
            draw_plasma(scene_time, ['purple', 'black'])  # Dark background
            draw_scrolling_text(scene_time, scene['colors'])
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.08)  # 12 FPS for classic demoscene feel
    
    log_module_finish("c64_demoscene", frame_count=frame, duration=time.monotonic() - start_time)
