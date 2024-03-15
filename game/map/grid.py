import csv
import random
from typing import List, Optional

import pygame
from pygame import Surface

from game.map.square import Square
from game.sprites.spritesheet import SpriteSheet
from utils.constants import GRID_BACKGROUND, MAP, TILE_MAP, SQUARE_SIZE
from utils.paths.assets_paths import UI_ICONS


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                         GRID CLASS                                            #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Grid:
    def __init__(self, size, win, border_map_path=None, tile_map_path=None, objects_map_path=None,
                 sprite_sheet_path=None, ss_columns=37, ss_rows=23):
        """
        Initialize a Grid object.

        Args:
            size (tuple): Size of the grid.
            win (pygame.Surface): Pygame window surface.
            border_map_path (str, optional): Path to the border map file. Defaults to None.
            tile_map_path (str, optional): Path to the tile map file. Defaults to None.
            objects_map_path (str, optional): Path to the objects map file. Defaults to None.
            sprite_sheet_path (str, optional): Path to the sprite sheet file. Defaults to None.
            ss_columns (int, optional): Number of columns in the sprite sheet. Defaults to 37.
            ss_rows (int, optional): Number of rows in the sprite sheet. Defaults to 23.
        """
        self.groups = []

        w, _ = win.get_size()
        self.gap = SQUARE_SIZE
        self.size = size
        self.win = win
        self.font = pygame.font.SysFont('Arial', self.gap)
        self.nodes = []
        self.hover = None

        self._create_array()

        # ──────── SPAWN POINT ──────── #
        self.spawn = None

        # ──────── KEY VISIBILITY ──────── #
        self.visible_key = True

        # ──────── READ MAPS ──────── #
        self.read_border_map(MAP if border_map_path is None else border_map_path)
        self.read_tile_map(TILE_MAP if tile_map_path is None else tile_map_path)
        self.read_tile_map(objects_map_path, True) if objects_map_path is not None else None

        # ──────── SPRITE SHEET ──────── #
        self.sprite_sheet = SpriteSheet(sprite_sheet_path, ss_columns, ss_rows, SQUARE_SIZE) if tile_map_path is not None else None
        self.key_sheet = SpriteSheet(UI_ICONS, 10, 9, SQUARE_SIZE)

        # ──────── UPDATE ──────── #
        self._update_array()

    # ####################################################################### #
    #                                  TRIVIAL                                #
    # ####################################################################### #

    def _create_array(self):
        self.nodes = []
        for i in range(self.size):
            self.nodes.append([])
            for j in range(self.size):
                node = Square(i, j, self.gap, self.size, self.size, 0)
                if node.is_border():
                    node.make_barrier()
                self.nodes[i].append(node)

    def _update_array(self):
        for row in self.nodes:
            for spot in row:
                spot.update_neighbors(self)
                spot.surrounding_barrier(self)

    def draw(self, **kwargs):
        surface = kwargs.pop('internal_surface', None)
        if surface is not None and not isinstance(surface, Surface):
            raise TypeError("surface must be an instance of pygame.Surface class")

        offset = kwargs.pop('offset', None)
        if offset is not None and not isinstance(offset, pygame.math.Vector2):
            raise TypeError("offset must be an instance of Vector2 class")
        else:
            print('There is no offset.') if offset is None else None

        show_id = kwargs.pop('id', None)
        if show_id is not None and not isinstance(show_id, bool):
            raise TypeError("show_id must be an instance of Boolean class")

        only_float = kwargs.pop('float', False)
        if not isinstance(only_float, bool):
            raise TypeError("float must be an instance of Boolean class")

        only_floor = kwargs.pop('floor', False)
        if not isinstance(only_floor, bool):
            raise TypeError("floor must be an instance of Boolean class")

        if only_floor:
            surface.fill(GRID_BACKGROUND)

        for row in self.nodes:
            for spot in row:
                if spot.is_key and self.visible_key:
                    key = self.key_sheet
                else:
                    key = None
                spot.draw(
                    win=surface,
                    sprite_sheet=self.sprite_sheet,
                    offset=offset,
                    only_float=only_float,
                    only_floor=only_floor,
                    key_sheet=key
                )
                if spot.is_border():
                    spot.make_barrier()

    def add(self, group):
        for row in self.nodes:
            for node in row:
                node.add(group)

    # ####################################################################### #
    #                                    MAP                                  #
    # ####################################################################### #

    def read_border_map(self, full_file_path: str) -> None:
        """
        Read the border map file and update the grid nodes accordingly.

        Args:
            full_file_path (str): The full file path of the border map file.
        """
        with open(full_file_path, 'r') as file:
            csv_file = csv.reader(file)
            lines = []
            for line in csv_file:
                # Split the line into characters
                characters = list(line[0].strip())
                # Append the characters to the lines list
                lines.append(characters)

            for y, row in enumerate(self.nodes):
                for x, node in enumerate(row):
                    if lines[x][y] == 'X':
                        node.make_barrier()
                    elif lines[x][y].isnumeric():
                        node.make_room(int(lines[x][y]))
                    else:
                        node.reset()

        # print("Map imported successfully.")

    def read_tile_map(self, file_path: str, is_objects_map: bool = False) -> None:
        """
        Read the tile map file and update the grid nodes accordingly.

        Args:
            file_path (str): The full file path of the tile map file.
            is_objects_map (bool, optional): A flag indicating whether the map is for objects. Defaults to False.
        """
        tile_map = []
        with open(file_path, mode='r') as file:
            csv_file = csv.reader(file)
            for line in csv_file:
                tile_map.append(line)

        for y, row in enumerate(self.nodes):
            for x, square in enumerate(row):
                square.set_tile_id(int(tile_map[x][y]), is_objects_map)

        # print("Tile map imported successfully.")

    # ####################################################################### #
    #                                COLLISIONS                               #
    # ####################################################################### #

    def has_collision(self, player_rect: pygame.Rect) -> List[Square]:
        """
        Check for collisions between the player and barriers in neighboring nodes.

        Args:
            player_rect (pygame.Rect): The rectangle representing the player.

        Returns:
            List[Barrier]: A list of barriers with which the player collides.
        """
        # Get the grid cell containing the player
        player_node = self.get_node((player_rect.centerx, player_rect.centery))

        if player_node is None:
            return []  # Player position is outside the grid

        # Create a list to store collided barriers
        collided_barriers: List[Square] = []

        # Iterate through neighboring nodes and check for collision with barriers along the specified axis
        for neighbor in player_node.barriers:
            # Check collision between player_rect and neighbor's rect
            if player_rect.colliderect(neighbor.rect):
                collided_barriers.append(neighbor)

        return collided_barriers

    # ####################################################################### #
    #                                   POSITION                              #
    # ####################################################################### #

    def get_node(self, pos: tuple) -> Square:
        """
        Get the node at the specified position.

        Args:
            pos (tuple): The position (y, x) of the node.

        Returns:
            Square: The node at the specified position.
        """
        y, x = map(int, pos)  # Convert y and x to integers
        row = y // self.gap
        col = x // self.gap
        return self.nodes[row][col]

    def get_node_from_array(self, row: int, col: int) -> Square:
        """
        Get the node from the array at the specified row and column.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            Square: The node at the specified row and column.
        """
        return self.nodes[row][col]

    def get_nodes_by_id(self, node_id: int) -> List[Square]:
        """
        Get nodes with the specified ID.

        Args:
            node_id (int): The ID of the nodes to retrieve.

        Returns:
            list: List of nodes with the specified ID.
        """
        return [node for row in self.nodes for node in row if node.id == node_id]

    def get_random_node(self) -> Square:
        """
        Get a random node that is not a barrier.

        Returns:
            Square: A random non-barrier node.
        """
        while True:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            node = self.nodes[row][col]
            if not node.is_barrier():
                return node

    def get_random_node_from_zones(self, zone_ids: List[int]) -> Optional[Square]:
        """
        Get a random node from zones with the specified IDs.

        Args:
            zone_ids (List[int]): List of zone IDs.

        Returns:
            Square: A random node from the specified zones, or None if no nodes found.
        """
        possible_nodes = [node for row in self.nodes for node in row if node.id in zone_ids]
        return random.choice(possible_nodes) if possible_nodes else None

    def get_random_node_from_zone(self, zone_id: int) -> Optional[Square]:
        """
        Get a random node from the zone with the specified ID.

        Args:
            zone_id (int): The ID of the zone.

        Returns:
            Square: A random node from the specified zone, or None if no nodes found.
        """
        possible_nodes = [node for row in self.nodes for node in row if node.id == zone_id]
        return random.choice(possible_nodes) if possible_nodes else None

    # ####################################################################### #
    #                                   NODES                                 #
    # ####################################################################### #

    def set_spawn_square(self, x: int, y: int) -> None:
        """
        Set the spawn square at the specified coordinates.

        Args:
            x (int): The x-coordinate of the spawn square.
            y (int): The y-coordinate of the spawn square.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            raise ValueError("Square out of bounds")
        self.spawn = self.nodes[x][y]

    def set_key_square(self, x: int, y: int) -> bool:
        """
        Set the key square at the specified coordinates.

        Args:
            x (int): The x-coordinate of the key square.
            y (int): The y-coordinate of the key square.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        self.nodes[x][y].make_key()
        return True

    def set_exit_square(self, x: int, y: int) -> bool:
        """
        Set the exit square at the specified coordinates.

        Args:
            x (int): The x-coordinate of the exit square.
            y (int): The y-coordinate of the exit square.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        self.nodes[x][y].make_exit()
        return True

    def is_key_square(self, x: int, y: int) -> bool:
        """
        Check if the square at the specified coordinates contains a key.

        Args:
            x (int): The x-coordinate of the square.
            y (int): The y-coordinate of the square.

        Returns:
            bool: True if the square contains a key, False otherwise.
        """
        node = self.get_node((x, y))
        return node.is_key

    def is_exit_square(self, x: int, y: int) -> bool:
        """
        Check if the square at the specified coordinates is an exit square.

        Args:
            x (int): The x-coordinate of the square.
            y (int): The y-coordinate of the square.

        Returns:
            bool: True if the square is an exit square, False otherwise.
        """
        node = self.get_node((x, y))
        return node.is_exit
