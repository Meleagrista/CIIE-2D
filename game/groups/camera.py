from utils.constants import *
from game.entities.player import Player
from game.map.grid import Grid

import pygame


class Camera(pygame.sprite.Group):
    """
    Class representing a camera view in a Pygame environment.

    Attributes:
        surface (pygame.Surface): The surface of the Pygame display.
        center (tuple): The center coordinates of the camera view.
        offset (pygame.math.Vector2): The offset of the camera view.
        internal_size (pygame.math.Vector2): The size of the internal surface of the camera.
        internal_surface (pygame.Surface): The internal surface of the camera.
        internal_rectangle (pygame.Rect): The rectangle representing the internal surface.
        zoom (float): The zoom factor of the camera.
        boundary_corners (dict): Dictionary containing the boundary offsets from the screen to the camera border.
        boundary (pygame.Rect): The boundary rectangle of the camera view.
    """

    def __init__(self):
        """
        Initializes the Camera object.
        """
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.center = (self.surface.get_width() // 2, self.surface.get_height() // 2,)
        self.offset = pygame.math.Vector2(0, 0)

        self.mask_surface = None

        # Zoom
        self.internal_size = pygame.math.Vector2(self.surface.get_width(), self.surface.get_height())
        self.internal_surface = pygame.Surface(self.internal_size)
        self.internal_rectangle = self.internal_surface.get_rect(center=self.center)

        self.zoom = 1

        # Offset from screen to camera border
        self.boundary_corners = {
            'left': 300,
            'right': 300,
            'top': 300,
            'bottom': 300
        }

        # Camera boundaries
        left_corner = self.boundary_corners['left']
        top_corner = self.boundary_corners['top']
        boundary_width = self.internal_surface.get_width() - (self.boundary_corners['left'] + self.boundary_corners['right'])
        boundary_height = self.internal_surface.get_height() - (self.boundary_corners['top'] + self.boundary_corners['bottom'])
        self.boundary = pygame.Rect(left_corner, top_corner, boundary_width, boundary_height)

    def draw_bar(self, position, width, height, percentage):
        """
        Draw a bar on the camera's internal surface.

        Args:
            position (pygame.math.Vector2): The position of the bar.
            width (int): The width of the bar.
            height (int): The height of the bar.
            percentage (float): The percentage filled of the bar.
        """
        position = position - self.offset
        pygame.draw.rect(self.internal_surface, GREEN, (position.x, position.y, width, height))
        pygame.draw.rect(self.internal_surface, RED, (position.x, position.y, width * percentage, height))
        self._update()

    def mask_update(self, enemy, surface, vertices, mask):
        """
        Draw vision for an enemy on the camera's internal surface.

        Args:
            enemy (Enemy): The enemy object.
            surface (pygame.Surface): The surface to draw on.
            vertices (list): List of vertices representing the vision area.
            mask (pygame.Surface): The mask surface.
        """
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

    def mask_draw(self, result_surface):
        self.mask_surface = result_surface

    def draw(self, surface, *args, **kwargs):
        """
        Draw objects on the camera's surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        player = kwargs.pop('player', None)
        if player is not None:
            if not isinstance(player, Player):
                raise TypeError("player must be an instance of Player class")
        grid = kwargs.pop('grid', None)
        if grid is not None:
            if not isinstance(grid, Grid):
                raise TypeError("grid must be an instance of Grid class")

        self.surface.fill((255, 255, 255))

        # zoom controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            if not self.zoom == 1:
                self.zoom -= 0.1
        elif keys[pygame.K_x]:
            if not self.zoom == 2:
                self.zoom += 0.1

        if player.rect.left < self.boundary.left:
            self.boundary.left = player.rect.left
        elif player.rect.right > self.boundary.right:
            self.boundary.right = player.rect.right
        if player.rect.top < self.boundary.top:
            self.boundary.top = player.rect.top
        elif player.rect.bottom > self.boundary.bottom:
            self.boundary.bottom = player.rect.bottom

        self.offset.x = self.boundary.left - self.boundary_corners['left']
        self.offset.y = self.boundary.top - self.boundary_corners['top']

        grid.draw(self.internal_surface, self.offset)

        # Sort ensures grid is drawn on background
        for sprite in sorted(self.sprites(), key=lambda custom_sprite: 0 - custom_sprite.rect.width):
            sprite.draw(self.internal_surface, self.offset)

        # Draw camera for debugging purposes
        """left_corner = self.boundary_corners['left']
        top_corner = self.boundary_corners['top']
        boundary_width = self.surface.get_width() - (self.boundary_corners['left'] + self.boundary_corners['right'])
        boundary_height = self.surface.get_height() - (self.boundary_corners['top'] + self.boundary_corners['bottom'])
        boundary = pygame.Rect(left_corner, top_corner, boundary_width, boundary_height)
        pygame.draw.rect(self.surface, 'yellow', boundary, 4)"""

        # TODO: This is where the vision is drawm.
        self.internal_surface.blit(self.mask_surface, (0, 0))

        self._update()

        # Call the base class draw method
        # super().draw(surface, *args, **kwargs)

    def _update(self):
        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_size * self.zoom)
        scaled_rectangle = scaled_surface.get_rect(center=self.center)
        self.surface.blit(scaled_surface, scaled_rectangle)
