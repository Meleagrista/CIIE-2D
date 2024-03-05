import csv

from pygame import Surface

from game.map.spritesheet import Spritesheet
from utils.constants import GRID_BACKGROUND, MAP, TILEMAP, SPRITE_SHEET, SQUARE_SIZE
from game.map.square import Square

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

    def __init__(self, size, win, map_path=None, tilemap_path=None, sprite_sheet_path=None):
        self.groups = []
        """
        Initializes the Grid object with the given size and window.

        Args:
            size (int): The size of the grid.
            win (pygame.Surface): The pygame window surface.

        Returns:
            None
        """
        w, _ = win.get_size()
        self.gap = SQUARE_SIZE  # w // size
        self.size = size
        self.win = win
        self.font = pygame.font.SysFont('Arial', self.gap)
        self.nodes = []
        self.hover = None

        self.create_array()
        self.read_border_map(MAP if map_path is None else map_path)
        self.read_tilemap(TILEMAP if tilemap_path is None else tilemap_path)
        self.sprite_sheet = Spritesheet(SPRITE_SHEET if sprite_sheet_path is None else sprite_sheet_path)
        self.update()

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

    def draw(self, *args, **kwargs):
        surface = kwargs.pop('internal_surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pyagme.Surface class")

        offset = kwargs.pop('offset', None)
        if offset is not None:
            if not isinstance(offset, pygame.math.Vector2):
                raise TypeError("offset must be an instance of Vector2 class")

        show_id = kwargs.pop('id', None)
        if show_id is not None:
            if not isinstance(show_id, bool):
                raise TypeError("show_id must be an instance of Boolean class")

        if offset is None:
            self.win.fill((125, 125, 125))
            for row in self.nodes:
                for spot in row:
                    spot.draw_sprite(self.win, self.sprite_sheet)
                    # spot.draw(self.win)
                    if spot.is_border():
                        spot.make_barrier()
                    elif spot.id != 0:
                        font = pygame.font.SysFont('arial', 20)
                        text = font.render(str(spot.id), True, (0, 0, 0))
                        self.win.blit(text, (spot.row * spot.size, spot.col * spot.size))
        else:
            font = pygame.font.SysFont('arial', 20)
            self.win.fill(GRID_BACKGROUND)
            for row in self.nodes:
                for spot in row:
                    spot.draw_sprite(surface, self.sprite_sheet, offset)
                    # spot.draw(surface, offset)
                    if spot.is_border():
                        spot.make_barrier()
                    elif spot.id != 0 and show_id:
                        text = font.render(str(spot.id), True, (0, 0, 0))
                        surface.blit(text,
                                     (spot.row * spot.size + spot.size // 2, spot.col * spot.size + spot.size // 2))

    def add(self, group):
        for row in self.nodes:
            for node in row:
                node.add(group)

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

    def get_random_node_from_zones(self, zone_ids):
        """
        Gets a random node from a list of possible ids.

        Returns:
            Square: A random node having one of the specified zone ids.
        """

        # Es un explorador: seleccionar un nodo cualquiera que no sea barrera
        if not zone_ids:
            return self.get_random_node()

        # Si no, escoger uno de la zona (o zonas) que pueda recorrer
        flattened_nodes = [node for row in self.nodes for node in row]
        possible_nodes = [node for node in flattened_nodes if node.id in set(zone_ids)]
        if not possible_nodes:
            return self.get_random_node()
        i = random.randint(0, len(possible_nodes) - 1)
        return possible_nodes[i]

    def get_random_node_from_zone(self, zone_id):
        flattened_nodes = [node for row in self.nodes for node in row]
        possible_nodes = [node for node in flattened_nodes if node.id == zone_id]
        if not possible_nodes:
            return None
        i = random.randint(0, len(possible_nodes) - 1)
        return possible_nodes[i]

    def set_key_square(self, x, y):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        self.nodes[x][y].toggle_key()

    def set_exit_square(self, x, y):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        self.nodes[x][y].make_exit()

    def is_key_square(self, x, y):
        node = self.get_node((x, y))
        return node.is_key

    def is_exit_square(self, x, y):
        node = self.get_node((x, y))
        return node.is_exit

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
                    node.make_room(int(character))
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

    def read_border_map(self, full_file_path):
        """
        Reads a map from a csv file and updates the grid accordingly.

        Args:
            full_file_path (str): The full path to the text file containing the map.

        Returns:
            None
        """
        with open(full_file_path, 'r') as file:
            csv_file = csv.reader(file)
            lines = []
            for line in csv_file:
                lines.append(line)

            x, y = 0, 0
            for row in self.nodes:
                x = 0
                for node in row:
                    if lines[x][y] == 'X':
                        node.make_barrier()
                    elif lines[x][y].isnumeric():
                        node.make_room(int(lines[x][y]))
                    else:
                        node.reset()
                    x += 1
                y += 1

        print("Map imported successfully.")

    def read_tilemap(self, file_path):
        tile_map = []
        with open(file_path, mode='r') as file:
            csv_file = csv.reader(file)
            for line in csv_file:
                tile_map.append(line)

        x, y = 0, 0
        for row in self.nodes:
            x = 0
            for square in row:
                square.set_tile_id(tile_map[x][y])
                x += 1
            y += 1

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
