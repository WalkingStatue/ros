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

def run_simulation(grid, agent_location, grid_buttons, root, item_images, status_text, stop_timer):
    obstacles = np.argwhere(grid > 0)
    survivors = np.argwhere(grid == -1)

    # Verification
    if not obstacles.size:
        raise ValueError("There must be at least one obstacle in the grid.")
    if not survivors.size:
        raise ValueError("There must be at least one survivor in the grid.")

    start_time = time.time()
    logging.info("Simulation started.")
    total_time = 0
    rescued_survivors = 0
    unreachable_survivors = 0
    move_counter = 0
    rescue_times = {}
    def animate_step(path, survivor_location, item_images, start_time):
        nonlocal agent_location, survivors, rescued_survivors, grid, move_counter, rescue_times
        initial_agent_location = agent_location  # Store the agent's initial location
        
        # Store original cell states for restoration
        saved_states = {}
        # Clear the initial agent location before the animation starts
        grid[initial_agent_location] = 0
        grid_buttons[initial_agent_location].config(bg="white", image=saved_states.get(initial_agent_location, {}).get("image", None))

        for step_index, step in enumerate(path):
            
            
            try:
                print(move_counter , "After update")
                move_counter += 1
                if move_counter == 1:
                    print(move_counter , "after Loop")
                # Only clear the agent's starting position
                    #grid[initial_agent_location] = 0  # Set the initial position to empty
                    grid_buttons[initial_agent_location].config(bg="white", image="")
                # Restore the previous cell's state
                if step_index > 0:
                    prev_step = path[step_index - 1]
                    grid[prev_step] = 0  # Ensure the previous location is empty
                    grid_buttons[prev_step].config(bg="white", image=saved_states[prev_step]["image"])

                # Save the current state of the cell before moving the agent
                if step not in saved_states:
                    saved_states[step] = {
                        "value": grid[step],
                        "image": grid_buttons[step].cget("image")
                    }

                # Update the agent's location and image
                agent_location = step
                grid[agent_location] = AgentType.AGENT.value
                grid_buttons[agent_location].config(bg="black", image=item_images[AgentType.AGENT][0])

                root.update()
                time.sleep(0.5)

                if step == survivor_location:
                    # Mark survivor as rescued
                    grid[step] = SurvivorType.RESCUED_SURVIVOR.value
                    grid_buttons[step].config(bg="black", image=item_images[SurvivorType.RESCUED_SURVIVOR][0])
                    rescue_time = time.time() - start_time
                    rescue_times[survivor_location] = rescue_time
                    rescued_survivors += 1
                    survivors = np.array([s for s in survivors if not np.array_equal(s, step)])
                    logging.info(f"Survivor at {step} rescued in {rescue_time:.2f} seconds.")
                    
                    # Check if this was the last survivor
                    if survivors.size == 0:
                        simulation_running = False
                        root.after(0, lambda: status_text.set("Simulation finished."))
                    
                    break

            except (IndexError, KeyError) as e:
                logging.error(f"Error in animate_step: {e}")
                messagebox.showerror("Animation Error", f"An error occurred during animation: {e}")
                return  # Exit the function if an error occurs


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
                        animate_step(path, survivor_location, item_images, start_time)
                    else:
                        logging.error(f"No path found to survivor at {survivor_location}. Giving up on this survivor.")
                        unreachable_survivors += 1
                        rescue_times[survivor_location] = "N/A"
                        # Remove survivor if no path found
                        survivors = np.array([s for s in survivors if not np.array_equal(s, survivor)])

        if survivors.size == 0:
            summary_message = f"Simulation complete.\n{rescued_survivors} survivors rescued."
            if unreachable_survivors > 0:
                summary_message += f"\nNo path available for {unreachable_survivors} survivor(s)."
            summary_message = f"Simulation complete.\n{rescued_survivors} survivors rescued."
            if unreachable_survivors > 0:
                summary_message += f"\nNo path available for {unreachable_survivors} survivor(s)."
            
            # Add rescue times to the summary message
            if rescue_times:
                summary_message += "\n\nRescue Times:"
                for location, rescue_time in rescue_times.items():
                    summary_message += f"\nSurvivor at {location}: {rescue_time:.2f} seconds"
            
            messagebox.showinfo("Simulation Complete", summary_message)
            # Reset the grid here. This requires a function to reset the grid in main.py
            reset_grid(grid, grid_buttons) #call reset_grid function from main.py
            status_text.set("Simulation finished.")
            root.after(0, stop_timer)
            break #added break to exit the while loop if no survivors left
        elif not path_found_for_any_survivor:
            summary_message = f"Simulation complete.\n{rescued_survivors} survivors rescued."
            if unreachable_survivors > 0:
                summary_message += f"\nNo path available for {unreachable_survivors} survivor(s)."
            
            # Add rescue times to the summary message
            if rescue_times:
                summary_message += "\n\nRescue Times:"
                for location, rescue_time in rescue_times.items():
                    if isinstance(rescue_time, float):
                        summary_message += f"\nSurvivor at {location}: {rescue_time:.2f} seconds"
                    else:
                        summary_message += f"\nSurvivor at {location}: {rescue_time}"
            
            messagebox.showinfo("Simulation Complete", summary_message)
            status_text.set("Simulation finished.")
            root.after(0, stop_timer)
            break #added break to exit the while loop if no path found for any survivors

    logging.info("Simulation finished.")
