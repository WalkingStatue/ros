import numpy as np
from enum import Enum

class ObstacleType(Enum):
    BUILDING = 3
    RUBBLE = 5
    FALLEN_TREE = 10 #Impassable

class AgentType(Enum):
    AGENT = 1

class SurvivorType(Enum):
    SURVIVOR = -1
    RESCUED_SURVIVOR = -2 
def create_grid(rows, cols):
    grid = np.zeros((rows, cols), dtype=int)
    #Place agent
    grid[0,0] = AgentType.AGENT.value
    return grid

def place_obstacles(grid, obstacles):
    for row, col, obstacle_type in obstacles:
        grid[row, col] = obstacle_type.value
