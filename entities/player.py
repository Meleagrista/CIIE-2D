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
        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ VISUAL REPRESENTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.x = x
        self.y = y
        self.size = NPC_SIZE
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

    # ####################################################################### #
    #                                   DRAW                                  #
    # ####################################################################### #

    def draw(self):
        """
        Draw the player.
        """
        rect_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, BLUE, (0, 0, self.size, self.size))
        rotated_rect = pygame.transform.rotate(rect_surface, self.angle)
        rect = rotated_rect.get_rect()
        rect.center = (self.x, self.y)
        self.screen.blit(rotated_rect, rect)
        end_point = (self.x - self.delta_x * 10, self.y - self.delta_y * 10)
        angle_to_horizontal = math.atan2(self.delta_y, self.delta_x)
        triangle_size = self.size // 2
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

    def move(self, keys):
        """
        Update the player's position and orientation.
        """
        direction_x = 0
        direction_y = 0
        direction = Direction.STOPPED

        if keys[pygame.K_w]:
            direction_y -= 1
        if keys[pygame.K_s]:
            direction_y += 1
        if keys[pygame.K_d]:
            direction_x += 1
        if keys[pygame.K_a]:
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

        # Update player's position based on direction
        self.x += direction.delta_x * self.speed
        self.y += direction.delta_y * self.speed
