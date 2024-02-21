from pygamepopup.menu_manager import MenuManager
from pygamepopup.components import InfoBox, Button
from pygamepopup.constants import BUTTON_SIZE

from utils.enums import Controls as Ctl
from utils.constants import *

from entities.enemy import Enemy
from entities.player import Player
from map.grid import Grid

from camera import Camera

import sys
import pygame
import pygamepopup


def do_nothing():
    pass


class GameManager:
    def __init__(self, mov_opt=Ctl.WASD):
        pygame.init()
        pygamepopup.init()

        self.win_size = GRID_SIZE * SQUARE_SIZE
        self.win = pygame.display.set_mode((self.win_size, self.win_size))
        self.clock = pygame.time.Clock()

        self.player = None
        self.grid = Grid(GRID_SIZE, self.win)
        self.enemies = pygame.sprite.Group()
        self.all_sprites = Camera()

        self.start()
        self.death_counter = 0

        self.mv_opt = mov_opt
        self.menu_manager = MenuManager(self.win)
        self.pause_menu = None
        self.death_menu = None

        self.create_menus()

    def start(self):
        self.spawn_enemies()
        self.spawn_player()

    def restart(self):
        self.death_counter = 0
        if self.player is not None:
            self.remove_player(self.player)
        self.close_menu()
        self.start()
        self.run()

    def run(self):
        self.close_menu()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.open_menu(self.pause_menu)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        self.menu_manager.click(event.button, event.pos)

            self.update()
            self.draw()

            if self.detect_player():
                if self.death_counter >= LIFE * FPS:
                    self.remove_player(self.player)
                    self.open_menu(self.death_menu)
                else:
                    self.death_counter = self.death_counter + 1
            else:
                if self.death_counter > 0:
                    self.death_counter = self.death_counter - 1

            self.draw_bar()

            pygame.display.flip()
            self.clock.tick(FPS)

        self.end()

    @staticmethod
    def end():
        pygame.quit()
        sys.exit()

    # ####################################################################### #
    #                                  ENTITIES                               #
    # ####################################################################### #

    def spawn_player(self):
        center = self.win_size // 2 - SQUARE_SIZE
        player = Player(center, center, 2, self.grid, Ctl.WASD)
        self.add_player(player)

    def add_player(self, player):
        self.player = player
        player.add(self.all_sprites)

    def remove_player(self, player):
        self.player = None
        player.kill()

    def spawn_enemies(self):
        self.remove_all_enemies()
        for i in range(2):
            x, y = self.grid.get_random_node().get_pos()
            enemy = Enemy((x, y), 0.5, 1, self.grid, self.win)
            self.add_enemy(enemy)

    def add_enemy(self, enemy):
        enemy.add(self.all_sprites, self.enemies)

    @staticmethod
    def remove_enemy(enemy):
        enemy.kill()

    def remove_all_enemies(self):
        for enemy in self.enemies.sprites():
            enemy.kill()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        # TODO: Use native method when we incorporate Sprite images
        self.all_sprites.custom_draw(self.player, self.grid)

    def mask_vision(self):
        mask_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)
        substract_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)

        for enemy in self.enemies.sprites():
            vertices = []
            for pair in enemy.corners:
                point1, point2 = pair
                vertices.append(point1)
                vertices.append(point2)
            self.all_sprites.draw_mask(enemy, substract_surface, vertices, mask_surface)

        mask = pygame.mask.from_surface(mask_surface)
        subtract = pygame.mask.from_surface(substract_surface)
        mask = mask.overlap_mask(subtract, (0, 0))

        result_surface = mask.to_surface(setcolor=None, unsetcolor=(0, 0, 0, 100))

        self.win.blit(result_surface, (0, 0))
        return mask

    def detect_player(self):
        mask_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), self.player.rect)
        mask = pygame.mask.from_surface(mask_surface)
        enemy_sight = self.mask_vision()
        return self.all_sprites.mask_overlap(mask, enemy_sight)

    # ####################################################################### #
    #                             USER INTERFACE                              #
    # ####################################################################### #

    def draw_bar(self):
        bar_size = 3
        bar_width = self.player.size * 3
        bar_height = self.player.size * 0.5
        bar_percentage = round(self.death_counter / (LIFE * FPS), 2)
        bar_y = self.player.rect.y - self.player.size - bar_height
        bar_x = self.player.rect.x - bar_width/bar_size
        self.all_sprites.draw_bar((bar_x, bar_y), bar_width, bar_height, bar_percentage)

    def open_menu(self, menu):
        if self.menu_manager.active_menu is not None:
            if self.menu_manager.active_menu.identifier == menu.identifier:
                print("Given menu is already opened")
                return
            else:
                self.menu_manager.close_active_menu()
        self.menu_manager.open_menu(menu)
        self.run_menu()

    def close_menu(self):
        if self.menu_manager.active_menu is not None:
            self.menu_manager.close_active_menu()

    def run_menu(self):
        while self.menu_manager.active_menu is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.MOUSEMOTION:
                    self.menu_manager.motion(event.pos)  # Highlight buttons upon hover
                elif event.type == pygame.KEYDOWN and self.menu_manager.active_menu.identifier == PAUSE_MENU_ID:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_manager.close_active_menu()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        self.menu_manager.click(event.button, event.pos)
            self.menu_manager.display()
            pygame.display.update()
            self.clock.tick(FPS)

    def create_menus(self):
        pause_menu = InfoBox(
            "Pause menu",
            [
                [
                    Button(
                        title="Resume",
                        callback=lambda: self.run(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                    )
                ],
                [
                    Button(
                        title="Restart",
                        callback=lambda: self.restart(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                    )
                ],
                [
                    Button(
                        title="Go to main menu",
                        callback=lambda: self.end(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                    )
                ],
            ],
            width=500,
            has_close_button=False,
            identifier=PAUSE_MENU_ID
        )
        die_menu = InfoBox(
            "You died",
            [
                [
                    Button(
                        title="Restart",
                        callback=lambda: self.restart(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                    )
                ],
                [
                    Button(
                        title="Go to main menu",
                        callback=lambda: self.end(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1])
                    )
                ],
            ],
            width=500,
            has_close_button=False,
            identifier=DIE_MENU_ID
        )
        self.pause_menu = pause_menu
        self.death_menu = die_menu
