import math

import pygame

from square import Square

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Grid:
    def __init__(self, size, win):
        w, _ = win.get_size()
        self.gap = w // size
        self.size = size
        self.win = win
        self.font = pygame.font.SysFont('Arial', self.gap)
        self.nodes = []
        self.hover = None

    def create_array(self):
        self.nodes = []
        for i in range(self.size):
            self.nodes.append([])
            for j in range(self.size):
                node = Square(i, j, self.gap, self.size, self.size, 0)
                self.nodes[i].append(node)
        self.update()

    """def draw_grid(self):
        for i in range(self.size):
            pygame.draw.line(self.win, BLACK, (0, i * self.gap), (self.gap * self.size - 1, i * self.gap))
            for j in range(self.size):
                pygame.draw.line(self.win, BLACK, (j * self.gap, 0), (j * self.gap, self.gap * self.size - 1))"""

    def update(self):
        for row in self.nodes:
            for spot in row:
                spot.update_neighbors(self)
                spot.surrounding_barrier(self)

    def draw(self):
        self.win.fill((125, 125, 125))
        self.update()
        for row in self.nodes:
            for spot in row:
                spot.draw(self.win)
                if spot.is_border():
                    spot.make_barrier()

    def hover_over(self, node):
        if self.hover is not None:
            if not self.hover.is_border() and not self.hover.is_barrier() and not self.hover.is_terminal() and not self.hover.is_path():
                self.hover.reset()
        if not node.is_border() and not node.is_barrier() and not node.is_terminal() and not node.is_path():
            node.make_selected()
        self.hover = node

    def get_node(self, pos):
        y, x = pos
        row = math.floor(y / self.gap)
        col = math.floor(x / self.gap)
        return self.nodes[row][col]

    def read_map(self, full_file_path):
        with open(full_file_path, 'r') as file:
            file_content = file.read()
            file_content_without_newline = file_content.replace('\n', '')
            split_result = [char for char in file_content_without_newline]
            list_of_nodes = []
            for row in self.nodes:
                for node in row:
                    list_of_nodes.append(node)
            for character, node in zip(split_result, list_of_nodes):
                if character == 'X':
                    node.make_barrier()
                else:
                    node.reset()
        print("Map imported successfully.")
