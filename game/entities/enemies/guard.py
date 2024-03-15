import math
import pygame

from game.entities.enemy import Enemy
from game.map.grid import Grid
from game.sprites.spritesheet import SpriteSheet
from utils.constants import NPC_SIZE
from utils.paths.assets_paths import CHARACTER_ASSETS


class Guard(Enemy):
    def __init__(self,
                 position,
                 grid: Grid,
                 window: pygame.Surface,
                 areas
                 ):
        super().__init__(position, 1, 8, grid, window, areas)

        #    1. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ CHASING RELATED VARS  ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._sprite_sheet = SpriteSheet(CHARACTER_ASSETS, 10, 13, NPC_SIZE * 2.5)
        self._animation_frames = 4
        self._animation_start = 100
        self._idle_frames = 2
        self._idle_start = 80

        #    2. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ CHASING RELATED VARS  ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.vision_timer = 0
        self.vision_max = 100
        self.player = None
        self.chase_node = None
        self.previous_node = None

        #    3. ~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~       VISION        ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.ray_cone = 60
        self.ray_reach = 6
        self.ray_radius = self.ray_reach * self.grid.gap

    def notified(self, player):

        if player.detected():

            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)

            if distance < self.ray_radius:
                super().notified(player)

            if "civilian" in player.exposer or distance < self.ray_radius * 1.5:

                if self.previous_node is None:
                    self.previous_node = self.grid.get_node((self.x, self.y))
                self.vision_timer = self.vision_max
                self.player = player

            # self.update()

    def update(self, **kwargs):
        current_node = self.grid.get_node((self.x, self.y))

        if self.has_vision():
            self._is_moving = True
            self.speed = 2
            self.ray_cone = 30
            self.ray_reach = 8
            self.ray_radius = self.ray_reach * self.grid.gap

            self.vision_timer = max(0, self.vision_timer - 1)
            self.chase_node = self.grid.get_node((self.player.x, self.player.y))

            if self.next_point is None or self.chase_node.compare_node(current_node):
                self.set_path(self.previous_node)
                self.previous_node = None
            elif self.has_reached(self.next_point):
                self.set_next_point()
                # Simplified version to avoid slow turnings
                self.set_simplified_path(self.chase_node)

        else:
            self.speed = 1
            self.ray_cone = 60
            self.ray_reach = 6
            self.ray_radius = self.ray_reach * self.grid.gap

            if self.next_point is None or self.end_node.compare_node(current_node):
                self.set_path()
            elif self.has_reached(self.next_point):
                self.set_next_point()

        super().update(**kwargs)

    def has_vision(self):
        return self.vision_timer > 0 and self.player is not None
