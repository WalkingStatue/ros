import random
import numpy as np

def create_grid(rows, cols):
    return np.zeros((rows, cols))

def place_obstacles(grid, num_obstacles):
    # Ensure obstacles are placed in a diverse manner
    obstacle_types = {"rubble": 5, "fallen tree": 10, "building": 3}
    obstacle_positions = set()

    while len(obstacle_positions) < num_obstacles:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        if grid[row, col] == 0 and (row, col) not in obstacle_positions:
            obstacle_type = random.choice(list(obstacle_types.keys()))
            grid[row, col] = obstacle_types[obstacle_type]
            obstacle_positions.add((row, col))

    # Create a maze to ensure connectivity
    create_maze(grid)

def create_maze(grid):
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = len(grid), len(grid[0])
    
    # Start from a random cell
    start_row, start_col = random.randint(0, rows - 1), random.randint(0, cols - 1)
    flood_fill(grid, start_row, start_col, visited)

    # Make sure all regions are reachable
    for _ in range(3):  # Attempt several times to fill the grid
        row, col = find_unvisited_cell(visited)
        if row is not None:
            flood_fill(grid, row, col, visited)

def flood_fill(grid, row, col, visited):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return
    if grid[row, col] != 0 or visited[row, col]:
        return
    visited[row, col] = True
    grid[row, col] = 0  # Mark as empty space for maze creation
    flood_fill(grid, row - 1, col, visited)
    flood_fill(grid, row + 1, col, visited)
    flood_fill(grid, row, col - 1, visited)
    flood_fill(grid, row, col + 1, visited)

def find_unvisited_cell(visited):
    unvisited_cells = [(row, col) for row in range(len(visited)) for col in range(len(visited[0])) if not visited[row, col]]
    if unvisited_cells:
        return random.choice(unvisited_cells)
    return None, None
