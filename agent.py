import random
import numpy as np

def place_survivors(grid, num_survivors, min_distance=3):
    for _ in range(num_survivors):
        placed = False
        attempts = 0
        while not placed and attempts < 100:  # Retry up to 100 times
            row = random.randint(0, len(grid) - 1)
            col = random.randint(0, len(grid[0]) - 1)
            if grid[row, col] == 0 and is_valid_position(grid, row, col, min_distance):
                grid[row, col] = -1  
                placed = True
            attempts += 1
        if not placed:
            print(f"Warning: Failed to place a survivor after 100 attempts. Consider increasing grid size or reducing survivor count.")

def place_agent(grid, min_distance=3):
    placed = False
    attempts = 0
    while not placed and attempts < 100:  # Retry up to 100 times
        agent_row = random.randint(0, len(grid) - 1)
        agent_col = random.randint(0, len(grid[0]) - 1)
        if grid[agent_row, agent_col] == 0 and is_valid_position(grid, agent_row, agent_col, min_distance):
            grid[agent_row, agent_col] = 2
            placed = True
            print(f"Agent placed at ({agent_row}, {agent_col})")
        attempts += 1
    if not placed:
        raise Exception("Error: Failed to place agent after 100 attempts. Consider increasing grid size or reducing obstacles.")

def is_valid_position(grid, row, col, min_distance):
    rows, cols = grid.shape
    for i in range(max(0, row - min_distance), min(rows, row + min_distance + 1)):
        for j in range(max(0, col - min_distance), min(cols, col + min_distance + 1)):
            if (i != row or j != col) and (0 <= i < rows and 0 <= j < cols) and (grid[i, j] == 2 or grid[i, j] == -1):
                return False
    return True
