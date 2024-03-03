import math

import pygame
from pygame import Mask, Surface
from typing_extensions import deprecated

from game.map.grid import Grid
from utils.auxiliar import get_direction, increase, decrease, has_changed
from utils.constants import *
from utils.enums import *
from utils.filepaths import DEATH_SOUND, PICK_UP_KEY_SOUND, DETECTED_SOUND


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
        self._max_health = LIFE * FPS
        self._health = self._max_health
        self._max_cooldown = FPS
        self._cooldown = self._max_cooldown
        self._is_alive = True
        self._is_exposed = False
        
        self._in_exit = False
        self._in_key = False
        self._has_key = False
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

        # Draw the square
        pygame.draw.rect(surface, BLUE, (self.rect.x - offset.x, self.rect.y - offset.y, self.size, self.size))

        # Draw the rotated triangle
        end_point = (self.rect.centerx - self.delta_x * 10 - offset.x, self.rect.centery - self.delta_y * 10 - offset.y)
        angle_to_horizontal = math.atan2(self.delta_y, self.delta_x)
        triangle_size = NPC_SIZE // 2
        triangle_points = [
            end_point,
            (
                end_point[0] + triangle_size * math.cos(angle_to_horizontal - math.radians(30)),
                end_point[1] + triangle_size * math.sin(angle_to_horizontal - math.radians(30)),
            ),
            (
                end_point[0] + triangle_size * math.cos(angle_to_horizontal + math.radians(30)),
                end_point[1] + triangle_size * math.sin(angle_to_horizontal + math.radians(30)),
            ),
        ]
        pygame.draw.polygon(surface, (255, 0, 0), triangle_points)

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
        #pygame.mixer.pre_init(44100, 16, 2, 4096)
        #pygame.mixer.init()

        #sound_detected = pygame.mixer.Sound(DETECTED_SOUND)
        if self.is_detected(player_mask=player_mask, enemy_mask=enemy_mask):
            self._is_exposed = True
            self._health = decrease(self._health)
            self._cooldown = 0
            if self._health <= 0:
                #sound_detected.stop()
                pygame.mixer.quit()
                pygame.mixer.pre_init(44100, 16, 2, 4096)
                pygame.mixer.init()
                sound_death = pygame.mixer.Sound(DEATH_SOUND)
                sound_death.play()
                self._is_alive = False
            #else:
                #sound_detected.play(-1)
            self.notify_observers()
        elif self._is_alive:
            #sound_detected.stop()
            pygame.mixer.quit()
            self._is_exposed = False
            self._cooldown = increase(self._cooldown, self._max_cooldown)
            if self._cooldown >= self._max_cooldown:
                self._health = increase(self._health, self._max_health)

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

        #if (self.x != new_x or self.y != new_y):
        #  sound = pygame.mixer.Sound(MOVEMENT_SOUND)
        #  channel = sound.play()

        # Update player's position
        self.x = new_x
        self.y = new_y

        # Update sprite
        self.rect.topleft = (self.x, self.y)

    def kill(self):
        for group in self.groups:
            group.remove(self)
        del self

    def add(self, *groups):
        for group in groups:
            group.add(self)
            if group not in self.groups:
                self.groups.append(group)

    def remove(self, *groups):
        for group in groups:
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
                sound_pick_up_key = pygame.mixer.Sound(PICK_UP_KEY_SOUND)
                sound_pick_up_key.play()
                self.notify_observers()

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
        return player_mask.overlap_area(enemy_mask, (0, 0)) > 0

    def alive(self):
        return self._is_alive

    def detected(self):
        return self._is_exposed

    def health(self):
        return self._health, self._max_health

    def in_door(self):
        return self._in_exit

    def in_key(self):
        return self._in_key

    def has_key(self):
        return self._has_key

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
