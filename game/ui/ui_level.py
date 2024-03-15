import pygame
from pygame import Surface

from menu.prototypes.gui_prototypes import Text
from utils.paths.assets_paths import FONT


class Indicator(pygame.sprite.Sprite, Text):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        fuente = pygame.font.Font(FONT, 50)
        self._x = screen.get_width() * 0.5
        self._y = 70

        self.font = fuente
        self.image = fuente.render('', True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(self._x, self._y))

        self.groups = []

    def set_text(self, new_text):
        self.image = self.font.render(new_text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(self._x, self._y))

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface and isinstance(surface, Surface):
            surface.blit(self.image, self.rect)
        else:
            raise TypeError("surface must be an instance of pygame.Surface class")

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
