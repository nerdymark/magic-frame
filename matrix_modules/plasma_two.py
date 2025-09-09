"""
True plasma effect based on sine wave mathematics - OPTIMIZED.
Implements the classic plasma algorithm using multiple sine functions
combined to create smooth, flowing patterns.
"""
import math
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def plasma_two(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate plasma effect using classic sine wave mathematics.
    Heavily optimized for maximum FPS on microcontrollers.
    """
    log_module_start("plasma_two", max_frames=max_frames)
    start_time = time.monotonic()
    
    # High-precision sine lookup table
    LUT_SIZE = 1024
    LUT_MASK = LUT_SIZE - 1
    sine_lut = []
    for i in range(LUT_SIZE):
        angle = (i * 6.28318530718) / LUT_SIZE  # 2*PI
        sine_lut.append(math.sin(angle))
    
    # Fast sine using lookup table
    def fast_sin(x):
        # Map to 0-1023 range
        idx = int(x * 162.97466) & LUT_MASK  # x * (1024 / 2π)
        return sine_lut[idx]
    
    # Pre-calculate all static values
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate coordinate divisions
    x_div16 = [x * 0.0625 for x in range(width)]  # x/16
    y_div8 = [y * 0.125 for y in range(height)]   # y/8
    xy_div16 = []
    for y in range(height):
        for x in range(width):
            xy_div16.append((x + y) * 0.0625)  # (x+y)/16
    
    # Pre-calculate distances from center (most expensive part)
    dist_center = []
    cx = width * 0.5
    cy = height * 0.5
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            # Store distance/8 directly
            dist_center.append(math.sqrt(dx * dx + dy * dy) * 0.125)
    
    # Pre-calculate color lookup tables
    COLOR_LUT_SIZE = 512
    red_lut = []
    green_lut = []
    blue_lut = []
    for i in range(COLOR_LUT_SIZE):
        phase = (i * 6.28318530718) / COLOR_LUT_SIZE
        red_lut.append(int(128 + 127 * math.sin(phase)))
        green_lut.append(int(128 + 127 * math.sin(phase + 2.094)))
        blue_lut.append(int(128 + 127 * math.sin(phase + 4.188)))
    
    frame = 0
    pixel_idx = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Pre-calculate time factors once per frame
        t1 = t * 2.0
        t2 = t * 1.7
        t3 = t * 1.3
        
        # Moving center calculations
        mcx = cx + fast_sin(t * 1.0) * 4.0
        mcy = cy + fast_sin(t * 0.85 + 1.571) * 4.0  # cos offset
        
        # Pre-calculate time sines for the frame
        sin_t1 = fast_sin(t1)
        sin_t2 = fast_sin(t2)
        sin_t3 = fast_sin(t3)
        
        pixel_idx = 0
        for y in range(height):
            # Pre-calculate y-based values once per row
            y_sin = fast_sin(y_div8[y] + t2)
            
            for x in range(width):
                # Optimized plasma calculation
                # Combine pre-calculated and dynamic values
                
                # Static components with time offset
                v1 = fast_sin(x_div16[x] + t1)
                v2 = y_sin  # Pre-calculated per row
                v3 = fast_sin(xy_div16[pixel_idx] + t3)
                v4 = fast_sin(dist_center[pixel_idx] + t1)
                
                # Moving center component (most expensive)
                dx = x - mcx
                dy = y - mcy
                # Approximate distance with fast calculation
                dist_approx = (abs(dx) + abs(dy)) * 0.09  # Manhattan distance approximation
                v5 = fast_sin(dist_approx)
                
                # Combine all values
                combined = (v1 + v2 + v3 + v4 + v5) * 102.4  # *0.2 * 512 for color LUT
                
                # Fast color lookup
                color_idx = int(combined + t1 * 81.92) & 511  # Modulo 512 with bitmask
                
                # Direct pixel write with pre-calculated mapping
                pixels[pixel_map[pixel_idx]] = (
                    red_lut[color_idx],
                    green_lut[color_idx],
                    blue_lut[color_idx]
                )
                
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        # No delay for maximum speed
        if delay > 0:
            time.sleep(delay)
    
    log_module_finish("plasma_two", frame_count=frame, duration=time.monotonic() - start_time)