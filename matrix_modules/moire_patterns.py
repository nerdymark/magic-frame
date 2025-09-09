"""
Moiré Pattern Effect - Simulated interference patterns from overlapping grids.
Creates authentic moiré patterns using mathematical interference between 
periodic patterns with slight differences in frequency, angle, or phase.
Optimized for LED matrix display with multiple pattern types.
"""
import math
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish, ultra_sin, ultra_cos, ultra_sqrt
from matrix_modules.constants import WIDTH, HEIGHT


def moire_patterns(pixels, width=WIDTH, height=HEIGHT, delay=0.0, max_frames=1000):
    """
    Generate animated moiré patterns using overlapping periodic structures.
    Creates interference patterns between grids, lines, and dots with 
    different frequencies and rotation angles.
    """
    log_module_start("moire_patterns", max_frames=max_frames)
    start_time = time.monotonic()
    
    # Pre-calculate serpentine LED mapping
    pixel_map = []
    for y in range(height):
        for x in range(width):
            if y % 2 == 0:
                pixel_map.append(y * width + (width - 1 - x))
            else:
                pixel_map.append(y * width + x)
    
    # Pre-calculate coordinate system centered at middle
    cx = width / 2.0
    cy = height / 2.0
    
    # Coordinate arrays for optimization
    coord_data = []
    for y in range(height):
        row = []
        for x in range(width):
            # Centered coordinates
            rel_x = x - cx
            rel_y = y - cy
            
            # Polar coordinates
            r = ultra_sqrt(rel_x * rel_x + rel_y * rel_y)
            theta = math.atan2(rel_y, rel_x)
            
            row.append((rel_x, rel_y, r, theta))
        coord_data.append(row)
    
    # Use ultra-fast lookup tables from constants/utils
    def fast_sin(x):
        return ultra_sin(x)
    
    def fast_cos(x):
        return ultra_cos(x)
    
    # Generate different moiré pattern types
    def create_line_moire(x, y, t, pattern_id):
        """Create line-based moiré patterns"""
        if pattern_id == 0:
            # Parallel lines with slight frequency difference
            freq1 = 0.8
            freq2 = 0.85
            angle1 = t * 0.2
            angle2 = t * 0.2 + 0.1
            
            # Rotate coordinates
            x1 = x * fast_cos(angle1) - y * fast_sin(angle1)
            y1 = x * fast_sin(angle1) + y * fast_cos(angle1)
            x2 = x * fast_cos(angle2) - y * fast_sin(angle2)
            y2 = x * fast_sin(angle2) + y * fast_cos(angle2)
            
            # Create line patterns
            pattern1 = fast_sin(x1 * freq1 + t)
            pattern2 = fast_sin(x2 * freq2 + t * 1.1)
            
        elif pattern_id == 1:
            # Curved lines creating complex interference
            freq1 = 0.6
            freq2 = 0.65
            
            pattern1 = fast_sin(x * freq1 + y * 0.1 + t)
            pattern2 = fast_sin(x * freq2 + y * 0.15 + t * 1.2)
            
        else:
            # Radial lines from center
            rel_x, rel_y, r, theta = coord_data[int(y)][int(x)]
            
            freq1 = 12
            freq2 = 13
            
            pattern1 = fast_sin(theta * freq1 + t)
            pattern2 = fast_sin(theta * freq2 + t * 1.3)
        
        # Interference calculation
        return pattern1 * pattern2
    
    def create_grid_moire(x, y, t, pattern_id):
        """Create grid-based moiré patterns"""
        if pattern_id == 0:
            # Square grids with slight rotation
            freq = 0.7
            angle1 = t * 0.1
            angle2 = t * 0.1 + 0.05
            
            # First grid
            x1 = x * fast_cos(angle1) - y * fast_sin(angle1)
            y1 = x * fast_sin(angle1) + y * fast_cos(angle1)
            grid1 = fast_sin(x1 * freq) * fast_sin(y1 * freq)
            
            # Second grid
            x2 = x * fast_cos(angle2) - y * fast_sin(angle2)
            y2 = x * fast_sin(angle2) + y * fast_cos(angle2)
            grid2 = fast_sin(x2 * freq * 1.05) * fast_sin(y2 * freq * 1.05)
            
        elif pattern_id == 1:
            # Hexagonal grid approximation
            freq1 = 0.5
            freq2 = 0.52
            
            # Create hexagonal-like patterns using multiple sine waves
            hex1 = (fast_sin(x * freq1) + 
                   fast_sin((x * 0.5 + y * 0.866) * freq1) + 
                   fast_sin((x * -0.5 + y * 0.866) * freq1)) / 3.0
            
            hex2 = (fast_sin(x * freq2 + t * 0.1) + 
                   fast_sin((x * 0.5 + y * 0.866) * freq2 + t * 0.1) + 
                   fast_sin((x * -0.5 + y * 0.866) * freq2 + t * 0.1)) / 3.0
            
            grid1 = hex1
            grid2 = hex2
            
        else:
            # Diagonal grids
            freq = 0.6
            grid1 = fast_sin((x + y) * freq + t) * fast_sin((x - y) * freq + t)
            grid2 = fast_sin((x + y) * freq * 1.08 + t * 1.1) * fast_sin((x - y) * freq * 1.08 + t * 1.1)
        
        return grid1 * grid2
    
    def create_dot_moire(x, y, t, pattern_id):
        """Create dot-based moiré patterns"""
        rel_x, rel_y, r, theta = coord_data[int(y)][int(x)]
        
        if pattern_id == 0:
            # Circular dot arrays
            freq1 = 1.2
            freq2 = 1.25
            
            # Create dot patterns using distance from grid points
            dot1 = fast_sin(r * freq1 + t) * fast_cos(theta * 8 + t)
            dot2 = fast_sin(r * freq2 + t * 1.1) * fast_cos(theta * 8 + t * 1.1)
            
        elif pattern_id == 1:
            # Square dot arrays
            freq = 1.0
            spacing1 = 3.0
            spacing2 = 3.1
            
            # Create square dot grids
            dot1 = fast_sin(x * spacing1 + t) * fast_sin(y * spacing1 + t)
            dot2 = fast_sin(x * spacing2 + t * 1.2) * fast_sin(y * spacing2 + t * 1.2)
            
        else:
            # Spiral dot patterns
            spiral1 = fast_sin(r * 0.8 + theta * 3 + t)
            spiral2 = fast_sin(r * 0.82 + theta * 3 + t * 1.3)
            dot1 = spiral1
            dot2 = spiral2
        
        return dot1 * dot2
    
    # Color palette generation
    def create_moire_palette(time_offset):
        """Create color palette emphasizing moiré interference patterns"""
        palette = []
        for i in range(256):
            # Map intensity to color
            norm = i / 255.0
            
            # Create high contrast for moiré visibility
            if norm < 0.2:
                # Dark regions
                r = int(norm * 5 * 50)
                g = int(norm * 5 * 30)
                b = int(norm * 5 * 80)
            elif norm < 0.4:
                # Transition
                t = (norm - 0.2) * 5
                r = int(50 + t * 100)
                g = int(30 + t * 150)
                b = int(80 + t * 50)
            elif norm < 0.6:
                # Bright interference bands
                t = (norm - 0.4) * 5
                base_hue = (time_offset * 2 + i) % 360
                # Convert to RGB with high saturation
                hue = base_hue + t * 60
                sat = 0.9
                val = 0.8 + 0.2 * t
                
                # HSV to RGB
                h = hue % 360
                c = val * sat
                x = c * (1 - abs((h / 60) % 2 - 1))
                m = val - c
                
                if h < 60:
                    r, g, b = c, x, 0
                elif h < 120:
                    r, g, b = x, c, 0
                elif h < 180:
                    r, g, b = 0, c, x
                elif h < 240:
                    r, g, b = 0, x, c
                elif h < 300:
                    r, g, b = x, 0, c
                else:
                    r, g, b = c, 0, x
                
                r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
            else:
                # Peak brightness
                t = (norm - 0.6) * 2.5
                r = int(255 - t * 50)
                g = int(255 - t * 30)
                b = int(255 - t * 20)
            
            palette.append((min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b))))
        return palette
    
    frame = 0
    pattern_modes = ['lines', 'grids', 'dots']
    current_mode = 0
    mode_change_time = 0
    
    while frame < max_frames:
        t = time.monotonic() - start_time
        
        # Change pattern type every 8 seconds
        if t - mode_change_time > 8.0:
            current_mode = (current_mode + 1) % len(pattern_modes)
            mode_change_time = t
        
        # Create dynamic color palette
        palette = create_moire_palette(t * 10)
        
        # Calculate which sub-pattern to use
        sub_pattern = int(t / 3) % 3
        
        pixel_idx = 0
        for y in range(height):
            for x in range(width):
                # Generate moiré pattern based on current mode
                if pattern_modes[current_mode] == 'lines':
                    moire_value = create_line_moire(x, y, t, sub_pattern)
                elif pattern_modes[current_mode] == 'grids':
                    moire_value = create_grid_moire(x, y, t, sub_pattern)
                else:  # dots
                    moire_value = create_dot_moire(x, y, t, sub_pattern)
                
                # Enhance moiré visibility with nonlinear mapping
                # Moiré patterns are most visible in interference regions
                enhanced_value = moire_value * moire_value  # Square for contrast
                
                # Add subtle animation to make patterns more dynamic
                animation_offset = fast_sin(t * 1.5 + x * 0.1 + y * 0.1) * 0.2
                final_value = enhanced_value + animation_offset
                
                # Normalize and map to color
                normalized = (final_value + 1.0) / 2.0  # Map -1,1 to 0,1
                color_idx = int(normalized * 255) % 256
                
                # Add time-based color shifting for dynamic effect
                shifted_idx = (color_idx + int(t * 30)) % 256
                
                color = palette[shifted_idx]
                
                # Apply intensity boost to interference patterns
                if abs(moire_value) > 0.7:  # Strong interference
                    boost = 1.3
                    color = (
                        min(255, int(color[0] * boost)),
                        min(255, int(color[1] * boost)),
                        min(255, int(color[2] * boost))
                    )
                
                pixels[pixel_map[pixel_idx]] = color
                pixel_idx += 1
        
        pixels.show()
        frame += 1
        
        if delay > 0:
            time.sleep(delay)
        else:
            time.sleep(0.03)  # ~33 FPS for smooth moiré animation
    
    log_module_finish("moire_patterns", frame_count=frame, duration=time.monotonic() - start_time)