import math
import random
from queue import PriorityQueue

import pygame

NPC_SIZE = 10
NPC_ANGLE = 90.0
VIEW_OFFSET = 2.5


def heuristic(current, goal, weight):
    current_x, current_y = current
    goal_x, goal_y = goal
    return math.sqrt((current_x - goal_x) ** 2 +
                     (current_y - goal_y) ** 2) + weight


class Enemy:
    def __init__(self, x, y, movement_speed, rotation_speed, grid, win):
        # MOVEMENT
        self.x = x
        self.y = y
        self.size = NPC_SIZE
        self.screen = win
        self.offset = VIEW_OFFSET * (NPC_SIZE / 20)
        # MOVEMENT VARIABLES
        self.angle = NPC_ANGLE
        self.speed = movement_speed
        self.rotation = rotation_speed
        self.need_spin = True
        self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
        self.delta_y = math.sin(math.radians(self.angle)) * self.offset
        # PATHFINDING
        self.grid = grid
        self.end = None
        self.start = None
        self.path_nodes = []
        self.next_node = None

    # ############################## MOVING ############################# #

    def angle_to_point(self, point, show: bool = False):
        # Calculate the angle between the current direction and the direction towards the given point
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
        # Convert threshold angle from degrees to radians
        threshold_angle = abs(self.rotation) + 1

        # Calculate the angle between the current direction and the direction towards the given point
        angle_to_point_deg = self.angle_to_point(point)

        # Convert angles to the range [-180, 180]
        angle_diff = (angle_to_point_deg - self.angle + 180) % 360 - 180

        """print('Difference between desired angle (' + str(angle_to_point_deg) + ') and actual angle (' + str(
            self.angle) + ') is ' + str(angle_diff))"""

        # Check if the angle difference is within the threshold
        return abs(angle_diff) <= threshold_angle

    def shortest_rotation(self, point):
        target_angle = self.angle_to_point(point)

        diff = (target_angle - self.angle + 360) % 360

        """print('[X] Distance between desired angle (' + str(target_angle) + ') and actual angle (' + str(
            self.angle) + ') is ' + str(diff))"""

        # Determine the shortest rotation direction
        if diff <= 180:
            return 1
        else:
            return -1

    def rotate(self, rotation):
        self.angle = (self.angle + rotation) % 360

    def update(self):
        current_pos = (self.x, self.y)
        if self.next_node is None or self.end.compare_pos(current_pos):
            self.pathfinding()
        elif self.next_node.compare_pos(current_pos):
            self.set_next_node()

        end_point = self.next_node.get_pos()
        self.draw_path(self.points_from_path(), 2, (0, 255, 0))
        self.draw_path(self.interpolate_points(2), 1, (0, 0, 255))

        if self.end is not None:
            pygame.draw.circle(self.screen, (255, 0, 0), self.end.get_pos_zip(), 3)
        if self.is_facing(end_point):
            if not self.need_spin:
                # print('He looked the right way!')
                self.need_spin = True
            self.x -= self.delta_x * self.speed
            self.y -= self.delta_y * self.speed
        else:
            if self.need_spin:
                if self.shortest_rotation(end_point) > 0:
                    self.rotation = abs(self.rotation)
                    # print('He should look to the left.')
                else:
                    self.rotation = -1 * abs(self.rotation)
                    # print('He should look to the right.')
                self.need_spin = False
            self.rotate(self.rotation)
            self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
            self.delta_y = math.sin(math.radians(self.angle)) * self.offset

    # ############################# DRAWING ############################# #

    def draw_path(self, point_list, point_size=1, point_color=(255, 0, 0)):
        for point in point_list:
            pygame.draw.circle(self.screen, point_color, point, point_size)

    def draw(self):
        # Create a surface for the rectangle with transparency
        rect_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Draw a _ rectangle on the surface
        pygame.draw.rect(rect_surface, (0, 255, 0), (0, 0, self.size, self.size))

        # Rotate the rectangle surface by the specified angle
        rotated_rect = pygame.transform.rotate(rect_surface, self.angle)

        # Get the rectangle object of the rotated rectangle
        rect = rotated_rect.get_rect()

        # Set the center of the rectangle to match the original center
        rect.center = (self.x, self.y)

        # Draw the rotated rectangle on the screen
        self.screen.blit(rotated_rect, rect)

        # Calculate the end point of the line
        end_point = (self.x - self.delta_x * 10, self.y - self.delta_y * 10)

        # Calculate the angle between the line and the horizontal axis
        angle_to_horizontal = math.atan2(self.delta_y, self.delta_x)

        # Determine the size of the triangle
        triangle_size = self.size // 2

        # Calculate the points of the triangle based on the angle
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

        # Draw a _ triangle on the screen with the calculated points
        pygame.draw.polygon(self.screen, (255, 0, 0), triangle_points)
        # pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 3)

    # ########################### PATHFINDING ########################### #
    @staticmethod
    def reconstruct_path(came_from, current):
        nodes = [current]
        while current in came_from:
            current = came_from[current]
            nodes.append(current)
            # current.make_path()
        return nodes[::-1]

    def a_star(self):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid.nodes for spot in row}
        g_score[self.start] = 0
        f_score = {spot: float("inf") for row in self.grid.nodes for spot in row}
        f_score[self.start] = heuristic(self.start.get_pos(), self.end.get_pos(), self.start.get_weight())

        open_set_hash = {self.start}

        while not open_set.empty():

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end:
                return self.reconstruct_path(came_from, self.end)

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + current.weight

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), self.end.get_pos(),
                                                                 neighbor.get_weight())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return []

    def points_from_path(self):
        points = []
        for square in self.path_nodes:
            points.append(square.get_pos())
        return points

    def interpolate_points(self, segments):
        points = self.points_from_path()
        smooth_points = []
        for i in range(len(points) - 1):
            ini = points[i]
            end = points[i + 1]

            for j in range(segments + 1):
                x_inter = ini[0] + (end[0] - ini[0]) * j / segments
                y_inter = ini[1] + (end[1] - ini[1]) * j / segments
                smooth_points.append((x_inter, y_inter))

        # Append the last point without interpolation
        smooth_points.append(points[-1])

        return smooth_points

    def pathfinding(self):
        self.set_start()
        self.set_random_end()
        self.path_nodes = self.a_star()
        self.next_node = self.path_nodes[1]
        self.path_nodes.pop(0)

    def set_next_node(self):
        try:
            index = self.path_nodes.index(self.next_node)
            self.next_node = self.path_nodes[index + 1]
            self.path_nodes.pop(index)
        except Exception as e:
            print(e)

    def set_start(self):
        self.start = self.grid.get_node((self.x, self.y))

    def set_manual_end(self, node):
        self.end = node

    def set_random_end(self):
        row = random.randint(0, self.grid.size - 1)
        col = random.randint(0, self.grid.size - 1)
        node = self.grid.nodes[row][col]
        while node.is_barrier():
            row = random.randint(0, self.grid.size - 1)
            col = random.randint(0, self.grid.size - 1)
            node = self.grid.nodes[row][col]
        print('End point created in position ' + str(node.get_pos()))
        self.end = node
