import pygame
from utils.constants import *


class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.center = (self.surface.get_width() // 2, self.surface.get_height() // 2,)
        self.offset = pygame.math.Vector2(0, 0)

        # zoom
        self.internal_size = pygame.math.Vector2(self.surface.get_width(), self.surface.get_height())
        self.internal_surface = pygame.Surface(self.internal_size)
        self.internal_rectangle = self.internal_surface.get_rect(center = self.center)

        self.zoom = 1

        # offset from screen to camera border
        self.boundary_corners = {
            'left': 300,
            'right': 300,
            'top': 300,
            'bottom': 300
        }

        # camera boundaries
        left_corner = self.boundary_corners['left']
        top_corner = self.boundary_corners['top']
        boundary_width = self.internal_surface.get_width() - (self.boundary_corners['left'] + self.boundary_corners['right'])
        boundary_height = self.internal_surface.get_height() - (self.boundary_corners['top'] + self.boundary_corners['bottom'])
        self.boundary = pygame.Rect(left_corner, top_corner, boundary_width, boundary_height)

    def draw_bar(self, position, width, height, percentage):
        position = position - self.offset
        pygame.draw.rect(self.internal_surface, GREEN, (position.x, position.y, width, height))
        pygame.draw.rect(self.internal_surface, RED, (position.x, position.y, width * percentage, height))
        self.update_surface()

    def draw_vision(self, enemy, surface, vertices, mask):
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

    def draw_mask(self, result_surface):
        self.internal_surface.blit(result_surface, (0, 0))
        self.update_surface()

    def custom_draw(self, player, grid):

        self.surface.fill((255, 255, 255))

        # zoom controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            if not self.zoom == 1:
                self.zoom -= 0.1
        if keys[pygame.K_x]:
            if not self.zoom == 2:
                self.zoom += 0.1

        # update boundary if player is outside
        if player.rect.left < self.boundary.left:
            self.boundary.left = player.rect.left
        if player.rect.right > self.boundary.right:
            self.boundary.right = player.rect.right
        if player.rect.top < self.boundary.top:
            self.boundary.top = player.rect.top
        if player.rect.bottom > self.boundary.bottom:
            self.boundary.bottom = player.rect.bottom

        self.offset.x = self.boundary.left - self.boundary_corners['left']
        self.offset.y = self.boundary.top - self.boundary_corners['top']

        grid.draw(self.internal_surface, self.offset)

        # Sort ensures grid is drawn on background
        for sprite in sorted(self.sprites(), key=lambda sprite: 0 - sprite.rect.width):
            sprite.draw(self.internal_surface, self.offset)

        # draw camera (for testing)
        left_corner = self.boundary_corners['left']
        top_corner = self.boundary_corners['top']
        boundary_width = self.surface.get_width() - (self.boundary_corners['left'] + self.boundary_corners['right'])
        boundary_height = self.surface.get_height() - (self.boundary_corners['top'] + self.boundary_corners['bottom'])
        boundary = pygame.Rect(left_corner, top_corner, boundary_width, boundary_height)
        pygame.draw.rect(self.surface, 'yellow', boundary, 4)

        self.update_surface()

    def update_surface(self):
        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_size * self.zoom)
        scaled_rectangle = scaled_surface.get_rect(center = self.center)

        self.surface.blit(scaled_surface, scaled_rectangle)
