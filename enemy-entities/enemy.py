import math
import random
from queue import PriorityQueue


def reconstruct_path(came_from, current):
    nodes = [current]
    while current in came_from:
        current = came_from[current]
        nodes.append(current)
        current.make_path()
    return nodes[::-1]


def heuristic(current, goal, weight):
    current_x, current_y = current
    goal_x, goal_y = goal
    return math.sqrt((current_x - goal_x) ** 2 +
                     (current_y - goal_y) ** 2) + weight


def a_star(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid.nodes for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid.nodes for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos(), start.get_weight())

    open_set_hash = {start}

    while not open_set.empty():

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return reconstruct_path(came_from, end)

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos(),
                                                             neighbor.get_weight())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return []


class Enemy:
    def __init__(self, grid):
        self.grid = grid
        self.end = None
        self.start = None
        self.nodes = []
        self.start: None
        self.end: None

    def get_path(self, grid):
        grid.update()
        self.nodes = a_star(grid, self.start, self.end)

    def set_start(self, node):
        # node.make_terminal()
        self.start = node

    def set_end(self, node):
        # node.make_terminal()
        self.end = node

    def set_random_end(self):
        row = random.randint(0, self.grid.size)
        col = random.randint(0, self.grid.size)
        self.end = self.grid.nodes[row][col]

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def traverse_path(self):
        # self.get_start().reset()
        # self.get_end().make_terminal()
        self.set_start(self.get_end())
        # new_node.make_terminal()
        self.set_random_end()
