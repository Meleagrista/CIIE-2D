import pygame
import pygame_menu

def start_game():
    pass

def change_difficulty():
    pass

#Creamos el tema que vamos a usar para el menu
def my_theme(font_size, title_font_size, font_color):
    #Cargamos la fuente a usar
    font_path = "assets/Crang.ttf"
    my_font = pygame.font.Font(font_path, font_size)

    #Elegimos la fuente para el título
    title_font = pygame.font.Font(font_path, title_font_size)

    #Cargamos la imagen de background
    img_bg_path = "assets/background_placeholder.jpg"
    background_img = pygame_menu.BaseImage(image_path=img_bg_path, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER)


    mytheme = pygame_menu.Theme(background_color = background_img, title_font = title_font,
                                title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE,
                                widget_font_color = font_color, widget_font = my_font, title_offset = (25,25))


    return mytheme



def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    menu = pygame_menu.Menu("Game Title", 800, 600, theme=my_theme(30,42,"white"),)

    menu.add.button("Play", start_game)
    """ menu.add.dropselect('Difficulty', ['Easy', 'Medium', 'Hard'], placeholder = "Select", 
                        selection_option_font_size = 10, onchange=change_difficulty) """

    credits_menu = pygame_menu.Menu("Credits", 800, 600, theme=my_theme(20,42, "white"))

    credits_menu.add.label("Contornos Inmersivos, Interactivos e de Entretemento")
    credits_menu.add.label("Grao en Enxenería Informática")
    credits_menu.add.label("Universidade da Coruña")

    credits_menu.add.label("Authors:")
    credits_menu.add.label("Martín do Río Rico")
    credits_menu.add.label("Yago Fernández Rego")
    credits_menu.add.label("David García Ramallal")
    credits_menu.add.label("Pelayo Vieites Pérez")


    menu.add.button("Credits", credits_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(screen)


if __name__ == "__main__":
    main()
