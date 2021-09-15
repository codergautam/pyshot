import math
import pygame
class Bullet:
    def __init__(self, x, y, player, px=False, py=False):
        self.pos = (x, y)
        self.player = player
        if player:
            mx, my = pygame.mouse.get_pos()
        else:
            mx, my = px, py
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((10, 4)).convert_alpha()
        if player:
            self.bullet.fill((51, 230, 255))
        else:
            self.bullet.fill((255, 51, 51))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        try:
            self.speed = 600 / clock.get_fps()
        except:
            self.speed = 10

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center=self.pos)
        surf.blit(self.bullet, bullet_rect)
