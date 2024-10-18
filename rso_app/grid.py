import numpy as np
from enum import Enum

class ObstacleType(Enum):
    BUILDING = 1
    RUBBLE = 2
    FALLEN_TREE = 3

class AgentType(Enum):
    AGENT = 1

class SurvivorType(Enum):
    SURVIVOR = 1

def create_grid(rows, cols):
    return np.zeros((rows, cols), dtype=int)

def place_obstacles(grid, obstacles):
    for row, col, obstacle_type in obstacles:
        grid[row, col] = obstacle_type.value
