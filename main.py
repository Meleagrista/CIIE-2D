import pygamepopup
import pygame
import pygame, os

from managers.audio_manager import AudioManager
from managers.game_manager import GameManager
from managers.scene_manager import SceneManager
from managers.menu_manager import MenuManager
from utils.filepaths import MUSIC_FALL_FROM_GRACE, MUSIC_MEDIEVAL

os.environ['SDL_VIDEO_CENTERED'] = '1'  # You have to call this before pygame.init()

if __name__ == "__main__":

    pygame.init()
    pygamepopup.init()

    manager = SceneManager()
    audio = AudioManager()
    game_scene = GameManager(manager, audio)
    manager.stack_scene(game_scene)
    menu_scene = MenuManager(manager, audio)
    manager.stack_scene(menu_scene)

    menu_scene.splash_screen(manager.screen, 10)

    audio.music_menu()

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
    
    
    Black Silent Fear by Magnetic Trailer | https://lesfm.net/
    Music promoted by https://www.chosic.com/free-music/all/
    Creative Commons CC BY 3.0
    https://creativecommons.org/licenses/by/3.0/
 

"""

