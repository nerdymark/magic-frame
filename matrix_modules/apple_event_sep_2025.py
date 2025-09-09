"""
Apple Event September 2025 inspired animation - ULTRA OPTIMIZED.
Uses the glowing blue, orange, and yellow color palette from the Apple logo
with classic plasma movement based on sine wave mathematics.
"""
import math
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def apple_event_sep_2025(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate Apple Event themed plasma effect.
    Maximum optimization for 60+ FPS on microcontrollers.
    """
    log_module_start("apple_event_sep_2025", max_frames=max_frames)
    start_time = time.monotonic()
    
    # High-precision sine lookup table
    LUT_SIZE = 1024
    LUT_MASK = LUT_SIZE - 1
    sine_lut = []
    for i in range(LUT_SIZE):
        angle = (i * 6.28318530718) / LUT_SIZE
        sine_lut.append(math.sin(angle))
    
    # Fast sine lookup
    def fast_sin(x):
        idx = int(x * 162.97466) & LUT_MASK
        return sine_lut[idx]
    
    # Pre-calculate pixel mapping for serpentine layout
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate all static coordinate values
    x_div16 = [x * 0.0625 for x in range(width)]
    y_div8 = [y * 0.125 for y in range(height)]
    xy_div16 = []
    for y in range(height):
        for x in range(width):
            xy_div16.append((x + y) * 0.0625)
    
    # Pre-calculate center distances
    dist_center = []
    cx = width * 0.5
    cy = height * 0.5
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist_center.append(math.sqrt(dx * dx + dy * dy) * 0.125)
    
    # Pre-generate Apple Event color palette with 512 entries
    PALETTE_SIZE = 512
    apple_palette = []
    
    for i in range(PALETTE_SIZE):
        # Map to 0-1 range with sine for smooth transitions
        norm = (math.sin((i / PALETTE_SIZE - 0.25) * 6.28318530718) + 1.0) * 0.5
        
        # Optimized gradient calculation
        if norm < 0.3:
            # Deep to bright blue
            t = norm * 3.333
            r = int(80 * t)
            g = int(50 + 150 * t)
            b = int(150 + 105 * t)
        elif norm < 0.5:
            # Bright blue to cyan
            t = (norm - 0.3) * 5.0
            r = int(80 + 40 * t)
            g = int(200 + 40 * t)
            b = int(255 - 35 * t)
        elif norm < 0.7:
            # Cyan to orange
            t = (norm - 0.5) * 5.0
            r = int(120 + 135 * t)
            g = int(240 - 90 * t)
            b = int(220 - 170 * t)
        elif norm < 0.85:
            # Orange glow
            t = (norm - 0.7) * 6.667
            r = 255
            g = int(150 + 50 * t)
            b = int(50 - 30 * t)
        else:
            # Back to deep blue
            t = (norm - 0.85) * 6.667
            r = int(255 - 255 * t)
            g = int(200 - 150 * t)
            b = int(20 + 130 * t)
        
        apple_palette.append((r, g, b))
    
    frame = 0
    glow_idx = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Time multipliers
        t1 = t * 2.0
        t2 = t * 1.7
        t3 = t * 1.3
        
        # Moving center with lookup table
        mcx = cx + fast_sin(t) * 4.0
        mcy = cy + fast_sin(t * 0.85 + 1.571) * 4.0
        
        # Fast glow effect using lookup
        glow_idx = (glow_idx + 10) & LUT_MASK
        glow = 0.85 + 0.15 * sine_lut[glow_idx]
        
        pixel_idx = 0
        for y in range(height):
            # Pre-calculate per-row value
            y_sin = fast_sin(y_div8[y] + t2)
            
            for x in range(width):
                # Classic plasma with Apple colors
                v1 = fast_sin(x_div16[x] + t1)
                v2 = y_sin
                v3 = fast_sin(xy_div16[pixel_idx] + t3)
                v4 = fast_sin(dist_center[pixel_idx] + t1)
                
                # Fast moving center distance
                dx = x - mcx
                dy = y - mcy
                dist_fast = (abs(dx) + abs(dy)) * 0.09
                v5 = fast_sin(dist_fast)
                
                # Combine and map to palette
                combined = (v1 + v2 + v3 + v4 + v5) * 102.4
                palette_idx = int(combined + t * 100) & 511
                
                # Get color from palette and apply glow
                color = apple_palette[palette_idx]
                pixels[pixel_map[pixel_idx]] = (
                    int(color[0] * glow),
                    int(color[1] * glow),
                    int(color[2] * glow)
                )
                
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
    
    log_module_finish("apple_event_sep_2025", frame_count=frame, duration=time.monotonic() - start_time)