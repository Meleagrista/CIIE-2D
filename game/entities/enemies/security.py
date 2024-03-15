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
        self.player = None
        self.chase_node = self.grid.spawn
        self.set_path(self.chase_node)
        self.update()

    def notified(self, player):

        if player.detected():
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)
            if distance < self.ray_radius:
                player.exposer = "security"
                super().notified(player)

        # player is stored to access its precise position
        if self.player is None:
            self.player = player

        self.update()

    def update(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))

        if self.player_known():
            # actively chasing the player
            self.chase_node = self.grid.get_node((self.player.x, self.player.y))

            if self.next_point is None or self.chase_node.compare_node(current_node):
                next_node = self.grid.get_random_node_from_zone(current_node.get_id())
                self.set_path(next_node)
            elif self.has_reached(self.next_point):
                self.set_next_point()
                # simplified version to avoid slow turnings
                self.set_simplified_path(self.chase_node)

        else:
            # normal behaviour
            if self.next_point is None or self.end_node.compare_node(current_node):
                next_node = self.grid.get_random_node_from_zone(current_node.get_id())
                self.set_path(next_node)
            elif self.has_reached(self.next_point):
                self.set_next_point()

        super().update(**kwargs)

    def player_known(self):
        return self.player is not None
