"""
An alluring plasma effect.
Three different colored blobs move around the screen, combining colors when overlapping.
Blobs are randomly generated and move in random directions.
The blobs have diffuse edges, which makes them look like plasma.
"""
import random
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish, ultra_sqrt
from matrix_modules.constants import WIDTH, HEIGHT

def plasma(pixels, width=WIDTH, height=HEIGHT, delay=0, max_frames=100000):
    log_module_start("plasma", max_frames=max_frames)
    start_time = time.monotonic()
    class Blob:
        def __init__(self):
            self.x = random.uniform(0, width - 1)
            self.y = random.uniform(0, height - 1)
            self.color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            self.size = random.uniform(2.5, 4.5)
            self.dx = random.uniform(-0.35, 0.35)
            self.dy = random.uniform(-0.35, 0.35)
        def move(self):
            self.x += self.dx
            self.y += self.dy
            if self.x < 0 or self.x >= width:
                self.dx = -self.dx
                self.x = max(0, min(width - 1, self.x))
            if self.y < 0 or self.y >= height:
                self.dy = -self.dy
                self.y = max(0, min(height - 1, self.y))

    blobs = [Blob() for _ in range(3)]

    for frame in range(max_frames):
        for blob in blobs:
            blob.move()
        blob_params = []
        for blob in blobs:
            blob_params.append((
                blob.x, blob.y,
                blob.color[0], blob.color[1], blob.color[2],
                blob.size * 2
            ))
        for y in range(height):
            for x in range(width):
                r = g = b = 0
                for bx, by, br, bg, bb, bsize in blob_params:
                    dx = abs(bx - x)
                    dy = abs(by - y)
                    if dx > bsize*1.25 or dy > bsize*1.25:
                        continue
                    d2 = (bx - x)**2 + (by - y)**2
                    if d2 >= bsize*bsize*1.56:
                        continue
                    intensity = max(0, 1 - (ultra_sqrt(d2) / max(0.1, bsize)))  # Prevent division by zero
                    r += int(br * intensity)
                    g += int(bg * intensity)
                    b += int(bb * intensity)
                r = min(255, r)
                g = min(255, g)
                b = min(255, b)
                set_pixel(pixels, x, y, (r, g, b), auto_write=False)
        pixels.show()
        if frame % 90 == 0:
            for blob in blobs:
                blob.dx += random.uniform(-0.03, 0.03)
                blob.dy += random.uniform(-0.03, 0.03)
                speed = ultra_sqrt(blob.dx**2 + blob.dy**2)
                if speed > 0.5:
                    factor = 0.5/speed
                    blob.dx *= factor
                    blob.dy *= factor
                elif speed < 0.2:
                    if speed > 0:  # Avoid division by zero
                        factor = 0.2/speed
                        blob.dx *= factor
                        blob.dy *= factor
                    else:
                        # If blob is stopped, give it a small random velocity
                        blob.dx = random.uniform(-0.2, 0.2)
                        blob.dy = random.uniform(-0.2, 0.2)
    
    log_module_finish("plasma", frame_count=max_frames, duration=time.monotonic() - start_time)