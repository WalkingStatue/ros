import time
import numpy as np
from astar import astar
from visualize import visualize_grid

def simulate(grid, agent_location):
    survivors = np.argwhere(grid == -1)  # Find all survivors
    total_time = 0

    while len(survivors) > 0:
        for survivor in survivors:
            survivor_location = tuple(survivor)
            path = astar(grid, agent_location, survivor_location, allow_diagonal=True)
            
            if path:
                print(f"Found path from {agent_location} to {survivor_location}: {path}")
                
                # Follow the path
                for step in path:
                    if step == survivor_location:
                        # Mark the survivor as rescued
                        grid[step] = -2
                        print(f"Survivor at {step} rescued.")
                        break

                    if grid[step] == 10:  # If an obstacle is encountered
                        print(f"Agent encountered an obstacle at {step}. Replanning path...")
                        break

                    # Move agent
                    grid[agent_location] = 0
                    agent_location = step
                    grid[agent_location] = 2
                    visualize_grid(grid)
                    time.sleep(0.5)

                # Update survivors list
                survivors = np.argwhere(grid == -1)

            else:
                print(f"No path found to survivor at {survivor_location}. Giving up on this survivor.")
                break  # Exit the loop to avoid infinite attempts

        if len(survivors) == 0:
            print("All survivors have been rescued.")
        else:
            print("Remaining survivors to be rescued:", survivors)

    print("Simulation finished.")
