import random
from grid import create_grid, place_obstacles
from visualize import visualize_grid
from agent import place_agent, place_survivors

# Get grid size from user input
print("Select a grid size:")
print("1. Small (10x10)")
print("2. Medium (15x15)")
print("3. Large (20x20)")

choice = int(input("Enter your choice (1-3): "))

if choice == 1:
    grid_rows, grid_cols = 10, 10
elif choice == 2:
    grid_rows, grid_cols = 15, 15
elif choice == 3:
    grid_rows, grid_cols = 20, 20
else:
    print("Invalid choice. Defaulting to small grid.")
    grid_rows, grid_cols = 10, 10

# Create the grid
world_grid = create_grid(grid_rows, grid_cols)

# Get the number of obstacles from the user
num_obstacles = int(input("Enter the number of obstacles: "))

# Place obstacles on the grid
place_obstacles(world_grid, num_obstacles)

# Get the number of survivors
num_survivors = int(input("Enter the number of survivors: "))

# Place survivors on the grid
place_survivors(world_grid, num_survivors)

# Place the agent on the grid
place_agent(world_grid)

# Visualize the grid with agents and survivors
visualize_grid(world_grid)

