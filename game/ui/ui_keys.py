import pygame
from pygame import Surface

from game.entities.player import Player
from game.sprites.spritesheet import SpriteSheet
from utils.paths.assets_paths import UI_ICONS


class Keys(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._x = 0
        self._y = 0

        self.key_obtained = False

        self.tile_size = 60
        self.tile_id = 36

        # Preload sprite sheet
        self._sprite_sheet = SpriteSheet(UI_ICONS, 10, 9, self.tile_size)

        # Initialize tile during initialization
        self.tile = self._sprite_sheet.get_sprite_by_number(self.tile_id)
        self.rect = self.tile.get_rect()

        self.groups = []

    def set_position(self, rect):
        self._x = rect.right + self.tile_size / 8
        self._y = rect.centery - self.tile_size / 2

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface and isinstance(surface, Surface) and self.key_obtained:
            surface.blit(self.tile, (self._x, self._y))

    def update(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        if player and isinstance(player, Player):
            self.key_obtained = player.has_key()

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
