import pygame

from utils.constants import SQUARE_SIZE


class SpriteSheet:
    def __init__(self, filename: str, total_columns: int, total_rows: int, tile_size: int = SQUARE_SIZE):
        """
        Initialize a SpriteSheet object.

        Args:
            filename (str): The filename of the sprite sheet image.
            total_columns (int): The total number of columns in the sprite sheet.
            total_rows (int): The total number of rows in the sprite sheet.
            tile_size (int): The size of each tile in pixels. Defaults to SQUARE_SIZE.

        Returns:
            None
        """
        self.filename = filename
        self.sprite_sheet = pygame.transform.scale(
            pygame.image.load(filename),
            (total_columns * tile_size, total_rows * tile_size))
        self.tile_size = tile_size
        self.total_columns = total_columns

    def get_sprite(self, x: int, y: int) -> pygame.Surface:
        """
        Retrieve a sprite from the sprite sheet at the specified position.

        Args:
            x (int): The column index of the sprite.
            y (int): The row index of the sprite.

        Returns:
            pygame.Surface: The sprite image.
        """
        sprite = pygame.Surface((self.tile_size, self.tile_size))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
        return sprite

    def get_sprite_by_number(self, number: int) -> pygame.Surface:
        """
        Retrieve a sprite from the sprite sheet based on its sequential number.

        Args:
            number (int): The sequential number of the sprite.

        Returns:
            pygame.Surface: The sprite image.
        """
        if number < 0:
            return self.get_sprite(10, 7)
        x = number % self.total_columns
        y = number // self.total_columns
        return self.get_sprite(x, y)
