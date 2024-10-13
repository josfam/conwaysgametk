#!/usr/bin/env python3

"""For classes and functions that control the game's canvas display"""

import tkinter as tk
from conway import GameOfLife
from utils.styles import button_style
from utils.constants import CANVAS_SIZE, CELL_SIZE
from utils.predefined_patterns import PREDEFINED_PATTERNS


class GameCanvas:
    """The canvas onto which Conway's Game of Life is shown"""

    def __init__(
        self,
        root: tk.Tk = None,
        game: GameOfLife = None,
        width: int = CANVAS_SIZE,
        height: int = CANVAS_SIZE,
    ):
        self.root = root
        self.game = game
        self.width = width
        self.height = height
        self.rows = height // CELL_SIZE
        self.cols = width // CELL_SIZE
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Buttons for controls
        self.start_btn = tk.Button(
            control_frame,
            text="Start",
            command=self.start_game,
            **button_style,
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.random_btn = tk.Button(
            control_frame,
            text="Random",
            command=self.randomize_grid,
            **button_style,
        )
        self.random_btn.pack(side=tk.LEFT, padx=5)
        self.reset_btn = tk.Button(
            control_frame,
            text="Clear",
            command=self.clear_grid,
            **button_style,
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = tk.Button(
            control_frame, text="Stop", command=self.stop_game, **button_style
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Pattern selection dropdown
        self.pattern_var = tk.StringVar(self.root)
        self.pattern_var.set("Select Pattern")  # Default value
        self.pattern_menu = tk.OptionMenu(
            control_frame,
            self.pattern_var,
            *PREDEFINED_PATTERNS.keys(),
            command=self.load_pattern,
        )
        self.pattern_menu.config(
            bg='coral', fg='white', font=('Helvetica', 10, 'bold')
        )  # Style dropdown
        self.pattern_menu.pack(side=tk.LEFT, padx=5)

        # Speed control slider
        self.speed_slider = tk.Scale(
            control_frame,
            from_=10,
            to=1000,
            orient=tk.HORIZONTAL,
            label="Speed (ms)",
            command=self.set_speed,
        )
        self.speed_slider.set(self.game.speed)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        # Bind mouse click to toggle cells
        self.canvas.bind("<Button-1>", self.game.toggle_cell)

    def start_game(self):
        """Starts updating the game state"""
        self.game.start()

    def stop_game(self):
        """Stops updating the game state"""
        self.game.stop()

    def randomize_grid(self):
        """Randomizes the placement of dead and alive cells on the canvas"""
        self.game.randomize_grid()
        self.render_canvas()

    def clear_grid(self):
        """"""
        self.game.clear_grid()
        self.render_canvas()

    def load_pattern(self, pattern_name):
        self.game.load_pattern(pattern_name)
        self.render_canvas()

    def set_speed(self, value):
        self.game.set_speed(value)

    def render_canvas(self):
        """Renders the current game state onto the canvas"""
        self.canvas.delete("all")
        cell_size = CELL_SIZE
        grid = self.game.get_current_state()

        for row in range(self.rows):
            y1 = row * cell_size
            y2 = y1 + cell_size
            for col in range(self.cols):
                x1 = col * cell_size
                x2 = x1 + cell_size

                # Check for Glider pattern and color it orange during transition
                if (
                    self.game.prev_grid[row][col] == 1
                    and self.game.grid[row][col] == 0
                ):  # Cell was alive and now dead
                    fill_color = "orange"
                elif grid[row][col] == 1:  # Cell is alive
                    fill_color = "Teal"
                else:
                    fill_color = "white"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill_color, outline="gray"
                )
