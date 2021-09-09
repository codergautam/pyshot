# GitHub:
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_rotate_towards_target.md
#
# Stack Overflow:
# https://stackoverflow.com/questions/58603835/how-to-rotate-an-imageplayer-to-the-mouse-direction/58604116#58604116

import math
import pygame
import os
import random


pygame.init()
window = pygame.display.set_mode((1280, 720))
player = pygame.transform.smoothscale(pygame.image.load("square.png").convert_alpha(), (100, 100))
    
class Enemy:
    def __init__(self):
        self.pos  = (random.randint(50, 1230),random.randint(50,680))
        self.enemy = pygame.transform.smoothscale(pygame.image.load("enemy.png").convert_alpha(), (50, 50))
        
    def isColliding(self,point):
        return self.rect.collidepoint(point)
    def update():
       
        pass
    def draw(self, px, py):
        correction_angle = 0
        enemy_pos = window.get_rect().center
        enemy_rect = player.get_rect(center=enemy_pos)

        enemy_rect.left = self.pos[0]
        enemy_rect.top = self.pos[1]
        
        #px, py = player x player y
        dx, dy = px - enemy_rect.centerx, py - enemy_rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

        rot_image = pygame.transform.rotate(self.enemy, angle)
        rot_image_rect = rot_image.get_rect(center=enemy_rect.center)
        self.rect = rot_image_rect

        window.blit(rot_image, rot_image_rect.topleft)
        


class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((10, 4)).convert_alpha()
        self.bullet.fill((51, 230, 255))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 10

    def update(self):  
       
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                   self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)  

def rotate(x,y):
    correction_angle = 0
    player_pos = window.get_rect().center
    player_rect = player.get_rect(center=player_pos)

    player_rect.left = x
    player_rect.top = y

    key = pygame.key.get_pressed()
    speed = 5
    if(x > 0):
        if key[pygame.K_a]:
            player_rect.move_ip(-1*speed, 0)
    if(x<1180):
        if key[ pygame.K_d]:
            player_rect.move_ip(speed, 0)
    if(y>0):
        if key[pygame.K_w]:
            player_rect.move_ip(0, -1*speed)
    if(y<620):
        if key[pygame.K_s]:
            player_rect.move_ip(0, speed)
    
    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player_rect.centerx, my - player_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    rot_image = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center=player_rect.center)


    window.blit(rot_image, rot_image_rect.topleft)
    return((player_rect.left, player_rect.top))


bullets = []
enemies = []
run = True
done = False
x = 0
y = 0
while run:
    window.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            bullets.append(Bullet(*(x+50,y+50)))
    if not done:
        if(len(enemies) < 10):
            enemies.append(Enemy())
        else:
            done = True

    for enemy in enemies:
        enemy.draw(x,y)

    for bullet in bullets[:]:
        bullet.update()
        for enemy in enemies:
            if enemy.isColliding(bullet.pos):
                try:
                    bullets.remove(bullet)
                except:
                    pass
                enemies.remove(enemy)
        if not window.get_rect().collidepoint(bullet.pos):
            bullets.remove(bullet)

    for bullet in bullets:
        bullet.draw(window)        
    x,y = rotate(x,y)



    pygame.display.flip()

pygame.quit()
exit()
