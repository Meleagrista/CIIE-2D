import sys
import pygame
from entities.enemy import Enemy
from map.grid import Grid
from utils.constants import *


# Define a function to start the game
def play_game():
    # Initialize pygame
    pygame.init()

    # Set up the game screen
    screen = pygame.display.set_mode((GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE))

    # Create a clock to control the frame rate
    clock = pygame.time.Clock()

    # Create the game grid
    grid = Grid(GRID_SIZE, screen)

    # Read the map data for the grid
    grid.read_map(MAP)

    # Create a list to hold enemy objects
    enemies = []
    # Spawn 5 enemies at random positions on the grid
    for i in range(5):
        x, y = grid.get_random_node().get_pos()
        enemies.append(Enemy(x, y, 1, 0.5, grid, screen))

    # Flag to control the game loop
    running = True
    # Game loop
    while running:
        # Event handling loop
        for event in pygame.event.get():
            # Check if the user wants to quit the game
            if event.type == pygame.QUIT:
                running = False
            # Check for mouse motion events
            elif event.type == pygame.MOUSEMOTION:
                # Get the node over which the mouse is hovering
                hover_node = grid.get_node(pygame.mouse.get_pos())
                # Update the grid to show the hover effect
                grid.hover_over(hover_node)

        # Draw the game grid
        grid.draw()
        # Update and draw each enemy
        for enemy in enemies:
            enemy.update()
            enemy.draw()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    # Quit pygame when the game loop exits
    pygame.quit()
    # Exit the Python interpreter
    sys.exit()