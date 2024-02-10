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
        self.neighbours = []
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
        self.id = 0

    def make_barrier(self):
        self.barrier = True
        self.color = BLACK
        self.id = 0

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

    def set_id(self, id):
        self.id = int(id)

    def get_id(self):
        return self.id

    def make_selected(self):
        self.color = GREEN

    def make_terminal(self):
        self.color = RED

    def make_path(self):
        self.color = YELLOW

    def update_neighbours(self, grid):

        # clean neighbours
        self.neighbours = []

        # auxiliar definitions
        bottom = self.row == self.total_rows - 1
        top = self.row == 0
        rightmost = self.col == self.total_cols - 1
        leftmost = self.col == 0

        down_node = up_node = right_node = left_node = None
        left_down_node = right_down_node = left_up_node = right_up_node = None

        # assign accessible cardinal nodes
        if not bottom:
            down_node = grid.nodes[self.row + 1][self.col]

        if not top:
            up_node = grid.nodes[self.row - 1][self.col]

        if not rightmost:
            right_node = grid.nodes[self.row][self.col + 1]

        if not leftmost:
            left_node = grid.nodes[self.row][self.col - 1]

        # assign accessible diagonal nodes
        if not bottom and not leftmost:
            left_down_node = grid.nodes[self.row + 1][self.col - 1]

        if not bottom and not rightmost:
            right_down_node = grid.nodes[self.row + 1][self.col + 1]

        if not top and not leftmost:
            left_up_node = grid.nodes[self.row - 1][self.col - 1]

        if not top and not rightmost:
            right_up_node = grid.nodes[self.row - 1][self.col + 1]

        # cardinal checks & additions
        if down_node is not None:
            self.add_neighbour(down_node)

        if up_node is not None:
            self.add_neighbour(up_node)

        if right_node is not None:
            self.add_neighbour(right_node)

        if left_node is not None:
            self.add_neighbour(left_node)

        # diagonal checks & additions
        if left_down_node is not None and (
                not left_node.is_barrier() and not down_node.is_barrier()):
            self.add_neighbour(left_down_node)

        if left_up_node is not None and (
                not left_node.is_barrier() and not up_node.is_barrier()):
            self.add_neighbour(left_up_node)

        if right_down_node is not None and (
                not right_node.is_barrier() and not down_node.is_barrier()):
            self.add_neighbour(right_down_node)

        if right_up_node is not None and (
                not right_node.is_barrier() and not up_node.is_barrier()):
            self.add_neighbour(right_up_node)

    def add_neighbour(self, node):
        if not node.is_barrier():
            self.neighbours.append(node)

    # #################################### PYGAME FUNCTIONS #################################### #

    def draw(self, win):
        # Calculate the top-left corner of the rectangle
        top_left_x = self.x - self.size / 2
        top_left_y = self.y - self.size / 2

        # Draw the rectangle with the adjusted coordinates
        pygame.draw.rect(win, self.color, (top_left_x, top_left_y, self.size * 0.99, self.size * 0.99))


