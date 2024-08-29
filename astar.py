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
