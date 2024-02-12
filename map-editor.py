import sys

import pygame

from map.gridOld import Grid

# Define constants
GRID_SIZE = 35
SQUARE_SIZE = 20
FPS = 60

path_to_folder = 'map/files/'
path_to_map = 'map/files/map-1.txt'

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE))
    pygame.display.set_caption("Map editor")
    clock = pygame.time.Clock()
    grid = Grid(GRID_SIZE, screen)
    grid.create_array()

    dragging = False    # Flag to track if the left mouse button is being dragged
    resetting = False   # Flag to track if the right mouse button is being pressed
    room = 0            # Room to be set

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    grid.save_map(path_to_folder)
                elif event.key == pygame.K_r:
                    grid.read_map(path_to_map)
                elif event.unicode.isdigit():
                    room = int(event.unicode)

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button is pressed
                    dragging = True
                elif event.button == 3:  # Right mouse button is pressed
                    resetting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button is released
                    dragging = False
                elif event.button == 3:  # Right mouse button is released
                    resetting = False

            elif event.type == pygame.MOUSEMOTION:
                if not dragging and not resetting:  # Only update on motion if not dragging or resetting
                    hover_node = grid.get_node(pygame.mouse.get_pos())

        if dragging:
            clicked_node = grid.get_node(pygame.mouse.get_pos())
            if room == 0:
                if not clicked_node.is_border():
                    clicked_node.make_barrier()
            else:
                if not clicked_node.is_border():
                    clicked_node.set_id(room)

        if resetting:
            clicked_node = grid.get_node(pygame.mouse.get_pos())
            if not clicked_node.is_border() and not clicked_node.is_terminal():
                clicked_node.reset()

        grid.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
