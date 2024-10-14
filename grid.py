import numpy as np
import random
from agent import ObstacleType

def create_grid(rows, cols):
    return np.zeros((rows, cols))

def place_obstacles(grid, num_obstacles):
    placed_obstacles = 0
    attempts = 0
    max_attempts = 1000 # Increased max attempts for robustness

    while placed_obstacles < num_obstacles and attempts < max_attempts:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        obstacle_type = random.choice(list(ObstacleType))
        if grid[row, col] == 0:
            grid[row, col] = obstacle_type.value
            placed_obstacles += 1
        attempts += 1

    if placed_obstacles < num_obstacles:
        print(f"Warning: Only {placed_obstacles} out of {num_obstacles} obstacles placed after {max_attempts} attempts. Consider increasing grid size or reducing obstacle count.")


def flood_fill(grid, row, col, visited):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return
    if grid[row, col] != 0 or visited[row, col]:
        return
    visited[row, col] = True
    grid[row, col] = 0  # Mark as empty space for maze creation

    # Cardinal directions (up, down, left, right)
    flood_fill(grid, row - 1, col, visited)
    flood_fill(grid, row + 1, col, visited)
    flood_fill(grid, row, col - 1, visited)
    flood_fill(grid, row, col + 1, visited)

    # Diagonal directions
    flood_fill(grid, row - 1, col - 1, visited)
    flood_fill(grid, row - 1, col + 1, visited)
    flood_fill(grid, row + 1, col - 1, visited)
    flood_fill(grid, row + 1, col + 1, visited)

def creates_maze(grid, row, col):
    if grid[row, col] != 0:
        return False

    min_maze_size = 20

    visited = np.zeros_like(grid, dtype=bool)

    for _ in range(3):
        start_row, start_col = find_unvisited_cell(visited)
        if start_row is None:
            return False

        flood_fill(grid, start_row, start_col, visited)

    unvisited_count = np.count_nonzero(~visited)
    return unvisited_count > min_maze_size

def find_unvisited_cell(visited):
    if not np.any(~visited):
        return None, None

    while True:
        row = random.randint(0, len(visited) - 1)
        col = random.randint(0, len(visited[0]) - 1)
        if not visited[row, col]:
            return row, col
