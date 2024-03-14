import pygame

from game.sprites.spritesheet import SpriteSheet
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
        self.tile_id = []

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
        self.is_floating = False

        self._current_frame = 0
        self._delay_frame = 2
        self._pass_frame = self._delay_frame
        self._jump_frame = 1
        self._state = 0

        self._key_offset = 0
        self._key_speed = 0.25
        self._key_limit = 1

    # ####################################################################### #
    #                                VARIABLES                                #
    # ####################################################################### #

    def set_id(self, node_id):
        self.id = int(node_id)

    def get_id(self):
        return self.id

    def set_tile_id(self, tile_id, is_objects_map):
        self.tile_id.append(int(tile_id))
        if is_objects_map and tile_id in FLOATING_TILES:
            self.is_floating = True
            self.barrier = False

    # ####################################################################### #
    #                                  DRAW                                   #
    # ####################################################################### #

    def draw_rect(self, win, offset):
        position_x = offset.x + self.size // 2
        position_y = offset.y + self.size // 2

        # Calculate the top-left corner of the rectangle
        top_left_x = (self.x - self.size / 2) - position_x - (self.size // 2)
        top_left_y = (self.y - self.size / 2) - position_y - (self.size // 2)

        # Check if the rectangle is completely outside the surface
        if (top_left_x + self.size * 2 < 0 or top_left_x > win.get_width() or
                top_left_y + self.size * 2 < 0 or top_left_y > win.get_height()):
            return  # Rectangle is completely outside the surface

        pygame.draw.rect(win, self.color, ((self.x - position_x), (self.y - position_y), self.size, self.size))

    def draw_sprite(self, win, sprite_id, sprite_sheet: SpriteSheet, offset):
        if sprite_id < 0 or sprite_sheet is None:
            return

        position_x = offset.x + self.size // 2
        position_y = offset.y + self.size // 2

        # Draw the tile with the adjusted coordinates
        tile = sprite_sheet.get_sprite_by_number(sprite_id)
        win.blit(tile, (self.x - position_x, self.y - position_y))

    def draw(
            self,
            win,
            sprite_sheet: SpriteSheet,
            offset=None,
            only_float=False,
            only_floor=False,
            key_sheet: SpriteSheet = None
    ):
        position_x = offset.x + self.size // 2
        position_y = offset.y + self.size // 2

        # Calculate the top-left corner of the rectangle
        top_left_x = (self.x - self.size / 2) - position_x - (self.size // 2)
        top_left_y = (self.y - self.size / 2) - position_y - (self.size // 2)

        if (top_left_x + self.size * 2 < 0 or top_left_x > win.get_width() or
                top_left_y + self.size * 2 < 0 or top_left_y > win.get_height()):
            return

        if only_floor:
            tiles_to_draw = [sprite_id for sprite_id in self.tile_id if sprite_id in GROUND_TILES]
        elif only_float:
            tiles_to_draw = [sprite_id for sprite_id in self.tile_id if
                             sprite_id in FLOATING_TILES and sprite_id >= 0]
        else:
            tiles_to_draw = [sprite_id for sprite_id in self.tile_id if
                             sprite_id not in GROUND_TILES and sprite_id >= 0 and sprite_id not in FLOATING_TILES]
            for i in range(len(tiles_to_draw)):
                if tiles_to_draw[i] in ANIMATED_TILES:
                    tiles_to_draw[i] = self.animate(tiles_to_draw[i])
                    break

        if tiles_to_draw is not None and len(tiles_to_draw) > 0:
            for sprite_id in tiles_to_draw:
                self.draw_sprite(win, sprite_id, sprite_sheet, offset)

        # Draw the key if possible.
        if key_sheet is not None and self.is_key and not only_float:
            temp = pygame.math.Vector2(offset.x, offset.y)
            temp.y = temp.y + self._key_offset
            self._key_offset = self._key_offset + self._key_speed
            if abs(self._key_offset) >= self._key_limit:
                self._key_speed = self._key_speed * -1
                self._key_offset = self._key_offset + self._key_speed
            self.draw_sprite(win, 79, key_sheet, temp)

    def animate(self, tile_id):
        if self._current_frame >= 3:
            self._current_frame = 0
        else:
            if self._pass_frame == 0:
                self._current_frame = self._current_frame + 1
                self._pass_frame = self._delay_frame
            else:
                self._pass_frame = self._pass_frame - 1
        if tile_id == TILE_SCREEN:
            distance = 2
        else:
            distance = 1
        jump = distance * self._current_frame
        if self._current_frame > 0:
            jump = jump + self._jump_frame
        return tile_id + jump

    # ####################################################################### #
    #                                POSITION                                 #
    # ####################################################################### #

    def get_grid_pos(self):
        return self.row, self.col

    def get_pos(self):
        return self.x, self.y

    def distance_to(self, other_node):
        x1, y1 = self.get_pos()
        x2, y2 = other_node.get_pos()
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # ####################################################################### #
    #                                VARIABLES                                #
    # ####################################################################### #

    def set_tile_set(self, tile_id_list):
        self.tile_id = tile_id_list

    def get_weight(self):
        return self.weight

    def is_barrier(self):
        return self.barrier

    def is_border(self):
        return self.col == 0 or self.row == 0 or self.col >= self.total_cols - 1 or self.row >= self.total_rows - 1

    def reset(self):
        self.barrier = False
        self.color = GRID_BACKGROUND

    def reset_for_editor(self):
        self.barrier = False
        self.color = WHITE
        self.id = 0

    def make_barrier(self):
        self.barrier = True
        self.color = BLACK
        self.image.fill((0, 0, 0))

    def toggle_key(self):
        self.is_key = not self.is_key
        self.color = YELLOW if self.is_key else WHITE  # TODO: Check
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
