import numpy as np
import pygame
from scipy.interpolate import CubicSpline

from map.grid import Grid
from utils.algorithms import *
from utils.constants import *


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        ENEMY CLASS                                            #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Enemy:
    def __init__(self, x: int, y: int, movement_speed: float, rotation_speed: float, grid: Grid, win):
        """
        Initialize an Enemy object.

        Args:
            x (int): X coordinate of the enemy.
            y (int): Y coordinate of the enemy.
            movement_speed (float): Speed of movement.
            rotation_speed (float): Speed of rotation.
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
        self.rotation = rotation_speed
        # self.need_spin = True
        self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
        self.delta_y = math.sin(math.radians(self.angle)) * self.offset

        # 3. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ PATHFINDING ALGORITHM ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.grid = grid
        self.end = None
        self.start = None
        self.path_points = []
        self.next_point = None
        self.path_nodes = []
        self.next_node = None

    # ####################################################################### #
    #                                   DRAW                                  #
    # ####################################################################### #

    def draw(self):
        """
        Draw the enemy.
        """
        rect_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(rect_surface, GREEN, (0, 0, self.size, self.size))
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

    def update(self):
        """
        Update the enemy's position and orientation.
        """
        current_pos = (self.x, self.y)
        if self.next_point is None or self.end.compare_pos(current_pos):
            self.pathfinding()
        elif self.has_reached(self.next_point):
            self.set_next_point()
        """if len(self.points_from_path()) > 1:
            self.draw_path(self.interpolate_points(8), 1, (0, 0, 255))"""
        end_point = self.next_point
        if self.is_facing(end_point):
            self.x -= self.delta_x * self.speed
            self.y -= self.delta_y * self.speed
        else:
            self.angle = self.angle_to_point(end_point)
            self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
            self.delta_y = math.sin(math.radians(self.angle)) * self.offset

    # ####################################################################### #
    #                                  ROTATE                                 #
    # ####################################################################### #

    def angle_to_point(self, point, show: bool = False):
        """
        Calculate the angle between the current direction and the direction towards the given point.

        Args:
            point (Tuple[int, int]): Target point.
            show (bool): Whether to print angle information.

        Returns:
            float: Angle.
        """
        delta_x = point[0] - self.x
        delta_y = point[1] - self.y
        angle_rad = math.atan2(delta_y, delta_x)
        angle_deg = math.degrees(angle_rad)
        if show:
            print('Original: ' + str(angle_deg))
        if angle_deg < 0:
            angle_final = -angle_deg
        else:
            angle_final = 360 - angle_deg
        if show:
            print('Transformed: ' + str(angle_final), '\n')
        return angle_final

    def is_facing(self, point):
        """
        Check if the enemy is facing a given point.

        Args:
            point (Tuple[int, int]): Target point.

        Returns:
            bool: True if facing, False otherwise.
        """
        threshold_angle = abs(self.rotation) + 1
        angle_to_point_deg = self.angle_to_point(point)
        angle_diff = (angle_to_point_deg - self.angle + 180) % 360 - 180
        return abs(angle_diff) <= threshold_angle

    def shortest_rotation(self, point):
        """
        Determine the shortest rotation direction towards a given point.

        Args:
            point (Tuple[int, int]): Target point.

        Returns:
            int: Rotation direction (-1 for left, 1 for right).
        """
        target_angle = self.angle_to_point(point)
        diff = (target_angle - self.angle + 360) % 360
        return 1 if diff <= 180 else -1

    def rotate(self, rotation):
        """
        Rotate the enemy by a given angle.

        Args:
            rotation (int): Rotation angle.
        """
        self.angle = (self.angle + rotation) % 360

    # ####################################################################### #
    #                                 PATHFIND                                #
    # ####################################################################### #

    def pathfinding(self):
        """
        Perform pathfinding to set the next node in the path.
        """
        self.set_start()
        self.set_random_end()
        self.path_nodes = a_star(self)
        self.next_node = self.path_nodes[1]
        self.path_points = self.interpolate_points(8)
        self.next_point = self.path_points[1]
        self.path_nodes.pop(0)
        self.path_points.pop(0)

    def set_next_node(self):
        """
        Set the next node and remove the previous from the path.
        """
        try:
            index = self.path_nodes.index(self.next_node)
            self.next_node = self.path_nodes[index + 1]
            self.path_nodes.pop(index)
        except Exception as e:
            print(e)

    def set_start(self):
        """
        Set the starting node for pathfinding.
        """
        self.start = self.grid.get_node((self.x, self.y))

    def set_manual_end(self, node):
        """
        Set the end node manually.

        Args:
            node: Node to set as the end.
        """
        self.end = node

    def set_random_end(self):
        """
        Set a random node as the end point for pathfinding.
        """
        self.end = self.grid.get_random_node()

    def draw_path(self, point_list, point_size=1, point_color=(255, 0, 0)):
        """
        Draws a path on the screen using circles to represent points.

        Args:
            point_list (list): List of points (tuples) to be drawn.
            point_size (int, optional): Size of the points. Defaults to 1.
            point_color (tuple, optional): RGB tuple representing the color of the points. Defaults to (255, 0, 0).
        """
        for point in point_list:
            pygame.draw.circle(self.screen, point_color, point, point_size)

    def set_next_point(self):
        """
        Sets the next point in the path.

        Raises:
            Exception: If the next point is not found in the path_points list.
        """
        try:
            index = self.path_points.index(self.next_point)
            self.next_point = self.path_points[index + 1]
            self.path_points.pop(index)
        except Exception as e:
            print(e)

    def has_reached(self, point, threshold: int = 1):
        """
        Checks if the current point has reached the specified point within a certain threshold.

        Args:
            point (tuple): The target point to check against.
            threshold (int, optional): The maximum allowable distance between the current point and the target point. Defaults to 1.

        Returns:
            bool: True if the current point is within the threshold of the target point, False otherwise.
        """
        return (point[0] - threshold <= self.x <= point[0] + threshold) and (
                point[1] - threshold <= self.y <= point[1] + threshold)

    def points_from_path(self):
        """
        Extracts points from path_nodes and returns them as a list.

        Returns:
            list: A list of points extracted from path_nodes.
        """
        points = []
        for square in self.path_nodes:
            points.append(square.get_pos())
        return points

    def interpolate_points(self, segments):
        """
        Interpolates points along the path using cubic spline interpolation.

        Args:
            segments (int): Number of segments for interpolation.

        Returns:
            list: A list of interpolated points.
        """
        points = np.array(self.points_from_path())
        t = np.arange(len(points))
        x = points[:, 0]
        y = points[:, 1]

        cs_x = CubicSpline(t, x)
        cs_y = CubicSpline(t, y)

        smooth_points = []
        for i in range(len(points) - 1):
            smooth_t = np.linspace(i, i + 1, segments)
            smooth_points.extend(np.column_stack([cs_x(smooth_t), cs_y(smooth_t)]))

        # Append the last point without interpolation
        smooth_points.append(points[-1])

        return [tuple(point) for point in smooth_points]
