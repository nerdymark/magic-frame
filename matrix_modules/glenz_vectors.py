"""
Glenz Vectors - transparent 3D rotating polygons.
Classic demoscene effect with see-through colored faces.
"""
import math
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish, SERPENTINE_MAP
from matrix_modules.constants import WIDTH, HEIGHT


def glenz_vectors(pixels, width=WIDTH, height=HEIGHT, delay=0.02, max_frames=1500):
    log_module_start("glenz_vectors", max_frames=max_frames)
    start_time = time.monotonic()
    frame_count = 0

    cx = width / 2.0
    cy = height / 2.0
    size = 6.0
    fov = 18.0

    # Cube vertices
    verts = (
        (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
    )

    # Faces: (vertex indices, r, g, b) - dim colors for additive blending
    faces = (
        ((0, 1, 2, 3), 20, 0, 0),     # Front - red
        ((4, 5, 6, 7), 0, 0, 20),     # Back - blue
        ((0, 1, 5, 4), 0, 20, 0),     # Top - green
        ((2, 3, 7, 6), 20, 20, 0),    # Bottom - yellow
        ((0, 3, 7, 4), 20, 0, 20),    # Left - magenta
        ((1, 2, 6, 5), 0, 20, 20),    # Right - cyan
    )

    while frame_count < max_frames:
        pixels.fill((0, 0, 0))

        t = frame_count * 0.03
        sa = math.sin(t)
        ca = math.cos(t)
        sb = math.sin(t * 0.7)
        cb = math.cos(t * 0.7)

        # Transform vertices
        proj = []
        for vx, vy, vz in verts:
            sx = vx * size
            sy = vy * size
            sz = vz * size
            # Rotate Y
            rx = sx * ca + sz * sa
            rz = -sx * sa + sz * ca
            # Rotate X
            ry = sy * cb - rz * sb
            rz2 = sy * sb + rz * cb
            # Project
            z_off = rz2 + fov
            if z_off < 1:
                z_off = 1
            scale = fov / z_off
            px = int(cx + rx * scale)
            py = int(cy + ry * scale)
            proj.append((px, py))

        # Draw each face as filled polygon with additive blending
        for vindices, fr, fg, fb in faces:
            # Get projected face vertices
            fverts = [proj[i] for i in vindices]

            # Simple scanline fill
            min_y = max(0, min(v[1] for v in fverts))
            max_y = min(height - 1, max(v[1] for v in fverts))

            nv = len(fverts)
            for y in range(min_y, max_y + 1):
                # Find x intersections
                xs = []
                for i in range(nv):
                    x0, y0 = fverts[i]
                    x1, y1 = fverts[(i + 1) % nv]
                    if y0 == y1:
                        continue
                    if (y0 <= y < y1) or (y1 <= y < y0):
                        t_edge = (y - y0) / (y1 - y0)
                        xs.append(int(x0 + t_edge * (x1 - x0)))
                if len(xs) < 2:
                    continue
                xs.sort()
                x_start = max(0, xs[0])
                x_end = min(width - 1, xs[-1])
                for x in range(x_start, x_end + 1):
                    idx = SERPENTINE_MAP[y * width + x]
                    cr, cg, cb = pixels[idx]
                    pixels[idx] = (
                        min(255, cr + fr),
                        min(255, cg + fg),
                        min(255, cb + fb),
                    )

        # Draw edges in bright white
        edges = ((0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7))
        for i0, i1 in edges:
            x0, y0 = proj[i0]
            x1, y1 = proj[i1]
            # Bresenham line
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx_s = 1 if x0 < x1 else -1
            sy_s = 1 if y0 < y1 else -1
            err = dx - dy
            while True:
                if 0 <= x0 < width and 0 <= y0 < height:
                    set_pixel(pixels, x0, y0, (60, 60, 60), auto_write=False)
                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x0 += sx_s
                if e2 < dx:
                    err += dx
                    y0 += sy_s

        pixels.show()
        frame_count += 1
        if delay > 0:
            time.sleep(delay)

    duration = time.monotonic() - start_time
    clear_pixels(pixels)
    log_module_finish("glenz_vectors", frame_count=frame_count, duration=duration)
