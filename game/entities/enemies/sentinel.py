import math
import random

import pygame

from game.entities.enemy import Enemy
from game.map.grid import Grid


class Sentinel(Enemy):
    def __init__(self,
                 position,
                 grid: Grid,
                 window: pygame.Surface,
                 areas
                 ):
        super().__init__(position, 1, 2, grid, window, areas)

        #    1. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~        VISUALS        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._animation_frames = 4
        self._animation_start = 10
        self._idle_frames = 4
        self._idle_start = 0

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       CHASING         ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.chase_node = None
        self.previous_node = None

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       VISION        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.ray_cone = 90
        self.ray_reach = 4
        self.ray_radius = self.ray_reach * self.grid.gap

    def notified(self, player):

        if player.detected():
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)

            if distance < self.ray_radius:
                if "sentinel" not in player.exposer:
                    player.exposer.append("sentinel")

            super().notified(player)

            if "sentinel" in player.exposer or "security" in player.exposer or distance < self.ray_radius * 1.5:
                player_node = self.grid.get_node((player.x, player.y))
                possible_nodes = player_node.neighbors
                possible_nodes.append(player_node)
                self.chase_node = random.choice(possible_nodes)
                self.previous_node = self.grid.get_node((self.x, self.y))
                self.set_path(self.chase_node)
                # self.update()

    def update(self, **kwargs):

        current_node = self.grid.get_node((self.x, self.y))

        if self.is_chasing():
            self._is_moving = True
            self.speed = 1.5
            self.ray_cone = 60
            self.ray_reach = 6
            self.ray_radius = self.ray_reach * self.grid.gap

            if self.next_point is None or self.chase_node.compare_node(current_node):
                self.chase_node = None
                self.set_path(self.previous_node)

            elif self.has_reached(self.next_point):
                self.set_next_point()
        else:
            self.speed = 1
            self.ray_cone = 90
            self.ray_reach = 4
            self.ray_radius = self.ray_reach * self.grid.gap

            if self.next_point is None or self.end_node.compare_node(current_node):
                self.set_path()
            elif self.has_reached(self.next_point):
                self.set_next_point()
        super().update(**kwargs)

    def is_chasing(self):
        return self.chase_node is not None
