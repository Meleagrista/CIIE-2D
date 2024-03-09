import math
import pygame

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

    def update_path(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))

        if self.chasing:
            if self.chase_position.compare_node(current_node):
                if self.seen_positions:
                    previous_position = self.seen_positions.pop()
                    self.pathfinding(previous_position)
                else:
                    self._status = GREEN
                    self.chasing = False
                    self.chase_position = None
                    self.pathfinding(self.end_node)
                self.setting_path = True
                self.setting_rotation = True
                self._is_moving = False
            else:
                self.set_direct_path(self.chase_position)
        else:
            if self.next_point is None or self.end_node.compare_node(current_node):
                self.pathfinding()
                self.setting_path = True
                self.setting_rotation = True
                self._is_moving = False
            elif self.has_reached(self.next_point):
                self.set_next_point()

    def notified(self, player):
        if player.detected():

            super().notified(player)

            self.chasing = True
            if self.chase_position is not None:
                self.seen_positions.append(self.chase_position)
            self.chase_position = self.grid.get_node((player.x, player.y))
            self.update(self.update_path())
