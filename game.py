#!/usr/bin/env python3

"""Runs the game"""

import tkinter as tk
from conway import GameOfLife
from utils.constants import APP_SCREEN_SIZE

# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f'{APP_SCREEN_SIZE}x{APP_SCREEN_SIZE}')
    root.title("Conway's Game of Life")
    game = GameOfLife(root)
    root.mainloop()
