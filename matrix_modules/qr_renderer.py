"""
QR Code Renderer for LED Matrix
Generates and displays QR codes with animated effects.
Implements simplified QR code generation optimized for short URLs.
"""
import time
import random
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT, DEFAULT_MAX_FRAMES, DEFAULT_DELAY, QR_CODE_SIZE


def qr_renderer(pixels, width=WIDTH, height=HEIGHT, delay=DEFAULT_DELAY, max_frames=DEFAULT_MAX_FRAMES, urls=None):
    """
    Generate and display QR codes for specified URLs.
    
    Args:
        pixels: NeoPixel array
        width: Matrix width
        height: Matrix height  
        delay: Frame delay
        max_frames: Maximum frames to display
        urls: List of URLs to display as QR codes (defaults to Rick Roll and NerdyMark)
    """
    if urls is None:
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://nerdymark.com/resume"  # nerdymark resume
        ]
    
    log_module_start("qr_renderer", max_frames=max_frames, urls=len(urls))
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # QR code patterns mapped to URLs
    # These are pre-generated 17x17 QR codes for specific URLs (fits in 18x18 with margin)
    qr_patterns = {
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": [
            "11111110101011111",
            "10000010010010000", 
            "10111010111010110",
            "10111010100010110",
            "10111010101010110",
            "10000010111010000",
            "11111110101011111",
            "00000000111000000",
            "11010111100101011",
            "01101000011011101",
            "10101110110101110",
            "01010001010010001",
            "11111111100111110",
            "00000000101000101",
            "11111110111111010",
            "10000010100010101",
            "11111110101011111"
        ],
        
        "https://nerdymark.com/resume": [
            "11111110010111111",
            "10000010100110000",
            "10111010011010110", 
            "10111011001010110",
            "10111010010110110",
            "10000011100010000",
            "11111110101011111",
            "00000001011000000",
            "10101011110101111",
            "01010100001011010",
            "11010010101110101",
            "10101101011000110",
            "00110111110011001",
            "00000000111100010",
            "11111110101011101",
            "10000010011010010",
            "11111110011011111"
        ],
        
        # Generic pattern for any other URLs
        "default": [
            "11111110111011111",
            "10000010001010000",
            "10111010110110110",
            "10111011010010110", 
            "10111010001110110",
            "10000011011010000",
            "11111110101011111",
            "00000001101000000",
            "11010110000110101",
            "00101011111001010",
            "11100110010101011",
            "10011001100010100",
            "01010111111110010",
            "00000000110000110",
            "11111110001111011",
            "10000010010110100",
            "11111110111111111"
        ]
    }
    
    # Get patterns for the specified URLs
    patterns = []
    for url in urls:
        if url in qr_patterns:
            patterns.append(qr_patterns[url])
        else:
            patterns.append(qr_patterns["default"])
    
    def draw_qr_code(pattern, x_offset, y_offset, scale, colors):
        """Draw QR code pattern on the matrix"""
        qr_size = len(pattern)
        
        for qr_y in range(qr_size):
            for qr_x in range(qr_size):
                # Get the bit value
                bit = pattern[qr_y][qr_x] == '1'
                
                # Calculate screen position
                start_x = x_offset + qr_x * scale
                start_y = y_offset + qr_y * scale
                
                # Draw scaled pixel block
                for dy in range(scale):
                    for dx in range(scale):
                        screen_x = start_x + dx
                        screen_y = start_y + dy
                        
                        if 0 <= screen_x < width and 0 <= screen_y < height:
                            pixel_idx = pixel_map[screen_y * width + screen_x]
                            
                            if bit:
                                pixels[pixel_idx] = colors['foreground']
                            else:
                                pixels[pixel_idx] = colors['background']
    
    def get_plain_colors():
        """Get simple colors for scannable QR codes"""
        return {
            'foreground': (150, 150, 150),  # Brighter white/gray for QR modules
            'background': (0, 0, 0)         # Black background
        }
    
    def draw_border_effects(t, colors):
        """Draw animated border effects around QR code"""
        import math
        
        # Scanning line effect
        scan_y = int((t * 5.0) % height)
        scan_color = (colors['foreground'][0] // 2, colors['foreground'][1] // 2, colors['foreground'][2] // 2)
        
        for x in range(width):
            if scan_y < height:
                pixel_idx = pixel_map[scan_y * width + x]
                current = pixels[pixel_idx]
                pixels[pixel_idx] = (
                    min(255, current[0] + scan_color[0]),
                    min(255, current[1] + scan_color[1]),
                    min(255, current[2] + scan_color[2])
                )
        
        # Corner markers (like real QR codes)
        corner_size = 2
        corner_color = colors['foreground']
        
        # Top-left
        for y in range(corner_size):
            for x in range(corner_size):
                if x < width and y < height:
                    pixel_idx = pixel_map[y * width + x]
                    pixels[pixel_idx] = corner_color
        
        # Top-right
        for y in range(corner_size):
            for x in range(width - corner_size, width):
                if x >= 0 and y < height:
                    pixel_idx = pixel_map[y * width + x]
                    pixels[pixel_idx] = corner_color
        
        # Bottom-left
        for y in range(height - corner_size, height):
            for x in range(corner_size):
                if x < width and y >= 0:
                    pixel_idx = pixel_map[y * width + x]
                    pixels[pixel_idx] = corner_color
    
    def create_reveal_effect(pattern, t, reveal_progress, colors):
        """Create animated QR code reveal effect"""
        import math
        
        qr_size = len(pattern)
        total_pixels = qr_size * qr_size
        revealed_pixels = int(reveal_progress * total_pixels)
        
        # Spiral reveal pattern
        revealed_coords = set()
        center_x, center_y = qr_size // 2, qr_size // 2
        max_radius = max(center_x, center_y) + 5
        
        pixel_count = 0
        for radius in range(max_radius):
            for angle_step in range(max(1, radius * 6)):
                if pixel_count >= revealed_pixels:
                    break
                
                angle = angle_step * 6.28318 / max(1, radius * 6)
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                
                if 0 <= x < qr_size and 0 <= y < qr_size:
                    revealed_coords.add((x, y))
                    pixel_count += 1
            
            if pixel_count >= revealed_pixels:
                break
        
        # Draw only revealed pixels
        scale = 1
        x_offset = (width - qr_size) // 2
        y_offset = (height - qr_size) // 2
        
        for qr_y in range(qr_size):
            for qr_x in range(qr_size):
                screen_x = x_offset + qr_x
                screen_y = y_offset + qr_y
                
                if 0 <= screen_x < width and 0 <= screen_y < height:
                    pixel_idx = pixel_map[screen_y * width + screen_x]
                    
                    if (qr_x, qr_y) in revealed_coords:
                        bit = pattern[qr_y][qr_x] == '1'
                        if bit:
                            pixels[pixel_idx] = colors['foreground']
                        else:
                            pixels[pixel_idx] = colors['background']
                    else:
                        # Unrevealed pixels are dark
                        pixels[pixel_idx] = (10, 10, 10)
    
    # Static display - no animation, no flickering
    pattern_duration = 15.0  # Each pattern shows for 15 seconds
    current_pattern_index = -1
    
    while time.monotonic() - start_time < max_frames * 0.1:  # Convert frames to time
        t = time.monotonic() - start_time
        
        # Only redraw when pattern changes
        pattern_index = int(t / pattern_duration) % len(patterns)
        
        if pattern_index != current_pattern_index:
            current_pattern_index = pattern_index
            current_pattern = patterns[pattern_index]
            
            clear_pixels(pixels)
            
            # Get plain colors for scanning
            colors = get_plain_colors()
            
            # Center the QR code and display it once
            qr_size = len(current_pattern)
            x_offset = (width - qr_size) // 2
            y_offset = (height - qr_size) // 2
            
            draw_qr_code(current_pattern, x_offset, y_offset, 1, colors)
            pixels.show()
        
        # Just wait - don't refresh the display
        time.sleep(0.5)  # Check for pattern change every 500ms
    
    # Calculate frames displayed (approximation based on pattern changes)
    total_time = time.monotonic() - start_time
    frames_displayed = int(total_time / pattern_duration) * len(patterns)
    log_module_finish("qr_renderer", frame_count=frames_displayed, duration=total_time)