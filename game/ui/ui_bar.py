import pygame
from pygame import Surface

from game.entities.player import Player
from game.sprites.spritesheet import SpriteSheet
from utils.paths.assets_paths import UI_ASSETS


class Bar(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._x = screen.get_width() * 0.02
        self._y = 0

        self._percentage = 0

        self.tile_size = 150
        self.tile_id = 1

        self._sprite_sheet = SpriteSheet(UI_ASSETS, 20, 11, self.tile_size)

        self.tile = self._sprite_sheet.get_sprite_by_number(self.tile_id)
        self.rect = self.tile.get_rect()

        self.groups = []

    def update(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")

        hp_value, hp_max = player.health()

        self._percentage = round(float(hp_value) / float(hp_max), 2)
        self.tile_id = int(round(self._percentage * 10))

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        self.tile = self._sprite_sheet.get_sprite_by_number(self.tile_id)
        surface.blit(self.tile, (self._x, self._y))

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
