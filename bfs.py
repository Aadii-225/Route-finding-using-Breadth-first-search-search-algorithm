import tkinter as tk
from collections import deque
import time

ROWS, COLS = 20, 20
CELL_SIZE = 30

class BFSVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Shortest Path Visualizer")

        # Title
        tk.Label(root, text="BFS Shortest Path Visualizer",
                 font=("Arial", 16, "bold")).pack()

        # 📘 Instructions
        tk.Label(root, text="Click/Drag to draw walls | Click 'Start BFS' to find shortest path",
                 font=("Arial", 10)).pack()

        # Canvas
        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        # Grid Setup
        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.start = (0, 0)
        self.end = (ROWS-1, COLS-1)

        #  Mouse Controls
        self.canvas.bind("<Button-1>", self.toggle_wall)
        self.canvas.bind("<B1-Motion>", self.drag_wall)

        # Buttons
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Start BFS", command=self.run_bfs, width=12).grid(row=0, column=0)
        tk.Button(frame, text="Clear Grid", command=self.reset_grid, width=12).grid(row=0, column=1)

        # Legend
        tk.Label(root,
                 text="Green=Start   Red=End   Black=Wall   Blue=Visited   Yellow=Shortest Path",
                 font=("Arial", 10)).pack()

        self.draw_grid()

    # Draw Grid
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                color = "white"

                if self.grid[i][j] == 1:
                    color = "black"

                if (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.end:
                    color = "red"

                self.canvas.create_rectangle(
                    j*CELL_SIZE, i*CELL_SIZE,
                    (j+1)*CELL_SIZE, (i+1)*CELL_SIZE,
                    fill=color, outline="gray"
                )

    # Click to toggle wall
    def toggle_wall(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if (row, col) != self.start and (row, col) != self.end:
            self.grid[row][col] = 1 - self.grid[row][col]

        self.draw_grid()

    #  Drag to draw walls
    def drag_wall(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            if (row, col) != self.start and (row, col) != self.end:
                self.grid[row][col] = 1

        self.draw_grid()

    #  Reset grid
    def reset_grid(self):
        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.draw_grid()

    #  BFS Visualization
    def run_bfs(self):
        queue = deque([self.start])
        visited = {self.start: None}

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.end:
                self.show_path(visited)
                return

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy

                if 0 <= nx < ROWS and 0 <= ny < COLS:
                    if self.grid[nx][ny] == 0 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited[(nx, ny)] = (x, y)

                        if (nx, ny) != self.end:
                            self.canvas.create_rectangle(
                                ny*CELL_SIZE, nx*CELL_SIZE,
                                (ny+1)*CELL_SIZE, (nx+1)*CELL_SIZE,
                                fill="lightblue"
                            )

                        self.root.update()
                        time.sleep(0.02)

    # Show shortest path
    def show_path(self, visited):
        node = self.end

        while node is not None:
            x, y = node

            if node != self.start and node != self.end:
                self.canvas.create_rectangle(
                    y*CELL_SIZE, x*CELL_SIZE,
                    (y+1)*CELL_SIZE, (x+1)*CELL_SIZE,
                    fill="yellow"
                )

            node = visited[node]

            self.root.update()
            time.sleep(0.04)

        # redraw start & end
        x, y = self.start
        self.canvas.create_rectangle(
            y*CELL_SIZE, x*CELL_SIZE,
            (y+1)*CELL_SIZE, (x+1)*CELL_SIZE,
            fill="green"
        )

        x, y = self.end
        self.canvas.create_rectangle(
            y*CELL_SIZE, x*CELL_SIZE,
            (y+1)*CELL_SIZE, (x+1)*CELL_SIZE,
            fill="red"
        )


# ▶ Run Application
root = tk.Tk()
app = BFSVisualizer(root)
root.mainloop()