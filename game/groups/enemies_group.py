import pygame

from game.entities.enemy import Enemy


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
            x, y = grid.get_random_node_from_zones(zones).get_pos()
            enemy = Enemy((x, y), 0.5, 1, grid, win, zones)
            enemies.append(enemy)

        # # Generar 2 guardias (entidad asociada a varias zonas)
        # x, y = grid.get_random_node_from_zones([1, 2]).get_pos()
        # enemy = Enemy((x, y), 0.5, 1, grid, win, [1, 2])
        #
        # enemies.append(enemy)
        #
        # x, y = grid.get_random_node_from_zones([2, 3]).get_pos()
        # enemy = Enemy((x, y), 0.5, 1, grid, win, [2, 3])
        #
        # enemies.append(enemy)
        #
        # # Generar 1 científico (entidad asociada a una única zona)
        # x, y = grid.get_random_node_from_zones([3]).get_pos()
        # enemy = Enemy((x, y), 0.5, 1, grid, win, [3])
        #
        # enemies.append(enemy)
        #
        # # Generar 1 explorador (entidad que puede recorrer cualquier zona)
        # x, y = grid.get_random_node().get_pos()
        # enemy = Enemy((x, y), 0.5, 1, grid, win, [])
        #
        # enemies.append(enemy)

        return enemies
