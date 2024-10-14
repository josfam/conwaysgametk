#!/usr/bin/env python3

"""Runs the game"""

import tkinter as tk
from canvas import GameCanvas
from game import Game
from game_of_life import GameOfLife
from pathlib import Path

def main():
    root = tk.Tk()
    icon_path = Path('./assets/icons/conway-lovelace.png')
    icon = tk.PhotoImage(file=str(icon_path))
    root.iconphoto(True, icon)
    print(icon_path)

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set APP_WIDTH and APP_HEIGHT as a percentage of the screen size
    APP_WIDTH = int(80 * screen_width / 100)  # 80% of screen width
    APP_HEIGHT = int(80 * screen_height / 100)  # 80% of screen height

    root.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
    root.title("Conway's Game of Life")

    # Initialize the game of life logic and canvas for drawing the grid
    game_of_life = GameOfLife()
    game_canvas = GameCanvas(root, game_of_life)

    # Initialize the game and run it
    game = Game(root, game_canvas, game_of_life)

    game.run()
    root.mainloop()


if __name__ == "__main__":
    main()
