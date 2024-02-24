from menu.prototypes.gui_prototypes import Button, ButtonSwitch
from game.utils.enums import Controls as Ctl

import pygame


class ButtonPlay(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, 'controller.png', (500, 50))

    def activate(self):
        self.screen.menu.run()


class ButtonConfiguration(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, 'config.png', (500, 90))

    def activate(self):
        self.screen.menu.show_configuration_screen()


class ButtonCredits(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, 'corona.png', (500, 130))

    def activate(self):
        self.screen.menu.show_credits_screen()


class ButtonExit(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, 'exit.png', (500, 170))

    def activate(self):
        self.screen.menu.exit()


class ButtonBackToMenu(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, 'return_pixel3.png', (520, 160))

    def activate(self):
        self.screen.menu.show_starting_screen()


class SwitchVolume(ButtonSwitch):
    def __init__(self, screen):
        ButtonSwitch.__init__(self, screen, 'switch_off.jpg', "switch_on.png", (500, 90), "On")

    def activate(self):
        # Cambiar el estado del interruptor
        if self.state == 'Off':
            pygame.mixer.music.set_volume(1.0)  # Max volume
            self.state = 'On'
            self.image = self.image_2
        else:
            pygame.mixer.music.set_volume(0.0)  # Mute
            self.state = 'Off'
            self.image = self.image_1


class SwitchController(ButtonSwitch):
    def __init__(self, screen):
        ButtonSwitch.__init__(self, screen, 'arrows.png', "wasd.png", (500, 130), "WASD")

    def activate(self):
        # global movement_option TODO: This shit needs to connect to somewhere.
        # Cambiar el estado del interruptor
        if self.state == 'Arrows':
            movement_option = Ctl.WASD
            self.state = 'WASD'
            self.image = self.image_2
        else:
            movement_option = Ctl.Arrows
            self.state = 'Arrows'
            self.image = self.image_1
