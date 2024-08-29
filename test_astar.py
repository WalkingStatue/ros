import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap  # Correct import for ListedColormap
from astar import astar

def visualize_grid(grid, filename='grid.png'):
    # Define a custom colormap with distinct colors
    cmap = ListedColormap(['white', 'blue', 'red', 'green', 'orange'])  # Colors for open terrain, building, rubble, agent, and rescued survivor
    bounds = [0, 1, 10, 20]  # Adjust bounds to fit your grid values
    norm = plt.Normalize(vmin=0, vmax=20)

    fig, ax = plt.subplots()
    cbar = ax.imshow(grid, cmap=cmap, norm=norm)

    # Add a colorbar for reference
    cbar = plt.colorbar(cbar, ticks=[0, 1, 2, 10])
    cbar.ax.set_yticklabels(['Open Terrain', 'Survivor', 'Agent', 'Fallen Tree'])

    # Mark the grid with text labels
    rows, cols = grid.shape
    for (i, j), val in np.ndenumerate(grid):
        if val == -2:
            ax.text(j, i, 'R', ha='center', va='center', color='black', fontsize=8)
        elif val == -1:
            ax.text(j, i, 'S', ha='center', va='center', color='black', fontsize=8)
        elif val == 2:
            ax.text(j, i, 'A', ha='center', va='center', color='black', fontsize=8)
        elif val == 10:
            ax.text(j, i, 'X', ha='center', va='center', color='black', fontsize=8)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title('Grid State')
    plt.savefig(filename)
    print(f"Grid visualization saved as {filename}")

def visualize_path(grid, path, filename='astar_path.png'):
    fig, ax = plt.subplots()

    # Use a colormap that ensures paths are visible
    cmap = ListedColormap(['white', 'blue', 'red', 'green', 'orange'])  # Colors for open terrain, building, rubble, agent, and rescued survivor
    norm = plt.Normalize(vmin=0, vmax=20)

    ax.imshow(grid, cmap=cmap, norm=norm)

    # Mark the path
    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_y, path_x, marker='o', color='red', linestyle='-', linewidth=2)

    # Mark start and end points
    if path:
        ax.plot(path[0][1], path[0][0], marker='o', color='green', markersize=8)  # Start
        ax.plot(path[-1][1], path[-1][0], marker='x', color='blue', markersize=8)  # End

    # Save the figure to a file
    plt.savefig(filename)
    print(f"Path visualization saved as {filename}")

def test_astar_with_visualization():
    start = (0, 0)
    survivors = [(9, 9)]  # Ensure this is a tuple

    # Define the grid with various terrains
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

    print("Initial grid state:")
    visualize_grid(grid, 'initial_grid_state.png')
    
    for i, goal in enumerate(survivors):
        print(f"Start position: {start}")
        print(f"Goal position (survivor): {goal}")

        path = astar(grid, start, goal, allow_diagonal=True)

        print(f"A* Path to survivor {i+1}: {path}")

        if path:
            visualize_path(grid, path, filename=f'astar_path_survivor_{i+1}.png')
            start = goal  # Update the start position to the last goal for the next path

            # Update grid to mark survivor as rescued
            grid[goal] = -2
            print(f"Updated grid after rescuing survivor {i+1}:")
            visualize_grid(grid, 'updated_grid_state.png')

    print("Final grid state:")
    visualize_grid(grid, 'final_grid_state.png')

if __name__ == "__main__":
    test_astar_with_visualization()
