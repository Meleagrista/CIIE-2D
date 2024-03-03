import pygame
from pygame import Surface

from game.entities.player import Player
from managers.resource_manager import ResourceManager
from utils.constants import PURPLE
from utils.filepaths import KEYS_IMG


class Keys(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._width = screen.get_width() * 0.05
        self._height = screen.get_height() * 0.05
        self._x = self._height
        self._y = self._height
        self.key_obtained = False
        self.image = ResourceManager.load_image(KEYS_IMG, -1)
        self.image = pygame.transform.scale(self.image, (self._width, self._width))
        self.rect = self.image.get_rect()

        self._groups = []

    def update(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")
        if player.has_key():
            self.key_obtained = True

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        pygame.draw.rect(surface, PURPLE, (self._x, self._y, self._width, self._height))
        if self.key_obtained:
            self.rect.topleft = (self._x, self._y)
            surface.blit(self.image, self.rect)

    def notified(self, **kwargs):
        pass

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
