import math
import pygame
import queue

from game.entities.enemy import Enemy
from game.map.grid import Grid
from utils.constants import ORANGE, GREEN, RED


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

        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ CHASING RELATED VARS  ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.chasing = False
        self.chase_position = None
        self.seen_positions = []

    def notified(self, player):
        distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                             (player.rect.centery - self.rect.centery) ** 2)

        if player.detected() and distance < self.ray_radius:

            player.exposer = self.__class__
            super().notified(player)

            self.chasing = True
            if self.chase_position is not None:
                self.seen_positions.append(self.chase_position)
            self.chase_position = self.grid.get_node((player.x, player.y))

            print(player.exposer)
            self.update()

    def update(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))

        if self.chasing and self.chase_position is not None:
            if self.chase_position.compare_node(current_node):
                if self.seen_positions:
                    # visit squares of previous player sights
                    previous_position = self.seen_positions.pop()
                    self.pathfinding(previous_position)
                    self.setting_path = True

                else:
                    # revert to normal status
                    self._status = GREEN
                    self.chasing = False
                    self.chase_position = None
                    self.pathfinding(self.end_node)
                    self.setting_path = True
                    self.setting_rotation = True
                    self._is_moving = False
            else:
                # direct sight to player is assumed here
                self.set_direct_path(self.chase_position)
        else:
            # normal behaviour
            if self.next_point is None or self.end_node.compare_node(current_node):
                self.pathfinding()
                self.setting_path = True
                self.setting_rotation = True
                self._is_moving = False
            elif self.has_reached(self.next_point):
                self.set_next_point()

        super().general_update(**kwargs)
