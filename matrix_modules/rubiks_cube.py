"""
Rubik's Cube animation for LED matrix.
Shows a 2D unfolded cross that shuffles and solves.
"""
import random
import time
from matrix_modules.utils import set_pixel, clear_pixels, log_module_start, log_module_finish
from matrix_modules.constants import WIDTH, HEIGHT

# Face colors scaled for LED display
FACE_COLORS = {
    'W': (60, 60, 60),
    'Y': (60, 50, 0),
    'R': (60, 0, 0),
    'O': (60, 25, 0),
    'G': (0, 60, 0),
    'B': (0, 0, 60),
}



class RubiksCube:
    """A 3x3 Rubik's Cube representation"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.faces = {
            'U': [['W'] * 3 for _ in range(3)],
            'D': [['Y'] * 3 for _ in range(3)],
            'L': [['O'] * 3 for _ in range(3)],
            'R': [['R'] * 3 for _ in range(3)],
            'F': [['G'] * 3 for _ in range(3)],
            'B': [['B'] * 3 for _ in range(3)],
        }

    def _rotate_cw(self, face):
        n = len(face)
        rotated = [[face[n - 1 - j][i] for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                face[i][j] = rotated[i][j]

    def move_R(self):
        self._rotate_cw(self.faces['R'])
        temp = [self.faces['F'][i][2] for i in range(3)]
        for i in range(3):
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2 - i][0]
            self.faces['B'][2 - i][0] = self.faces['U'][i][2]
            self.faces['U'][i][2] = temp[i]

    def move_L(self):
        self._rotate_cw(self.faces['L'])
        temp = [self.faces['F'][i][0] for i in range(3)]
        for i in range(3):
            self.faces['F'][i][0] = self.faces['U'][i][0]
            self.faces['U'][i][0] = self.faces['B'][2 - i][2]
            self.faces['B'][2 - i][2] = self.faces['D'][i][0]
            self.faces['D'][i][0] = temp[i]

    def move_U(self):
        self._rotate_cw(self.faces['U'])
        temp = self.faces['F'][0][:]
        self.faces['F'][0] = self.faces['R'][0][:]
        self.faces['R'][0] = self.faces['B'][0][:]
        self.faces['B'][0] = self.faces['L'][0][:]
        self.faces['L'][0] = temp

    def move_D(self):
        self._rotate_cw(self.faces['D'])
        temp = self.faces['F'][2][:]
        self.faces['F'][2] = self.faces['L'][2][:]
        self.faces['L'][2] = self.faces['B'][2][:]
        self.faces['B'][2] = self.faces['R'][2][:]
        self.faces['R'][2] = temp

    def move_F(self):
        self._rotate_cw(self.faces['F'])
        temp = [self.faces['U'][2][i] for i in range(3)]
        for i in range(3):
            self.faces['U'][2][i] = self.faces['L'][2 - i][2]
            self.faces['L'][2 - i][2] = self.faces['D'][0][2 - i]
            self.faces['D'][0][2 - i] = self.faces['R'][i][0]
            self.faces['R'][i][0] = temp[i]

    def move_B(self):
        self._rotate_cw(self.faces['B'])
        temp = [self.faces['U'][0][i] for i in range(3)]
        for i in range(3):
            self.faces['U'][0][i] = self.faces['R'][i][2]
            self.faces['R'][i][2] = self.faces['D'][2][2 - i]
            self.faces['D'][2][2 - i] = self.faces['L'][2 - i][0]
            self.faces['L'][2 - i][0] = temp[i]

    def random_move(self):
        moves = [self.move_R, self.move_L, self.move_U,
                 self.move_D, self.move_F, self.move_B]
        random.choice(moves)()

    def draw(self, pixels):
        """Draw 5-face cross filling the 18x18 grid. 2px per square, no gaps."""
        pixels.fill((0, 0, 0))

        # Layout (each face 6x6 pixels):
        #       [U]         x=6..11, y=0..5
        #  [L]  [F]  [R]    x=0..17, y=6..11
        #       [D]         x=6..11, y=12..17

        face_positions = (
            ('U', 6, 0),
            ('L', 0, 6),
            ('F', 6, 6),
            ('R', 12, 6),
            ('D', 6, 12),
        )

        for face_name, fx, fy in face_positions:
            face = self.faces[face_name]
            for row in range(3):
                for col in range(3):
                    color = FACE_COLORS[face[row][col]]
                    px = fx + col * 2
                    py = fy + row * 2
                    set_pixel(pixels, px, py, color, auto_write=False)
                    set_pixel(pixels, px + 1, py, color, auto_write=False)
                    set_pixel(pixels, px, py + 1, color, auto_write=False)
                    set_pixel(pixels, px + 1, py + 1, color, auto_write=False)

        pixels.show()


def rubiks_cube(pixels, width=WIDTH, height=HEIGHT, delay=0.5, max_frames=1000):
    """
    Animate a Rubik's Cube shuffling itself.
    """
    log_module_start("rubiks_cube", max_frames=max_frames)
    start_time = time.monotonic()

    cube = RubiksCube()
    frame = 0

    # Show solved state
    cube.draw(pixels)
    time.sleep(1.5)

    # Shuffle animation (fast)
    for _ in range(20):
        cube.random_move()
        cube.draw(pixels)
        time.sleep(0.08)

    # Main animation loop
    while frame < max_frames:
        cube.random_move()
        cube.draw(pixels)
        frame += 1
        time.sleep(delay)

        # Occasionally reset to solved state
        if frame % 80 == 0:
            cube.reset()
            cube.draw(pixels)
            time.sleep(1.5)

            # Scramble again
            for _ in range(20):
                cube.random_move()
                cube.draw(pixels)
                time.sleep(0.08)

    duration = time.monotonic() - start_time
    log_module_finish("rubiks_cube", frame_count=frame, duration=duration)
    clear_pixels(pixels)
