import math
import random
import pygame
from map.square import Square


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                         GRID CLASS                                            #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Grid:
    """
    A class representing a grid environment for pathfinding visualization.

    Attributes:
        size (int): The size of the grid (number of rows/columns).
        win (pygame.Surface): The pygame window surface to draw the grid on.
        gap (int): The gap between grid cells calculated based on window size and grid size.
        font (pygame.font.Font): The font used for rendering text in grid cells.
        nodes (list): A 2D list containing all the grid cells (Square objects).
        hover (Square): The grid cell currently being hovered over by the mouse cursor.
    """

    def __init__(self, size, win):
        """
        Initializes the Grid object with the given size and window.

        Args:
            size (int): The size of the grid.
            win (pygame.Surface): The pygame window surface.

        Returns:
            None
        """
        w, _ = win.get_size()
        self.gap = w // size
        self.size = size
        self.win = win
        self.font = pygame.font.SysFont('Arial', self.gap)
        self.nodes = []
        self.hover = None

        self.create_array()

    def create_array(self):
        """
        Creates the grid by initializing Square objects in a 2D array.

        Returns:
            None
        """
        self.nodes = []
        for i in range(self.size):
            self.nodes.append([])
            for j in range(self.size):
                node = Square(i, j, self.gap, self.size, self.size, 0)
                self.nodes[i].append(node)
        self.update()

    def draw(self):
        """
        Draws the grid on the pygame window surface.

        Returns:
            None
        """
        self.win.fill((125, 125, 125))
        self.update()
        for row in self.nodes:
            for spot in row:
                spot.draw(self.win)
                if spot.is_border():
                    spot.make_barrier()

    def update(self):
        """
        Updates the neighbors and surrounding barriers of each grid cell.

        Returns:
            None
        """
        for row in self.nodes:
            for spot in row:
                spot.update_neighbors(self)
                spot.surrounding_barrier(self)

    def hover_over(self, node):
        """
        Highlights the grid cell currently being hovered over.

        Args:
            node (Square): The grid cell being hovered over.

        Returns:
            None
        """
        if self.hover is not None:
            if not self.hover.is_border() and not self.hover.is_barrier() and not self.hover.is_terminal() and not self.hover.is_path():
                self.hover.reset()
        if not node.is_border() and not node.is_barrier() and not node.is_terminal() and not node.is_path():
            node.make_selected()
        self.hover = node

    def get_node(self, pos):
        """
        Gets the grid cell at the specified position.

        Args:
            pos (tuple): The position (x, y) of the grid cell.

        Returns:
            Square: The grid cell at the specified position.
        """
        y, x = pos
        row = math.floor(y / self.gap)
        col = math.floor(x / self.gap)
        return self.nodes[row][col]

    def get_random_node(self):
        """
        Gets a random non-barrier grid cell.

        Returns:
            Square: A random non-barrier grid cell.
        """
        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - 1)
        node = self.nodes[row][col]
        while node.is_barrier():
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            node = self.nodes[row][col]
        return node

    def read_map(self, full_file_path):
        """
        Reads a map from a text file and updates the grid accordingly.

        Args:
            full_file_path (str): The full path to the text file containing the map.

        Returns:
            None
        """
        with open(full_file_path, 'r') as file:
            file_content = file.read()
            file_content_without_newline = file_content.replace('\n', '')
            split_result = [char for char in file_content_without_newline]
            list_of_nodes = []
            for row in self.nodes:
                for node in row:
                    list_of_nodes.append(node)
            for character, node in zip(split_result, list_of_nodes):
                if character == 'X':
                    node.make_barrier()
                else:
                    node.reset()
        print("Map imported successfully.")

