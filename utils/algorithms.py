import math
from queue import PriorityQueue


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                   PATHFINDING ALGORITHMS                                      #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

def heuristic(current, goal, weight):
    """
    Calculate the heuristic value.
    Args:
        current (Tuple[int, int]): Current position.
        goal (Tuple[int, int]): Goal position.
        weight (int): Weight.

    Returns:
        float: Heuristic value.
    """
    current_x, current_y = current
    goal_x, goal_y = goal
    return math.sqrt((current_x - goal_x) ** 2 + (current_y - goal_y) ** 2) + weight


def reconstruct_path(came_from, current):
    """
    Reconstruct the path from the start to the end.

    Args:
        came_from (Dict): Mapping of nodes to their predecessors.
        current: Current node.

    Returns:
        List: List of nodes representing the path.
    """
    nodes = [current]
    while current in came_from:
        current = came_from[current]
        nodes.append(current)
    return nodes[::-1]


def a_star(self):
    """
    Perform A* pathfinding.

    Returns:
        List: List of nodes representing the path.
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, self.start_node))
    came_from = {}
    g_score = {spot: float("inf") for row in self.grid.nodes for spot in row}
    g_score[self.start_node] = 0
    f_score = {spot: float("inf") for row in self.grid.nodes for spot in row}
    f_score[self.start_node] = heuristic(self.start_node.get_pos(), self.end_node.get_pos(), self.start_node.get_weight())
    open_set_hash = {self.start_node}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == self.end_node:
            return reconstruct_path(came_from, self.end_node)

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), self.end_node.get_pos(),
                                                             neighbor.get_weight())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return []
