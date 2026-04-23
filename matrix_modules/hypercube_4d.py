"""
4D Hypercube (Tesseract) renderer for LED matrix.
Projects a rotating 4D cube through 3D space onto 2D display.
Based on 4D rendering techniques from computational geometry.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


def hypercube_4d(pixels, width=WIDTH, height=HEIGHT, delay=0.02, max_frames=500):
    """
    Render a rotating 4D hypercube (tesseract) projected onto 2D LED matrix.
    Uses stereographic projection from 4D -> 3D -> 2D.
    """
    log_module_start("hypercube_4d", max_frames=max_frames)
    start_time = time.monotonic()

    # Generate vertices of a 4D hypercube (tesseract)
    # A tesseract has 16 vertices (2^4)
    vertices_4d = []
    for i in range(16):
        x = 1 if i & 1 else -1
        y = 1 if i & 2 else -1
        z = 1 if i & 4 else -1
        w = 1 if i & 8 else -1
        vertices_4d.append([x, y, z, w])

    # Generate edges of tesseract
    # Two vertices are connected if they differ in exactly one coordinate
    edges = []
    for i in range(16):
        for j in range(i + 1, 16):
            # Check if vertices differ in exactly one bit (one coordinate)
            diff = i ^ j
            if diff & (diff - 1) == 0:  # Check if diff is a power of 2
                edges.append((i, j))

    def rotate_4d(point, angle_xy, angle_xz, angle_xw, angle_yz, angle_yw, angle_zw):
        """Rotate a 4D point in multiple planes"""
        x, y, z, w = point

        # XY plane rotation
        cos_xy, sin_xy = math.cos(angle_xy), math.sin(angle_xy)
        x, y = x * cos_xy - y * sin_xy, x * sin_xy + y * cos_xy

        # XZ plane rotation
        cos_xz, sin_xz = math.cos(angle_xz), math.sin(angle_xz)
        x, z = x * cos_xz - z * sin_xz, x * sin_xz + z * cos_xz

        # XW plane rotation (4D specific)
        cos_xw, sin_xw = math.cos(angle_xw), math.sin(angle_xw)
        x, w = x * cos_xw - w * sin_xw, x * sin_xw + w * cos_xw

        # YZ plane rotation
        cos_yz, sin_yz = math.cos(angle_yz), math.sin(angle_yz)
        y, z = y * cos_yz - z * sin_yz, y * sin_yz + z * cos_yz

        # YW plane rotation (4D specific)
        cos_yw, sin_yw = math.cos(angle_yw), math.sin(angle_yw)
        y, w = y * cos_yw - w * sin_yw, y * sin_yw + w * cos_yw

        # ZW plane rotation (4D specific)
        cos_zw, sin_zw = math.cos(angle_zw), math.sin(angle_zw)
        z, w = z * cos_zw - w * sin_zw, z * sin_zw + w * cos_zw

        return [x, y, z, w]

    def project_4d_to_3d(point_4d, distance_4d=3.0):
        """Project 4D point to 3D using perspective projection"""
        x, y, z, w = point_4d
        # Perspective projection from 4D to 3D
        scale = distance_4d / (distance_4d - w)
        return [x * scale, y * scale, z * scale]

    def project_3d_to_2d(point_3d, distance_3d=5.0):
        """Project 3D point to 2D using perspective projection"""
        x, y, z = point_3d
        # Perspective projection from 3D to 2D
        scale = distance_3d / (distance_3d - z)
        return [x * scale, y * scale]

    def draw_line(x0, y0, x1, y1, color, intensity=1.0):
        """Draw a line between two points using Bresenham's algorithm with anti-aliasing"""
        # Scale and center coordinates
        cx, cy = width / 2, height / 2
        scale = min(width, height) / 6  # Scale factor for display

        x0 = int(x0 * scale + cx)
        y0 = int(y0 * scale + cy)
        x1 = int(x1 * scale + cx)
        y1 = int(y1 * scale + cy)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        # Apply intensity to color
        color = tuple(int(c * intensity) for c in color)

        while True:
            if 0 <= x0 < width and 0 <= y0 < height:
                set_pixel(pixels, x0, y0, color, auto_write=False)

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    frame = 0

    while frame < max_frames:
        current_time = time.monotonic() - start_time
        clear_pixels(pixels, auto_write=False)

        # Multiple rotation angles for complex 4D rotation
        angle1 = current_time * 0.5  # XY plane
        angle2 = current_time * 0.3  # XZ plane
        angle3 = current_time * 0.7  # XW plane (4D)
        angle4 = current_time * 0.2  # YZ plane
        angle5 = current_time * 0.4  # YW plane (4D)
        angle6 = current_time * 0.6  # ZW plane (4D)

        # Transform all vertices
        transformed_vertices = []
        for vertex in vertices_4d:
            # Rotate in 4D space
            rotated = rotate_4d(vertex, angle1, angle2, angle3, angle4, angle5, angle6)
            # Project to 3D
            proj_3d = project_4d_to_3d(rotated, distance_4d=3.5)
            # Project to 2D
            proj_2d = project_3d_to_2d(proj_3d, distance_3d=4.0)
            transformed_vertices.append((proj_2d, proj_3d[2], rotated[3]))  # Store 2D pos, depth, and w coordinate

        # Sort edges by average depth for proper rendering order
        edge_depths = []
        for edge in edges:
            v1, v2 = edge
            avg_depth = (transformed_vertices[v1][1] + transformed_vertices[v2][1]) / 2
            avg_w = (transformed_vertices[v1][2] + transformed_vertices[v2][2]) / 2
            edge_depths.append((edge, avg_depth, avg_w))

        # Sort by depth (back to front)
        edge_depths.sort(key=lambda x: -x[1])

        # Draw edges with depth-based coloring and intensity
        for edge_data in edge_depths:
            edge, depth, w_coord = edge_data
            v1, v2 = edge

            # Calculate color based on 4D position (w coordinate)
            # Creates a rainbow effect that shows the 4D nature
            hue = (w_coord + 2) / 4 * 360  # Normalize w from [-2, 2] to [0, 360]

            # Convert HSV to RGB
            h = hue / 60
            c = 1.0
            x = c * (1 - abs((h % 2) - 1))

            if h < 1:
                r, g, b = c, x, 0
            elif h < 2:
                r, g, b = x, c, 0
            elif h < 3:
                r, g, b = 0, c, x
            elif h < 4:
                r, g, b = 0, x, c
            elif h < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x

            # Apply depth-based intensity (farther = dimmer)
            intensity = 0.3 + 0.7 * (1 - (depth + 3) / 6)  # Normalize depth
            intensity = max(0.2, min(1.0, intensity))

            # Edge color with depth and 4D effects
            color = (int(r * 255), int(g * 255), int(b * 255))

            # Draw the edge
            x0, y0 = transformed_vertices[v1][0]
            x1, y1 = transformed_vertices[v2][0]
            draw_line(x0, y0, x1, y1, color, intensity)

        # Draw vertices as bright points
        cx, cy = width / 2, height / 2
        scale = min(width, height) / 6

        for i, (pos_2d, depth, w_coord) in enumerate(transformed_vertices):
            x, y = pos_2d
            px = int(x * scale + cx)
            py = int(y * scale + cy)

            if 0 <= px < width and 0 <= py < height:
                # Vertices glow brighter than edges
                hue = (w_coord + 2) / 4 * 360
                h = hue / 60

                if h < 1:
                    r, g, b = 1, h % 1, 0
                elif h < 2:
                    r, g, b = 2 - h, 1, 0
                elif h < 3:
                    r, g, b = 0, 1, h - 2
                elif h < 4:
                    r, g, b = 0, 4 - h, 1
                elif h < 5:
                    r, g, b = h - 4, 0, 1
                else:
                    r, g, b = 1, 0, 6 - h

                intensity = 0.5 + 0.5 * (1 - (depth + 3) / 6)
                vertex_color = (
                    min(255, int(r * 255 * intensity * 1.5)),
                    min(255, int(g * 255 * intensity * 1.5)),
                    min(255, int(b * 255 * intensity * 1.5))
                )
                set_pixel(pixels, px, py, vertex_color, auto_write=False)

        pixels.show()
        frame += 1

        if delay > 0:
            time.sleep(delay)

    log_module_finish("hypercube_4d", frame_count=frame, duration=time.monotonic() - start_time)