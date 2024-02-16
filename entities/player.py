from map.grid import Grid
from utils.constants import *
import math
import pygame
from utils.enums import Direction


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        PLAYER CLASS                                           #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Player:
    def __init__(self, x: int, y: int, movement_speed: float, grid: Grid, win):
        """
        Initialize an Enemy object.

        Args:
            x (int): X coordinate of the enemy.
            y (int): Y coordinate of the enemy.
            movement_speed (float): Speed of movement.
            grid (Grid): Grid for pathfinding.
            win: Surface for drawing.
        """
        self.x = x
        self.y = y
        self.size = NPC_SIZE

        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ VISUAL REPRESENTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
        self.screen = win
        self.offset = VIEW_OFFSET * (NPC_SIZE / 20)

        # 2. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ MOVEMENT AND ROTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.angle = NPC_ANGLE
        self.speed = movement_speed
        self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
        self.delta_y = math.sin(math.radians(self.angle)) * self.offset
        self.grid = grid
        self.last_direction = Direction.NORTH

        self.is_alive = True

    # ####################################################################### #
    #                                   DRAW                                  #
    # ####################################################################### #

    def draw(self):
        """
        Draw the player.
        """
        # Draw the square
        pygame.draw.rect(self.screen, BLUE, self.rect)

        # Draw the rotated triangle
        end_point = (self.rect.centerx - self.delta_x * 10, self.rect.centery - self.delta_y * 10)
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
        pygame.draw.polygon(self.screen, (255, 0, 0), triangle_points)

    # ####################################################################### #
    #                                   MOVE                                  #
    # ####################################################################### #

    def move(self, keys, movement_option='WASD'):
        """
        Update the player's position and orientation.
        """
        direction_x = 0
        direction_y = 0
        direction = Direction.STOPPED

        if movement_option == 'WASD':
            if keys[pygame.K_w]:
                direction_y -= 1
            if keys[pygame.K_s]:
                direction_y += 1
            if keys[pygame.K_d]:
                direction_x += 1
            if keys[pygame.K_a]:
                direction_x -= 1
        else:
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
