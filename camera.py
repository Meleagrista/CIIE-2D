import pygame
from constants import *

class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
        self.half_width = self.surface.get_width() // 2
        self.half_height = self.surface.get_height() // 2

    def draw_bar(self, position, width, height, percentage):
        position = position - self.offset
        pygame.draw.rect(self.surface, GREEN, (position.x, position.y, width, height))
        pygame.draw.rect(self.surface, RED, (position.x, position.y, width * percentage, height))

    def draw_mask(self, enemy, surface, vertices, mask):
        vertices = list(map(lambda point: point - self.offset, vertices))
        position_x = int(enemy.x) - self.offset[0]
        position_y = int(enemy.y) - self.offset[1]
        if len(vertices) > 2:
            pygame.draw.polygon(mask, (255, 255, 255), vertices)
        pygame.draw.circle(mask, (255, 255, 255, 255), (position_x, position_y), enemy.size * 2)
        vision = enemy.ray_reach * SQUARE_SIZE
        pygame.draw.circle(surface, (255, 255, 255, 255), (position_x, position_y), vision)

    def mask_overlap(self, mask, enemy_sight):
        return mask.overlap_area(enemy_sight, self.offset) > 0

    def custom_draw(self, player, grid):

        self.surface.fill((255, 255, 255))
        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_height

        grid.draw(self.offset)

        # Sort ensures grid is drawn on background
        for sprite in sorted(self.sprites(), key=lambda sprite: 0 - sprite.rect.width):
            # offset_position = sprite.rect.topleft - self.offset
            sprite.draw(self.surface, self.offset)
