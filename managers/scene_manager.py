import pygame

from utils.constants import FPS
from utils.enums import Controls as Ctl

# TODO: Extract these into a constants file.
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


class SceneManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
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
