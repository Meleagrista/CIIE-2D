import random
import sys
import pygame
from map.grid import Grid
from entities.enemy import Enemy

# Define constants
GRID_SIZE = 35
SQUARE_SIZE = 20
FPS = 60

path_to_map = 'map/map-files/map-1.txt'

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE))
    pygame.display.set_caption("Game development")
    clock = pygame.time.Clock()
    grid = Grid(GRID_SIZE, screen)
    grid.create_array()
    grid.read_map(path_to_map)

    pos = (random.randint(0, GRID_SIZE * SQUARE_SIZE), random.randint(0, GRID_SIZE * SQUARE_SIZE))
    node = grid.get_node(pos)
    while node.is_barrier():
        pos = (random.randint(0, GRID_SIZE * SQUARE_SIZE), random.randint(0, GRID_SIZE * SQUARE_SIZE))
        node = grid.get_node(pos)

    print('Entity spawned in ' + str(pos))
    x, y = pos
    enemy = Enemy(x, y, 1, 0.5, grid, screen)

    dragging = False  # Flag to track if the left mouse button is being dragged
    resetting = False  # Flag to track if the right mouse button is being pressed
    """setting_terminal = False
    start_set = False
    end_set = False
    path_set = False"""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                hover_node = grid.get_node(pygame.mouse.get_pos())
                grid.hover_over(hover_node)

        grid.draw()
        enemy.update()
        enemy.dummy(enemy.end.get_pos())
        enemy.dummy(enemy.next_node.get_pos())
        enemy.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
