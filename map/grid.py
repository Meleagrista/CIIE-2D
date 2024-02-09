import math
import os
import pygame

from map.square import Square

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
                elif character.isnumeric():
                    node.set_id(character)
                else:
                    node.reset()
        print("Map imported successfully.")


    def save_map(self, file_path):

        files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        # Extract the numbers from the filenames and find the maximum
        numbers = []
        for file in files:
            if file.startswith('map') and file.split('.')[0].split('-')[1].isdigit():
                numbers = [int(file.split('.')[0].split('-')[1])]
        if numbers:
            next_number = max(numbers) + 1
        else:
            next_number = 1

        # Open a file for writing
        with open(file_path + 'map-' + str(next_number) + '.txt', 'w') as file:
            # Write content to the file
            for row in self.nodes:
                for node in row:
                    if node.is_barrier():
                        file.write('X')
                    else:
                        print(chr(node.get_id()))
                        file.write(chr(node.get_id()))
                file.write('\n')

        print("Map exported successfully.")
