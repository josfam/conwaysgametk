#!/usr/bin/env python3

import tkinter as tk
import random

# Predefined patterns
PREDEFINED_PATTERNS = {
    "Glider": [[0, 1, 0], [0, 0, 1], [1, 1, 1]],
    "Blinker": [[1, 1, 1]],
    "Block": [[1, 1], [1, 1]],
}

# Game of Life class
class GameOfLife:
    def __init__(self, root, width=600, height=600, cell_size=20):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.generation_history = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.is_running = False
        self.speed = 100

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Button styles
        button_style = {'bg': 'coral', 'fg': 'white', 'font': ('Helvetica', 10, 'bold')}

        # Buttons for controls
        self.start_btn = tk.Button(control_frame, text="Start", command=self.start, **button_style)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.random_btn = tk.Button(control_frame, text="Random", command=self.randomize_grid, **button_style)
        self.random_btn.pack(side=tk.LEFT, padx=5)
        self.reset_btn = tk.Button(control_frame, text="Clear", command=self.reset_grid, **button_style)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop, **button_style)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Pattern selection dropdown
        self.pattern_var = tk.StringVar(self.root)
        self.pattern_var.set("Select Pattern")  # Default value
        self.pattern_menu = tk.OptionMenu(control_frame, self.pattern_var, *PREDEFINED_PATTERNS.keys(), command=self.load_pattern)
        self.pattern_menu.config(bg='coral', fg='white', font=('Helvetica', 10, 'bold'))  # Style dropdown
        self.pattern_menu.pack(side=tk.LEFT, padx=5)

        # Speed control slider
        self.speed_slider = tk.Scale(control_frame, from_=10, to=1000, orient=tk.HORIZONTAL, label="Speed (ms)", command=self.set_speed)
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
            self.generation_history = [[None for _ in range(self.cols)] for _ in range(self.rows)]
            self.draw_grid()

    def reset_grid(self):
        self.is_running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.generation_history = [[None for _ in range(self.cols)] for _ in range(self.rows)]
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
            new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            for row in range(self.rows):
                for col in range(self.cols):
                    live_neighbors = self.count_live_neighbors(row, col)

                    # Game rules
                    if self.grid[row][col] == 1:
                        if live_neighbors < 2 or live_neighbors > 3:
                            new_grid[row][col] = 0
                        else:
                            new_grid[row][col] = 1
                    else:
                        if live_neighbors == 3:
                            new_grid[row][col] = 1

            # Save current grid to history for oscillator/spaceship detection
            self.generation_history = [row[:] for row in self.grid]
            self.grid = new_grid
            self.draw_grid()
            self.root.after(self.speed, self.update)

    def count_live_neighbors(self, row, col):
        """Count the number of live neighbors for a cell."""
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dr, dc in neighbors:
            r, c = row + dr, col + dc
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

                # Color transition to orange for oscillators/spaceships
                if self.generation_history[row][col] == self.grid[row][col] == 1:
                    color = "orange"  # Oscillator/Spaceship detected
                else:
                    color = "Teal" if self.grid[row][col] == 1 else "white"

                draw(x1, y1, x2, y2, fill=color, outline="gray")

    def set_speed(self, value):
        """Adjust the speed of the game based on the slider value."""
        self.speed = int(value)

# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f'{800}x{800}')
    root.title("Conway's Game of Life")
    game = GameOfLife(root)
    root.mainloop()
