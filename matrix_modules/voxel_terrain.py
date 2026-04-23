"""
Voxel Terrain - height-map terrain flyover.
Classic Comanche-style voxel rendering on LED matrix.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def voxel_terrain(pixels, width=WIDTH, height=HEIGHT, delay=0.02, max_frames=1500):
    log_module_start("voxel_terrain", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    def terrain_height(wx, wz):
        """Cheap terrain height from summed sines."""
        h = math.sin(wx * 0.3) * 3.0
        h += math.sin(wz * 0.4) * 2.5
        h += math.sin(wx * 0.7 + wz * 0.5) * 1.5
        return h

    def height_color(h, dist):
        """Color based on terrain height and distance."""
        bright = max(0.15, min(1.0, 2.5 / (dist + 1)))
        if h < -2.0:
            # Water
            r, g, b = 0, 10, 50
        elif h < 0.0:
            # Sand/beach
            r, g, b = 40, 35, 10
        elif h < 2.5:
            # Grass
            r, g, b = 0, 45, 10
        elif h < 4.5:
            # Rock
            r, g, b = 35, 25, 15
        else:
            # Snow
            r, g, b = 55, 55, 60
        return (int(r * bright), int(g * bright), int(b * bright))

    sky_color = (0, 0, 12)

    while frame_count < max_frames:
        # Camera position moves forward
        cam_z = frame_count * 0.4
        cam_y = 6.0  # Camera height

        # Clear to sky
        for y in range(height):
            for x in range(width):
                set_pixel(pixels, x, y, sky_color, auto_write=False)

        # For each screen column, cast forward and draw terrain
        for sx in range(width):
            # Column occlusion: track highest drawn pixel (from bottom up)
            max_drawn_y = height

            # Sample terrain at increasing depths
            for d_step in range(20):
                dist = 1.0 + d_step * 1.5
                # World x position (spread columns across view)
                wx = (sx - width / 2.0) * dist / 12.0
                wz = cam_z + dist

                h = terrain_height(wx, wz)

                # Project height to screen y
                if dist < 0.5:
                    continue
                screen_y = int(height / 2.0 + (cam_y - h) * 5.0 / dist)

                # Clamp
                screen_y = max(0, min(height - 1, screen_y))

                # Draw column from screen_y down to max_drawn_y
                if screen_y < max_drawn_y:
                    color = height_color(h, dist)
                    for py in range(screen_y, max_drawn_y):
                        set_pixel(pixels, sx, py, color, auto_write=False)
                    max_drawn_y = screen_y

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("voxel_terrain", frame_count=frame_count, duration=duration)
