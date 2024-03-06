import pygame
from pygame import Surface

from game.entities.player import Player
from utils.constants import GREEN, RED, BLACK
from utils.assets_paths import HEALTH_BAR


class Bar(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._width = screen.get_width() * 0.25
        self._height = screen.get_height() * 0.02
        self._x = self._height
        self._y = self._height
        self._percentage = 0

        self.groups = []

    def update(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")

        hp_value, hp_max = player.health()
        self._percentage = round(hp_value / hp_max, 2)

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        health_bar_img = pygame.image.load(HEALTH_BAR)
        scaled_image = pygame.transform.scale(health_bar_img, (int(self._width) * 1.08, self._height * 1.95))
        surface.blit(scaled_image, (self._x * 0.5, self._y * 0.5))

        pygame.draw.rect(surface, RED, (self._x, self._y, self._width, self._height))
        pygame.draw.rect(surface, GREEN, (self._x, self._y, self._width * self._percentage, self._height))

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
