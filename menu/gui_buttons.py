from menu.prototypes.gui_prototypes import Button, ButtonSwitch
from utils.enums import Controls as Ctl
from utils.filepaths import *

import pygame


class ButtonPlay(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, BUTTON_PLAY, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.40))

    def activate(self):
        self.screen.menu.run()


class ButtonConfiguration(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, BUTTON_CONFIGURATION, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.50))

    def activate(self):
        self.screen.menu.show_configuration_screen()


class ButtonCredits(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, BUTTON_CREDITS, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.60))

    def activate(self):
        self.screen.menu.show_credits_screen()


class ButtonExit(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, BUTTON_EXIT, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.70))

    def activate(self):
        self.screen.menu.exit()


class ButtonBackToMenu(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, BUTTON_BACK, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.80))

    def activate(self):
        self.screen.menu.show_starting_screen()


class SwitchVolume(ButtonSwitch):
    def __init__(self, screen):
        ButtonSwitch.__init__(self, screen, SWITCH_OFF, SWITCH_ON, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.60), "On")

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
        ButtonSwitch.__init__(self, screen, BUTTON_ARROWS, BUTTON_WASD, (pygame.display.Info().current_w * 0.35, pygame.display.Info().current_h * 0.40), "WASD")

    def activate(self):
        # Cambiar el estado del interruptor
        if self.state == 'Arrows':
            self.screen.menu.set_movement_option(Ctl.WASD)
            self.state = 'WASD'
            self.image = self.image_2
        else:
            self.screen.menu.set_movement_option(Ctl.Arrows)
            self.state = 'Arrows'
            self.image = self.image_1
