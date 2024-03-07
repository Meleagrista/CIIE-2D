import pygame

from utils.constants import SQUARE_SIZE


class SpriteSheet:
    def __init__(self, filename, total_columns, total_rows, tile_size=SQUARE_SIZE):
        self.filename = filename
        self.sprite_sheet = pygame.transform.scale(
            pygame.image.load(filename),
            (total_columns * tile_size, total_rows * tile_size))
        self.tile_size = tile_size
        self.total_columns = total_columns

    def get_sprite(self, x, y):
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        return sprite

    def get_sprite_by_number(self, number):
        if number < 0:
            return self.get_sprite(10, 7)
        x = number % self.total_columns
        y = number // self.total_columns
        return self.get_sprite(x, y)
