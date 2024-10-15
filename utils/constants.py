"""Constants to be used in the game"""

import platform

APP_WIDTH = None
APP_HEIGHT = None
CANVAS_HEIGHT = None
CANVAS_WIDTH = None
MIN_CELL_SIZE = 5
MAX_CELL_SIZE = 100

os_type = platform.system().lower()

if 'linux' in os_type or 'darwin' in os_type: # mac and linux
    # A bigger canvas and app width in linux
    APP_WIDTH = 1400
    APP_HEIGHT = 900
    CANVAS_HEIGHT = 800
    CANVAS_WIDTH = 800
else: # windows
    APP_WIDTH = 1200
    APP_HEIGHT = 600
    CANVAS_HEIGHT = 500
    CANVAS_WIDTH = 500

ACCEPTED_CELL_SIZES = [
    x for x in range(10, 100)
    if CANVAS_HEIGHT % x == 0]
CELL_SIZE = ACCEPTED_CELL_SIZES[len(ACCEPTED_CELL_SIZES) // 2]
