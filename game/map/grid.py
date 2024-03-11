import csv

from pygame import Surface
from typing_extensions import deprecated

from game.sprites.spritesheet import SpriteSheet
from utils.constants import GRID_BACKGROUND, MAP, TILE_MAP, SQUARE_SIZE
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

    def __init__(self, size, win, border_map_path=None, tile_map_path=None, objects_map_path=None,
                 sprite_sheet_path=None, ss_columns=37, ss_rows=23):
        self.groups = []

        w, _ = win.get_size()
        self.gap = SQUARE_SIZE
        self.size = size
        self.win = win
        self.font = pygame.font.SysFont('Arial', self.gap)
        self.nodes = []
        self.hover = None

        self.create_array()

        self.spawn = None

        # Read border map (which also includes the room ids) and tile maps for ground and objects
        self.read_border_map(MAP if border_map_path is None else border_map_path)
        self.read_tile_map(TILE_MAP if tile_map_path is None else tile_map_path)
        self.read_tile_map(objects_map_path, True) if objects_map_path is not None else None

        # Set the sprite sheet for drawing the grid
        self.sprite_sheet = SpriteSheet(sprite_sheet_path, ss_columns, ss_rows) if tile_map_path is not None else None

        self.update()

    # ####################################################################### #
    #                                  TRIVIAL                                #
    # ####################################################################### #

    def create_array(self):
        self.nodes = []
        for i in range(self.size):
            self.nodes.append([])
            for j in range(self.size):
                node = Square(i, j, self.gap, self.size, self.size, 0)
                if node.is_border():
                    node.make_barrier()
                self.nodes[i].append(node)
        self.update()

    def draw(self, **kwargs):
        surface = kwargs.pop('internal_surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        offset = kwargs.pop('offset', None)
        if offset is not None:
            if not isinstance(offset, pygame.math.Vector2):
                raise TypeError("offset must be an instance of Vector2 class")
        else:
            print('There is no offset.')

        show_id = kwargs.pop('id', None)
        if show_id is not None:
            if not isinstance(show_id, bool):
                raise TypeError("show_id must be an instance of Boolean class")

        only_float = kwargs.pop('float', None)
        if only_float is not None:
            if not isinstance(only_float, bool):
                raise TypeError("float must be an instance of Boolean class")
        else:
            only_float = False

        only_floor = kwargs.pop('floor', None)
        if only_floor is not None:
            if not isinstance(only_floor, bool):
                raise TypeError("floor must be an instance of Boolean class")
        else:
            only_floor = False

        if only_floor:
            surface.fill(GRID_BACKGROUND)

        if offset is None:
            for row in self.nodes:
                for spot in row:
                    spot.draw(surface, self.sprite_sheet)

                    if spot.is_border():
                        spot.make_barrier()
        else:
            for row in self.nodes:
                for spot in row:
                    spot.draw(
                        win=surface,
                        sprite_sheet=self.sprite_sheet,
                        offset=offset,
                        only_float=only_float,
                        only_floor=only_floor
                    )

                    if spot.is_border():
                        spot.make_barrier()

    def add(self, group):
        for row in self.nodes:
            for node in row:
                node.add(group)

    def update(self):
        for row in self.nodes:
            for spot in row:
                spot.update_neighbors(self)
                spot.surrounding_barrier(self)

    # ####################################################################### #
    #                                   POSITION                              #
    # ####################################################################### #

    def get_node(self, pos):
        y, x = pos
        row = math.floor(y / self.gap)
        col = math.floor(x / self.gap)
        return self.nodes[row][col]

    def get_nodes_by_id(self, node_id):
        nodes = []
        for row in self.nodes:
            nodes = nodes + list(filter(lambda node: node.id == node_id, row))
        return nodes

    def get_random_node(self):
        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - 1)
        node = self.nodes[row][col]
        while node.is_barrier():
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            node = self.nodes[row][col]
        return node

    def get_random_node_from_zones(self, zone_ids):
        if not zone_ids:
            return self.get_random_node()

        flattened_nodes = [node for row in self.nodes for node in row]
        possible_nodes = [node for node in flattened_nodes if node.id in set(zone_ids)]
        if not possible_nodes:
            return self.get_random_node()
        i = random.randint(0, len(possible_nodes) - 1)
        return possible_nodes[i]

    def get_random_node_from_zone(self, zone_id):
        if zone_id is None:
            return self.get_random_node()
        flattened_nodes = [node for row in self.nodes for node in row]
        possible_nodes = [node for node in flattened_nodes if node.id == zone_id]
        if not possible_nodes:
            return None
        i = random.randint(0, len(possible_nodes) - 1)
        return possible_nodes[i]

    # ####################################################################### #
    #                                   NODES                                 #
    # ####################################################################### #

    def set_spawn_square(self, x, y):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            raise ValueError  # TODO: Add correct exception
        self.spawn = self.nodes[x][y]

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

    @deprecated("This method is no longer used.")
    def hover_over(self, node):
        if self.hover is not None:
            if not self.hover.is_border() and not self.hover.is_barrier():
                self.hover.reset()
        if not node.is_border() and not node.is_barrier():
            node.make_selected()
        self.hover = node

    # ####################################################################### #
    #                                    MAP                                  #
    # ####################################################################### #

    def read_map(self, full_file_path):
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
        with open(full_file_path, 'r') as file:
            csv_file = csv.reader(file)
            lines = []
            for line in csv_file:
                # Split the line into characters
                characters = list(line[0].strip())
                # Append the characters to the lines list
                lines.append(characters)

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

    def read_tile_map(self, file_path, is_objects_map=False):
        tile_map = []
        with open(file_path, mode='r') as file:
            csv_file = csv.reader(file)
            for line in csv_file:
                tile_map.append(line)

        x, y = 0, 0
        for row in self.nodes:
            x = 0
            for square in row:
                square.set_tile_id(int(tile_map[x][y]), is_objects_map)
                x += 1
            y += 1

        print("Tile map imported successfully.")

    # ####################################################################### #
    #                                COLLISIONS                               #
    # ####################################################################### #

    def has_collision(self, player_rect):
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
