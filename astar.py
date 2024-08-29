import heapq
import numpy as np

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
        # Primary comparison by f_score
        if self.f == other.f:
            # Tie-breaker: Prefer nodes with a lower h_score
            return self.h < other.h
        return self.f < other.f


def manhattan_distance(node_position, end_position):
    return abs(node_position[0] - end_position[0]) + abs(node_position[1] - end_position[1])

def astar(maze, start, end, allow_diagonal=False):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []  # Priority queue for nodes to explore
    closed_list = np.zeros_like(maze, dtype=bool)  # Track visited nodes
    open_dict = {}  # Dictionary to track the best g-score for each position

    heapq.heappush(open_list, (start_node.f, start_node))
    open_dict[start_node.position] = start_node.g

    # Define possible movements
    move_positions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, down, left, right
    if allow_diagonal:
        move_positions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Add diagonals

    while open_list:
        # Get the node with the lowest f score
        current_node = heapq.heappop(open_list)[1]
        closed_list[current_node.position[0], current_node.position[1]] = True

        # Generate children (neighboring nodes)
        children = []
        for new_position in move_positions:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Check if the new position is within the grid bounds
            if not (0 <= node_position[0] < len(maze) and 0 <= node_position[1] < len(maze[0])):
                continue

            # Check if the new position is walkable (not an obstacle)
            if maze[node_position[0]][node_position[1]] == 10:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

            # Early goal check
            if new_node.position == end_node.position:
                path = []
                while new_node is not None:
                    path.append(new_node.position)
                    new_node = new_node.parent
                return path[::-1]  # Return reversed path

        # Loop through children
        for child in children:
            if closed_list[child.position[0], child.position[1]]:
                continue

            # Calculate costs for the child node
            terrain_cost = maze[child.position[0]][child.position[1]]
            if allow_diagonal and abs(child.position[0] - current_node.position[0]) + abs(child.position[1] - current_node.position[1]) == 2:
                terrain_cost *= 1.4  # Adjust cost for diagonal movement

            child.g = current_node.g + terrain_cost
            child.h = manhattan_distance(child.position, end_node.position)
            child.f = child.g + child.h

            # Check if a better path to this child already exists
            if child.position in open_dict and open_dict[child.position] <= child.g:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, (child.f, child))
            open_dict[child.position] = child.g

    # No path found
    return None

