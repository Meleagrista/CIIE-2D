import math
import pygame

from game.entities.enemies.enemy import Enemy
from game.map.grid import Grid
from utils.constants import GREEN, FPS


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
        self.vision_timer = 0
        self.vision_max = 100
        self.player = None
        self.chase_node = None
        self.previous_node = None

    def notified(self, player):
        distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                             (player.rect.centery - self.rect.centery) ** 2)

        if player.detected():

            if distance < self.ray_radius:
                super().notified(player)

            if player.exposer == "civilian" or distance < self.ray_radius:

                if self.previous_node is None:
                    self.previous_node = self.grid.get_node((self.x, self.y))
                self.vision_timer = self.vision_max
                self.player = player

            self.update()

    def update(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))

        if self.has_vision():
            self.vision_timer = max(0, self.vision_timer - 1)
            self.chase_node = self.grid.get_node((self.player.x, self.player.y))

            if self.chase_node.compare_node(current_node):
                self.set_path(self.previous_node)
                self.previous_node = None
            elif self.has_reached(self.next_point):
                self.set_next_point()
                self.chase_node = self.grid.get_node((self.player.x, self.player.y))
                # simplified version to avoid slow turnings
                self.set_simplified_path(self.chase_node)

        else:
            # normal behaviour
            if self.next_point is None or self.end_node.compare_node(current_node):
                self.set_path()
            elif self.has_reached(self.next_point):
                self.set_next_point()

        super().general_update(**kwargs)

    def has_vision(self):
        return self.vision_timer > 0 and self.player is not None
