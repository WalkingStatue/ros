import numpy as np
from simulation import simulate  # Ensure this import matches your module structure

import numpy as np
from astar import astar

def test_simulation_with_obstacles():
    # Create a test grid with more obstacles
    grid = np.array([
    [0,  5,  0, 10, 0,  5,  3,  0,  0, 10],
    [0,  5,  0,  0, 0, 10,  5,  3,  0,  0],
    [0, 10, 0,  5, 3,  0,  5,  5, 10, 10],
    [0,  3, 0, 10, 5, 10,  5,  0,  0, 10],
    [10, 5, 0,  5, 5,  0, 10,  3, 10,  0],
    [10, 5, 0, 10, 0,  0, 10,  0, 10,  0],
    [0,  0, 0,  5, 10, 10,  0,  0, 10,  0],
    [5,  0, 5,  0,  0, 10,  5, 10, 0,  0],
    [0, 10, 5,  3,  5,  0,  5,  0, 0,  0],
    [0,  0, 10,  0,  5, 10,  0,  0, 0, -1]  # Survivor here at (9, 9)
])

    # Place survivors (-1) and agent (2) on the grid
    agent_location = (0, 0)
    grid[agent_location] = 2  # Agent at (0, 0)

    print("Initial Grid State:")
    print_grid(grid)  # Print initial state for verification

    # Run the simulation
    print("\nRunning Simulation...")
    simulate(grid, agent_location)

    print("\nFinal Grid State:")
    print_grid(grid)  # Print final state for verification

    # Additional checks can be performed here, e.g., checking the number of rescued survivors

def print_grid(grid):
    print("\n".join(" ".join(str(int(cell)) for cell in row) for row in grid))

if __name__ == "__main__":
    test_simulation_with_obstacles()
