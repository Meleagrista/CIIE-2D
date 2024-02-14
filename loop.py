import sys
import pygame
from entities.enemy import Enemy
from map.grid import Grid
from entities.player import Player
from utils.constants import *


# Define a function to start the game
def play_game():
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set the size of the window
    win_size = GRID_SIZE * SQUARE_SIZE
    screen = pygame.display.set_mode((win_size, win_size))

    # Create the game grid
    grid = Grid(GRID_SIZE, screen)
    grid.read_map(MAP)

    # Create a list to hold enemy objects
    enemies = []
    for i in range(5):
        x, y = grid.get_random_node().get_pos()
        enemies.append(Enemy(x, y, 0.5, 1, grid, screen))

    # Create the player entity
    player = Player(win_size // 2 - SQUARE_SIZE, win_size // 2 - SQUARE_SIZE, 2, grid, screen)

    # Flag to control the game loop
    running = True
    # Game loop
    while running:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            """elif event.type == pygame.MOUSEMOTION:
                hover_node = grid.get_node(pygame.mouse.get_pos())
                grid.hover_over(hover_node)"""

        # Draw the game grid
        grid.draw()

        # Update and draw each enemy
        for enemy in enemies:
            enemy.update()
            enemy.cast()

        # Update and draw each enemy
        for enemy in enemies:
            enemy.draw()

        # Update and draw the player
        player.move(pygame.key.get_pressed())
        player.draw()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    # Quit pygame when the game loop exits
    pygame.quit()
    sys.exit()
