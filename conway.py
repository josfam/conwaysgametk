#!/usr/bin/env python3

"""For classes and functions that enforce the rules and track the internal
state for Conway's game of life"""

import random
import tkinter as tk
from utils.constants import CANVAS_SIZE, CELL_SIZE
from utils.predefined_patterns import PREDEFINED_PATTERNS


class GameOfLife:
    """Represents the rules, and game state for Conway's game of life"""

    def __init__(
        self, width=CANVAS_SIZE, height=CANVAS_SIZE, cell_size=CELL_SIZE
    ):
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # track the previous game state
        self.prev_grid = [
            [0 for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.is_running = False
        self.speed = 100
        self.randomize_grid()

    def get_current_state(self):
        """Returns the current state of the grid."""
        return self.grid

    def toggle_cell(self, event):
        """Toggles the alive state of the cell in this location"""
        if not self.is_running:
            row = event.y // self.cell_size
            col = event.x // self.cell_size
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0

    def load_pattern(self, pattern_name):
        """Load a predefined pattern into the grid."""
        if not self.is_running:
            self.clear_grid()
            pattern = PREDEFINED_PATTERNS[pattern_name]
            start_row = self.rows // 2 - len(pattern) // 2
            start_col = self.cols // 2 - len(pattern[0]) // 2

            for r, row in enumerate(pattern):
                for c, value in enumerate(row):
                    self.grid[start_row + r][start_col + c] = value

    def randomize_grid(self):
        """Randomizes the placement of dead and alive cells within the grid"""
        self.grid = [
            [random.choice([0, 1]) for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def clear_grid(self):
        """Fills the grid with dead cells, thereby clearing it"""
        self.is_running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.prev_grid = [
            [0 for _ in range(self.cols)] for _ in range(self.rows)
        ]  # Reset previous state

    def start(self):
        """Start the game and updates the grid's state"""
        if not self.is_running:
            self.is_running = True
            self.update()

    def stop(self):
        """Stops the game from updating further"""
        if self.is_running:
            self.is_running = False

    def update(self):
        """Update the grid for the next generation based on the rules of the game."""
        if self.is_running:
            self.prev_grid = [
                row[:] for row in self.grid
            ]  # Save the current state
            self.grid = self.next_generation()
            return True
        return False

    def next_generation(self):
        """Returns the new generation of cells, based on the state of
        the old generation, according to the rules of the game"""
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbors = self.count_live_neighbors(row, col)
                if self.grid[row][col] == 1:  # Cell is alive
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[row][col] = 0  # Cell dies
                    else:
                        new_grid[row][col] = 1  # Cell lives
                else:  # Cell is dead
                    if live_neighbors == 3:
                        new_grid[row][col] = 1  # Cell becomes alive
        return new_grid

    def count_live_neighbors(self, row, col):
        """Count the number of live neighbors for a cell"""
        neighbor_steps = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        count = 0
        for neighbor_step in neighbor_steps:
            y_step, x_step = neighbor_step[0], neighbor_step[1]
            neighbor_row, neighbor_col = row + y_step, col + x_step
            inside_canvas = (
                0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols
            )
            if not inside_canvas:
                continue
            if self.grid[neighbor_row][neighbor_col] == 1:
                count += 1
        return count

    def set_speed(self, value):
        """Adjust the speed of the game based on the slider value."""
        self.speed = int(value)
