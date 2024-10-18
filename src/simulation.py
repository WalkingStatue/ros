import time
import numpy as np
from astar import astar
from visualize import visualize_grid

def simulate(grid, agent_location):
    survivors = np.argwhere(grid == -1)
    total_time = 0

    while len(survivors) > 0:
        for survivor in survivors:
            survivor_location = tuple(survivor)
            path = astar(grid, agent_location, survivor_location, allow_diagonal=True)

            if path:
                print(f"Found path from {agent_location} to {survivor_location}: {path}")

                for step in path:
                    if step == survivor_location:
                        grid[step] = -2
                        print(f"Survivor at {step} rescued.")
                        break
                    
                    if grid[step] > 0:  #Check for any obstacle
                        print(f"Agent encountered an obstacle at {step}. Replanning path...")
                        #Replan path
                        new_path = astar(grid, agent_location, survivor_location, allow_diagonal=True)
                        if new_path:
                            path = new_path
                            print(f"New path found: {path}")
                        else:
                            print(f"No path found after replanning. Giving up on this survivor.")
                            break

                    grid[agent_location] = 0
                    agent_location = step
                    grid[agent_location] = 2
                    visualize_grid(grid)
                    time.sleep(0.5)

                survivors = np.argwhere(grid == -1)

            else:
                print(f"No path found to survivor at {survivor_location}. Giving up on this survivor.")
                break

        if len(survivors) == 0:
            print("All survivors have been rescued.")
        else:
            print("Remaining survivors to be rescued:", survivors)

    print("Simulation finished.")
