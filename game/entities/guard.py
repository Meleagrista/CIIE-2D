import math

from game.entities.enemy import Enemy
from game.map.grid import Grid
from utils.constants import ORANGE, GREEN, RED


class Guard(Enemy):
    def notified(self, player):
        if player.detected():
            self.following = True
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)
            if distance <= self.ray_radius + player.size:
                self._status = RED
            elif distance <= (self.ray_radius + player.size) * 2:
                self._status = ORANGE
            else:
                self._status = GREEN

            last_position = self.grid.get_node((player.x, player.y))

            if not self.last_seen:
                self.chase(last_position)
            if self.last_seen and (self.last_seen.get_pos() - last_position.get_pos() > 2):
                self.last_seen.append(last_position)
                self.investigate()

    def chase(self, objective):
        self.chasing = True
        self.chase_position = objective
        self.update()

    def investigate(self):
        if not self.last_seen:
            self.investigating = False
            self.set_path(self.end_node)
            self.update()
            return
        self.chasing = False
        self.investigating = True
        self.set_path(self.last_seen.pop())
        self.update()
