#!/usr/bin/env python3

"""For classes and functions that control the game's canvas display"""

import tkinter as tk
from game_of_life import GameOfLife
from utils.styles import button_style, canvas_colors, font_style
from utils.constants import CANVAS_WIDTH, CANVAS_HEIGHT, ACCEPTED_CELL_SIZES
from utils.predefined_patterns import PREDEFINED_PATTERNS


class GameCanvas:
    """The canvas onto which Conway's Game of Life is shown"""

    def __init__(
        self,
        root: tk.Tk = None,
        game: GameOfLife = None,
    ):
        self.root = root
        self.game = game
        self.width = CANVAS_WIDTH
        self.height = CANVAS_HEIGHT
        self.rows = self.height // self.game.cell_size
        self.cols = self.width // self.game.cell_size

        # canvas and speed slider frame
        canvas_slider = tk.Frame(self.root)
        canvas_slider.pack(padx=20, pady=20, side=tk.LEFT, expand=True)

        self.canvas = tk.Canvas(
            canvas_slider, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack(anchor=tk.CENTER, expand=True, side=tk.LEFT)

        # frame for slider and label
        slider_label = tk.Frame(canvas_slider)
        slider_label.pack(side=tk.LEFT)

        # Speed control slider
        self.speed_slider = tk.Scale(
            slider_label,
            from_=1000,
            to=10,
            resolution=30,  # a step of 50 units
            orient=tk.VERTICAL,
            command=self.set_speed,
            length=CANVAS_WIDTH // 2,
            relief=tk.FLAT,
            troughcolor=canvas_colors.get('default').get('slider_trough'),
        )
        self.speed_slider.set(self.game.speed)
        self.speed_slider.pack(side=tk.TOP, expand=True)

        # add custom speed label alongside the slider
        speed_text = tk.Label(
            slider_label, text='delay (ms)', font=font_style.get('default')
        ).pack(side=tk.TOP, expand=True, ipadx=30)
        self.bind_keys()

    def bind_keys(self):
        """Initializes all the key binds for the game"""
        # Bind mouse click to toggle cells
        self.canvas.bind("<Button-1>", self.game.toggle_cell)
        # Bind up and down arrows to setting the grid size
        self.root.bind('<Up>', self.increase_cell_size)
        self.root.bind('<Down>', self.decrease_cell_size)

    def increase_cell_size(self, event=None):
        """Increases the size of cells in the game"""
        current = self.game.cell_size
        try:
            _next = ACCEPTED_CELL_SIZES[ACCEPTED_CELL_SIZES.index(current) + 1]
            self.set_cell_size(_next)
        except IndexError:
            return

    def decrease_cell_size(self, event=None):
        """Decreases the size of cells in the game"""
        current = self.game.cell_size
        try:
            _next = ACCEPTED_CELL_SIZES[ACCEPTED_CELL_SIZES.index(current) - 1]
            self.set_cell_size(_next)
        except IndexError:
            return

    def set_cell_size(self, new_cell_size):
        self.game.set_cell_size(new_cell_size)

    def set_speed(self, value):
        self.game.set_speed(value)

    def render_canvas(self, colors=canvas_colors.get('default')):
        """Renders the current game state onto the canvas"""
        self.canvas.delete("all")
        cell_size = self.game.cell_size
        print(f'[canvas.py,render_canvas]: cell size now = {cell_size}')
        grid = self.game.get_current_state()

        rows = self.game.rows
        cols = self.game.cols

        for row in range(rows):
            y1 = row * cell_size
            y2 = y1 + cell_size
            for col in range(cols):
                x1 = col * cell_size
                x2 = x1 + cell_size

                # Check for Glider pattern and color it orange during transition
                if (
                    self.game.prev_grid[row][col] == 1
                    and self.game.grid[row][col] == 0
                ):  # Cell was alive and now dead
                    fill_color = colors.get('just_died')
                elif grid[row][col] == 1:  # Cell is alive
                    fill_color = colors.get('alive')
                else:
                    fill_color = colors.get('dead')

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill_color,
                    outline=colors.get('cell_border'),
                )
