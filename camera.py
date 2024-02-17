import pygame


class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
        self.half_width = self.surface.get_width() // 2
        self.half_height = self.surface.get_height() // 2

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Sort ensures grid is drawn on background
        for sprite in sorted(self.sprites(), key=lambda sprite: 0 - sprite.rect.width):
            offset_position = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_position)
