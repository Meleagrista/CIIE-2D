import pygame

from game.entities.player import Player
from game.map.grid import Grid
from utils.constants import *


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.center = (self.surface.get_width() // 2, self.surface.get_height() // 2,)
        self.offset = pygame.math.Vector2(0, 0)

        self.surface_mask = None

        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ ZOOM RELATED VARIABLE ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._internal_size = pygame.math.Vector2(self.surface.get_width(), self.surface.get_height())
        self._internal_surface = pygame.Surface(self._internal_size)
        self._internal_rectangle = self._internal_surface.get_rect(center=self.center)

        self._zoom_level = 1

        # 2. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ OFFSET AND BOUNDARIES ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._boundary_corners = {'left': 300, 'right': 300, 'top': 300, 'bottom': 300}

        self._boundary = pygame.Rect(
            self._boundary_corners['left'],
            self._boundary_corners['top'],
            self._internal_surface.get_width() - (self._boundary_corners['left'] + self._boundary_corners['right']),
            self._internal_surface.get_height() - (self._boundary_corners['top'] + self._boundary_corners['bottom'])
        )

    def enemy_mask(self, enemy, surface, vertices, mask):
        vertices = list(map(lambda point: point - self.offset, vertices))
        position_x = int(enemy.x) - self.offset[0]
        position_y = int(enemy.y) - self.offset[1]
        if len(vertices) > 2:
            pygame.draw.polygon(mask, (255, 255, 255), vertices)
        pygame.draw.circle(mask, (255, 255, 255, 255), (position_x, position_y), enemy.size * 2)
        pygame.draw.circle(surface, (255, 255, 255, 255), (position_x, position_y), enemy.ray_radius)

    def player_mask(self, player):
        mask_surface = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        player_rect = (
            player.rect.x - self.offset[0],
            player.rect.y - self.offset[1],
            player.rect.width,
            player.rect.height
        )
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), player_rect)
        return pygame.mask.from_surface(mask_surface)

    def draw(self, *args, **kwargs):
        player = kwargs.pop('player', None)
        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")

        grid = kwargs.pop('grid', None)
        if grid is not None:
            if not isinstance(grid, Grid):
                raise TypeError("grid must be an instance of Grid class")

        self.surface.fill((255, 255, 255))

        # self._zoom()
        self._boundaries(player)

        self.offset.x = self._boundary.left - self._boundary_corners['left']
        self.offset.y = self._boundary.top - self._boundary_corners['top']

        kwargs['internal_surface'] = self._internal_surface
        kwargs['offset'] = self.offset

        grid.draw(*args, **kwargs)

        for sprite in sorted(self.sprites(), key=lambda custom_sprite: 0 - custom_sprite.rect.width):
           sprite.draw(*args, **kwargs)

        self._update()

    def _zoom(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            if not self._zoom_level == 1:
                self._zoom_level -= 0.1
        elif keys[pygame.K_x]:
            if not self._zoom_level == 2:
                self._zoom_level += 0.1

    def _boundaries(self, player):
        if player.rect.left < self._boundary.left:
            self._boundary.left = player.rect.left
        elif player.rect.right > self._boundary.right:
            self._boundary.right = player.rect.right
        if player.rect.top < self._boundary.top:
            self._boundary.top = player.rect.top
        elif player.rect.bottom > self._boundary.bottom:
            self._boundary.bottom = player.rect.bottom

    def _update(self):
        if self.surface_mask is not None:
            self._internal_surface.blit(self.surface_mask.to_surface(setcolor=None, unsetcolor=(0, 0, 0, 100)), (0, 0))
        scaled_surface = pygame.transform.scale(self._internal_surface, self._internal_size * self._zoom_level)
        scaled_rectangle = scaled_surface.get_rect(center=self.center)
        self.surface.blit(scaled_surface, scaled_rectangle)
