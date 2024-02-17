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
from ui.menu import main_menu

PAUSE_MENU_ID = "pause_menu"
DIE_MENU_ID = "die_menu"


# Define a function to start the game
def play_game(movement_option):
    # Initialize pygame
    pygame.init()
    pygamepopup.init()
    clock = pygame.time.Clock()

    # Set the size of the window
    win_size = GRID_SIZE * SQUARE_SIZE
    screen = pygame.display.set_mode((win_size, win_size))

    # Initialize variables for the menus
    menu_manager = MenuManager(screen)
    pause_menu, die_menu = get_menus(movement_option)

    # Create the game grid
    grid = Grid(GRID_SIZE, screen)
    grid.read_map(MAP)

    # Create a list to hold enemy objects
    enemies = []
    for i in range(2):
        x, y = grid.get_random_node().get_pos()
        enemies.append(Enemy((x, y), 0.5, 1, grid, screen))

    # Create the player entity
    player = Player(win_size // 2 - SQUARE_SIZE, win_size // 2 - SQUARE_SIZE, 2, grid, screen)

    # Flag to control the game loop
    running = True

    # Game loop
    while running and player.is_alive:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu(menu_manager, pause_menu)
                    menu_loop(menu_manager, clock)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    menu_manager.click(event.button, event.pos)
        """elif event.type == pygame.MOUSEMOTION:
                        hover_node = grid.get_node(pygame.mouse.get_pos())
                        grid.hover_over(hover_node)"""

        # Draw the game grid
        grid.draw()

        # Update and draw the player
        player.move(pygame.key.get_pressed(), movement_option)
        player.draw()
        
        # Update and draw each enemy
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)

        # Update and draw the player
        player.move(pygame.key.get_pressed(), movement_option)
        player.draw()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    # If the player died, show the die menu
    if not player.is_alive:
        show_menu(menu_manager, die_menu)
        menu_loop(menu_manager, clock)

    # Quit pygame when the game loop exits
    else:
        pygame.quit()
        sys.exit()


def get_menus(movement_option):
    pause_menu = InfoBox("Pause menu",
                         [
                             [Button(
                                 title="Go to main menu",
                                 callback=lambda: main_menu(),
                                 size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                             )],
                             [Button(
                                 title="Restart",
                                 callback=lambda: play_game(movement_option),
                                 size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                             )],
                         ],
                         width=500,
                         close_button_text="Resume",
                         identifier=PAUSE_MENU_ID
                         )
    die_menu = InfoBox("You died",
                       [
                           [Button(
                               title="Go to main menu",
                               callback=lambda: main_menu(),
                               size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                           )],
                           [Button(
                               title="Restart",
                               callback=lambda: play_game(movement_option),
                               size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                           )],
                       ],
                       width=500,
                       has_close_button=False,
                       identifier=DIE_MENU_ID
                       )

    return pause_menu, die_menu


def show_menu(menu_manager, menu):
    # display a menu if it is not already open
    if menu_manager.active_menu is not None:
        if menu_manager.active_menu.identifier == menu.identifier:
            print("Given menu is already opened")
            return
        else:
            menu_manager.close_active_menu()
    menu_manager.open_menu(menu)


def menu_loop(menu_manager, clock):
    while menu_manager.active_menu is not None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEMOTION:
                menu_manager.motion(event.pos)  # Highlight buttons upon hover
            elif event.type == pygame.KEYDOWN and menu_manager.active_menu.identifier == PAUSE_MENU_ID:
                if event.key == pygame.K_ESCAPE:
                    menu_manager.close_active_menu()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    menu_manager.click(event.button, event.pos)
        menu_manager.display()
        pygame.display.update()
        clock.tick(FPS)
