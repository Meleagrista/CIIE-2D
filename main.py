import pygamepopup
import pygame

from managers.game_manager import GameManager
from managers.scene_manager import SceneManager
from managers.menu_manager import MenuManager
from utils.filepaths import MUSIC

if __name__ == "__main__":
    pygame.init()
    pygamepopup.init()

    manager = SceneManager()
    game_scene = GameManager(manager)
    manager.stack_scene(game_scene)
    menu_scene = MenuManager(manager)
    manager.stack_scene(menu_scene)

    pygame.mixer.init()

    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.play(-1)

    menu_scene.splash_screen(manager.screen, 10)

    manager.run()

    pygame.quit()
