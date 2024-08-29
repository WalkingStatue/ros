import numpy as np
from astar import astar
from visualize import visualize_grid
import time

def simulate(grid, agent_location):
    survivor_locations = np.argwhere(grid == -1)
    rescued_survivors = 0
    max_replanning_attempts = 5  # Limit on replanning attempts
    
    for survivor_location in survivor_locations:
        replanning_attempts = 0
        tried_paths = set() 

        while replanning_attempts < max_replanning_attempts:
            path = astar(grid, agent_location, tuple(survivor_location))

            if path:
                path_successful = False  # Assume the path is not successful initially
                for step in path[1:]:
                    if grid[step] == 0 or step == tuple(survivor_location): 
                        # Move the agent
                        if grid[agent_location] == 2:
                            grid[agent_location] = 0
                        agent_location = step
                        grid[agent_location] = 2
                        visualize_grid(grid)
                        time.sleep(0.5)

                        if step == tuple(survivor_location): 
                            grid[step] = -2  # Mark the survivor as rescued
                            rescued_survivors += 1
                            print(f"Rescued survivor at {step}!")
                            path_successful = True  # Path was successful
                            break  # Exit the for loop to proceed to the next survivor

                    else:
                        print(f"Agent encountered an obstacle at {step}. Replanning path...")
                        tried_paths.add(step)
                        path_successful = False
                        break

                if path_successful:  # If the path was successful, break the outer while loop
                    break
 
            else:
                print(f"No path found to survivor at {survivor_location}. Giving up on this survivor.")
                break

            # Replan if path unsuccessful
            replanning_attempts += 1
            if not path_successful:
                new_path = attempt_obstacle_avoidance(grid, agent_location, tuple(survivor_location), tried_paths)
                if new_path:
                    continue 

        if replanning_attempts >= max_replanning_attempts:
            print(f"Failed to reach survivor at {survivor_location} after {max_replanning_attempts} attempts.")

    print(f"Total survivors rescued: {rescued_survivors}")

def attempt_obstacle_avoidance(grid, agent_location, survivor_location, tried_paths):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        new_position = (agent_location[0] + direction[0], agent_location[1] + direction[1])
        if (0 <= new_position[0] < len(grid) and 0 <= new_position[1] < len(grid[0]) and
            grid[new_position] == 0 and new_position not in tried_paths):
            return astar(grid, new_position, survivor_location)
    return None
