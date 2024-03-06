import math

import pygame
from pygame import Mask, Surface
from typing_extensions import deprecated

from game.map.grid import Grid
from managers.resource_manager import ResourceManager
from utils.auxiliar import get_direction, increase, decrease, has_changed
from utils.constants import *
from utils.enums import *
from utils.assets_paths import SHEET_CHARACTER, COORDINATES_CHARACTER


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PLAYER CLASS                                           #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, movement_speed: float, grid: Grid):
        """
        Initialize an Enemy object.

        Args:
            x (int): X coordinate of the player.
            y (int): Y coordinate of the player.
            movement_speed (float): Speed of movement.
            grid (Grid): Grid for pathfinding.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.groups = []
        self.size = NPC_SIZE

        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ VISUAL REPRESENTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.sheet = ResourceManager.load_image(SHEET_CHARACTER, -1)
        self.sheet = self.sheet.convert_alpha()
        self.offset = VIEW_OFFSET * (NPC_SIZE / 20)
        self.image = pygame.Surface((NPC_SIZE, NPC_SIZE))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.current_sprite = 0

        # 2. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ MOVEMENT AND ROTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.grid = grid
        self.angle = NPC_ANGLE
        self.speed = movement_speed
        self.last_direction = Direction.NORTH
        self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
        self.delta_y = math.sin(math.radians(self.angle)) * self.offset

        # 3. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ OBSERVER PATTERN LIST ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._observers = []
        self._max_health = LIFE * FPS
        self._health = self._max_health
        self._max_cooldown = FPS
        self._cooldown = self._max_cooldown
        self._recovering = False
        self._is_alive = True
        self._is_exposed = False
        self._is_moving = False

        self._in_exit = False
        self._in_key = False
        self._has_key = False

        self._interacted_with_key = False
        # self._toggle_key_controls = False
        # self._picked_up_key = False

    def draw(self, **kwargs):
        surface = kwargs.pop('internal_surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pyagme.Surface class")

        offset = kwargs.pop('offset', None)
        if offset is not None:
            if not isinstance(offset, pygame.math.Vector2):
                raise TypeError("offset must be an instance of Vector2 class")

        angle_to_horizontal = math.atan2(self.delta_y, self.delta_x)

        # Draw the player
        stopped_coordinates = ResourceManager.load_coordinates(self.current_sprite, COORDINATES_CHARACTER)
        my_sprite = self.sheet.subsurface(stopped_coordinates)

        # Calculate angle in degrees
        angle_in_degrees = -(math.degrees(angle_to_horizontal) - 90) % 360

        # Scale sprite to fit the size of the rectangle
        scaled_sprite = pygame.transform.scale(my_sprite, (self.size, self.size))

        # Rotate scaled sprite
        rotated_sprite = pygame.transform.rotate(scaled_sprite, angle_in_degrees)

        # Adjust position of rotated sprite
        rotated_sprite_rect = rotated_sprite.get_rect(center=scaled_sprite.get_rect().center)

        # pygame.draw.rect(surface, BLUE, (self.rect.x - offset.x, self.rect.y - offset.y, self.size, self.size))

        # Draw rotated sprite
        surface.blit(
            source=rotated_sprite,
            dest=(self.rect.x - offset.x + rotated_sprite_rect.x, self.rect.y - offset.y + rotated_sprite_rect.y)
        )

    def update(self, **kwargs):
        movement_option = kwargs.pop('movement_option', None)
        if movement_option is not None:
            if not isinstance(movement_option, Controls):
                raise TypeError("movement_option must be an instance of Controls enum,")

        player_mask = kwargs.pop('player_mask', None)
        if player_mask is not None:
            if not isinstance(player_mask, Mask):
                raise TypeError("player_mask must be an instance of Mask type,")

        enemy_mask = kwargs.pop('enemy_mask', None)
        if enemy_mask is not None:
            if not isinstance(enemy_mask, Mask):
                raise TypeError("enemy_mask must be an instance of Mask type,")

        ##############################
        # ENEMY DETECTION
        ##############################
        if self.is_detected(player_mask=player_mask, enemy_mask=enemy_mask):
            self._health = decrease(self._health)
            self._recovering = False
            self._cooldown = 0
            if self._health <= 0:
                self._is_alive = False
            if not self._is_exposed or not self._is_alive:
                self._is_exposed = True
                self.notify_observers()
        elif self._is_alive:
            self._is_exposed = False
            self._cooldown = increase(self._cooldown, self._max_cooldown)
            if self._cooldown >= self._max_cooldown and self._health < self._max_health and not self._recovering:
                self._recovering = True
                self.notify_observers()
            elif self._recovering:
                self._recovering = False
                self.notify_observers()

            if self._recovering:
                self._health = increase(self._health, self._max_health)

            if self._is_exposed:
                self._is_exposed = False
                self.notify_observers()

        ##############################
        # MOVEMENT AND DIRECTION
        ##############################

        direction, direction_x, direction_y = get_direction(movement_option)

        if direction == Direction.STOPPED:
            self.angle = self.last_direction.angle()
        else:
            self.angle = direction.angle()
            self.last_direction = direction
        self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
        self.delta_y = math.sin(math.radians(self.angle)) * self.offset

        # Normalize the direction vector for diagonal movement
        if direction_x != 0 and direction_y != 0:
            direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            direction_x /= direction_length
            direction_y /= direction_length

        # Calculate the new position the player wants to move to with adjusted speed
        new_x = self.x + direction_x * self.speed
        new_y = self.y + direction_y * self.speed

        # Update player's position
        self.rect = pygame.Rect(new_x, new_y, NPC_SIZE, NPC_SIZE)

        ##############################
        # COLLISION DETECTION
        ##############################

        collisions = self.grid.has_collision(self.rect)

        while len(collisions) != 0:
            set_collisions = collisions
            for collision in set_collisions:
                if collision.rect.left < self.rect.right or collision.rect.right > self.rect.left:
                    new_x = self.x
                    new_y = self.y + direction.delta_y * (self.speed * FRICTION)
                    self.rect = pygame.Rect(new_x, new_y, NPC_SIZE, NPC_SIZE)
                    collisions = self.grid.has_collision(self.rect)
                    if len(collisions) == 0:
                        break
                if collision.rect.top < self.rect.bottom or collision.rect.bottom > self.rect.top:
                    new_y = self.y
                    new_x = self.x + direction.delta_x * (self.speed * FRICTION)
                    self.rect = pygame.Rect(new_x, new_y, NPC_SIZE, NPC_SIZE)
                    collisions = self.grid.has_collision(self.rect)
                    if len(collisions) == 0:
                        break
            if len(set_collisions) == len(collisions):
                new_y = self.y
                new_x = self.x
                self.rect = pygame.Rect(new_x, new_y, NPC_SIZE, NPC_SIZE)
                collisions = self.grid.has_collision(self.rect)

        ##############################
        # KEY COLLECTION
        ##############################

        if has_changed(self.grid.is_key_square(new_x, new_y), self._in_key):
            self._in_key = self.grid.is_key_square(new_x, new_y)
            self.notify_observers()

        if self._in_key:
            self._interact()

        if has_changed(self.grid.is_exit_square(new_x, new_y), self._in_exit):
            self._in_exit = self.grid.is_exit_square(new_x, new_y)
            self.notify_observers()

        self._in_key = self.grid.is_key_square(new_x, new_y)
        self._in_exit = self.grid.is_exit_square(new_x, new_y)

        if self.x == new_x and self.y == new_y and self._is_moving:
            self._is_moving = False
            self.notify_observers()
        elif (self.x != new_x or self.y != new_y) and not self._is_moving:
            self._is_moving = True
            self.notify_observers()

        # Update player's position
        self.x = new_x
        self.y = new_y

        # Update sprite
        self.rect.topleft = (self.x, self.y)

        ##############################
        # ANIMATION
        ##############################

        if self._is_moving:
            self.current_sprite = (self.current_sprite + 1) % TOTAL_MOVEMENT_SPRITES
            self.image = ResourceManager.load_coordinates(self.current_sprite, COORDINATES_CHARACTER)
        elif self._is_moving and self.current_sprite != TOTAL_MOVEMENT_SPRITES:
            self.current_sprite = (self.current_sprite + 1)
            self.image = ResourceManager.load_coordinates(self.current_sprite, COORDINATES_CHARACTER)
        elif not self._is_moving:
            self.current_sprite = STOPPED
            self.image = ResourceManager.load_coordinates(self.current_sprite, COORDINATES_CHARACTER)

    def add(self, *groups):
        for group in groups:
            group.add(self)
            if group not in self.groups:
                self.groups.append(group)

    def remove(self, *groups):
        for group in groups:
            if self in group:
                group.remove(self)
            if group in self.groups:
                self.groups.remove(group)

    # ####################################################################### #
    #                                INTERACTION                              #
    # ####################################################################### #

    def _interact(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self._in_key:
                self._has_key = True
                self._interacted_with_key = True
                self.notify_observers()
                self._interacted_with_key = False

    # ####################################################################### #
    #                                OBSERVER                                 #
    # ####################################################################### #

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.notified()

    @staticmethod
    def is_detected(player_mask: Mask, enemy_mask: Mask):
        if player_mask is None or enemy_mask is None:
            return False
        return player_mask.overlap_area(enemy_mask, (0, 0)) > 0

    def alive(self):
        return self._is_alive

    def detected(self):
        return self._is_exposed

    def health(self):
        return self._health, self._max_health

    def moving(self):
        return self._is_moving

    def recovering(self):
        return self._recovering

    def in_door(self):
        return self._in_exit

    def in_key(self):
        return self._in_key

    def has_key(self):
        return self._has_key

    def interacted_key(self):
        return self._interacted_with_key

    @deprecated("This method is no longer used.")
    def picked_up_key(self):
        """if self._picked_up_key:
            # Set the control variable to False so that game manager does not get confused
            self._picked_up_key = False
            return True
        else:
            return False"""

    @deprecated("This method is no longer used.")
    def key_controls(self):
        """if self._toggle_key_controls:
            # Set the control variable to False so that game manager does not get confused
            self._toggle_key_controls = False
            return True
        else:
            return False"""
