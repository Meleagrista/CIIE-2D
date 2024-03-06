import pygame

from game.map.spritesheet import Spritesheet
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
        barriers (list): A list of surrounding barriers.
        id (int): The identification number of the square.
        barrier (bool): A flag indicating whether the square is a barrier.
        color (tuple): The color of the square.
        weight (int): The weight of the square used in pathfinding algorithms.
        hover (bool): A flag indicating whether the square is being hovered over.
        rect (pygame.Rect): The rectangle representing the square.
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
        super().__init__()

        self.row = row
        self.col = col
        self.x = (row * size) + size * 0.5
        self.y = (col * size) + size * 0.5
        self.size = size
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.neighbors = []
        self.barriers = []
        self.id = -1
        self.tile_id = -1
        self.barrier = False
        self.color = GRID_BACKGROUND
        self.weight = weight
        self.hover = False

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.rect = pygame.Rect((row * size), (col * size), size + 1, size + 1)

        self.is_key = False
        self.is_exit = False

    # ####################################################################### #
    #                                VARIABLES                                #
    # ####################################################################### #

    def set_id(self, node_id):
        self.id = int(node_id)

    def get_id(self):
        return self.id

    def set_tile_id(self, tile_id):
        self.tile_id = int(tile_id)

    # ####################################################################### #
    #                                  DRAW                                   #
    # ####################################################################### #

    def draw(self, win, offset=None):
        """
        Draw the square on the pygame window surface.

           Args:
            win (pygame.Surface): The pygame window surface.
            offset: offset to be drawn on the pygame surface

           Returns:
            None
         """
        if offset is None:
            # Calculate the top-left corner of the rectangle
            top_left_x = self.x - self.size / 2
            top_left_y = self.y - self.size / 2

            # Draw the rectangle with the adjusted coordinates
            pygame.draw.rect(win, self.color, (top_left_x, top_left_y, self.size * 0.99, self.size * 0.99))
        else:
            position_x = offset.x + self.size // 2
            position_y = offset.y + self.size // 2

            # Calculate the top-left corner of the rectangle
            top_left_x = (self.x - self.size / 2) - position_x - (self.size // 2)
            top_left_y = (self.y - self.size / 2) - position_y - (self.size // 2)

            # Check if the rectangle is completely outside the surface
            if (top_left_x + self.size * 2 < 0 or top_left_x > win.get_width() or
                    top_left_y + self.size * 2 < 0 or top_left_y > win.get_height()):
                return  # Rectangle is completely outside the surface

            # Draw the rectangle with the adjusted coordinates
            if GRID_SHOW:
                pygame.draw.rect(win, self.color, (top_left_x, top_left_y, self.size * 0.99, self.size * 0.99))
            else:
                pygame.draw.rect(win, self.color, ((self.x - position_x), (self.y - position_y), self.size, self.size))

    def draw_sprite(self, win, spritesheet: Spritesheet, offset=None):
        """
        Draw the square on the pygame window surface.

           Args:
            win (pygame.Surface): The pygame window surface.
            offset: offset to be drawn on the pygame surface
            spritesheet

           Returns:
            None
         """
        if self.tile_id == -1 or spritesheet is None:
            self.draw(win, offset)
            return

        if offset is None:
            # Calculate the top-left corner of the rectangle
            top_left_x = self.x - self.size / 2
            top_left_y = self.y - self.size / 2

            # Draw the tile with the adjusted coordinates
            tile = spritesheet.get_sprite_by_number(self.tile_id)
            win.blit(tile, (top_left_x, top_left_y))
        else:
            position_x = offset.x + self.size // 2
            position_y = offset.y + self.size // 2

            tile = spritesheet.get_sprite_by_number(self.tile_id)
            win.blit(tile, (self.x - position_x, self.y - position_y))

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
        self.color = GRID_BACKGROUND

    def reset_for_editor(self):
        """
        Reset the state of the square, setting white.

        Returns:
            None
        """
        self.barrier = False
        self.color = WHITE
        self.id = 0

    def make_barrier(self):
        """
        Make the square a barrier.

        Returns:
            None
        """
        self.barrier = True
        self.color = BLACK
        self.image.fill((0, 0, 0))

    def toggle_key(self):
        self.is_key = not self.is_key
        self.color = YELLOW if self.is_key else WHITE  # Funcionará?
        self.image.fill((0, 0, 0))

    def make_exit(self):
        self.is_exit = True
        self.color = GREEN
        self.image.fill((0, 0, 0))

    def make_room(self, room_id):
        self.barrier = False
        self.color = WHITE
        self.set_id(room_id)
        self.image.fill((255, 255, 255))

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
        Update the weights of neighboring squares if the current square is a barrier.

        Args:
            grid (Grid): The grid containing the squares.

        Returns:
            None
        """
        bottom = self.row == self.total_rows - 1
        top = self.row == 0
        rightmost = self.col == self.total_cols - 1
        leftmost = self.col == 0

        if self.is_barrier():
            if not bottom:
                grid.nodes[self.row + 1][self.col].weight += WEIGHT
            if not rightmost:
                grid.nodes[self.row][self.col + 1].weight += WEIGHT
            if not top:
                grid.nodes[self.row - 1][self.col].weight += WEIGHT
            if not leftmost:
                grid.nodes[self.row][self.col - 1].weight += WEIGHT

    def add_neighbour(self, node, force_barrier=False):
        """
        Add a node as a neighbor if it's not a barrier.

        Args:
            node (Node): The node to be added as a neighbor.
            force_barrier (Bool): Whether the node must be always a barrier.

        Returns:
            None
            :param node:
            :param force_barrier:
        """
        if node.is_barrier() or force_barrier:
            self.barriers.append(node)
        else:
            self.neighbors.append(node)

    def update_neighbors(self, grid):
        """
        Update the neighboring squares of the square based on its position.

        Args:
            grid (Grid): The grid containing the squares.

        Returns:
            None
        """
        self.neighbors = []
        self.barriers = []

        bottom = self.row == self.total_rows - 1
        top = self.row == 0
        rightmost = self.col == self.total_cols - 1
        leftmost = self.col == 0

        down_node = up_node = right_node = left_node = None
        left_down_node = right_down_node = left_up_node = right_up_node = None

        # Assign accessible cardinal nodes
        if not bottom:
            down_node = grid.nodes[self.row + 1][self.col]

        if not top:
            up_node = grid.nodes[self.row - 1][self.col]

        if not rightmost:
            right_node = grid.nodes[self.row][self.col + 1]

        if not leftmost:
            left_node = grid.nodes[self.row][self.col - 1]

        # Assign accessible diagonal nodes
        if not bottom and not leftmost:
            left_down_node = grid.nodes[self.row + 1][self.col - 1]

        if not bottom and not rightmost:
            right_down_node = grid.nodes[self.row + 1][self.col + 1]

        if not top and not leftmost:
            left_up_node = grid.nodes[self.row - 1][self.col - 1]

        if not top and not rightmost:
            right_up_node = grid.nodes[self.row - 1][self.col + 1]

        # Cardinal checks & additions
        if down_node is not None:
            self.add_neighbour(down_node)

        if up_node is not None:
            self.add_neighbour(up_node)

        if right_node is not None:
            self.add_neighbour(right_node)

        if left_node is not None:
            self.add_neighbour(left_node)

        # Diagonal checks & additions
        if left_down_node is not None and (
                not left_node.is_barrier() and not down_node.is_barrier()):
            self.add_neighbour(left_down_node)

        if left_down_node is not None and left_down_node.is_barrier():
            self.add_neighbour(left_down_node, force_barrier=True)

        if left_up_node is not None and (
                not left_node.is_barrier() and not up_node.is_barrier()):
            self.add_neighbour(left_up_node)

        if left_up_node is not None and left_up_node.is_barrier():
            self.add_neighbour(left_up_node, force_barrier=True)

        if right_down_node is not None and (
                not right_node.is_barrier() and not down_node.is_barrier()):
            self.add_neighbour(right_down_node)

        if right_down_node is not None and right_down_node.is_barrier():
            self.add_neighbour(right_down_node, force_barrier=True)

        if right_up_node is not None and (
                not right_node.is_barrier() and not up_node.is_barrier()):
            self.add_neighbour(right_up_node)

        if right_up_node is not None and right_up_node.is_barrier():
            self.add_neighbour(right_up_node, force_barrier=True)

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
