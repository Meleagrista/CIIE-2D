from typing import List, Tuple

import pygame
from pygame import Surface
from typing_extensions import deprecated

from game.entities.enemy import Enemy
from game.entities.player import Player
from game.map.grid import Grid


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # Surface-related attributes
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.surface = pygame.display.get_surface()
        self.center = (self.surface.get_width() // 2, self.surface.get_height() // 2,)
        self.offset = pygame.math.Vector2(0, 0)
        self.surface_mask = None
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Zoom-related attributes
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._internal_size = pygame.math.Vector2(self.surface.get_width(), self.surface.get_height())
        self._internal_surface = pygame.Surface(self._internal_size)
        self._internal_rectangle = self._internal_surface.get_rect(center=self.center)
        self._zoom_level = 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Boundary-related attributes
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._boundary_corners = {'left': 300, 'right': 300, 'top': 300, 'bottom': 300}
        self._boundary = pygame.Rect(
            self._boundary_corners['left'],
            self._boundary_corners['top'],
            self._internal_surface.get_width() - (self._boundary_corners['left'] + self._boundary_corners['right']),
            self._internal_surface.get_height() - (self._boundary_corners['top'] + self._boundary_corners['bottom'])
        )
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Enemy-related attributes
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        win = pygame.display.get_surface()
        self._enemy_surface = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
        self._enemy_untreated_vertices = []
        self._enemy_untreated_positions = []
        self._enemy_mask = pygame.mask.from_surface(self._enemy_surface)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _calculate_enemy_mask(self, enemy: Enemy, vertices: List[int]) -> None:
        if not self._in_range(enemy.rect.center, enemy.ray_radius):
            return

        vertices = list(map(lambda point: point - self.offset, vertices))

        position_x = int(enemy.x) - self.offset[0]
        position_y = int(enemy.y) - self.offset[1]

        pygame.draw.rect(
            self._enemy_surface,
            (255, 255, 255, 255),
            pygame.Rect(position_x - enemy.size / 2, position_y - enemy.size / 2, enemy.size, enemy.size)
        )

        if len(vertices) > 2:
            pygame.draw.polygon(self._enemy_surface, (255, 255, 255), vertices)

    def save_enemy_mask(self, enemy: Enemy, vertices: List[int]) -> None:
        if enemy.in_range(self._internal_surface, self._boundary.center, enemy.ray_radius):
            self._enemy_untreated_vertices.append(vertices)
            self._enemy_untreated_positions.append(enemy)

    def return_enemy_mask(self) -> Surface:
        return self._enemy_mask

    def _calculate_player_mask(self, player: Player) -> pygame.mask.Mask:
        mask_surface = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        player_rect = (
            player.rect.x - self.offset[0],
            player.rect.y - self.offset[1],
            player.rect.width,
            player.rect.height
        )
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), player_rect)
        return pygame.mask.from_surface(mask_surface)

    def return_player_mask(self, player: Player) -> pygame.mask.Mask:
        return self._calculate_player_mask(player)

    def draw(self, *args, **kwargs):
        player = kwargs.get('player')
        if player is not None and not isinstance(player, Player):
            raise TypeError("player must be an instance of Player class")

        grid = kwargs.get('grid')
        if grid is not None and not isinstance(grid, Grid):
            raise TypeError("grid must be an instance of Grid class")

        # Fill the surface with white color
        self.surface.fill((255, 255, 255))

        # Adjust the boundaries
        self._boundaries(player)

        # Set the offset
        self.offset.x = self._boundary.left - self._boundary_corners['left']
        self.offset.y = self._boundary.top - self._boundary_corners['top']

        # Prepare kwargs for grid drawing
        kwargs['internal_surface'] = self._internal_surface
        kwargs['offset'] = self.offset
        kwargs['center'] = self._boundary.center
        kwargs['float'] = False
        kwargs['floor'] = True

        # Draw the grid
        if grid:
            grid.draw(**kwargs)
        else:
            print('No Grid has reached the camera.')

        # Prepare enemy surface
        win = pygame.display.get_surface()
        self._enemy_surface = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)

        # Calculate enemy masks
        for vertices, enemy in zip(self._enemy_untreated_vertices, self._enemy_untreated_positions):
            self._calculate_enemy_mask(enemy, vertices)

        # Clear untreated enemies
        self._enemy_untreated_vertices = []
        self._enemy_untreated_positions = []

        # Create enemy mask
        self._enemy_mask = pygame.mask.from_surface(self._enemy_surface)

        # Draw player rectangle
        if player:
            position_x = int(player.x) - self.offset[0]
            position_y = int(player.y) - self.offset[1]
            pygame.draw.rect(
                self._enemy_surface,
                (255, 255, 255, 255),
                pygame.Rect(position_x, position_y, player.size * 2, player.size * 2)
            )

        # Blend enemy mask with internal surface
        if self._enemy_mask is not None:
            self._internal_surface.blit(
                pygame.mask.from_surface(
                    self._enemy_surface).to_surface(setcolor=None, unsetcolor=(0, 0, 0, 100)), (0, 0))

        # Draw the grid again (if needed)
        kwargs['float'] = False
        kwargs['floor'] = False
        if grid:
            grid.draw(**kwargs)

        # Draw sprites
        for sprite in sorted(self.sprites(), key=lambda custom_sprite: 0 - custom_sprite.rect.width):
            sprite.draw(*args, **kwargs)

        # Draw floating grid elements
        kwargs['float'] = True
        kwargs['floor'] = False
        if grid:
            grid.draw(**kwargs)

        # Scale and blit the internal surface to the main surface
        scaled_surface = pygame.transform.scale(self._internal_surface, self._internal_size * self._zoom_level)
        scaled_rectangle = scaled_surface.get_rect(center=self.center)
        self.surface.blit(scaled_surface, scaled_rectangle)

    def _zoom(self) -> None:
        """
        Adjusts the zoom level of the camera based on user input.

        This method checks for user input to adjust the zoom level of the camera. If the 'z' key is pressed, the zoom level
        decreases, and if the 'x' key is pressed, the zoom level increases.

        Returns:
            None
        """
        keys_to_zoom_levels = {pygame.K_z: 0.9, pygame.K_x: 1.1}  # Mapping of keys to zoom levels
        for key, zoom_level in keys_to_zoom_levels.items():
            if pygame.key.get_pressed()[key]:  # Check if the key is pressed
                # Ensure the zoom level stays within the range [0.1, 2.0]
                self._zoom_level = max(0.1, min(2.0, self._zoom_level + zoom_level))

    def _boundaries(self, player) -> None:
        """
        Adjusts the camera boundaries based on the player's position.

        This method updates the camera boundaries to include the player's position, ensuring that the player remains
        within the visible area.

        Args:
            player: The Player object whose position is used to update the camera boundaries.

        Returns:
            None
        """
        # Update the camera boundaries to include the player's rectangle
        # self._boundary = self._boundary.union(player.rect)
        self._boundary.left = min(player.rect.left, self._boundary.left)
        self._boundary.right = max(player.rect.right, self._boundary.right)
        self._boundary.top = min(player.rect.top, self._boundary.top)
        self._boundary.bottom = max(player.rect.bottom, self._boundary.bottom)

    def _in_range(self, position: Tuple[int, int], padding: int) -> bool:
        """
        Checks if a given position is within the visible area of the camera.

        This method determines whether a specified position is within the visible area of the camera, considering a
        specified padding around the edges.

        Args:
            position: The position to be checked.
            padding: The padding applied around the edges of the visible area.

        Returns:
            bool: True if the position is within the visible area, False otherwise.
        """
        # Calculate the horizontal and vertical distances from the position to the center of the camera boundary
        horizontal_distance = abs(position[0] - self._boundary.centerx)
        vertical_distance = abs(position[1] - self._boundary.centery)

        # Check if the position is within the visible area based on horizontal and vertical distances and padding
        return horizontal_distance < (self._internal_surface.get_width() // 2 + padding) and \
            vertical_distance < (self._internal_surface.get_height() // 2 + padding)

    @deprecated('This method has been replaced')
    def _update(self):
        """if self.surface_mask is not None:
            self._internal_surface.blit(self.surface_mask.to_surface(setcolor=None, unsetcolor=(0, 0, 0, 100)), (0, 0))
        scaled_surface = pygame.transform.scale(self._internal_surface, self._internal_size * self._zoom_level)
        scaled_rectangle = scaled_surface.get_rect(center=self.center)
        self.surface.blit(scaled_surface, scaled_rectangle)"""
        raise NotImplemented
