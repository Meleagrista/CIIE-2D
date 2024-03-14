import queue

import numpy as np
from pygame import Surface

from scipy.interpolate import CubicSpline
from typing_extensions import deprecated
from game.map.grid import Grid
from game.sprites.spritesheet import SpriteSheet
from utils.algorithms import *
from utils.auxiliar import *
from utils.constants import *
from utils.paths.assets_paths import ENEMY_ASSETS


# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#
#                                        ENEMY CLASS                                            #
# ====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====*====#

class Enemy(pygame.sprite.Sprite):
    def __init__(self,
                 position,
                 movement_speed,
                 rotation_speed,
                 grid: Grid,
                 window: pygame.Surface,
                 areas
                 ):
        super().__init__()
        self.groups = []

        # 1. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ VISUAL REPRESENTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.x, self.y = position
        self.size = NPC_SIZE
        self.offset = VIEW_OFFSET * (NPC_SIZE / 20)
        self.image = pygame.Surface((NPC_SIZE, NPC_SIZE))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self._sprite_sheet = SpriteSheet(ENEMY_ASSETS, 10, 33, NPC_SIZE * 2.5)
        self._animation_frames = 4
        self._animation_start = 0
        self._idle_frames = 4
        self._idle_start = 0
        self._current_frame = 0
        self._looking_right = True
        self._is_moving = False

        # 2. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ MOVEMENT AND ROTATION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.angle = NPC_ANGLE
        self.speed = movement_speed
        self.rotation = rotation_speed
        self.setting_rotation = True
        self.setting_path = False
        self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
        self.delta_y = math.sin(math.radians(self.angle)) * self.offset
        self.areas = queue.Queue()
        for area in areas:
            self.areas.put(area)

        # 3. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ PATHFINDING ALGORITHM ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.grid = grid
        self.end_node = None
        self.start_node = None
        self.path_nodes = []
        self.path_points = []
        self.next_point = None

        # 4. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ RAY CASTING AND VISION ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.ray_cone = FIELD_OF_VISION
        self.ray_reach = REACH_OF_VISION
        self.ray_radius = self.ray_reach * self.grid.gap
        self.corners = []
        self.mask = None  # Deprecated parameter
        self.win_height = window.get_height()
        self.win_width = window.get_width()

        # 5. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #    ~~ PLAYER STATUS OBSERVER ~~
        #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._status = GREEN

    def draw(self, center, **kwargs):
        surface = kwargs.pop('internal_surface', None)
        if surface is not None:
            if not isinstance(surface, Surface):
                raise TypeError("surface must be an instance of pygame.Surface class")

        offset = kwargs.pop('offset', None)
        if offset is not None:
            if not isinstance(offset, pygame.math.Vector2):
                raise TypeError("offset must be an instance of Vector2 class")

        if not self.in_range(surface, center, self.size * 2):
            return

        if is_looking_right(self.angle):
            self._looking_right = True
        if is_looking_left(self.angle):
            self._looking_right = False

        sprite_rect = self.image.get_rect()
        sprite_rect.centerx = self.rect.centerx
        sprite_rect.bottom = self.rect.bottom - 10

        flipped_image = pygame.transform.flip(self.image, not self._looking_right, False)

        surface.blit(
            source=flipped_image,
            dest=(sprite_rect.x - offset.x, sprite_rect.y - offset.y)
        )

    def in_range(self, surface, center, padding):

        horizontal_distance = abs(self.x - center[0])
        vertical_distance = abs(self.y - center[1])

        return ((horizontal_distance < surface.get_width() // 2 + padding) and
                vertical_distance < surface.get_height() // 2 + padding)

    def update(self, **kwargs):

        #################################
        # DRAWING PATH (OPTIONAL)
        #################################
        # if len(self.points_from_path()) > 1 and show:  self.draw_path(self.path_points, 1, (0, 0, 255))

        ##############################
        # UPDATING ANGLE AND MOVEMENT
        ##############################
        end_point = self.next_point
        updated_angle = self.angle_to_point(end_point)

        if self.setting_path:
            if self.is_facing(end_point):
                self.setting_path = False
            else:
                if self.setting_rotation:
                    if self.shortest_rotation(end_point) > 0:
                        self.rotation = abs(self.rotation)
                    else:
                        self.rotation = -1 * abs(self.rotation)
                    self.setting_rotation = False
                self.rotate(self.rotation)

                if (
                        (self.rotation > 0 and self.angle > updated_angle) or
                        (self.rotation < 0 and self.angle < updated_angle)
                ):
                    # If overshot, revert the rotation and set the correct angle
                    self.angle = updated_angle

                self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
                self.delta_y = math.sin(math.radians(self.angle)) * self.offset
        else:
            iteration_count = 0
            while (abs(updated_angle - self.angle) > 45) and (iteration_count < 2):
                end_point = self.next_point
                self.set_next_point()
                if self.next_point is not None:
                    end_point = self.next_point
                updated_angle = self.angle_to_point(end_point)
                iteration_count += 1

            self.angle = updated_angle

            self.delta_x = -math.cos(math.radians(self.angle)) * self.offset
            self.delta_y = math.sin(math.radians(self.angle)) * self.offset

            self.x -= self.delta_x * self.speed
            self.y -= self.delta_y * self.speed

        ##############################
        # ANIMATION
        ##############################

        self._current_frame += 0.5

        if self._is_moving:
            self._current_frame %= self._animation_frames  # Ensure frame counter wraps around
            self.image = self._sprite_sheet.get_sprite_by_number(self._animation_start + int(self._current_frame))
        else:
            self._current_frame %= self._idle_frames  # Ensure frame counter wraps around
            self.image = self._sprite_sheet.get_sprite_by_number(self._idle_start + int(self._current_frame))

        ##############################
        # CASTING RAYS
        ##############################
        self.cast()

        # Update sprite
        self.rect.center = (self.x, self.y)

    def notified(self, player):
        if player.detected():
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)
            if distance <= self.ray_radius + player.size:
                self._status = RED
            elif distance <= (self.ray_radius + player.size) * 2:
                self._status = ORANGE
            else:
                self._status = GREEN

    def add(self, *groups):
        for group in groups:
            group.add(self)
            if group not in self.groups:
                self.groups.append(group)

    def remove(self, *groups):
        for group in groups:
            if self in group:
                group.remove(self)
            if group in self.groups:
                self.groups.remove(group)

    # ####################################################################### #
    #                               PATHFINDING                               #
    # ####################################################################### #

    def pathfinding(self, end=None, interpolation=8, simplified=True):
        try:
            self.set_start()
            if end is not None:
                self.end_node = end
            else:
                self.set_random_end()
            self.set_intermediate_points(self.a_star(), interpolation, simplified)
        except Exception as e:
            print(e)
            print(self.path_nodes)

    def set_intermediate_points(self, nodes, segments, simplified):
        if segments is None:
            segments = 8
        self.path_nodes = nodes
        self.path_points = self.interpolate_points(segments)
        self.next_point = self.path_points[1]
        self.path_nodes.pop(0)
        self.path_points.pop(0)
        if not simplified:
            self.setting_path = True
            self.setting_rotation = True
            self._is_moving = False

    def set_start(self):
        self.start_node = self.grid.get_node((self.rect.centerx, self.rect.centery))

    def set_end(self, node):
        self.end_node = node

    def set_random_end(self):
        current_node = self.grid.get_node((self.x, self.y))

        if self.areas.empty():
            end_node = self.grid.get_random_node()
            while current_node.distance_to(end_node) < 3 * SQUARE_SIZE:
                end_node = self.grid.get_random_node()
            self.end_node = end_node
        else:
            while True:
                zone = self.areas.get()
                end_node = self.grid.get_random_node_from_zone(zone)
                if end_node is not None and not current_node.compare_node(end_node):
                    self.end_node = end_node
                    self.areas.put(zone)
                    break
                elif self.areas.empty():
                    end_node = self.grid.get_random_node()
                    while current_node.distance_to(end_node) < 3 * SQUARE_SIZE:
                        end_node = self.grid.get_random_node()
                    self.end_node = end_node
                    return

    def set_path(self, node=None, segments=None):
        self.pathfinding(node, segments)

    def set_simplified_path(self, node=None, segments=None):
        self.pathfinding(node, segments, True)

    def set_next_point(self):
        try:
            index = self.path_points.index(self.next_point)
            self.next_point = self.path_points[index + 1]
            self.path_points.pop(index)
        except Exception:
            self.next_point = None

    def has_reached(self, point, threshold: int = 1):
        return (point[0] - threshold <= self.x <= point[0] + threshold) and (
                point[1] - threshold <= self.y <= point[1] + threshold)

    def points_from_path(self):
        points = []
        for square in self.path_nodes:
            points.append(square.get_pos())
        return points

    def interpolate_points(self, segments):
        points = np.array(self.points_from_path())

        if len(points) < 2:
            return points

        t = np.arange(len(points))
        x = points[:, 0]
        y = points[:, 1]

        cs_x = CubicSpline(t, x)
        cs_y = CubicSpline(t, y)

        smooth_points = []
        for i in range(len(points) - 1):
            smooth_t = np.linspace(i, i + 1, segments)
            smooth_points.extend(np.column_stack([cs_x(smooth_t), cs_y(smooth_t)]))

        smooth_points.append(points[-1])

        point_list = [tuple(point) for point in smooth_points]

        if len(point_list) < 2:
            return points

        return point_list

    # ####################################################################### #
    #                               RAY CASTING                               #
    # ####################################################################### #

    def cast(self):
        ##############################
        # INITIALIZE VARIABLES
        ##############################
        start = increase_degree(self.angle, self.ray_cone / 2 + 1)
        ray_degree = start
        end = increase_degree(self.angle, -self.ray_cone / 2)
        previous_point = None
        corner_list = []
        contact_point = None

        ##############################
        # CASTING RAYS
        ##############################
        while compare_degree(ray_degree, start, end):
            ray_degree = increase_degree(ray_degree, -1)
            tan_ray_angle = math.tan(math.radians(ray_degree))

            ##############################
            # HORIZONTAL RAYS
            ##############################
            ray_distance = 0
            if ray_degree == 90 or ray_degree == 270:
                ray_degree += 0.001
            if ray_degree > 180:
                up = False
                ray_y = math.ceil(self.y / self.grid.gap) * self.grid.gap + 0.001
                offset_y = -self.grid.gap
            else:
                up = True
                ray_y = math.ceil(self.y / self.grid.gap) * self.grid.gap - self.grid.gap
                offset_y = self.grid.gap
            ray_x = (self.y - ray_y) / tan_ray_angle + self.x if tan_ray_angle != 0 else self.x
            offset_x = offset_y / tan_ray_angle if tan_ray_angle != 0 else 0
            while ray_distance < self.ray_reach and ray_distance < self.grid.size:
                map_x = int(ray_x // self.grid.gap)
                map_y = int(ray_y // self.grid.gap - (1 if up else 0))
                if (
                        0 <= map_x < self.grid.size and
                        0 <= map_y < self.grid.size and self.grid.nodes[map_x][map_y].is_barrier()
                ):
                    ray_distance = self.ray_reach
                else:
                    ray_x = ray_x + offset_x
                    ray_y = ray_y - offset_y
                    ray_distance += 1
            horizontal_x, horizontal_y = ray_x, ray_y
            horizontal_distance = dist(self.x, self.y, horizontal_x, horizontal_y)

            ##############################
            # VERTICAL RAYS
            ##############################
            ray_distance = 0
            if ray_degree == 90 or ray_degree == 270:
                ray_degree += 0.001
            if 90 < ray_degree < 270:
                right = False
                ray_x = math.ceil(self.x / self.grid.gap) * self.grid.gap - self.grid.gap
                offset_x = -self.grid.gap
            else:
                right = True
                ray_x = math.ceil(self.x / self.grid.gap) * self.grid.gap + 0.001
                offset_x = self.grid.gap
            ray_y = (self.x - ray_x) * tan_ray_angle + self.y if tan_ray_angle != 0 else self.y
            offset_y = offset_x * tan_ray_angle if tan_ray_angle != 0 else 0
            while ray_distance < self.ray_reach and ray_distance < self.grid.size:
                map_x = int(ray_x // self.grid.gap - (0 if right else 1))
                map_y = int(ray_y // self.grid.gap)
                if (
                        0 <= map_x < self.grid.size and
                        0 <= map_y < self.grid.size and self.grid.nodes[map_x][map_y].is_barrier()
                ):
                    ray_distance = self.ray_reach
                else:
                    ray_x += offset_x
                    ray_y -= offset_y
                    ray_distance += 1
            vertical_x, vertical_y = ray_x, ray_y
            vertical_distance = dist(self.x, self.y, vertical_x, vertical_y)

            ##############################
            # COMPARING AND UPDATING CONTACT POINTS
            ##############################
            if vertical_distance < horizontal_distance:
                contact_point = (vertical_x, vertical_y)
            else:
                contact_point = (horizontal_x, horizontal_y)
            if not is_point_neighbour(previous_point, contact_point):
                if previous_point is None:
                    corner_list.append(((self.x, self.y), contact_point))
                else:
                    corner_list.append((previous_point, contact_point))
            previous_point = contact_point

        ##############################
        # FINALIZING CORNER LIST AND UPDATING MASK
        ##############################
        corner_list.append((contact_point, (self.x, self.y)))
        self.corners = corner_list

    def a_star(self):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start_node))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid.nodes for spot in row}
        g_score[self.start_node] = 0
        f_score = {spot: float("inf") for row in self.grid.nodes for spot in row}
        f_score[self.start_node] = heuristic(
            self.start_node.get_pos(),
            self.end_node.get_pos(),
            self.start_node.get_weight()
        )
        open_set_hash = {self.start_node}

        while not open_set.empty():
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end_node:
                return reconstruct_path(came_from, self.end_node)

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + current.weight

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), self.end_node.get_pos(),
                                                                 neighbor.get_weight())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return []

    # ####################################################################### #
    #                                 ROTATION                                #
    # ####################################################################### #

    def angle_to_point(self, point, show=False):
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
        threshold_angle = abs(self.rotation) + 1
        angle_to_point_deg = self.angle_to_point(point)
        angle_diff = (angle_to_point_deg - self.angle + 180) % 360 - 180
        return abs(angle_diff) <= threshold_angle

    def shortest_rotation(self, point):
        target_angle = self.angle_to_point(point)
        diff = (target_angle - self.angle + 360) % 360
        return 1 if diff <= 180 else -1

    def rotate(self, rotation):
        self.angle = (self.angle + rotation) % 360

    # ####################################################################### #
    #                                DEPRECATED                               #
    # ####################################################################### #

    @deprecated("This method is too expensive.")
    def update_mask(self, corners):
        ##############################
        # COLLECT VERTICES
        ##############################
        vertices = []
        for pair in corners:
            point1, point2 = pair
            vertices.append(point1)
            vertices.append(point2)

        ##############################
        # CREATE MASK SURFACE
        ##############################
        mask_surface = pygame.Surface((self.win_width, self.win_height), pygame.SRCALPHA)

        ##############################
        # CREATE LIMIT CIRCLE MASK
        ##############################
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (int(self.x), int(self.y)),
                           REACH_OF_VISION * self.grid.gap)
        limit_circle_mask = pygame.mask.from_surface(mask_surface)

        ##############################
        # CREATE MASK
        ##############################
        mask_surface.fill((0, 0, 0, 0))
        if len(vertices) > 2:
            pygame.draw.polygon(mask_surface, (255, 255, 255), vertices)
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (int(self.x), int(self.y)), self.size * 3)
        self.mask = pygame.mask.from_surface(mask_surface)
        self.mask = self.mask.overlap_mask(limit_circle_mask, (0, 0))

    @deprecated("This method is too expensive.")
    def draw_mask(self, surface):
        mask_surface = pygame.Surface((surface.get_height(), surface.get_height()), pygame.SRCALPHA)

        fill_mask(mask_surface, self.mask)
        surface.blit(mask_surface, (0, 0))

    @deprecated("This method is a debugging tool.")
    def draw_circle_and_line(self, surface, pos, origin_pos=None):
        if origin_pos is None:
            pygame.draw.line(surface, (0, 255, 0), (self.x, self.y), pos, 1)
            pygame.draw.circle(surface, (255, 0, 0), pos, 3)
        else:
            pygame.draw.line(surface, (0, 255, 0), origin_pos, pos, 1)
            pygame.draw.circle(surface, (255, 0, 0), pos, 3)

    @deprecated("This method is deprecated.")
    def draw_point_of_view(self, surface, corners):
        vertices = []
        for pair in corners:
            point1, point2 = pair
            vertices.append(point1)
            vertices.append(point2)
        pygame.draw.polygon(surface, PASTEL_RED, vertices)

    @deprecated("This method is a debugging tool.")
    def draw_path(self, surface, point_list, offset, point_size=1, point_color=(255, 0, 0)):
        for point in point_list:
            pygame.draw.circle(surface, point_color, point - offset, point_size)
