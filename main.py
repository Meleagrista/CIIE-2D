# from game.gamemanager import GameManager
from managers.game_manager import GameManager
from managers.menu_manager import MenuManager

import pygame

from utils.filepaths import MUSIC

if __name__ == "__main__":
    # game = GameManager()
    # game.run()
    pygame.init()

    manager = GameManager()
    menu_scene = MenuManager(manager)
    manager.stack_scene(menu_scene)

    pygame.mixer.init()

    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.play(-1)

    menu_scene.splash_screen(manager.screen, 10)

    manager.run()

    pygame.quit()

"""if __name__ == '__main__':
    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    escena = Menu(director)
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Inicialize the music mixer
    pygame.mixer.init()
    # Loads and reproduce music 
    pygame.mixer.music.load('assets/fall-from-grace.mp3')  # HAY QUE METER EL COPYRIGHT EN CREDITOS
    pygame.mixer.music.play(-1)  # -1 to infinity music
    # Ejecutamos la Splash Screen
    escena.splash_screen(director.screen, 10)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()"""
