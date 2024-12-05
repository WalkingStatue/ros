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
    rescued_survivors = 0
    unreachable_survivors = 0

    def animate_step(path, survivor_location, step_index, item_images):
        nonlocal agent_location, survivors, rescued_survivors
        try:
            for step_index in range(len(path)):
                step = path[step_index]
                if step != survivor_location:
                    grid[agent_location] = 0
                    try:
                        grid_buttons[agent_location].config(bg="white", image="")
                    except KeyError:
                        logging.error(f"KeyError: Invalid button index {agent_location}")
                        return
                    agent_location = step
                    grid[agent_location] = 2
                    try:
                        grid_buttons[agent_location].config(bg="black", image=item_images[AgentType.AGENT][0])
                    except KeyError:
                        logging.error(f"KeyError: Invalid button index {agent_location}")
                        return
                    root.update()
                    time.sleep(0.5) # Use time.sleep for animation instead of root.after
                else:
                    grid[step] = -2
                    try:
                        grid_buttons[step].config(bg="black", image=item_images[SurvivorType.SURVIVOR][0])
                    except KeyError:
                        logging.error(f"KeyError: Invalid button index {step}")
                        return
                    logging.info(f"Survivor at {step} rescued.")
                    rescued_survivors += 1
                    # Remove the rescued survivor from the survivors array
                    survivors = np.array([s for s in survivors if not np.array_equal(s, step)])
                    root.update()
                    break # Exit the loop after rescuing a survivor
        except IndexError as e:
            logging.error(f"IndexError in animate_step: {e}")
            messagebox.showerror("Animation Error", f"An error occurred during animation: {e}")

    def distance(a, b):
        return np.linalg.norm(a - b)

    while survivors.size > 0:
        path_found_for_any_survivor = False
        # Sort survivors by distance from the agent
        distances = np.apply_along_axis(lambda s: distance(s, np.array(agent_location)), 1, survivors)
        sorted_indices = np.argsort(distances)
        survivors = survivors[sorted_indices]

        survivors_copy = np.copy(survivors) # Create a copy to iterate safely
        for survivor_index in range(survivors_copy.shape[0]):
            if survivor_index < survivors_copy.shape[0]: # Check if index is still valid
                survivor = survivors_copy[survivor_index]
                survivor_location = tuple(survivor)
                # Check if the survivor is still present before attempting to rescue them
                if grid[survivor_location] == SurvivorType.SURVIVOR.value:
                    path = astar(grid, agent_location, survivor_location)
                    if path:
                        path_found_for_any_survivor = True
                        logging.info(f"Found path from {agent_location} to {survivor_location}: {path}")
                        animate_step(path, survivor_location, 0, item_images)
                    else:
                        logging.error(f"No path found to survivor at {survivor_location}. Giving up on this survivor.")
                        unreachable_survivors += 1
                        #remove survivor if no path found
                        survivors = np.array([s for s in survivors if not np.array_equal(s, survivor)])

        if survivors.size == 0:
            summary_message = f"Simulation complete.\n{rescued_survivors} survivors rescued."
            if unreachable_survivors > 0:
                summary_message += f"\nNo path available for {unreachable_survivors} survivor(s)."
            messagebox.showinfo("Simulation Complete", summary_message)
            # Reset the grid here.  This requires a function to reset the grid in main.py
            reset_grid(grid, grid_buttons) #call reset_grid function from main.py
            status_text.set("Simulation finished.")
            break #added break to exit the while loop if no survivors left
        elif not path_found_for_any_survivor:
            summary_message = f"Simulation complete.\n{rescued_survivors} survivors rescued."
            if unreachable_survivors > 0:
                summary_message += f"\nNo path available for {unreachable_survivors} survivor(s)."
            messagebox.showinfo("Simulation Complete", summary_message)
            status_text.set("Simulation finished.")
            break #added break to exit the while loop if no path found for any survivors

    logging.info("Simulation finished.")
