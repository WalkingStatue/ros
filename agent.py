import random

def place_survivors(grid, num_survivors, min_distance=3):
    for _ in range(num_survivors):
        while True:
            row = random.randint(0, len(grid) - 1)
            col = random.randint(0, len(grid[0]) - 1)
            if grid[row, col] == 0 and is_valid_position(grid, row, col, min_distance):
                grid[row, col] = -1  # Assuming -1 represents a survivor
                break

def place_agent(grid, min_distance=3):
    while True:
        agent_row = random.randint(0, len(grid) - 1)
        agent_col = random.randint(0, len(grid[0]) - 1)
        if grid[agent_row, agent_col] == 0 and is_valid_position(grid, agent_row, agent_col, min_distance):
            grid[agent_row, agent_col] = 2  # Assuming 2 represents the agent
            break

def is_valid_position(grid, row, col, min_distance):
    for i in range(row - min_distance, row + min_distance + 1):
        for j in range(col - min_distance, col + min_distance + 1):
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                if grid[i, j] == 2 or grid[i, j] == -1:
                    return False
    return True