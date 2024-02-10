import sys
import pygame
from entities.enemy import Enemy
<<<<<<< Updated upstream
=======
from entities.player import Player
>>>>>>> Stashed changes
from map.grid import Grid
from utils.constants import *


# Define a function to start the game
def play_game():
    # Initialize pygame
    pygame.init()

<<<<<<< Updated upstream
    # Set up the game screen
    screen = pygame.display.set_mode((GRID_SIZE * SQUARE_SIZE, GRID_SIZE * SQUARE_SIZE))

    # Create a clock to control the frame rate
=======
    # Set the size of the window
    win_size = GRID_SIZE * SQUARE_SIZE

    screen = pygame.display.set_mode((win_size, win_size))
>>>>>>> Stashed changes
    clock = pygame.time.Clock()

    # Create the game grid
    grid = Grid(GRID_SIZE, screen)
<<<<<<< Updated upstream

    # Read the map data for the grid
    grid.read_map(MAP)

    # Create a list to hold enemy objects
    enemies = []
    # Spawn 5 enemies at random positions on the grid
=======
    grid.read_map(MAP)

    # Create the player entity
    player = Player(win_size // 2, win_size // 2, 1, grid, screen)

    # Create a list to hold enemy objects
    enemies = []
>>>>>>> Stashed changes
    for i in range(5):
        x, y = grid.get_random_node().get_pos()
        enemies.append(Enemy(x, y, 1, 0.5, grid, screen))

    # Flag to control the game loop
    running = True
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    # Game loop
    while running:
        # Event handling loop
        for event in pygame.event.get():
<<<<<<< Updated upstream
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
=======
            if event.type == pygame.QUIT:
                running = False
            """elif event.type == pygame.MOUSEMOTION:
                hover_node = grid.get_node(pygame.mouse.get_pos())
                grid.hover_over(hover_node)"""

        # Draw the game grid
        grid.draw()

        # Update and draw the player
        player.move(pygame.key.get_pressed())
        player.draw()

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    # Exit the Python interpreter
    sys.exit()
=======
    sys.exit()
>>>>>>> Stashed changes
