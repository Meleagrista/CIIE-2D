import math
import pygame

from game.entities.enemies.enemy import Enemy
from game.map.grid import Grid


class Security(Enemy):
    def __init__(self,
                 position,
                 movement_speed,
                 rotation_speed,
                 grid: Grid,
                 window: pygame.Surface,
                 areas
                 ):
        super().__init__(position, movement_speed, rotation_speed, grid, window, areas)

        #    1. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ CHASING RELATED VARS  ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._idle_start = 0

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ CHASING RELATED VARS  ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.chase_position = None
        self.seen_positions = []

    def notified(self, player):
        distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                             (player.rect.centery - self.rect.centery) ** 2)

        if player.detected() and distance < self.ray_radius:
            self.update()

    def update(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))
        super().general_update(**kwargs)
