import pygamepopup
import pygame

from managers.game_manager import GameManager
from managers.scene_manager import SceneManager
from managers.menu_manager import MenuManager
from utils.filepaths import MUSIC_FALL_FROM_GRACE, MUSIC_MEDIEVAL

if __name__ == "__main__":
    pygame.init()
    pygamepopup.init()

    manager = SceneManager()
    game_scene = GameManager(manager)
    manager.stack_scene(game_scene)
    menu_scene = MenuManager(manager)
    manager.stack_scene(menu_scene)

    # parametros: frecuencia, nº bits (calidad), mono(1)/estereo(2), buffer
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()

    pygame.mixer.music.load(MUSIC_FALL_FROM_GRACE)
    # play(-1) -> infinity
    pygame.mixer.music.play(-1)

    menu_scene.splash_screen(manager.screen, 10)

    pygame.mixer.music.stop()

    # parametros: frecuencia, nº bits (calidad), mono(1)/estereo(2), buffer
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()

    pygame.mixer.music.load(MUSIC_MEDIEVAL)
    # play(-1) -> infinity
    pygame.mixer.music.play(-1)

    manager.run()

    pygame.quit()




"""
    Fall From Grace by Darren Curtis | https://www.darrencurtismusic.com/
    Music promoted by https://www.chosic.com/free-music/all/
    Creative Commons CC BY 3.0
    https://creativecommons.org/licenses/by/3.0/



    Medieval Fantasy by MaxKoMusic | https://maxkomusic.com/
    Music promoted by https://www.chosic.com/free-music/all/
    Creative Commons CC BY-SA 3.0
    https://creativecommons.org/licenses/by-sa/3.0/

"""

