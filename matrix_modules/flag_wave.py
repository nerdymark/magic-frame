"""
Display a waving flag on the screen with natural fluid dynamics.
"""
import time
import math
import random
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import FLAG_DURATION_FRAMES, READABLE_DELAY, WIDTH, HEIGHT

def flag_wave(pixels, width=WIDTH, height=HEIGHT, mode="pride", delay=READABLE_DELAY, max_frames=FLAG_DURATION_FRAMES):
    """
    Display a naturally waving flag with realistic fabric physics.
    Uses multiple wave components for more organic motion.
    """
    log_module_start("flag_wave", mode=mode, max_frames=max_frames)

    # Initialize wind simulation parameters
    wind_base = 0.8 + random.random() * 0.4  # Base wind strength
    wind_gust = 0.0  # Current gust strength
    wind_gust_target = 0.0
    wind_turbulence = [random.random() * 0.1 for _ in range(3)]  # Small turbulence components

    stripes = {
        "pride": [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                 (0, 200, 0), (0, 100, 255), (120, 0, 200), (238, 130, 238)],
        "trans": [
            (91, 206, 250),   # Light blue
            (245, 169, 184),  # Pink
            (255, 255, 255),  # White
            (245, 169, 184),  # Pink
            (91, 206, 250)    # Light blue
        ],
        "ukraine": [
            (0, 87, 183),     # Ukrainian blue
            (255, 215, 0)     # Ukrainian yellow
        ],
        "usa": [
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (255, 255, 255),
            (255, 0, 0)
        ],
        "palestine": [
            (0,   0,   0),    # Black  (top third)
            (255, 255, 255),  # White  (middle third)
            (0,  122,  61),   # Green  (bottom third)
        ]
    }

    colors = stripes.get(mode, stripes["pride"])
    stripe_height = height / len(colors)

    def get_stripe_color(y):
        stripe_index = int(y / stripe_height)
        return colors[min(stripe_index, len(colors) - 1)]

    def interpolate_color(color1, color2, factor):
        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor)
        )

    def adjust_brightness(color, factor):
        # Apply factor with some color preservation
        preservation_factor = 0.3
        adjusted_factor = preservation_factor + (1 - preservation_factor) * factor

        return (
            min(255, max(0, int(color[0] * adjusted_factor))),
            min(255, max(0, int(color[1] * adjusted_factor))),
            min(255, max(0, int(color[2] * adjusted_factor)))
        )

    def get_complex_wave(x, y, t, wind_strength):
        """Calculate wave displacement using multiple harmonics for natural motion"""
        # Normalize coordinates
        x_norm = x / width
        y_norm = y / height

        # Primary wave - main flag ripple, stronger at the free edge
        primary = math.sin(x_norm * 2.5 * math.pi + t * 3.5 * wind_strength) * (0.5 + x_norm * 0.5)

        # Secondary wave - adds variation, different frequency
        secondary = math.sin(x_norm * 4.0 * math.pi + t * 5.2 * wind_strength + 1.5) * 0.3 * x_norm

        # Vertical wave component - makes top and bottom wave slightly differently
        vertical = math.sin(y_norm * math.pi * 1.5 + t * 2.8) * 0.15 * x_norm

        # Turbulence - small rapid oscillations for fabric texture
        turb1 = math.sin(x_norm * 12 * math.pi + t * 8.5) * 0.05 * x_norm * wind_turbulence[0]
        turb2 = math.cos(y_norm * 8 * math.pi + t * 7.2) * 0.03 * x_norm * wind_turbulence[1]

        # Combine all wave components with distance-based amplitude
        # Flag is "attached" at left edge (x=0) and free at right edge (x=width)
        # Base amplitude even near the pole so the whole flag moves
        amplitude = (0.8 + 2.5 * x_norm) * (1.0 + wind_strength * 0.5)

        return amplitude * (primary + secondary + vertical + turb1 + turb2)

    def get_lighting_factor(x, y, wave_displacement, normal_x, t):
        """Calculate realistic lighting based on surface normal"""
        # Simulate directional light from top-left
        light_dir_x = 0.7
        light_dir_y = -0.7

        # Approximate surface normal based on wave gradient
        # Normal points "out" of the flag surface
        normal_z = 0.8  # Z component of normal (out of screen)

        # Dot product for lambertian shading
        dot = normal_x * light_dir_x + normal_z * 0.5

        # Add subtle specular highlight for silk-like appearance
        specular = math.pow(max(0, dot), 12) * 0.15

        ambient = 0.55
        diffuse = dot * 0.4

        lighting = ambient + diffuse + specular

        return max(0.45, min(1.2, lighting))

    start_time = time.monotonic()
    frame = 0

    # Pre-calculate wave displacement array for efficiency
    wave_field = [[0.0 for _ in range(width)] for _ in range(height)]

    while frame < max_frames:
        current_time = time.monotonic() - start_time

        # Update wind simulation
        if random.random() < 0.02:  # 2% chance of new gust each frame
            wind_gust_target = random.random() * 0.8
        wind_gust += (wind_gust_target - wind_gust) * 0.05  # Smooth transition
        wind_gust_target *= 0.98  # Decay gust over time

        # Update turbulence slowly
        for i in range(3):
            if random.random() < 0.05:
                wind_turbulence[i] = random.random() * 0.15

        # Current total wind strength
        wind_total = wind_base + wind_gust

        # Pre-calculate wave field for this frame
        for y in range(height):
            for x in range(width):
                wave_field[y][x] = get_complex_wave(x, y, current_time, wind_total)

        # Render pixels with wave displacement and lighting
        for y in range(height):
            for x in range(width):
                # Get wave displacement
                wave_displacement = wave_field[y][x]

                # Calculate surface normal approximation for lighting
                if x > 0:
                    normal_x = wave_field[y][x] - wave_field[y][x-1]
                else:
                    normal_x = wave_field[y][x]

                # Apply wave to y coordinate
                wave_y = y + wave_displacement
                base_y = int(wave_y)
                frac = wave_y - base_y

                # Get color with smooth interpolation
                if 0 <= base_y < height - 1:
                    color1 = get_stripe_color(base_y)
                    color2 = get_stripe_color(base_y + 1)
                    color = interpolate_color(color1, color2, frac)
                elif base_y < 0:
                    color = get_stripe_color(0)
                else:
                    color = get_stripe_color(height - 1)

                # Apply realistic lighting based on surface normal
                lighting = get_lighting_factor(x, y, wave_displacement, normal_x, current_time)
                color = adjust_brightness(color, lighting)

                # USA flag canton (blue field with stars)
                if mode == "usa" and x < width // 3 and y < height // 2:
                    # Simple star pattern with vibrant blue
                    base_color = (0, 100, 255) if (x + y) % 2 == 0 else (255, 255, 255)
                    color = adjust_brightness(base_color, lighting)

                # Palestine flag: red triangle on the hoist side
                if mode == "palestine":
                    tip_x   = 7                        # column where triangle tip meets
                    half_h  = (height - 1) / 2.0
                    if x < tip_x:
                        max_half = half_h * (1.0 - x / tip_x)
                        if abs(y - half_h) <= max_half:
                            color = adjust_brightness((205, 0, 0), lighting)

                set_pixel(pixels, x, y, color, auto_write=False)

        pixels.show()
        frame += 1
        if delay > 0:
            time.sleep(delay)
    
    log_module_finish("flag_wave", frame_count=frame, duration=time.monotonic() - start_time)
