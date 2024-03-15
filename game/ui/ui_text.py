import pygame
from pygame import Surface

from menu.prototypes.gui_prototypes import Text
from utils.paths.assets_paths import FONT


class Message(pygame.sprite.Sprite, Text):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        fuente = pygame.font.Font(FONT, 25)
        self._x = screen.get_width() * 0.5
        self._y = screen.get_height() * 0.66

        self.font = fuente
        self.image = fuente.render('', True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(self._x, self._y))

        self.active = True

        self.groups = []

    def draw(self, **kwargs):
        if self.active:
            surface = kwargs.pop('surface', None)
            if surface and isinstance(surface, Surface):
                surface.blit(self.image, self.rect)
            else:
                raise TypeError("surface must be an instance of pygame.Surface class")

    def notified(self, **kwargs):
        message = kwargs.pop('text', None)
        if message is not None:
            if not isinstance(message, str):
                raise TypeError("message must be an instance of a string")

        if self.active:
            state = kwargs.pop('key_gone', False)
            self.active = not state

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
