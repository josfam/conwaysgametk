#!/usr/bin/env python3

"""For classes and functions that control the game's other control widgets
(buttons, sliders, etc) that are not related to the content on the game canvas
itself"""

import tkinter as tk
from conway import GameOfLife
from utils.styles import button_style, canvas_colors, font_style
from utils.constants import CANVAS_SIZE, CELL_SIZE
from utils.predefined_patterns import PREDEFINED_PATTERNS


class ControlPanel:
    """Sets up other ui controls (buttons, sliders, etc) that are not part of
    game canvas itself"""

    def __init__(self, root: tk.Tk, game_of_life: GameOfLife):
        self.root = root
        self.game = game_of_life

        # Main frame for control buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(padx=50, side=tk.RIGHT, expand=True)

        # first subframe for choosing patterns
        pattern_control = tk.Frame(self.control_frame)
        pattern_control.pack(pady=10, side='top')

        # large spacer between top and bottom button groups
        spacer = tk.Frame(self.control_frame)
        spacer.pack(pady=50, expand=True)

        # second subframe for controlling canvas simulation
        sim_control = tk.Frame(self.control_frame)
        sim_control.pack(pady=10, side='top')

        # Buttons in pattern control
        self.random_btn = tk.Button(
            # button for random patterns
            pattern_control,
            text="Random",
            command=self.randomize_grid,
            **button_style,
        )

        # Pattern selection dropdown
        self.pattern_var = tk.StringVar(self.root)
        self.pattern_var.set("Select Pattern")  # Default value
        self.pattern_menu = tk.OptionMenu(
            pattern_control,
            self.pattern_var,
            *PREDEFINED_PATTERNS.keys(),
            command=self.load_pattern,
        )
        self.pattern_menu.config(
            **button_style, direction='left'
        )  # Style dropdown
        self.pattern_menu.pack(side=tk.TOP, padx=5, expand=True)

        # buttons in sim control
        self.start_btn = tk.Button(
            # button for starting the simulation
            sim_control,
            text="Start",
            command=self.start_game,
            **button_style,
        ).pack(side=tk.TOP, padx=5)

        self.stop_btn = tk.Button(
            sim_control, text="Stop", command=self.stop_game, **button_style
        )
        self.stop_btn.pack(side=tk.TOP, padx=5)

        self.random_btn.pack(side=tk.TOP, padx=5)
        self.clear_btn = tk.Button(
            sim_control,
            text="Clear",
            command=self.clear_grid,
            **button_style,
        )
        self.clear_btn.pack(side=tk.TOP, padx=5)

    def start_game(self):
        """Starts updating the game state"""
        self.game.start()

    def stop_game(self):
        """Stops updating the game state"""
        self.game.stop()

    def randomize_grid(self):
        """Randomizes the placement of dead and alive cells on the canvas"""
        self.game.randomize_grid()

    def clear_grid(self):
        """Clears the grid"""
        self.game.clear_grid()

    def load_pattern(self, pattern_name):
        """"""
        self.game.load_pattern(pattern_name)

    def set_speed(self, value):
        """Sets the rate at which the simulation renders"""
        self.game.set_speed(value)
