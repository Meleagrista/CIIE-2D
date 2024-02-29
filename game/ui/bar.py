import pygame

from game.entities.player import Player
from utils.constants import GREEN, RED


class Bar(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, player: Player):
        super().__init__()
        self._width = screen.get_width() * 0.25
        self._height = screen.get_height() * 0.02
        self._x = self._height
        self._y = self._height
        self._percentage = 0

        self._groups = []
        self._player = player

    def draw(self, surface):
        hp_value, hp_max = self._player.health()
        self._percentage = round(hp_value / hp_max, 2)
        pygame.draw.rect(surface, RED, (self._x, self._y, self._width, self._height))
        pygame.draw.rect(surface, GREEN, (self._x, self._y, self._width * self._percentage, self._height))

    def kill(self):
        for group in self._groups:
            group.remove(self)
        del self

    def add(self, *groups):
        for group in groups:
            group.add(self)
            if group not in self._groups:
                self._groups.append(group)

    def remove(self, *groups):
        for group in groups:
            group.remove(self)
            if group in self._groups:
                self._groups.remove(group)
