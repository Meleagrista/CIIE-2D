import pygame

from game.entities.enemies.guard import Guard


class Enemies(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._player = None

    def set_player(self, player):
        self._player = player

    def notified(self):
        if self._player.detected():
            for sprite in self.sprites():
                sprite.notified(self._player)

    @staticmethod
    def introduce(enemy, *groups):
        enemy.add(*groups)

    def remove(self, enemy=None):
        if enemy:
            enemy.kill()
        else:
            self.remove_all()

    def remove_all(self):
        if len(self.sprites()) > 0:
            for enemy in self.sprites():
                enemy.kill()

    def spawn(self, grid, win, enemies_zones):
        self.remove_all()

        enemies = []

        for zones in enemies_zones:
            if len(zones) > 0:
                initial_zone = zones[0]
            else:
                initial_zone = None
            x, y = grid.get_random_node_from_zone(initial_zone).get_pos()
            enemy = Guard((x, y), 1, 3, grid, win, zones)
            enemies.append(enemy)

        return enemies
