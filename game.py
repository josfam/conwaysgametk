#!/usr/bin/env python3

import tkinter as tk
import random
from utils.constants import APP_SCREEN_SIZE, CANVAS_SIZE, CELL_SIZE
from utils.predefined_patterns import PREDEFINED_PATTERNS


# Game of Life class
class GameOfLife:
    def __init__(
        self, root, width=CANVAS_SIZE, height=CANVAS_SIZE, cell_size=CELL_SIZE
    ):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.prev_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]  # Track previous state
        self.is_running = False
        self.speed = 100

        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Button styles
        button_style = {
            'bg': 'coral',
            'fg': 'white',
            'font': ('Helvetica', 10, 'bold'),
        }

        # Buttons for controls
        self.start_btn = tk.Button(
            control_frame, text="Start", command=self.start, **button_style
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
            command=self.reset_grid,
            **button_style,
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = tk.Button(
            control_frame, text="Stop", command=self.stop, **button_style
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
        self.speed_slider.set(self.speed)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        # Bind mouse click to toggle cells
        self.canvas.bind("<Button-1>", self.toggle_cell)

        # Use random grid initially
        self.randomize_grid()

    def toggle_cell(self, event):
        if not self.is_running:
            row = event.y // self.cell_size
            col = event.x // self.cell_size
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
            self.draw_grid()

    def load_pattern(self, pattern_name):
        """Load a predefined pattern into the grid."""
        if not self.is_running:
            self.reset_grid()
            pattern = PREDEFINED_PATTERNS[pattern_name]
            start_row = self.rows // 2 - len(pattern) // 2
            start_col = self.cols // 2 - len(pattern[0]) // 2

            for r, row in enumerate(pattern):
                for c, value in enumerate(row):
                    self.grid[start_row + r][start_col + c] = value
            self.draw_grid()

    def randomize_grid(self):
        if not self.is_running:
            self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
            self.draw_grid()

    def reset_grid(self):
        self.is_running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.prev_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]  # Reset previous state
        self.draw_grid()

    def start(self):
        """Start the game and continuously update the grid."""
        if not self.is_running:
            self.is_running = True
            self.update()

    def stop(self):
        self.is_running = False

    def update(self):
        """Update the grid for the next generation based on the rules of the game."""
        if self.is_running:
            self.prev_grid = [row[:] for row in self.grid]  # Save the current state
            self.grid = self.next_generation()
            self.draw_grid()
            self.root.after(self.speed, self.update)

    def next_generation(self):
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
        """Count the number of live neighbors for a cell."""
        neighbors = [
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
        for n in neighbors:
            r, c = row + n[0], col + n[1]
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 1:
                count += 1
        return count

    def draw_grid(self):
        """Draw the current grid state on the canvas."""
        self.canvas.delete("all")
        cell_size = self.cell_size
        draw = self.canvas.create_rectangle

        for row in range(self.rows):
            y1 = row * cell_size
            y2 = y1 + cell_size
            for col in range(self.cols):
                x1 = col * cell_size
                x2 = x1 + cell_size

                # Check for Glider pattern and color it orange during transition
                if self.prev_grid[row][col] == 1 and self.grid[row][col] == 0:  # Cell was alive and now dead
                    fill_color = "orange"
                elif self.grid[row][col] == 1:  # Cell is alive
                    if self.is_glider_cell(row, col):  # Check if it's part of a Glider
                        fill_color = "orange"
                    else:
                        fill_color = "Teal"
                else:
                    fill_color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="gray")

    def is_glider_cell(self, row, col):
        """Check if the cell at (row, col) is part of a Glider pattern."""
        glider = PREDEFINED_PATTERNS["Glider"]
        start_row = self.rows // 2 - len(glider) // 2
        start_col = self.cols // 2 - len(glider[0]) // 2
        
        for r, pattern_row in enumerate(glider):
            for c, value in enumerate(pattern_row):
                if value == 1:
                    if (start_row + r == row) and (start_col + c == col):
                        return True
        return False

    def set_speed(self, value):
        """Adjust the speed of the game based on the slider value."""
        self.speed = int(value)

# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f'{APP_SCREEN_SIZE}x{APP_SCREEN_SIZE}')
    root.title("Conway's Game of Life")
    game = GameOfLife(root)
    root.mainloop()
