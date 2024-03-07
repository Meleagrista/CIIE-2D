import pygame

from utils.constants import SQUARE_SIZE


class SpriteSheet:
    def __init__(self, filename, total_columns, total_rows, tile_width=SQUARE_SIZE, tile_height=SQUARE_SIZE):
        self.filename = filename
        self.sprite_sheet = pygame.transform.scale(
            pygame.image.load(filename),
            (total_columns*tile_height, total_rows*tile_width))
        self.tile_height = tile_height
        self.tile_width = tile_width
        self.total_columns = total_columns

    def get_sprite(self, x, y):
        sprite = pygame.Surface((self.tile_width, self.tile_height))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x*self.tile_width, y*self.tile_height, self.tile_width, self.tile_height))
        return sprite

    def get_sprite_by_number(self, number):
        if number < 0:
            return self.get_sprite(10, 7)
        x = number % self.total_columns
        y = number // self.total_columns
        return self.get_sprite(x, y)
