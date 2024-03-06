import pygame
from pygame import Surface

from game.entities.player import Player
from managers.resource_manager import ResourceManager
from utils.constants import PURPLE
from utils.assets_paths import KEYS_IMG, POPUP_IMAGE


class Keys(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self._width = screen.get_width() * 0.075
        self._height = screen.get_height() * 0.075
        self._x = self._height * 0.2
        self._y = self._height * 0.75
        self.key_obtained = False
        self.image = ResourceManager.load_image(KEYS_IMG, -1)
        self.image = pygame.transform.scale(self.image, (self._width * 0.9, self._width * 0.9))
        self.background = pygame.image.load(POPUP_IMAGE)

        self.groups = []

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        self.background = pygame.transform.scale(self.background, (self._width, self._height))

        # Dibuja la imagen en la superficie en la posición del rectángulo
        surface.blit(self.background, (self._x, self._y))

        if self.key_obtained:
            surface.blit(self.image, (self._x, self._y))

    def notified(self, **kwargs):
        player = kwargs.pop('player', None)

        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")
            
        if player.has_key():
            self.key_obtained = True

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
