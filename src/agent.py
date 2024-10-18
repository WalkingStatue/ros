import random
import numpy as np
from enum import Enum

class ObstacleType(Enum):
    BUILDING = 1
    RUBBLE = 2
    FALLEN_TREE = 3

def place_survivors(grid, num_survivors, min_distance=3):
    placed_survivors = 0
    attempts = 0
    max_attempts = 1000 # Increased max attempts for robustness

    while placed_survivors < num_survivors and attempts < max_attempts:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        if grid[row, col] == 0 and is_valid_position(grid, row, col, min_distance):
            grid[row, col] = -1
            placed_survivors += 1
        attempts += 1

    if placed_survivors < num_survivors:
        print(f"Warning: Only {placed_survivors} out of {num_survivors} survivors placed after {max_attempts} attempts. Consider increasing grid size or reducing survivor count.")


def place_agent(grid, min_distance=3):
    placed = False
    attempts = 0
    max_attempts = 1000 # Increased max attempts for robustness

    while not placed and attempts < max_attempts:
        agent_row = random.randint(0, len(grid) - 1)
        agent_col = random.randint(0, len(grid[0]) - 1)
        if grid[agent_row, agent_col] == 0 and is_valid_position(grid, agent_row, agent_col, min_distance):
            grid[agent_row, agent_col] = 2
            placed = True
            print(f"Agent placed at ({agent_row}, {agent_col})")
        attempts += 1
    if not placed:
        print(f"Warning: Failed to place agent after {max_attempts} attempts. Consider increasing grid size or reducing obstacles.")
        return False
    return True

def is_valid_position(grid, row, col, min_distance):
    rows, cols = grid.shape
    for i in range(max(0, row - min_distance), min(rows, row + min_distance + 1)):
        for j in range(max(0, col - min_distance), min(cols, col + min_distance + 1)):
            if (i != row or j != col) and (0 <= i < rows and 0 <= j < cols) and (grid[i, j] == 2 or grid[i, j] == -1 or grid[i,j] > 0):
                return False
    return True

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
