import math
import random

import pygame

from game.entities.enemies.enemy import Enemy
from game.map.grid import Grid
from utils.constants import GREEN


class Sentinel(Enemy):
    def __init__(self,
                 position,
                 movement_speed,
                 rotation_speed,
                 grid: Grid,
                 window: pygame.Surface,
                 areas
                 ):
        super().__init__(position, movement_speed / 1.5, rotation_speed, grid, window, areas)

        #    1. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~        VISUALS        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._animation_start = 70
        self._idle_start = 80

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       CHASING         ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.chase_node = None
        self.previous_node = None

    def notified(self, player):

        if player.detected():
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)
            if distance < self.ray_radius:
                player.exposer = "sentinel"
            super().notified(player)

            if player.exposer == "sentinel" or player.exposer == "security":
                player_node = self.grid.get_node((player.x, player.y))
                possible_nodes = player_node.neighbors
                possible_nodes.append(player_node)
                self.chase_node = random.choice(possible_nodes)
                self.previous_node = self.grid.get_node((self.x, self.y))
                self.set_path(self.chase_node)
                self.update()

    def update(self, **kwargs):

        current_node = self.grid.get_node((self.x, self.y))

        if self.is_chasing():
            if self.next_point is None or self.chase_node.compare_node(current_node):
                self.chase_node = None
                self.set_path(self.previous_node)

            elif self.has_reached(self.next_point):
                self.set_next_point()
        else:
            # normal behaviour
            if self.next_point is None or self.end_node.compare_node(current_node):
                self.set_path()
            elif self.has_reached(self.next_point):
                self.set_next_point()
        super().update(**kwargs)

    def is_chasing(self):
        return self.chase_node is not None
