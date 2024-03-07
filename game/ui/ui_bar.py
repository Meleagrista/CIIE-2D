import pygame
from pygame import Surface

from game.entities.player import Player
from game.sprites.spritesheet import SpriteSheet
from utils.paths.assets_paths import UI_ASSETS


class Bar(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        # self._width = screen.get_width() * 0.25
        # self._height = screen.get_height() * 0.02
        self._x = screen.get_width() * 0.02
        self._y = 0
        self._percentage = 0

        self._sprite_sheet = SpriteSheet(UI_ASSETS, 20, 11, 150)

        image = self._sprite_sheet.get_sprite_by_number(1)
        self.rect = image.get_rect()

        self.groups = []

    def update(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")

        hp_value, hp_max = player.health()

        # self._percentage = round(hp_value / hp_max, 2)

        self._percentage = round(float(hp_value) / float(hp_max), 2)

        # self._x, self._y = player.rect.center
        # self._x = self._x - self.rect.width/2
        # self._y = self._y - self.rect.height * 1.2

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        # offset = kwargs.pop('offset', None)
        # if offset is not None:
        #     if not isinstance(offset, pygame.math.Vector2):
        #         raise TypeError("offset must be an instance of Vector2 class")

        # pygame.draw.rect(surface, RED, (self._x, self._y, self._width, self._height))
        # pygame.draw.rect(surface, GREEN, (self._x, self._y, self._width * self._percentage, self._height))

        tile_id = int(round(self._percentage * 10))
        tile = self._sprite_sheet.get_sprite_by_number(tile_id)

        surface.blit(tile, (self._x, self._y))

    def notified(self, **kwargs):
        pass

    def add(self, *groups):
        for group in groups:
            group.add(self)
            if group not in self.groups:
                self.groups.append(group)

    def remove(self, *groups):
        for group in groups:
            if self in group:
                group.remove(self)
            if group in self.groups:
                self.groups.remove(group)
