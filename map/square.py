import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Square:

    def __init__(self, row, col, size, total_rows, total_cols, weight):
        # Positional variables
        self.row = row
        self.col = col
        self.x = (row * size) + size * 0.5
        self.y = (col * size) + size * 0.5
        self.size = size
        self.total_rows = total_rows
        self.total_cols = total_cols
        # Pathfinding variables
        self.neighbors = []
        self.id = 0
        self.barrier = False
        # State variables
        self.color = WHITE
        self.weight = weight
        self.hover = False

    # ########################### POSITION ########################### #

    def get_grid_pos(self):
        return self.row, self.col

    def get_pos(self):
        return self.x, self.y

    def get_weight(self):
        return self.weight

    # ############################# STATE ############################ #

    def is_barrier(self):
        return self.barrier

    def is_border(self):
        return self.col == 0 or self.row == 0 or self.col >= self.total_cols - 1 or self.row >= self.total_rows - 1

    def reset(self):
        self.barrier = False
        self.color = WHITE

    def make_barrier(self):
        self.barrier = True
        self.color = BLACK

    def set_id(self, id):
        self.id = int(id)

    # ########################## INTERACTIVE ######################### #

    def compare_node(self, node):
        return self.row == node.row and self.col == node.col

    def compare_pos(self, pos, threshold: int = 1):
        return (self.x - threshold <= pos[0] <= self.x + threshold) and (self.y - threshold <= pos[1] <= self.y + threshold)

    def surrounding_barrier(self, grid):
        if self.row < self.total_rows - 1:
            grid.nodes[self.row + 1][self.col].weight += 1

        if self.col < self.total_cols - 1:
            grid.nodes[self.row][self.col + 1].weight += 1

        if self.row < self.total_rows - 1 and self.col < self.total_cols - 1:
            grid.nodes[self.row + 1][self.col + 1].weight += 1

        if self.col > 0:
            grid.nodes[self.row][self.col - 1].weight += 1

        if self.col > 0 and self.row < self.total_rows - 1:
            grid.nodes[self.row + 1][self.col - 1].weight += 1

        if self.row > 0:
            grid.nodes[self.row - 1][self.col].weight += 1

        if self.row > 0 and self.col < self.total_cols - 1:
            grid.nodes[self.row - 1][self.col + 1].weight += 1

        if self.row > 0 and self.col > 0:
            grid.nodes[self.row - 1][self.col - 1].weight += 1

    # #################################### PATHFINDING FUNCTIONS #################################### #

    def is_terminal(self):
        return self.color == RED

    def is_path(self):
        return self.color == YELLOW

    def make_selected(self):
        self.color = GREEN

    def make_terminal(self):
        self.color = RED

    def make_path(self):
        self.color = YELLOW

    # #################################### PYGAME FUNCTIONS #################################### #

    def draw(self, win):
        # Calculate the top-left corner of the rectangle
        top_left_x = self.x - self.size / 2
        top_left_y = self.y - self.size / 2

        # Draw the rectangle with the adjusted coordinates
        pygame.draw.rect(win, self.color, (top_left_x, top_left_y, self.size * 0.99, self.size * 0.99))

    def update_neighbors(self, grid):
        self.neighbors = []

        # ################################# CARDINAL NEIGHBOURS ################################# #

        if self.row < self.total_rows - 1 and not grid.nodes[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid.nodes[self.row + 1][self.col])

        if self.row > 0 and not grid.nodes[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid.nodes[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid.nodes[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid.nodes[self.row][self.col + 1])

        if self.col > 0 and not grid.nodes[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid.nodes[self.row][self.col - 1])

        # ################################# DIAGONAL NEIGHBOURS ################################# #

        # LEFT UP
        if self.col > 0 and self.row > 0 and ((not grid.nodes[self.row - 1][self.col].is_barrier()) or (
                not grid.nodes[self.row][self.col - 1].is_barrier())) and not grid.nodes[self.row - 1][
                self.col - 1].is_barrier() and (not grid.nodes[self.row-1][self.col].is_barrier() and not grid.nodes[self.row][self.col-1].is_barrier()):
            self.neighbors.append(grid.nodes[self.row - 1][self.col - 1])

        # RIGHT UP
        if self.row > 0 and self.col < self.total_rows - 1 and (
                (not grid.nodes[self.row - 1][self.col].is_barrier()) or (
                not grid.nodes[self.row][self.col + 1].is_barrier())) and not grid.nodes[self.row - 1][
            self.col + 1].is_barrier() and (not grid.nodes[self.row-1][self.col].is_barrier() and not grid.nodes[self.row][self.col+1].is_barrier()):
            self.neighbors.append(grid.nodes[self.row - 1][self.col + 1])

        # RIGHT DOWN
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and (
                (not grid.nodes[self.row][self.col + 1].is_barrier()) or (
                not grid.nodes[self.row + 1][self.col].is_barrier())) and not grid.nodes[self.row + 1][
                self.col + 1].is_barrier() and (not grid.nodes[self.row+1][self.col].is_barrier() and not grid.nodes[self.row][self.col+1].is_barrier()):
            self.neighbors.append(grid.nodes[self.row + 1][self.col + 1])

        # LEFT DOWN
        if self.col > 0 and self.row < self.total_rows - 1 and (
                (not grid.nodes[self.row][self.col - 1].is_barrier()) or (
                not grid.nodes[self.row + 1][self.col].is_barrier())) and (not grid.nodes[self.row + 1][
                self.col - 1].is_barrier()) and (not grid.nodes[self.row+1][self.col].is_barrier() and not grid.nodes[self.row][self.col-1].is_barrier()):
            self.neighbors.append(grid.nodes[self.row + 1][self.col - 1])
