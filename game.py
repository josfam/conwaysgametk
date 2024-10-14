#!/usr/bin/env python3

"""The rules and internal state for Conways game of life"""

import tkinter as tk
from canvas import GameCanvas
from game_of_life import GameOfLife
from control_panel import ControlPanel


class Game:
    """Represents the game, that is the canvas, plus the game of life rules"""

    def __init__(
        self, root: tk.Tk, game_canvas: GameCanvas, game_of_life: GameOfLife
    ):
        self.root = root
        self.game_canvas = game_canvas
        self.game_of_life = game_of_life
        self.control_panel = ControlPanel(self.root, self.game_of_life)

    def update_game_canvas(self):
        """Redraws the game canvas, based on the current grid state"""
        self.game_canvas.render_canvas()
        # run the game again after 100ms intervals
        if self.game_of_life.update():
            self.game_canvas.render_canvas()
        self.root.after(self.game_of_life.speed, self.update_game_canvas)

    def run(self):
        """Runs the game and updates the canvas"""
        self.update_game_canvas()
