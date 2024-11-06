def reset_grid(grid, grid_buttons):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            grid[row, col] = 0
            grid_buttons[(row, col)].config(bg="white", image="")
