import numpy as np
import matplotlib.pyplot as plt
import heapq
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current node to end
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

def manhattan_distance(node_position, end_position):
    return abs(node_position[0] - end_position[0]) + abs(node_position[1] - end_position[1])

def astar(maze, start, end, allow_diagonal=True):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []  # Priority queue for nodes to explore
    closed_list = np.zeros_like(maze, dtype=bool)  # Track visited nodes
    open_dict = {}  # Dictionary to track the best g-score for each position

    heapq.heappush(open_list, (start_node.f, start_node))
    open_dict[start_node.position] = start_node.g

    heuristic_weight = 1.4

    move_positions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, down, left, right
    if allow_diagonal:
        move_positions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Add diagonals

    while open_list:
        current_node = heapq.heappop(open_list)[1]
        closed_list[current_node.position[0], current_node.position[1]] = True

        if current_node.position == end_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        children = []
        for move in move_positions:
            node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            if not (0 <= node_position[0] < len(maze) and 0 <= node_position[1] < len(maze[0])):
                continue

            if maze[node_position[0]][node_position[1]] == 10:  # Fallen trees are impassable
                continue

            if closed_list[node_position[0], node_position[1]]:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

            for child in children:
                if closed_list[child.position[0], child.position[1]]:
                    continue

                # Map characters to terrain costs
                terrain_char = maze[child.position[0]][child.position[1]]
                if terrain_char == 0:  # Open terrain
                    terrain_cost = 1
                elif terrain_char == 5:  # Rubble
                    terrain_cost = 5
                elif terrain_char == 3:  # Building
                    terrain_cost = 3
                elif terrain_char == 10:  # Fallen tree (impassable)
                    continue  # Skip this child
                else:  # Default cost for any other character
                    terrain_cost = 1

                if allow_diagonal and (abs(move[0]) + abs(move[1])) == 2:
                    terrain_cost *= 1.4

                child.g = current_node.g + terrain_cost
                child.h = manhattan_distance(child.position, end_node.position) * heuristic_weight
                child.f = child.g + child.h

                if child.position in open_dict and open_dict[child.position] <= child.g:
                    continue

                heapq.heappush(open_list, (child.f, child))
                open_dict[child.position] = child.g

                if child == end_node:
                    path = []
                    while child:
                        path.append(child.position)
                        child = child.parent
                    return path[::-1]  # Return reversed path

    return None
    
def animate_path(grid, path):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Define colors for each type of terrain and state
    cmap = ListedColormap([
        'green',    # -2: Rescued survivor
        'orange',   # -1: Survivor
        'white',    # 0: Open space
        'blue',     # 3: Building
        'gray',     # 5: Rubble
        'brown'     # 10: Fallen tree
    ]) 

    bounds = [-2, -1, 0, 3, 5, 10]  
    norm = plt.Normalize(vmin=-2, vmax=10) 

    ax.imshow(grid, cmap=cmap, norm=norm)
    
    # Add static elements (start, end, grid, etc.)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.5)
    ax.set_xticks([])  
    ax.set_yticks([])

    # Create custom legend patches for terrain types
    legend_patches = [
        mpatches.Patch(color='green', label='Rescued survivor (-2)'),
        mpatches.Patch(color='orange', label='Survivor (-1)'),
        mpatches.Patch(color='white', label='Open space (0)'),
        mpatches.Patch(color='blue', label='Building (3)'),
        mpatches.Patch(color='gray', label='Rubble (5)'),
        mpatches.Patch(color='brown', label='Fallen tree (10)'),
        mpatches.Patch(color='yellow', label='Path'),
        mpatches.Patch(color='magenta', label='Start'),
        mpatches.Patch(color='cyan', label='End')
    ]
    
    # Add a legend with patches on the side
    ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

    # Initialize the path line and start/end markers
    line, = ax.plot([], [], marker='o', color='yellow', linestyle='-', linewidth=3, markersize=8)
    start_marker, = ax.plot([], [], marker='o', color='magenta', markersize=12)
    end_marker, = ax.plot([], [], marker='x', color='cyan', markersize=12)

    def init():
        line.set_data([], [])
        start_marker.set_data([], [])
        end_marker.set_data([], [])
        return line, start_marker, end_marker

    def update(frame):
        xdata, ydata = zip(*path[:frame + 1])
        line.set_data(ydata, xdata)

        if frame == 0:
            start_marker.set_data(ydata[0], xdata[0])
        elif frame == len(path) - 1:
            end_marker.set_data(ydata[-1], xdata[-1])

        return line, start_marker, end_marker

    ani = FuncAnimation(fig, update, frames=len(path), init_func=init, blit=True, interval=500, repeat=False)

    plt.title('A* Path Visualization (Animated)', fontsize=16, pad=20)
    plt.show()


def test_astar_with_visualization():
    start = (0, 0)
    survivors = [(9, 9)]

    grid = np.array([
    [0,  5,  0, 10, 0,  5,  3,  0,  0, 10],
    [0,  5,  0,  0, 0, 10,  5,  3,  0,  0],
    [0, 10, 0,  5, 3,  0,  5,  5, 10, 10],
    [0,  3, 0, 10, 5, 10,  5,  0,  0, 10],
    [10, 5, 0,  5, 5,  0, 10,  3, 10,  0],
    [10, 5, 0, 10, 0,  0, 10,  0, 10,  0],
    [0,  0, 0,  5, 10, 10,  0,  0, 10,  0],
    [5,  0, 5,  0,  10, 10,  5, 10, 10,  0],
    [0, 10, 5,  3,  5,  0,  5,  0, 0,  0],
    [0,  0, 10,  0,  5, 10,  5,  10, 0, -1] 
])

    for i, goal in enumerate(survivors):
        print(f"Start position: {start}")
        print(f"Goal position (survivor): {goal}")

        path = astar(grid, start, goal, allow_diagonal=True)

        print(f"A* Path to survivor {i+1}: {path}")

        if path:
            # Only visualize the path, not the initial or final grid states
            animate_path(grid, path)
            start = goal 
            grid[goal] = -2 

if __name__ == "__main__":
    test_astar_with_visualization()