import os
import sys

def clear_screen():
    # Clear the screen for different operating systems
    os.system('cls' if os.name == 'nt' else 'clear')

def visualize_grid(grid):
    clear_screen()  # Clear the screen for a fresh view

    # Print the legend
    print("Legend:")
    print("  : Open terrain")
    print("#: Building")
    print(".: Rubble")
    print("X: Fallen tree")
    print("A: Agent")
    print("S: Survivor")
    print("R: Rescued Survivor")  # Added for rescued survivors
    print()

    rows, cols = len(grid), len(grid[0])
    
    # Print top border
    print(' ' + '─' * (cols * 2 + 1))
    
    for row in grid:
        # Print left border
        print('│', end=' ')
        for cell in row:
            if cell == 0:
                print(' ', end=' ')
            elif cell == 2:
                print('A', end=' ')
            elif cell == -1:
                print('S', end=' ')
            elif cell == -2:
                print('R', end=' ')
            elif cell == 10:
                print('X', end=' ')
            elif cell == 5:
                print('.', end=' ')
            elif cell == 3:
                print('#', end=' ')
        # Print right border
        print('│')
    
    # Print bottom border
    print(' ' + '─' * (cols * 2 + 1))

    sys.stdout.flush()  # Ensure all output is written to the terminal
