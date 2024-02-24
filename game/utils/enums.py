from enum import Enum, auto


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        DIRECTIONS                                             #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTHEAST = (1, -1)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (-1, 1)
    NORTHWEST = (-1, -1)
    STOPPED = (0, 0)

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    @property
    def delta_x(self):
        return self.dx

    @property
    def delta_y(self):
        return self.dy

    def is_cardinal(self):
        if self == Direction.EAST or self == Direction.NORTH:
            return True
        if self == Direction.WEST or self == Direction.SOUTH:
            return True
        if self == Direction.STOPPED:
            return True

    @staticmethod
    def general_direction(general_direction):
        if general_direction == Direction.EAST:
            direction_list = [Direction.NORTHEAST, Direction.SOUTHEAST]
        elif general_direction == Direction.NORTH:
            direction_list = [Direction.NORTHEAST, Direction.NORTHWEST]
        elif general_direction == Direction.WEST:
            direction_list = [Direction.NORTHWEST, Direction.SOUTHWEST]
        elif general_direction == Direction.SOUTH:
            direction_list = [Direction.SOUTHWEST, Direction.SOUTHEAST]
        else:
            direction_list = []
        return direction_list

    def angle(self):
        """
        Returns the angle in degrees corresponding to the direction.
        East is 0, North is 90, West is 180, South is 270.
        """
        if self == Direction.EAST:
            return 0
        elif self == Direction.NORTH:
            return 90
        elif self == Direction.WEST:
            return 180
        elif self == Direction.SOUTH:
            return 270
        elif self == Direction.NORTHEAST:
            return 45
        elif self == Direction.NORTHWEST:
            return 135
        elif self == Direction.SOUTHEAST:
            return 315
        elif self == Direction.SOUTHWEST:
            return 225

    def __str__(self):
        return self.name


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        CONTROLLERS                                            #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
class Controls(Enum):
    WASD = "WASD"
    Arrows = "Arrows"

    @staticmethod
    def from_string(s):
        for control in Controls:
            if s == control.value:
                return control
        raise ValueError("Invalid control string")

