"""Constants to be used in the game"""

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 600
CELL_SIZE = 20
MIN_CELL_SIZE = 5
MAX_CELL_SIZE = 100
ACCEPTED_CELL_SIZES = [
    x for x in range(10, 100)
    if CANVAS_HEIGHT % x == 0
]

print(ACCEPTED_CELL_SIZES)