from enum import Enum


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
