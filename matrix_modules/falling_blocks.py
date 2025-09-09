"""
An eye-catching falling blocks effect.
A random colored 2x2 block falls from a random position at the top of the screen.
The blocks use gravity to fall to the bottom of the screen, or to the first block they encounter.
Adjacent block colors are affected by the falling block, creating a colorful effect.

Wiring is serpentine, so every other row is reversed.
if y % 2 == 0:
    x = abs(x - width + 1)
"""
import random
import time
from matrix_modules.utils import set_pixel, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT


class FallingBlock:
    def __init__(self, width, height):
        """
        Initialize a falling block.
        """
        # Use even X coordinates for neat stacking (since blocks are 2 wide)
        self.x = random.randrange(0, width-1, 2)  # Start at even coordinates
        self.y = 0
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        self.block_width = 2
        self.block_height = 2
        self.dx = 0  # No horizontal movement
        self.dy = random.uniform(0.35, 0.75)  # Vertical movement only
        self.width = width
        self.height = height
        self.falling = True

    def move(self, settled_blocks):
        """
        Move the block down the screen.
        """
        if self.falling:
            # Only apply vertical movement
            self.y += self.dy

            # Check for collision with bottom of screen
            if self.y + self.block_height >= self.height:
                self.falling = False
                self.y = self.height - self.block_height  # Ensure exact positioning at bottom

            # Check for collision with settled blocks
            elif self.check_collision(settled_blocks):
                self.falling = False
                # Find the highest settled block we're colliding with and land on top
                collision_y = self.height - self.block_height
                for block in settled_blocks:
                    settled_block_x = int(block.x)
                    settled_block_y = int(block.y)
                    block_x = int(self.x)
                    
                    # Check if we overlap horizontally
                    if (block_x < settled_block_x + block.block_width and
                        block_x + self.block_width > settled_block_x):
                        # Land on top of this block
                        collision_y = min(collision_y, settled_block_y - self.block_height)
                
                self.y = max(0, collision_y)

            # Keep within screen bounds
            self.x = max(0, min(self.width - self.block_width, self.x))
            self.y = max(0, min(self.height - self.block_height, self.y))

    def check_collision(self, settled_blocks):
        """
        Check if the block collides with any settled blocks.
        """
        next_y = int(self.y + self.dy)

        # Return early if we'd hit the bottom
        if next_y + self.block_height > self.height:
            return True

        # Check for collision with other blocks
        block_x = int(self.x)
        
        for block in settled_blocks:
            settled_block_x = int(block.x)
            settled_block_y = int(block.y)
            
            # Check if blocks would overlap using bounding box collision
            if (block_x < settled_block_x + block.block_width and
                block_x + self.block_width > settled_block_x and
                next_y < settled_block_y + block.block_height and
                next_y + self.block_height > settled_block_y):
                return True

        return False


def falling_blocks(pixels, width=WIDTH, height=HEIGHT, delay=0, max_frames=100000):
    """
    The main function to run the falling blocks effect.
    
    Parameters:
    - pixels: The NeoPixel or similar object representing the LED matrix
    - width: Width of the LED matrix
    - height: Height of the LED matrix
    - delay: Optional delay between frames (seconds)
    - max_frames: Maximum number of frames to run the animation
    """
    log_module_start("falling_blocks", max_frames=max_frames)
    start_time = time.monotonic()

    # Initialize the falling blocks
    blocks = []
    for _ in range(5):  # Start with fewer blocks
        blocks.append(FallingBlock(width, height))

    # Main animation loop
    frame_count = 0
    settled_blocks = []

    while frame_count < max_frames:
        # Clear the display
        for y in range(height):
            for x in range(width):
                set_pixel(pixels, x, y, (0, 0, 0), auto_write=False)

        # Update and draw settled blocks first
        for block in settled_blocks:
            for dy in range(block.block_height):
                for dx in range(block.block_width):
                    bx = int(block.x) + dx
                    by = int(block.y) + dy
                    if 0 <= bx < width and 0 <= by < height:
                        set_pixel(pixels, bx, by, block.color, auto_write=False)

        # Check if screen is mostly full (75% of screen has blocks)
        # Count how many positions have blocks
        filled_positions = set()
        for block in settled_blocks:
            for dy in range(block.block_height):
                for dx in range(block.block_width):
                    bx = int(block.x) + dx
                    by = int(block.y) + dy
                    if 0 <= bx < width and 0 <= by < height:
                        filled_positions.add((bx, by))
        
        total_positions = width * height
        fill_percentage = len(filled_positions) / total_positions
        
        if fill_percentage >= 0.75:  # Screen is 75% full
            # End the animation - screen is full
            log_module_finish("falling_blocks", frame_count=frame_count, duration=time.monotonic() - start_time)
            break

        # Update and draw all active blocks
        active_blocks = []
        for block in blocks:
            block.move(settled_blocks)

            # Draw the block (2x2 square)
            for dy in range(block.block_height):
                for dx in range(block.block_width):
                    bx = int(block.x) + dx
                    by = int(block.y) + dy
                    if 0 <= bx < width and 0 <= by < height:
                        set_pixel(pixels, bx, by, block.color, auto_write=False)

            # Track blocks that are still falling
            if block.falling:
                active_blocks.append(block)
            else:
                # Snap to grid when landing for neat stacking
                block.x = round(block.x)
                settled_blocks.append(block)

        # Generate new blocks to replace ones that stopped falling
        while len(active_blocks) < 5:  # Keep 5 active blocks
            active_blocks.append(FallingBlock(width, height))

        blocks = active_blocks

        # Show the updated display
        try:
            pixels.show()
        except Exception as e:
            print(f"Error updating display: {e}")
            return frame_count

        # Apply delay if specified
        if delay > 0:
            time.sleep(delay)

        frame_count += 1

    log_module_finish("falling_blocks", frame_count=frame_count, duration=time.monotonic() - start_time)
    return frame_count
