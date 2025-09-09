"""
Ripple Plasma effect - ULTRA-OPTIMIZED VERSION
Creates multiple circular ripples with interference patterns.
Maximum performance with pre-calculated lookup tables.
"""
import math
import time
from matrix_modules.utils import set_pixel, ultra_sin, ultra_cos, ultra_sqrt, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def ripple_plasma(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate ripple plasma effect - ULTRA-OPTIMIZED for maximum FPS!
    Reduced complexity with pre-calculated tables and simplified math.
    """
    log_module_start("ripple_plasma", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # REDUCED ripple sources for performance - only 3 instead of 5
    ripple_sources = [
        (width * 0.3, height * 0.3),   # Top-left
        (width * 0.7, height * 0.7),   # Bottom-right  
        (width * 0.5, height * 0.5),   # Center
    ]
    
    # Pre-calculate distances from each ripple source
    source_distances = []
    for src_x, src_y in ripple_sources:
        distances = []
        for y in range(height):
            row = []
            for x in range(width):
                dx = x - src_x
                dy = y - src_y
                # Use integer distance for speed - close enough for small matrix
                dist = int(ultra_sqrt(dx * dx + dy * dy) * 10) / 10  # Round to 0.1
                row.append(dist)
            distances.append(row)
        source_distances.append(distances)
    
    # PRE-CALCULATED color palette - no dynamic generation!
    # Simple blue-to-white water theme
    water_palette = []
    for i in range(256):
        # Simple blue gradient
        intensity = i / 255.0
        if intensity < 0.3:
            # Deep blue
            factor = intensity / 0.3
            r = int(10 * factor)
            g = int(50 + 100 * factor)
            b = int(100 + 100 * factor)
        elif intensity < 0.7:
            # Blue to cyan
            factor = (intensity - 0.3) / 0.4
            r = int(10 + 40 * factor)
            g = int(150 + 80 * factor)
            b = int(200 + 55 * factor)
        else:
            # Cyan to white
            factor = (intensity - 0.7) / 0.3
            r = int(50 + 205 * factor)
            g = int(230 + 25 * factor)
            b = int(255)
        
        water_palette.append((min(255, r), min(255, g), min(255, b)))
    
    # Pre-calculate wave parameters for each source
    wave_speeds = [2.5, 3.2, 2.8]  # Different speeds for variety
    wave_frequencies = [0.4, 0.35, 0.45]  # Different wavelengths
    wave_amplitudes = [1.0, 0.8, 1.2]  # Different strengths
    
    frame = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Pre-calculate wave phases for this frame
        wave_phases = []
        for i, speed in enumerate(wave_speeds):
            wave_phases.append(t * speed)
        
        # Render each pixel - SIMPLIFIED calculation
        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                # Calculate total wave influence - SIMPLIFIED!
                total_wave = 0
                
                # Only calculate from 3 sources instead of 5
                for i in range(3):
                    dist = source_distances[i][y][x]
                    phase = wave_phases[i]
                    frequency = wave_frequencies[i]
                    amplitude = wave_amplitudes[i]
                    
                    # Simple wave calculation - no complex interference
                    wave = ultra_sin(dist * frequency + phase) * amplitude
                    
                    # Simple distance attenuation
                    if dist > 8:
                        wave *= 0.5  # Fade distant waves
                    
                    total_wave += wave
                
                # REMOVED complex interference calculations for speed
                
                # Simple color mapping - no HSV conversion!
                normalized = (total_wave + 3.0) / 6.0  # Map -3 to 3 -> 0 to 1
                normalized = max(0, min(1, normalized))  # Clamp
                
                color_idx = int(normalized * 255)
                color = water_palette[color_idx]
                
                # Simple time-based color shift (much faster than per-pixel)
                time_shift = int(t * 10) % 40
                if time_shift < 20:
                    # Slightly brighter
                    color = (
                        min(255, color[0] + 10),
                        min(255, color[1] + 15),
                        min(255, color[2] + 20)
                    )
                
                pixels[pixel_map[pixel_idx]] = color
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.02)  # 50 FPS target - much faster!
    
    log_module_finish("ripple_plasma", frame_count=frame, duration=time.monotonic() - start_time)