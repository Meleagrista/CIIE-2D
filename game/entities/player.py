import math
from typing_extensions import deprecated

import pygame
from pygame import Mask

from game.map.grid import Grid
from game.sprites.spritesheet import SpriteSheet
from utils.auxiliar import get_direction, increase, decrease, has_changed
from utils.constants import *
from utils.enums import *
from utils.paths.assets_paths import CHARACTER_ASSETS


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PLAYER CLASS                                           #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Player(pygame.sprite.Sprite):
    def __init__(self,
                 x: int,
                 y: int,
                 movement_speed: float,
                 grid: Grid
                 ):
        """
        Initialize a Player object.

        Args:
            x (int): X coordinate of the player.
            y (int): Y coordinate of the player.
            movement_speed (float): Speed of movement.
            grid (Grid): Grid for pathfinding.
        """
        super().__init__()

        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ VISUAL REPRESENTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.x = x
        self.y = y
        self.groups = []
        self.size = NPC_SIZE * 0.5
        self._sprite_sheet = SpriteSheet(CHARACTER_ASSETS, 10, 13, NPC_SIZE * 2.5)
        self._animation_frames = 4
        self._animation_start = 35
        self._animation_idle = 2
        self._current_frame = 0
        self._looking_right = True
        self.offset = VIEW_OFFSET * (NPC_SIZE / 20)
        self.image = pygame.Surface((NPC_SIZE, NPC_SIZE))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

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

        # 4. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ HEALTH AND COOLDOWN   ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._max_health = LIFE * FPS
        self._health = self._max_health
        self._max_cooldown = FPS
        self._cooldown = self._max_cooldown
        self._recovering = False

        # 5. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ STATUS FLAGS           ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._is_alive = True
        self._is_exposed = False
        self._is_moving = False

        self.exposer = []

        self._in_exit = False
        self._in_key = False
        self._has_key = False
        self._interacted_with_key = False

    def draw(self, **kwargs):
        surface = kwargs.pop('internal_surface', None)
        offset = kwargs.pop('offset', None)

        # Check if surface and offset are provided and of correct types
        if surface is not None and not isinstance(surface, pygame.Surface):
            raise TypeError("surface must be an instance of pygame.Surface class")
        if offset is not None and not isinstance(offset, pygame.math.Vector2):
            raise TypeError("offset must be an instance of Vector2 class")

        # Calculate sprite position
        sprite_rect = self.image.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom - 10)

        # Flip the image if needed
        flipped_image = pygame.transform.flip(self.image, self._looking_right, False)

        # Draw the rotated sprite
        surface.blit(flipped_image, (sprite_rect.x - offset.x, sprite_rect.y - offset.y))

    def update(self, **kwargs):
        # Variable initialization
        movement_option = kwargs.pop('movement_option', None)
        player_mask = kwargs.pop('player_mask', None)
        enemy_mask = kwargs.pop('enemy_mask', None)

        # Check if movement option, player mask, and enemy mask are provided and of correct types
        if movement_option is not None and not isinstance(movement_option, Controls):
            raise TypeError("movement_option must be an instance of Controls enum")
        if player_mask is not None and not isinstance(player_mask, Mask):
            raise TypeError("player_mask must be an instance of Mask type")
        if enemy_mask is not None and not isinstance(enemy_mask, Mask):
            raise TypeError("enemy_mask must be an instance of Mask type")

        # ENEMY DETECTION AND HEALTH HANDLING
        if self._is_detected(player_mask=player_mask, enemy_mask=enemy_mask):
            self._health = decrease(self._health)
            self._recovering = False
            self._cooldown = 0
            if self._health <= 0:
                self._is_alive = False
            if not self._is_exposed or not self._is_alive:
                self._is_exposed = True
                self.notify_observers()

        elif self._is_alive:
            previous_exposer = self.exposer
            if self._is_exposed:
                self._is_exposed = False
                self.notify_observers()
            else:
                self.exposer = []
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
            if previous_exposer != self.exposer:
                self.notify_observers()

        ##############################
        # MOVEMENT AND DIRECTION
        direction, direction_x, direction_y = get_direction(movement_option)

        if direction.is_west():
            self._looking_right = True
        if direction.is_east():
            self._looking_right = False

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

        # COLLISION DETECTION
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

        # KEY COLLECTION AND EXIT DETECTION
        in_key = self._in_key
        self._in_key = self.grid.is_key_square(new_x + self.size / 2, new_y + self.size / 2)
        if has_changed(self._in_key, in_key):
            self.notify_observers()

        if self._in_key:
            self._interact()

        self._in_exit = self.grid.is_exit_square(new_x, new_y)
        if has_changed(self._in_exit, self._in_exit):
            self.notify_observers()

        # MOVEMENT CHECK
        if self.x == new_x and self.y == new_y and self._is_moving:
            self._is_moving = False
            self.notify_observers()
        elif (self.x != new_x or self.y != new_y) and not self._is_moving:
            self._is_moving = True
            self.notify_observers()

        # Update player's position
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (self.x, self.y)

        # ANIMATION
        if self._is_moving:
            self._current_frame += 0.5  # Increment frame counter by 0.5
            self._current_frame %= self._animation_frames  # Ensure frame counter wraps around
            self.image = self._sprite_sheet.get_sprite_by_number(self._animation_start + int(self._current_frame))
        elif not self._is_moving:
            self.image = self._sprite_sheet.get_sprite_by_number(self._animation_idle)

    def add(self, *groups):
        for group in groups:
            group.add(self)
        self.groups.extend(groups)

    def remove(self, *groups):
        for group in groups:
            group.remove(self)
        self.groups = [group for group in self.groups if group not in groups]

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.notified()

    # ####################################################################### #
    #                                PROPERTIES                               #
    # ####################################################################### #

    def alive(self) -> bool:
        """Check if the player is alive."""
        return self._is_alive

    def detected(self) -> bool:
        """Check if the player is detected by enemies."""
        return self._is_exposed

    def health(self) -> tuple[int, int]:
        """Get the player's current health and maximum health."""
        return self._health, self._max_health

    def moving(self) -> bool:
        """Check if the player is currently moving."""
        return self._is_moving

    def recovering(self) -> bool:
        """Check if the player is currently recovering."""
        return self._recovering

    def in_door(self) -> bool:
        """Check if the player is in front of a door."""
        return self._in_exit

    def in_key(self) -> bool:
        """Check if the player is in a key area."""
        return self._in_key

    def has_key(self) -> bool:
        """Check if the player has collected the key."""
        return self._has_key

    def interacted_key(self) -> bool:
        """Check if the player has interacted with the key."""
        return self._interacted_with_key

    # ####################################################################### #
    #                                INTERACTION                              #
    # ####################################################################### #

    def _interact(self) -> None:
        """
        Interact with the environment.

        If the player is in a key area and hasn't collected the key, pressing space will
        collect the key, trigger observers, and hide the key in the environment.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self._in_key and not self._has_key:
                self._has_key = True
                self._interacted_with_key = True
                self.notify_observers()
                self._interacted_with_key = False
                self.grid.visible_key = False

    @staticmethod
    def _is_detected(player_mask: Mask, enemy_mask: Mask) -> bool:
        """
        Check if the player is detected by an enemy.

        Args:
            player_mask (Mask): The mask representing the player's position.
            enemy_mask (Mask): The mask representing the enemy's position.

        Returns:
            bool: True if the player is detected by the enemy, False otherwise.
        """
        return (
                player_mask is not None and
                enemy_mask is not None and
                player_mask.overlap_area(enemy_mask, (0, 0)) > 0
        )

    # ####################################################################### #
    #                                DEPRECATED                               #
    # ####################################################################### #

    @deprecated("This method is no longer used.")
    def picked_up_key(self):
        """if self._picked_up_key:
            # Set the control variable to False so that game manager does not get confused
            self._picked_up_key = False
            return True
        else:
            return False"""
        raise NotImplemented

    @deprecated("This method is no longer used.")
    def key_controls(self):
        """if self._toggle_key_controls:
            # Set the control variable to False so that game manager does not get confused
            self._toggle_key_controls = False
            return True
        else:
            return False"""
        raise NotImplemented
