import pygame

# TODO: Extact these into a constants file.
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Placeholder name")
        self.scene_stack = []
        self.scene_quit = False
        self.clock = pygame.time.Clock()

    def loop(self, scene):

        pygame.event.clear()

        self.scene_quit = False

        while not self.scene_quit:
            time = self.clock.tick(60)

            scene.events(pygame.event.get())
            scene.update(time)
            scene.draw(self.screen)

            pygame.display.flip()

    def run(self):
        while len(self.scene_stack) > 0:
            scene = self.scene_stack[len(self.scene_stack) - 1]
            self.loop(scene)

    def exit_scene(self):
        self.scene_quit = True
        if len(self.scene_stack) > 0:
            self.scene_stack.pop()

    def exit(self):
        self.scene_stack = []
        self.scene_quit = True

    def change_scene(self, scene):
        self.exit_scene()
        self.scene_stack.append(scene)

    def stack_scene(self, scene):
        self.scene_quit = True
        self.scene_stack.append(scene)
