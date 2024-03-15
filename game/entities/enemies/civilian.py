import math

import pygame

from game.entities.enemy import Enemy
from game.map.grid import Grid
from game.sprites.spritesheet import SpriteSheet
from utils.constants import NPC_SIZE
from utils.paths.assets_paths import ENEMY_ASSETS


class Civilian(Enemy):
    def __init__(self,
                 position,
                 grid: Grid,
                 window: pygame.Surface,
                 area
                 ):
        super().__init__(position, 1, 8, grid, window, [area])

        #    1. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~        VISUALS        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._sprite_sheet = SpriteSheet(ENEMY_ASSETS, 10, 33, NPC_SIZE * 1.8)
        self._animation_frames = 4
        self._animation_start = 130
        self._idle_frames = 2
        self._idle_start = 122

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       ESCAPING        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.escape_node = None
        self.previous_node = None

        #    3. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       VISION        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.ray_cone = 120
        self.ray_reach = 2
        self.ray_radius = self.ray_reach * self.grid.gap

    def notified(self, player):

        current_room = self.grid.get_node((self.x, self.y)).get_id()
        player_room = self.grid.get_node((player.x, player.y)).get_id()

        if player.detected() and current_room == player_room:

            if self.within_reach((player.x, player.y)):
                if "civilian" not in player.exposer:
                    player.exposer.append("civilian")

            super().notified(player)

            self.escape_node = self.grid.get_random_node()
            while self.escape_node.get_id() == player_room:
                self.escape_node = self.grid.get_random_node()

            self.previous_node = self.grid.get_node((self.x, self.y))
            # Fewer segments to counter greater speed
            self.set_path(self.escape_node, 4)

    def update(self, **kwargs):

        current_node = self.grid.get_node((self.x, self.y))

        if self.is_escaping():
            self._is_moving = True
            self.speed = 3
            self.ray_cone = 240
            self.ray_reach = 1
            self.ray_radius = self.ray_reach * self.grid.gap

            if self.escape_node.compare_node(current_node):
                self.escape_node = None
                self.set_path(self.previous_node)
            elif self.has_reached(self.next_point):
                self.set_next_point()
        else:
            self.speed = 1
            self.ray_cone = 120
            self.ray_reach = 2
            self.ray_radius = self.ray_reach * self.grid.gap

            if self.next_point is None or self.end_node.compare_node(current_node):
                next_node = self.grid.get_random_node_from_zone(current_node.get_id())
                self.set_path(node=next_node)

        super().update(**kwargs)

    def is_escaping(self):
        return self.escape_node is not None
