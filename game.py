

import math
import pygame
import os
import random

import time

from pygame.image import load
import easygui as g

from pygame.constants import RESIZABLE

pygame.init()
myfont = pygame.font.Font('calibri.ttf', 30)
overkillsfont = pygame.font.Font('calibri.ttf', 50)
gameoverfont = pygame.font.Font('calibri.ttf', 100)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
player = pygame.transform.smoothscale(pygame.image.load("square.png").convert_alpha(), (100, 100))
    
class Enemy:
    def __init__(self):
        self.pos  = (random.randint(50, 1230),random.randint(50,680))
        self.enemy = pygame.transform.smoothscale(pygame.image.load("enemy.png").convert_alpha(), (50, 50))
        self.bullets = []
        self.lastUpdate = time.time()
        self.random = random.randint(10,50)/10
        
    def isColliding(self,point):
        return self.rect.collidepoint(point)
    def shoot(self, px, py):
        self.bullets.append(Bullet(*(self.pos[0]+50,self.pos[1]+50), False, px, py))
    def update(self, px, py):
        if(time.time() >= self.random+self.lastUpdate):
            self.shoot(px, py)
            self.lastUpdate = time.time()
            self.random = random.randint(10,50)/10
        #time.sleep(1)
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
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((10, 4)).convert_alpha()
        if player:
            self.bullet.fill((51, 230, 255))
        else:
            self.bullet.fill((255, 51, 51))
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
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            player_rect.move_ip(-1*speed, 0)
    if(x<1180):
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            player_rect.move_ip(speed, 0)
    if(y>0):
        if key[pygame.K_w] or key[pygame.K_UP]:
            player_rect.move_ip(0, -1*speed)
    if(y<620):
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            player_rect.move_ip(0, speed)
    
    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player_rect.centerx, my - player_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    rot_image = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center=player_rect.center)


    window.blit(rot_image, rot_image_rect.topleft)
    return((player_rect.left, player_rect.top, rot_image_rect))


bullets = []
enemies = []
run = True
done = False
dead = False
loading = False
clock = pygame.time.Clock()

x = 0
y = 0
kills = 0
while run:
    print(clock.get_fps())
    window.fill((255, 255, 255))
    if(loading):

        loading = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if not dead:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(num_buttons=3)[0]:
                        pos = pygame.mouse.get_pos()
                        bullets.append(Bullet(*(x+50,y+50),True))
        if(len(enemies) == 0):
            done = False
        if not done:
            if(len(enemies) <= 4):
                enemies.append(Enemy())
            else:
                done = True

        for enemy in enemies:
            for enemybullet in enemy.bullets:
                enemybullet.update()
                if not window.get_rect().collidepoint(enemybullet.pos):
                    try:
                        enemy.bullets.remove(enemybullet)
                    except:
                        pass
                else:
                    enemybullet.draw(window)
                    if player_rect.collidepoint(enemybullet.pos):
                        enemy.bullets.remove(enemybullet)
                        #dead rip
                        dead = True
            enemy.draw(x,y)
            enemy.update(x,y)

        for bullet in bullets[:]:
            if not dead:
                bullet.update()
                for enemy in enemies:
                    if enemy.isColliding(bullet.pos):
                        try:
                            bullets.remove(bullet)
                        except:
                            pass
                        enemies.remove(enemy)
                        kills += 1
                if not window.get_rect().collidepoint(bullet.pos):
                    try:
                        bullets.remove(bullet)
                    except:
                        pass
        if not dead:               
            for bullet in bullets:
                bullet.draw(window)       
            x,y,player_rect = rotate(x,y)
        else:

            textsurface = gameoverfont.render('Game over ', False, (0, 0, 0))
            killsurface = overkillsfont.render('You got '+str(kills)+" kills", False, (0, 0, 0))
            text_rect = textsurface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2-SCREEN_HEIGHT/4))
            kill_rect = killsurface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2-SCREEN_HEIGHT/15))
            w, h = pygame.display.get_surface().get_size()
            window.blit(textsurface,text_rect)
            window.blit(killsurface,kill_rect)
            rect = pygame.Rect(0,0, SCREEN_WIDTH/5, SCREEN_HEIGHT/14)
            rect.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + SCREEN_HEIGHT/15)
            if(rect.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(window, (170, 170,170),rect)
            else:
                pygame.draw.rect(window, (211, 211,211),rect)
            againsurface = myfont.render('Play Again', False, (0,0,0))
            again_rect = againsurface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + SCREEN_HEIGHT/15))
            window.blit(againsurface,again_rect)
            if pygame.mouse.get_pressed(num_buttons=3)[0] and rect.collidepoint(pygame.mouse.get_pos()):
                kills = 0
                bullets.clear()
                enemies.clear()
                dead = False
            
        if not dead:
            textsurface = myfont.render('Kills: '+str(kills), False, (0, 0, 0))
            window.blit(textsurface,(0,0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()
