from pygame import Surface, Mask

from utils.constants import *
from utils.enums import *
from game.map.grid import Grid

import math
import pygame


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PLAYER CLASS                                           #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, movement_speed: float, grid: Grid):
        """
        Initialize an Enemy object.

        Args:
            x (int): X coordinate of the enemy.
            y (int): Y coordinate of the enemy.
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
        self._health = LIFE * FPS
        self._is_alive = True

    def draw(self, surface, offset):
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
                raise TypeError("movement_option must be an isntance of Controls enum,")

        surface = kwargs.pop('surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an isntance of Surface type,")

        player_mask = kwargs.pop('player_mask', None)
        if player_mask is not None:
            if not isinstance(player_mask, Mask):
                raise TypeError("player_mask must be an isntance of Mask type,")

        enemy_mask = kwargs.pop('enemy_mask', None)
        if enemy_mask is not None:
            if not isinstance(enemy_mask, Mask):
                raise TypeError("enemy_mask must be an isntance of Mask type,")

        if self.is_detected(surface=surface, player_mask=player_mask, enemy_mask=enemy_mask):
            if self._health > 0:
                self._health = self._health - 1
            else:
                self._is_alive = False
            self.notify_observers()
        elif self._is_alive:
            self._health = self._health + 1

        direction_x = 0
        direction_y = 0
        direction = Direction.STOPPED

        keys = pygame.key.get_pressed()

        if movement_option == Controls.WASD:
            if keys[pygame.K_w]:
                direction_y -= 1
            if keys[pygame.K_s]:
                direction_y += 1
            if keys[pygame.K_d]:
                direction_x += 1
            if keys[pygame.K_a]:
                direction_x -= 1
        elif movement_option == Controls.Arrows:
            if keys[pygame.K_UP]:
                direction_y -= 1
            if keys[pygame.K_DOWN]:
                direction_y += 1
            if keys[pygame.K_RIGHT]:
                direction_x += 1
            if keys[pygame.K_LEFT]:
                direction_x -= 1

        # Handle diagonal movement
        if direction_x != 0 and direction_y != 0:
            if direction_x == 1 and direction_y == -1:
                direction = Direction.NORTHEAST
            elif direction_x == 1 and direction_y == 1:
                direction = Direction.SOUTHEAST
            elif direction_x == -1 and direction_y == 1:
                direction = Direction.SOUTHWEST
            elif direction_x == -1 and direction_y == -1:
                direction = Direction.NORTHWEST
        # Handle opposite directions
        elif direction_x != 0 or direction_y != 0:
            if direction_x == 1:
                direction = Direction.EAST
            elif direction_x == -1:
                direction = Direction.WEST
            elif direction_y == -1:
                direction = Direction.NORTH
            elif direction_y == 1:
                direction = Direction.SOUTH
        else:
            direction = Direction.STOPPED

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
    #                                OBSERVER                                 #
    # ####################################################################### #

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.notified()

    def is_detected(self, surface: Surface, player_mask: Mask, enemy_mask: Mask):
        return player_mask.overlap_area(enemy_mask, (0, 0)) > 0

    def alive(self):
        return self._is_alive
