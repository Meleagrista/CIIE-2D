import pygame
from pygame import Surface

from menu.prototypes.gui_prototypes import Text
from utils.filepaths import FONT


class Message(pygame.sprite.Sprite, Text):
    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        fuente = pygame.font.Font(FONT, 20)
        self._x = screen.get_width() * 0.5
        self._y = screen.get_height() * 0.66

        text_surface = fuente.render('', True, (255, 255, 255))
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
        message = kwargs.pop('text', None)
        if message is not None:
            if not isinstance(message, str):
                raise TypeError("message must be an instance of a String")

        self.set_text(message)

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
