import os
import pygame
import pygame_menu
from utils.constants import *
from utils.unicode import replace_accented_characters
from loop import play_game


# Function to start the game (placeholder)
def start_game():
    play_game()


# Function to handle difficulty change (placeholder)
def change_difficulty():
    pass


# Function to create a custom theme for menus
def create_theme(font_size, title_font_size, font_color):
    font_path = "assets/pixel.regular.ttf"
    my_font = pygame.font.Font(font_path, font_size)
    title_font = pygame.font.Font(font_path, title_font_size)

    # Load the image
    background_img_path = "assets/desert-pixel-placeholder.png"
    image = pygame.image.load(background_img_path)

    target_width = 800
    target_height = 600

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
    menu = pygame_menu.Menu("Credits", 800, 600, theme=create_theme(CREDITS_FONT, TITLE_FONT, FONT_COLOR))
    for label in labels.split('\n'):
        menu.add.label(label)
    return menu


# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Create the main menu
    menu = pygame_menu.Menu("Game Title", 800, 600, theme=create_theme(MENU_FONT, TITLE_FONT, FONT_COLOR))

    # Create the credits menu
    credits_menu = write_credits(replace_accented_characters(CREDITS))

    menu.add.button("Play", start_game)
    menu.add.button("Credits", credits_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)


if __name__ == "__main__":
    main()
