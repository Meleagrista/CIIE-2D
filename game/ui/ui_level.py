import pygame
from pygame import Surface

from menu.prototypes.gui_prototypes import Text
from utils.paths.assets_paths import FONT


class Indicator(pygame.sprite.Sprite, Text):
    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        fuente = pygame.font.Font(FONT, 50)
        self._x = screen.get_width() * 0.5
        self._y = 70

        text_surface = fuente.render('LEVEL 1', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self._x, self._y))

        Text.__init__(self, screen, fuente, (255, 255, 255), '', text_rect.topleft)

        self.groups = []

    def draw(self, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pyagme.Surface class")

        surface.blit(self.image, self.rect)

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

    def set_text(self, new_text):
        text_surface = self.font.render(new_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self._x, self._y))
        self.image = text_surface
        self.set_rect(text_rect)
