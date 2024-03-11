import pygame

from managers.game_manager import GameManager
from utils.constants import FPS

from utils.enums import Controls as Ctl
from utils.paths.maps_paths import LEVELS


class SceneManager:
    def __init__(self, audio):
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

        self.levels = []
        self.set_levels(audio)
        self.menu_active = True

    def __str__(self):
        stack = ""
        for scene in self.scene_stack:
            attr = ""
            try:
                attr = "Level number " + str(scene.level.level_number)
            except AttributeError:
                attr = "Menu"

            stack += str(type(scene)) + ": " + attr + "\n"

        return "SceneManager with the following scene stack:\n" + stack

    def set_levels(self, audio):
        for level_number in LEVELS.keys():
            self.levels.append(GameManager(self, audio, level_number))

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
        # Debug
        # print("Running " + str(self))
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
            if self.menu_active:  # Check if either the menu or level 1 has to be appended to the stack
                self.menu_active = False
                self.scene_stack.append(self.levels[0])
            else:
                self.menu_active = True
                self.scene_stack.append(current_scene)  # Put the current scene at the end of the stack

            self.run()

    def stack_scene(self, scene):
        self.scene_stack.append(scene)

    def pop_scene(self):
        self.scene_stack.pop(0)

    def advance_level(self, next_level):
        # Debug
        # print("Changing to level ", next_level)
        # print(self)

        self.scene_stack.pop(1)
        self.scene_stack.append(self.levels[next_level-1])
        self.run()

    def go_to_menu(self):
        self.scene_stack = [self.scene_stack[0], self.scene_stack[1]]
        self.run()
