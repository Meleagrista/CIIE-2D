import pygame

from managers.game_manager import GameManager
from utils.constants import FPS

from utils.enums import Controls as Ctl


class SceneManager:
    def __init__(self):
        info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
        screen_width, screen_height = info.current_w, info.current_h

        # screen_width, screen_height = 800, 800

        window_width, window_height = screen_width - 30, screen_height - 90
        # window_width, window_height = 800, 800

        self.screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
        self.scene_stack = []
        self.clock = pygame.time.Clock()
        self.language = 'en'

        self.movement_option = Ctl.WASD

    def set_movement_option(self, option: Ctl):
        self.movement_option = option

    def set_language(self, language):
        self.language = language

    def get_movement_option(self):
        return self.movement_option

    def get_screen(self):
        return self.screen
    
    def get_language(self):
        return self.language

    def loop(self, scene):
        pygame.event.clear()

        while len(self.scene_stack) > 0:
            self.clock.tick(FPS)
            events = pygame.event.get()
            scene.events(events)
            scene.update(movement_option=self.movement_option)
            scene.draw(self.screen)

            pygame.display.flip()

    def run(self):
        if len(self.scene_stack) > 0:
            scene = self.scene_stack[len(self.scene_stack) - 1]
            if isinstance(scene, GameManager):
                scene.set_menus()
            self.loop(scene)
        else:
            self.loop(None)

    def exit(self):
        self.scene_stack = []
        self.run()

    def change_scene(self):
        if len(self.scene_stack) > 1:
            current_scene = self.scene_stack.pop(0)  # Remove the current scene from the beginning of the stack
            self.scene_stack.append(current_scene)  # Put the current scene at the end of the stack
            self.run()

    def stack_scene(self, scene):
        self.scene_stack.append(scene)
