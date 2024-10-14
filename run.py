#!/usr/bin/env python3

"""Runs the game"""

import tkinter as tk
from canvas import GameCanvas
from game import Game
from conway import GameOfLife
from utils.constants import APP_WIDTH, APP_HEIGHT

# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
    root.title("Conway's Game of Life")

    # initialize the game of life logic and canvas for drawing the grid
    game_of_life = GameOfLife()
    game_canvas = GameCanvas(root, game_of_life)

    # initialize the game and run it
    game = Game(root, game_canvas, game_of_life)
    game.run()

    # start the main loop
    root.mainloop()
