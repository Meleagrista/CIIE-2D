import sys
import pygame
import pygamepopup
from pygamepopup.components import InfoBox, Button
from pygamepopup.constants import BUTTON_SIZE
from pygamepopup.menu_manager import MenuManager

from entities.enemy import Enemy
from map.grid import Grid
from entities.player import Player
from utils.constants import *
from menu import main_menu


# Define a function to start the game
def play_game():
    # Initialize pygame and pygamepopup
    pygame.init()
    pygamepopup.init()
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
        enemies.append(Enemy(x, y, 1, 0.5, grid, screen))

    # Create the player entity
    player = Player(win_size // 2 - SQUARE_SIZE, win_size // 2 - SQUARE_SIZE, 1, grid, screen)

    # Flag to control the game loop
    running = True

    # Game loop
    while running and player.is_alive:
        # Event handling loop
        for event in pygame.event.get():
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

        # Update and draw each enemy
        for enemy in enemies:
            enemy.update()
            enemy.draw()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    if not player.is_alive:
        show_die_menu(screen, clock)

    else:
        # Quit pygame when the game loop exits
        pygame.quit()
        sys.exit()


def show_die_menu(screen, clock):
    menu_manager = MenuManager(screen)

    die_menu = InfoBox("You died",
                       [
                           [Button(
                               title="Go to main menu",
                               callback=lambda: main_menu(),
                               size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                           )],
                           [Button(
                               title="Restart",
                               callback=lambda: play_game(),
                               size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                           )],
                       ],
                       width=500,
                       has_close_button=False
                       )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    if not menu_manager.active_menu.is_position_inside(event.pos):
                        menu_manager.close_active_menu()
                    menu_manager.click(event.button, event.pos)

        menu_manager.open_menu(die_menu)
        menu_manager.display()
        pygame.display.update()
        clock.tick(FPS)


