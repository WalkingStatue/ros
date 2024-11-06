import time
import numpy as np
from astar import astar
#from visualize import visualize_grid
import logging
from grid import AgentType, SurvivorType #Import missing types
from tkinter import messagebox
from grid_utils import reset_grid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_simulation(grid, agent_location, grid_buttons, root, item_images, status_text):
    obstacles = np.argwhere(grid > 0)
    survivors = np.argwhere(grid == -1)

    # Verification
    if not obstacles.size:
        raise ValueError("There must be at least one obstacle in the grid.")
    if not survivors.size:
        raise ValueError("There must be at least one survivor in the grid.")

    logging.info("Simulation started.")
    total_time = 0

    def animate_step(path, survivor_location, step_index, item_images):
        nonlocal agent_location, survivors
        for step_index in range(len(path)):
            step = path[step_index]
            if step != survivor_location:
                grid[agent_location] = 0
                try:
                    grid_buttons[agent_location].config(bg="white", image="")
                except IndexError:
                    logging.error(f"IndexError: Invalid button index {agent_location}")
                    return
                agent_location = step
                grid[agent_location] = 2
                try:
                    grid_buttons[agent_location].config(bg="black", image=item_images[AgentType.AGENT][0])
                except IndexError:
                    logging.error(f"IndexError: Invalid button index {agent_location}")
                    return
                root.update()
                time.sleep(0.5) # Use time.sleep for animation instead of root.after
            else:
                grid[step] = -2
                try:
                    grid_buttons[step].config(bg="black", image=item_images[SurvivorType.SURVIVOR][0])
                except IndexError:
                    logging.error(f"IndexError: Invalid button index {step}")
                    return
                logging.info(f"Survivor at {step} rescued.")
                # Remove the rescued survivor from the survivors array
                survivors = np.array([s for s in survivors if not np.array_equal(s, survivor)])
                root.update()
                break # Exit the loop after rescuing a survivor

    while survivors.size > 0:
        for survivor_index in range(survivors.shape[0]):
            survivor = survivors[survivor_index]
            survivor_location = tuple(survivor)
            # Check if the survivor is still present before attempting to rescue them
            if grid[survivor_location] == SurvivorType.SURVIVOR.value:
                path = astar(grid, agent_location, survivor_location, allow_diagonal=True)
                if path:
                    logging.info(f"Found path from {agent_location} to {survivor_location}: {path}")
                    animate_step(path, survivor_location, 0, item_images)
                else:
                    logging.error(f"No path found to survivor at {survivor_location}. Giving up on this survivor.")
                    break
            else:
                logging.info(f"Survivor at {survivor_location} already rescued.")

        if survivors.size == 0:
            logging.info("All survivors have been rescued.")
            messagebox.showinfo("Simulation Complete", "All survivors found!")
            # Reset the grid here.  This requires a function to reset the grid in main.py
            reset_grid(grid, grid_buttons) #call reset_grid function from main.py
            status_text.set("Simulation finished.")
        else:
            logging.info(f"Remaining survivors to be rescued: {survivors}")

    logging.info("Simulation finished.")
