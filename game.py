#!/usr/bin/env python3

import tkinter as tk
import random

# Game of Life class
class GameOfLife:
    def __init__(self, root, width=500, height=500, cell_size=30):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.is_running = False

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Buttons for controls
        self.start_btn = tk.Button(self.root, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT)
        self.stop_btn = tk.Button(self.root, text="Stop", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT)
        self.reset_btn = tk.Button(self.root, text="Reset", command=self.reset_grid)
        self.reset_btn.pack(side=tk.LEFT)
        self.random_btn = tk.Button(self.root, text="Random", command=self.randomize_grid)
        self.random_btn.pack(side=tk.LEFT)

        # Bind mouse click to toggle cells
        self.canvas.bind("<Button-1>", self.toggle_cell)

    def toggle_cell(self, event):
        if not self.is_running:
            row = event.y // self.cell_size
            col = event.x // self.cell_size
            self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0
            self.draw_grid()

    def randomize_grid(self):
        if not self.is_running:
            self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
            self.draw_grid()

    def reset_grid(self):
        self.is_running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def start(self):
        self.is_running = True
        self.update()

    def stop(self):
        self.is_running = False

    def update(self):
        if self.is_running:
            self.grid = self.next_generation()
            self.draw_grid()
            self.root.after(100, self.update)

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
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for n in neighbors:
            r, c = row + n[0], col + n[1]
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 1:
                count += 1
        return count

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.grid[row][col] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")


# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Conway's Game of Life")
    root.resizable(False, False)
    game = GameOfLife(root)
    root.mainloop()
