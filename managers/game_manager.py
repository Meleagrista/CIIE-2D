import pygame
from pygamepopup.components import InfoBox, Button
from pygamepopup.constants import BUTTON_SIZE
from pygamepopup.menu_manager import MenuManager

from game.groups.camera import Camera
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.map.grid import Grid
from managers.prototypes.scene_prototype import Scene
from utils.constants import *


class GameManager(Scene):
    def __init__(self, manager):
        Scene.__init__(self, manager)

        self.win_size = GRID_SIZE * SQUARE_SIZE
        self.win = pygame.display.set_mode((self.win_size, self.win_size))

        self.player = None
        self.grid = Grid(GRID_SIZE, self.win)
        self.enemies = pygame.sprite.Group()
        self.all_sprites = Camera()

        self.start()
        self.death_counter = 0

        self.menu_manager = MenuManager(self.win)
        self.pause_menu = None
        self.death_menu = None

        self.create_menus()

    def events(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                self.exit()
            elif self.is_open_menu():
                if event.type == pygame.MOUSEMOTION:
                    self.menu_manager.motion(event.pos)  # Highlight buttons upon hover
                elif event.type == pygame.KEYDOWN and self.menu_manager.active_menu.identifier == PAUSE_MENU_ID:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_manager.close_active_menu()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        self.menu_manager.click(event.button, event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.open_menu(self.pause_menu)

    def draw(self, screen):
        # TODO: Use native method when we incorporate Sprite deprecated_images
        self.all_sprites.draw(screen, player=self.player, grid=self.grid)
        self.draw_bar()

        if self.is_open_menu():
            self.menu_manager.display()

        pygame.display.update()

    def update(self, **kwargs):
        if not self.is_open_menu():
            self.all_sprites.update(**kwargs)

            if self.detect_player():
                if self.death_counter >= LIFE * FPS:
                    self.open_menu(self.death_menu)
                else:
                    self.death_counter = self.death_counter + 1
            else:
                if self.death_counter > 0:
                    self.death_counter = self.death_counter - 1

    # ####################################################################### #
    #                               CLASS METHODS                             #
    # ####################################################################### #

    def exit(self):
        self.manager.exit()

    def close(self):
        self.restart()
        self.manager.change_scene()

    def start(self):
        self.spawn_enemies()
        self.spawn_player()

    def resume(self):
        self.close_menu()

    def restart(self):
        self.death_counter = 0
        if self.player is not None:
            self.remove_player(self.player)
        self.close_menu()
        self.start()

    # ####################################################################### #
    #                                  ENTITIES                               #
    # ####################################################################### #

    def add_player(self, player):
        self.player = player
        player.add(self.all_sprites)

    def remove_player(self, player):
        self.player = None
        player.kill()

    def spawn_player(self):
        center = self.win_size // 2 - SQUARE_SIZE
        player = Player(center, center, 2, self.grid)
        self.add_player(player)

    def add_enemy(self, enemy):
        enemy.add(self.all_sprites, self.enemies)

    def remove_enemy(self, enemy=None):
        if enemy is None:
            self.remove_all_enemies()
        else:
            enemy.kill()

    def remove_all_enemies(self):
        for enemy in self.enemies.sprites():
            enemy.kill()

    def spawn_enemies(self):
        self.remove_all_enemies()

        # Generar 2 guardias (entidad asociada a varias zonas)
        x, y = self.grid.get_random_node_from_zones([1, 2]).get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [1, 2])
        self.add_enemy(enemy)

        x, y = self.grid.get_random_node_from_zones([2, 3]).get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [2, 3])
        self.add_enemy(enemy)

        # Generar 1 científico (entidad asociada a una única zona)
        x, y = self.grid.get_random_node_from_zones([3]).get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [3])
        self.add_enemy(enemy)

        # Generar 1 explorador (entidad que puede recorrer cualquier zona)
        x, y = self.grid.get_random_node().get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [])
        self.add_enemy(enemy)

    def mask_vision(self):
        mask_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)
        subtract_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)

        for enemy in self.enemies.sprites():
            vertices = []
            for pair in enemy.corners:
                point1, point2 = pair
                vertices.append(point1)
                vertices.append(point2)
            self.all_sprites.mask_update(enemy, subtract_surface, vertices, mask_surface)

        mask = pygame.mask.from_surface(mask_surface)
        subtract = pygame.mask.from_surface(subtract_surface)
        mask = mask.overlap_mask(subtract, (0, 0))

        result_surface = mask.to_surface(setcolor=None, unsetcolor=(0, 0, 0, 100))

        self.all_sprites.mask_draw(result_surface)
        return mask

    def detect_player(self):
        mask_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), self.player.rect)
        mask = pygame.mask.from_surface(mask_surface)
        enemy_sight = self.mask_vision()
        return self.all_sprites.mask_overlap(mask, enemy_sight)

    # ####################################################################### #
    #                             BAR METHODS                                 #
    # ####################################################################### #

    def draw_bar(self):
        bar_size = 3
        bar_width = self.player.size * 3
        bar_height = self.player.size * 0.5
        bar_percentage = round(self.death_counter / (LIFE * FPS), 2)
        bar_y = self.player.rect.y - self.player.size - bar_height
        bar_x = self.player.rect.x - bar_width/bar_size
        self.all_sprites.draw_bar((bar_x, bar_y), bar_width, bar_height, bar_percentage)

    # ####################################################################### #
    #                             MENU METHODS                                #
    # ####################################################################### #

    def is_open_menu(self):
        return self.menu_manager.active_menu is not None

    def open_menu(self, menu):
        if self.is_open_menu():
            if self.menu_manager.active_menu.identifier == menu.identifier:
                print("Given menu is already opened.")
                self.menu_manager.close_active_menu()
            else:
                self.menu_manager.close_active_menu()
        self.menu_manager.open_menu(menu)

    def close_menu(self):
        if self.is_open_menu():
            self.menu_manager.close_active_menu()

    def create_menus(self):
        pause_menu = InfoBox(
            "Pause menu",
            [
                [
                    Button(
                        title="Resume",
                        callback=lambda: self.resume(),
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
                        callback=lambda: self.close(),
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
                        callback=lambda: self.close(),
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
