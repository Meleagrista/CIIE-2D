import math
import pygame

from game.entities.enemies.enemy import Enemy
from game.map.grid import Grid
from utils.constants import GREEN


class Guard(Enemy):
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
            player.exposer = "guard"
            super().notified(player)

            if self.chase_position is not None:
                self.seen_positions.append(self.chase_position)
            self.chase_position = self.grid.get_node((player.x, player.y))
            self.set_direct_path(self.chase_position)

            self.update()

    def update(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))

        if self.is_chasing():
            if self.chase_position.compare_node(current_node):
                # revert to normal status
                self._status = GREEN
                self.chase_position = None
                self.set_path()
            elif self.has_reached(self.next_point):
                self.set_next_point()
        else:
            # normal behaviour
            if self.next_point is None or self.end_node.compare_node(current_node):
                self.set_path()
            elif self.has_reached(self.next_point):
                self.set_next_point()

        super().general_update(**kwargs)

    def is_chasing(self):
        return self.chase_position is not None
