import pygame
from utils.constants import *


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        SQUARE CLASS                                           #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Square:
    """
    A class representing a square grid cell in the pathfinding visualization grid.

    Attributes:
        row (int): The row index of the square.
        col (int): The column index of the square.
        x (float): The x-coordinate of the center of the square.
        y (float): The y-coordinate of the center of the square.
        size (int): The size of the square.
        total_rows (int): The total number of rows in the grid.
        total_cols (int): The total number of columns in the grid.
        neighbors (list): A list of neighboring squares.
        id (int): The identification number of the square.
        barrier (bool): A flag indicating whether the square is a barrier.
        color (tuple): The color of the square.
        weight (int): The weight of the square used in pathfinding algorithms.
        hover (bool): A flag indicating whether the square is being hovered over.
    """

    def __init__(self, row, col, size, total_rows, total_cols, weight):
        """
        Initializes a Square object with the given parameters.

        Args:
            row (int): The row index of the square.
            col (int): The column index of the square.
            size (int): The size of the square.
            total_rows (int): The total number of rows in the grid.
            total_cols (int): The total number of columns in the grid.
            weight (int): The weight of the square used in pathfinding algorithms.

        Returns:
            None
        """
        self.row = row
        self.col = col
        self.x = (row * size) + size * 0.5
        self.y = (col * size) + size * 0.5
        self.size = size
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.neighbors = []
        self.id = 0
        self.barrier = False
        self.color = WHITE
        self.weight = weight
        self.hover = False

    # ####################################################################### #
    #                                  DRAW                                   #
    # ####################################################################### #

    def draw(self, win):
        """
        Draw the square on the pygame window surface.

           Args:
            win (pygame.Surface): The pygame window surface.
           Returns:
            None
         """
        # Calculate the top-left corner of the rectangle
        top_left_x = self.x - self.size / 2
        top_left_y = self.y - self.size / 2

        # Draw the rectangle with the adjusted coordinates
        if GRID_SHOW:
            pygame.draw.rect(win, self.color, (top_left_x, top_left_y, self.size * 0.99, self.size * 0.99))
        else:
            pygame.draw.rect(win, self.color, (top_left_x, top_left_y, self.size, self.size))

    # ####################################################################### #
    #                                POSITION                                 #
    # ####################################################################### #

    def get_grid_pos(self):
        """
        Get the row and column indices of the square.

        Returns:
            tuple: The row and column indices of the square.
        """
        return self.row, self.col

    def get_pos(self):
        """
        Get the coordinates of the center of the square.

        Returns:
            tuple: The x and y coordinates of the center of the square.
        """
        return self.x, self.y

    # ####################################################################### #
    #                                VARIABLES                                #
    # ####################################################################### #

    def get_weight(self):
        """
        Get the weight of the square.

        Returns:
            int: The weight of the square.
        """
        return self.weight

    def is_barrier(self):
        """
        Check if the square is a barrier.

        Returns:
            bool: True if the square is a barrier, False otherwise.
        """
        return self.barrier

    def is_border(self):
        """
        Check if the square is on the border of the grid.

        Returns:
            bool: True if the square is on the border, False otherwise.
        """
        return self.col == 0 or self.row == 0 or self.col >= self.total_cols - 1 or self.row >= self.total_rows - 1

    def reset(self):
        """
        Reset the state of the square.

        Returns:
            None
        """
        self.barrier = False
        self.color = WHITE

    def make_barrier(self):
        """
        Make the square a barrier.

        Returns:
            None
        """
        self.barrier = True
        self.color = BLACK

    def make_selected(self):
        """
        Mark the square as selected.

        Returns:
            None
        """
        self.color = GREEN

    # ####################################################################### #
    #                                NEIGHBOURS                               #
    # ####################################################################### #

    def surrounding_barrier(self, grid):
        """
        Update the weights of neighboring squares.

        Args:
            grid (Grid): The grid containing the squares.

        Returns:
            None
        """
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

    def update_neighbors(self, grid):
        """
        Update the neighboring squares of the square.

        Args:
            grid (Grid): The grid containing the squares.

        Returns:
            None
        """
        self.neighbors = []

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~          DOWN         ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.row < self.total_rows - 1 and not grid.nodes[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid.nodes[self.row + 1][self.col])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~           UP          ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.row > 0 and not grid.nodes[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid.nodes[self.row - 1][self.col])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~         RIGHT         ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.col < self.total_rows - 1 and not grid.nodes[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid.nodes[self.row][self.col + 1])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~         LEFT          ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.col > 0 and not grid.nodes[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid.nodes[self.row][self.col - 1])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~        LEFT-UP        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.col > 0 and self.row > 0 and ((not grid.nodes[self.row - 1][self.col].is_barrier()) or (
                not grid.nodes[self.row][self.col - 1].is_barrier())) and not grid.nodes[self.row - 1][
            self.col - 1].is_barrier():
            self.neighbors.append(grid.nodes[self.row - 1][self.col - 1])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       RIGHT-UP        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.row > 0 and self.col < self.total_rows - 1 and (
                (not grid.nodes[self.row - 1][self.col].is_barrier()) or (
                not grid.nodes[self.row][self.col + 1].is_barrier())) and not grid.nodes[self.row - 1][
            self.col + 1].is_barrier():
            self.neighbors.append(grid.nodes[self.row - 1][self.col + 1])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       RIGHT-DOWN      ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and (
                (not grid.nodes[self.row][self.col + 1].is_barrier()) or (
                not grid.nodes[self.row + 1][self.col].is_barrier())) and not grid.nodes[self.row + 1][
            self.col + 1].is_barrier():
            self.neighbors.append(grid.nodes[self.row + 1][self.col + 1])

        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       LEFT-DOWN       ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if self.col > 0 and self.row < self.total_rows - 1 and (
                (not grid.nodes[self.row][self.col - 1].is_barrier()) or (
                not grid.nodes[self.row + 1][self.col].is_barrier())) and not grid.nodes[self.row + 1][
            self.col - 1].is_barrier():
            self.neighbors.append(grid.nodes[self.row + 1][self.col - 1])

    # ####################################################################### #
    #                                  EQUALS                                 #
    # ####################################################################### #

    def compare_node(self, node):
        """
        Compare this square with another square.

        Args:
            node (Square): The square to compare with.

        Returns:
            bool: True if the squares have the same row and column indices, False otherwise.
        """
        return self.row == node.row and self.col == node.col

    def compare_pos(self, pos, threshold: int = 1):
        """
        Compare the position with the center of the square.

        Args:
            pos (tuple): The position to compare with.
            threshold (int): The threshold for the comparison.

        Returns:
            bool: True if the position is within the threshold distance of the center of the square, False otherwise.
        """
        return (self.x - threshold <= pos[0] <= self.x + threshold) and (
                self.y - threshold <= pos[1] <= self.y + threshold)
