import os
import pygame
import pygame_menu
import time
from utils.constants import *
from utils.auxiliar import replace_accented_characters
import loop

movement_option = 'WASD'


# Function to start the game (placeholder)
def start_game():
    global movement_option
    pygame.mixer.music.stop()
    loop.play_game(movement_option)


# Function to handle difficulty change (placeholder)
def change_difficulty():
    pass


# Function for the Splash Screen
def splash_screen(screen, wait_seconds):
    # Get user screen size
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Loads the image
    splash_image = pygame.image.load("assets/splash_screen_placeholder.jpeg")
    splash_image = pygame.transform.scale(splash_image, (screen_width, screen_height))

    # Draws the splash screen image
    screen.blit(splash_image, (0, 0))

    # Updates the screen
    pygame.display.flip()

    # Waits until the user interacts (or the time ends)
    start_time = time.time()
    running = True
    while running and time.time() - start_time < wait_seconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

        # Limits to 60fps
        pygame.time.delay(1000 // 60)


# Function to create a custom theme for menus
def create_theme(font_size, title_font_size, font_color):
    font_path = "assets/pixel.regular.ttf"
    my_font = pygame.font.Font(font_path, font_size)
    title_font = pygame.font.Font(font_path, title_font_size)

    # Load the image
    background_img_path = "assets/desert-pixel-placeholder.png"
    image = pygame.image.load(background_img_path)

    # Get user screen size
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    target_width = screen_width
    target_height = screen_height

    # Define the new size for the image (e.g., half the original size)
    new_width = image.get_width() // (image.get_width() / target_width)
    new_height = image.get_height() // (image.get_height() / target_height)

    # Scale down the image
    scaled_image = pygame.transform.scale(image, (new_width, new_height))

    # Save the scaled image to a temporary file
    temp_img_path = "temp_scaled_image.png"
    pygame.image.save(scaled_image, temp_img_path)

    # Create a BaseImage with the scaled image path
    base_image = pygame_menu.BaseImage(temp_img_path, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER)

    # Remove the temporary file
    os.remove(temp_img_path)

    mytheme = pygame_menu.Theme(background_color=base_image, title_font=title_font,
                                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                                widget_font_color=font_color, widget_font=my_font, title_offset=(25, 25))
    return mytheme


# Function to create the credit's menu with given labels
def write_credits(labels):
    # Get user screen size
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    menu = pygame_menu.Menu("Credits", screen_width, screen_height,
                            theme=create_theme(CREDITS_FONT, TITLE_FONT, FONT_COLOR))
    for label in labels.split('\n'):
        menu.add.label(label)
    return menu


"""
SI NOS QUEDAMOS ESA CANCION HAY QUE INCLUIR LO SIGUIENTE EN LOS CREDITOS:

Fall From Grace by Darren Curtis | https://www.darrencurtismusic.com/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons CC BY 3.0
https://creativecommons.org/licenses/by/3.0/



"""


# Function that allows to change between WASD and Arrows movement
def change_movement_option(value, index):
    global movement_option
    movement_option = value
    print(f'User selected {value} at index {index}')


# Function that changes the volume
def change_volume(value):
    if value:
        pygame.mixer.music.set_volume(1.0)  # Max volume
    else:
        pygame.mixer.music.set_volume(0.0)  # Mute


# Main function
def main_menu():
    global movement_option

    pygame.init()

    # Inicialize the music mixer
    pygame.mixer.init()

    # Loads and reproduce music 
    pygame.mixer.music.load('assets/Fall-From-Grace(chosic.com).mp3')
    pygame.mixer.music.play(-1)  # -1 to infinity music

    # Get user screen size
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    splash_screen(screen, 10)

    # Create the main menu
    menu = pygame_menu.Menu("Game Title", screen_width, screen_height,
                            theme=create_theme(MENU_FONT, TITLE_FONT, FONT_COLOR))

    # Create the credits menu
    credits_menu = write_credits(replace_accented_characters(CREDITS))

    # Create the controls menu
    controls_menu = pygame_menu.Menu("Settings", screen_width, screen_height,
                                     theme=create_theme(MENU_FONT, TITLE_FONT, FONT_COLOR))
    controls_menu.add.selector('Player movement: ', [('WASD', 1), ('Arrows', 2)], onchange=change_movement_option)
    controls_menu.add.toggle_switch('Volume:', True, onchange=change_volume,
                                    state_color=((255, 78, 69), (183, 255, 115)), slider_thickness=10)
    # controls_menu.add.selector('Volume :', ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], onchange=change_volume)

    menu.add.button("Play", start_game)
    menu.add.button("Settings", controls_menu)
    menu.add.button("Credits", credits_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)


if __name__ == "__main__":
    main_menu()
