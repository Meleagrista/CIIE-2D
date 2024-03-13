import math
import pygame

from game.entities.enemies.enemy import Enemy
from game.map.grid import Grid


class Civilian(Enemy):
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
        #    ~~        VISUALS        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._animation_start = 110
        self._idle_start = 120

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       ESCAPING        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.escape_node = None
        self.previous_node = None

    def notified(self, player):

        current_room = self.grid.get_node((self.x, self.y)).get_id()
        player_room = self.grid.get_node((player.x, player.y)).get_id()

        if not self.is_escaping() and player.detected() and current_room == player_room:

            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)

            if distance < 100:
                player.exposer = "civilian"
            super().notified(player)

            self.speed = self.speed * 3
            self.escape_node = self.grid.get_random_node()
            while self.escape_node.get_id() == player_room:
                self.escape_node = self.grid.get_random_node()

            self.previous_node = self.grid.get_node((self.x, self.y))
            # less segments to counter greater speed
            self.set_path(self.escape_node, 4)
            self.update()

    def update(self, **kwargs):

        current_node = self.grid.get_node((self.x, self.y))

        if self.is_escaping():
            if self.escape_node.compare_node(current_node):
                self.speed = self.speed // 3
                self.escape_node = None
                self.set_path(self.previous_node)

            elif self.has_reached(self.next_point):
                self.set_next_point()
        else:
            # normal behaviour
            if self.next_point is None or self.end_node.compare_node(current_node):
                next_node = self.grid.get_random_node_from_zone(current_node.get_id())
                self.set_path(next_node)
            elif self.has_reached(self.next_point):
                self.set_next_point()
        super().general_update(**kwargs)

    def is_escaping(self):
        return self.escape_node is not None
