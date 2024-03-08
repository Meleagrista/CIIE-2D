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


