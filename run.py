#!/usr/bin/env python3

"""Runs the game"""

import sys
import tkinter as tk
from canvas import GameCanvas
from game import Game
from game_of_life import GameOfLife
from pathlib import Path
from utils.constants import APP_WIDTH, APP_HEIGHT

def main():
    root = tk.Tk()

    # Handle paths properly when making an executable with PyInstaller
    if getattr(sys, 'frozen', False):  # If the app is frozen (bundled)
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent

    icon_path = base_path / 'assets/icons/conway-lovelace.png'

    # icon_path = Path('./assets/icons/conway-lovelace.png')
    icon = tk.PhotoImage(file=str(icon_path))
    root.iconphoto(True, icon)

    place_app_window(root)
    root.title("Conway's Game of Life")
    root.resizable(False, False)
    # Initialize the game of life logic and canvas for drawing the grid
    game_of_life = GameOfLife()
    game_canvas = GameCanvas(root, game_of_life)

    # Initialize the game and run it
    game = Game(root, game_canvas, game_of_life)

    game.run()
    root.mainloop()

def place_app_window(root: tk.Tk):
    """Places the application window on the user's screen
    at a specific position"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    y_offset = -20  # push the window up a bit (useful for rendering on windows)
    center_x = int(screen_width/2 - APP_WIDTH / 2)
    center_y = int(screen_height/2 - APP_HEIGHT / 2) + y_offset
    root.geometry(f'{APP_WIDTH}x{APP_HEIGHT}+{center_x}+{center_y}')

if __name__ == "__main__":
    main()
