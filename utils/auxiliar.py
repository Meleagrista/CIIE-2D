import math

import numpy as np
import pygame
from unidecode import unidecode


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
