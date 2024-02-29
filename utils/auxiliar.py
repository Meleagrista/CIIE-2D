import math
import pygame

from unidecode import unidecode
from utils.enums import Direction, Controls

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                  PLAYER ABSTRACTION FUNCTIONS                                 #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#


def increase(value, max_value):
    return min(value + 1, max_value)


def decrease(value):
    return max(value - 1, 0)


def has_changed(new, old):
    return new != old


def get_direction(movement_option):
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

    return direction, direction_x, direction_y

# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                  TEXT REFACTORING FUNCTIONS                                   #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

def replace_accented_characters(text):
    """
    Replace accented characters with their base characters.

    Parameters:
        text (str): The input text with accented characters.

    Returns:
        str: The text with accented characters replaced by their base characters.
    """
    return unidecode(text)


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        MASKING FUNCTIONS                                      #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

def fill_mask(surface, mask):
    # Convert the mask to a surface with white for the mask area and transparent for the rest
    result_surface = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=None)

    surface.blit(result_surface, (0, 0))


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                     ANGLE TOOLS FUNCTIONS                                     #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

def increase_degree(angle, increment):
    return (angle + increment) % 360


def compare_degree(angle, start, end):
    # Normalize angles to be between 0 and 360 degrees
    angle %= 360
    start %= 360
    end %= 360

    # Check if angle1 is between start and end
    if start <= end:
        return angle <= start or angle >= end
    return end <= angle <= start


def dist(origin_x, origin_y, point_x, point_y):
    return math.sqrt((point_x - origin_x) * (point_x - origin_x) + (point_y - origin_y) * (point_y - origin_y))


def is_point_neighbour(point1, point2):
    if point1 is None or point2 is None:
        return False
    x1, y1 = point1
    x2, y2 = point2
    return x1 == x2 or y1 == y2
