from utils.constants import GRID_BACKGROUND, MAP
from map.square import Square

import math
import os
import random
import pygame


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
        self.read_map(MAP)

    # ####################################################################### #
    #                                  TRIVIAL                                #
    # ####################################################################### #

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
                if node.is_border():
                    node.make_barrier()
                self.nodes[i].append(node)
        self.update()

    def draw(self, show_id=False):
        """
        Draws the grid on the pygame window surface.

        Returns:
            None
        """
        font = pygame.font.SysFont('arial', 20)
        self.win.fill(GRID_BACKGROUND)
        self.update()
        for row in self.nodes:
            for spot in row:
                spot.draw(self.win)
                if spot.is_border():
                    spot.make_barrier()
                elif spot.id != 0 and show_id:
                    text = font.render(str(spot.id), True, (0, 0, 0))
                    self.win.blit(text, (spot.row * spot.size + spot.size // 2, spot.col * spot.size + spot.size // 2))

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

    # ####################################################################### #
    #                                   NODES                                 #
    # ####################################################################### #

    def hover_over(self, node):
        """
        Highlights the grid cell currently being hovered over.

        Args:
            node (Square): The grid cell being hovered over.

        Returns:
            None
        """
        if self.hover is not None:
            if not self.hover.is_border() and not self.hover.is_barrier():
                self.hover.reset()
        if not node.is_border() and not node.is_barrier():
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

    def get_nodes_by_id(self, node_id):
        """
        Gets all grid cells with the corresponding id.

        Args:
            node_id (int): The id of the grid cell.

        Returns:
            list: A list of all grid cells with the specified id.
        """
        nodes = []
        for row in self.nodes:
            nodes = nodes + list(filter(lambda node: node.id == node_id, row))
        return nodes

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

    # ####################################################################### #
    #                                    MAP                                  #
    # ####################################################################### #

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
                elif character.isnumeric():
                    node.set_id(int(character))
                else:
                    node.reset()
        print("Map imported successfully.")

    def save_map(self, file_path):
        """
        Stores the map in a text file.

        Args:
            file_path (str): The path to the folder where the map will be saved.

        Returns:
            None
        """
        files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        numbers = []
        for file in files:
            if file.startswith('map') and file.split('.')[0].split('-')[1].isdigit():
                numbers = [int(file.split('.')[0].split('-')[1])]
        if numbers:
            next_number = max(numbers) + 1
        else:
            next_number = 1

        with open(file_path + 'map-' + str(next_number) + '.txt', 'w') as file:
            for row in self.nodes:
                for node in row:
                    if node.is_barrier():
                        file.write('X')
                    else:
                        file.write(str(node.get_id()))
                file.write('\n')
        print("Map exported successfully.")

    # ####################################################################### #
    #                                COLLISIONS                               #
    # ####################################################################### #

    def has_collision(self, player_rect):
        """
        Checks whether the player (a square) is entering inside a barrier along the specified axis.

        Args:
            player_rect (pygame.Rect): The player's bounding box.

        Returns:
            tuple: A tuple containing a list of collided barrier nodes and a dictionary indicating collision directions.
        """

        # Get the grid cell containing the player
        player_node = self.get_node((player_rect.centerx, player_rect.centery))

        if player_node is None:
            return []  # Player position is outside the grid

        # Create a list to store collided barriers
        collided_barriers = []

        # Iterate through neighboring nodes and check for collision with barriers along the specified axis
        for neighbor in player_node.barriers:
            # Check collision between player_rect and neighbor's rect
            if player_rect.colliderect(neighbor.rect):
                collided_barriers.append(neighbor)

        return collided_barriers
