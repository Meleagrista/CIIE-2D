import sys
import pygame
from grid import Grid

# Define constants
GRID_SIZE = 35
SQUARE_SIZE = 20
FPS = 60

path_to_map = 'map-generation/map-files/map-1.txt'

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE))
    pygame.display.set_caption("Game development")
    clock = pygame.time.Clock()
    grid = Grid(GRID_SIZE, screen)
    grid.create_array()

    dragging = False  # Flag to track if the left mouse button is being dragged
    resetting = False  # Flag to track if the right mouse button is being pressed
    """setting_terminal = False
    start_set = False
    end_set = False
    path_set = False"""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    grid.read_map(path_to_map)

            elif event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button is pressed
                    dragging = True
                elif event.button == 2:  # Middle button pressed
                    setting_terminal = True
                elif event.button == 3:  # Right mouse button is pressed
                    resetting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button is released
                    dragging = False
                elif event.button == 2:  # Middle button released
                    setting_terminal = False
                elif event.button == 3:  # Right mouse button is released
                    resetting = False

            elif event.type == pygame.MOUSEMOTION:
                if not dragging and not resetting:  # Only update on motion if not dragging or resetting
                    hover_node = grid.get_node(pygame.mouse.get_pos())
                    grid.hover_over(hover_node)

        if dragging:
            clicked_node = grid.get_node(pygame.mouse.get_pos())
            if not clicked_node.is_border():
                clicked_node.make_barrier()

        if resetting:
            clicked_node = grid.get_node(pygame.mouse.get_pos())
            if not clicked_node.is_border() and not clicked_node.is_terminal():
                clicked_node.reset()

        """if setting_terminal:
            clicked_node = grid.get_node(pygame.mouse.get_pos())
            if start_set and end_set and clicked_node != path.get_end():
                path.substitute_path(clicked_node)
                path_set = False
            if not start_set:
                path.set_start(clicked_node)
                start_set = True
            if not end_set and clicked_node != path.get_start():
                path.set_end(clicked_node)
                end_set = True
            if start_set and end_set and not path_set:
                path.get_path(grid)
                path_set = True"""

        grid.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
