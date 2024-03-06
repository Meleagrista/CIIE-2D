import json
import pygame
from pygamepopup.components import InfoBox, Button
from pygamepopup.constants import BUTTON_SIZE
from pygamepopup.menu_manager import MenuManager
from typing_extensions import deprecated

from game.groups.interface_group import Interface
from game.groups.render_group import Camera
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.groups.enemies_group import Enemies
from game.map.grid import Grid
from game.map.level import Level
from game.ui.ui_bar import Bar
from game.ui.ui_keys import Keys
from game.ui.ui_text import Message
from managers.prototypes.scene_prototype import Scene
from utils.constants import *
from utils.assets_paths import FONT, POPUP_IMAGE_PAUSE, POPUP_IMAGE_DEATH
from utils.maps_paths import LEVEL_1


class GameManager(Scene):
    def __init__(self, manager, audio):
        Scene.__init__(self, manager)

        self.win = pygame.display.get_surface()
        self.win_size = self.win.get_width()

        # Read level
        with open(LEVEL_1, 'r') as file:
            data = file.read().replace('\n', '')

        # j = json.loads(data)
        self.level = Level(**json.loads(data))

        self.player = None
        self.grid = Grid(
            size=100,
            win=self.win,
            map_path=self.level.map.border_map_path,
            tile_map_path=self.level.map.tile_map_path,
            sprite_sheet_path=self.level.level_sprite_sheet.path,
            ss_columns=self.level.level_sprite_sheet.columns,
            ss_rows=self.level.level_sprite_sheet.rows

        )

        self.grid.set_spawn_square(self.level.coordinates.player_initial_x, self.level.coordinates.player_initial_y)
        self.enemies = Enemies()
        self.all_sprites = Camera()
        self.interface = Interface()

        self.audio = audio

        self._start()

        self._set_interface()

        self.grid.set_key_square(self.level.coordinates.key_x, self.level.coordinates.key_y)
        self.grid.set_exit_square(self.level.coordinates.exit_x, self.level.coordinates.exit_y)

        self.menu_manager = MenuManager(self.win)
        self._set_menus()

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
        self.all_sprites.draw(player=self.player, grid=self.grid)
        self.interface.draw(surface=screen)

        if self.is_open_menu():
            self.menu_manager.display()

        pygame.display.update()

    def update(self, **kwargs):
        # self.all_sprites.update(**kwargs)
        if not self.is_open_menu():
            kwargs['player_mask'] = self.all_sprites.player_mask(self.player)
            kwargs['enemy_mask'] = self._render()
            kwargs['language'] = self.manager.get_language()
            self.all_sprites.update(**kwargs)
            self.interface.update(**kwargs)

    def notified(self):
        if self.player.detected():
            self.audio.play_detected()
        else:
            self.audio.stop_detected()

        if not self.player.alive():  # Player has died
            self.audio.play_death()
            self.open_menu(self.death_menu)

        if self.player.in_door():  # Player has reached the end
            if self.player.has_key():
                self.audio.play_finish()
                self.exit()

        if self.player.has_key() and self.player.interacted_key():
            self.audio.play_key()

        if self.player.moving():
            self.audio.play_movement()
        else:
            self.audio.stop_movement()

        if self.player.recovering():
            self.audio.play_recovering()
        else:
            self.audio.stop_recovering()

    # ####################################################################### #
    #                               CLASS METHODS                             #
    # ####################################################################### #

    def exit(self):
        self.manager.exit()

    def _close(self):
        self._restart()
        self.audio.music_menu()
        self.manager.change_scene()

    def _start(self):
        self._spawn_player()
        # self._spawn_enemies()

    def _resume(self):
        self.close_menu()

    def _restart(self):
        if self.player is not None:
            self._remove_player(self.player)
        self.enemies.remove_all()
        self.close_menu()
        self._start()

    # ####################################################################### #
    #                                  ENTITIES                               #
    # ####################################################################### #

    def _render(self):
        mask_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)
        subtract_surface = pygame.Surface((self.win_size, self.win_size), pygame.SRCALPHA)

        for enemy in self.enemies.sprites():
            vertices = []
            for pair in enemy.corners:
                point1, point2 = pair
                vertices.append(point1)
                vertices.append(point2)
            self.all_sprites.enemy_mask(enemy, subtract_surface, vertices, mask_surface)

        mask = pygame.mask.from_surface(mask_surface)
        subtract = pygame.mask.from_surface(subtract_surface)
        mask = mask.overlap_mask(subtract, (0, 0))

        self.all_sprites.surface_mask = mask

        return self.all_sprites.surface_mask

    def _add_player(self, player):
        self.player = player
        player.add(self.all_sprites)

    def _remove_player(self, player):
        player.kill()
        self.player = None

    def _spawn_player(self):
        x, y = self.grid.spawn.get_pos()
        player = Player(x, y, SPEED, self.grid)

        self._add_player(player)
        self.enemies.set_player(self.player)
        self.interface.set_player(self.player)

        self.player.add_observer(self)
        self.player.add_observer(self.enemies)
        self.player.add_observer(self.interface)

    def _spawn_enemies(self):
        enemies = self.enemies.spawn(self.grid, self.win, self.level.enemies_zones)
        for enemy in enemies:
            self.enemies.introduce(enemy, self.all_sprites, self.enemies)

    # ####################################################################### #
    #                             MENU METHODS                                #
    # ####################################################################### #

    def is_open_menu(self):
        return self.menu_manager.active_menu is not None

    def open_menu(self, menu):
        self.close_menu()
        self.menu_manager.open_menu(menu)

    def close_menu(self):
        self.menu_manager.close_active_menu()

    def _set_menus(self):
        pause_menu = InfoBox(
            "",
            [
                [
                    Button(
                        title="RESUME",
                        callback=lambda: self._resume(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1]),
                        text_hover_color=PURPLE,
                        font=pygame.font.Font(FONT, 16),
                        no_background=True
                    )
                ],
                [
                    Button(
                        title="RESTART",
                        callback=lambda: self._restart(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1]),
                        text_hover_color=PURPLE,
                        font=pygame.font.Font(FONT, 16),
                        no_background=True
                    )
                ],
                [
                    Button(
                        title="MAIN MENU",
                        callback=lambda: self._close(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1]),
                        text_hover_color=PURPLE,
                        font=pygame.font.Font(FONT, 16),
                        no_background=True
                    )
                ],
            ],
            width=300,
            has_close_button=False,
            identifier=PAUSE_MENU_ID,
            background_path=POPUP_IMAGE_PAUSE
        )
        die_menu = InfoBox(
            "",
            [
                [
                    Button(
                        title="RESTART",
                        callback=lambda: self._restart(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1]),
                        text_hover_color=PURPLE,
                        font=pygame.font.Font(FONT, 16),
                        no_background=True
                    )
                ],
                [
                    Button(
                        title="MAIN MENU",
                        callback=lambda: self._close(),
                        size=(BUTTON_SIZE[0], BUTTON_SIZE[1]),
                        text_hover_color=PURPLE,
                        font=pygame.font.Font(FONT, 16),
                        no_background=True
                    )
                ],
            ],
            width=300,
            has_close_button=False,
            identifier=DIE_MENU_ID,
            background_path=POPUP_IMAGE_DEATH
        )
        self.pause_menu = pause_menu
        self.death_menu = die_menu

    def _set_interface(self):
        bar = Bar(self.win)
        bar.add(self.interface)
        message = Message(self.win)
        message.add(self.interface)
        keys_box = Keys(self.win)
        keys_box.add(self.interface)

    # ####################################################################### #
    #                                DEPRECATED                               #
    # ####################################################################### #

    @deprecated("This method has been replaced")
    def _force_spawn_enemies(self):
        self._remove_all_enemies()

        # Generar 2 guardias (entidad asociada a varias zonas)
        x, y = self.grid.get_random_node_from_zones([1, 2]).get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [1, 2])
        self._add_enemy(enemy)

        x, y = self.grid.get_random_node_from_zones([2, 3]).get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [2, 3])
        self._add_enemy(enemy)

        # Generar 1 científico (entidad asociada a una única zona)
        x, y = self.grid.get_random_node_from_zones([3]).get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [3])
        self._add_enemy(enemy)

        # Generar 1 explorador (entidad que puede recorrer cualquier zona)
        x, y = self.grid.get_random_node().get_pos()
        enemy = Enemy((x, y), 0.5, 1, self.grid, self.win, [])
        self._add_enemy(enemy)

    @deprecated("This method has been replaced")
    def _add_enemy(self, enemy):
        enemy.add(self.all_sprites, self.enemies)

    @deprecated("This method has been replaced")
    def _remove_enemy(self, enemy=None):
        if enemy:
            enemy.kill()
        else:
            self._remove_all_enemies()

    @deprecated("This method has been replaced")
    def _remove_all_enemies(self):
        for enemy in self.enemies.sprites():
            enemy.kill()
