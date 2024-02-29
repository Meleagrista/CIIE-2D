import pygame
from pygame import Surface


class Interface(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, *args, **kwargs):
        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pyagme.Surface class")

        for sprite in self.sprites():
            sprite.draw(surface)
