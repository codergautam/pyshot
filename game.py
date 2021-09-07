# GitHub:
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_rotate_towards_target.md
#
# Stack Overflow:
# https://stackoverflow.com/questions/58603835/how-to-rotate-an-imageplayer-to-the-mouse-direction/58604116#58604116

import math
import pygame
import os


pygame.init()
window = pygame.display.set_mode((1280, 720))
player = pygame.transform.smoothscale(pygame.image.load("square.png").convert_alpha(), (100, 100))

def rotate(x,y):
    correction_angle = 90
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

    window.fill((255, 255, 255))
    window.blit(rot_image, rot_image_rect.topleft)
    return((player_rect.left, player_rect.top))



run = True
x = 0
y = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    x,y = rotate(x,y)


    pygame.display.flip()

pygame.quit()
exit()
