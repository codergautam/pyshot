import math
import random
import time

from threading import Event, Thread

import pygame
from pygame.constants import RESIZABLE

from Bullet import Bullet
from Pickup import Pickup

pygame.init()
font10 = pygame.font.Font('assets/calibri.ttf', 30)
font50 = pygame.font.Font('assets/calibri.ttf', 50)
font100 = pygame.font.Font('assets/calibri.ttf', 100)
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)

player = pygame.transform.smoothscale(pygame.image.load("assets/square.png").convert_alpha(), (100, 100))
bullet_icon = pygame.transform.smoothscale(pygame.image.load("assets/bullet.png").convert_alpha(), (150, 150))
bullet_pick = pygame.transform.smoothscale(pygame.image.load("assets/bullet.png").convert_alpha(), (50, 50))
speed_pick = pygame.transform.smoothscale(pygame.image.load("assets/speed.png").convert_alpha(), (50, 50))

enemy_shoot_sound = pygame.mixer.Sound(file="assets/enemy_shoot.ogg")
bullet_pick_sound = pygame.mixer.Sound(file="assets/bullet_pickup.ogg")
shoot_sound = pygame.mixer.Sound(file="assets/shoot.ogg")
kill_sound = pygame.mixer.Sound(file="assets/kill.ogg")
empty_sound = pygame.mixer.Sound(file="assets/empty.ogg")
death_sound = pygame.mixer.Sound(file="assets/death.ogg")

powerup_speed = False

speed_remaining = None


class Enemy:
    def __init__(self):
        self.pos = (random.randint(75, SCREEN_WIDTH - 75),
                    random.randint(75, SCREEN_HEIGHT - 75))
        # print (self.pos)
        self.enemy = pygame.transform.smoothscale(
            pygame.image.load("assets/enemy.png").convert_alpha(), (50, 50))
        self.bullets = []
        self.lastUpdate = time.time()

        self.random = random.randint(10, 30) / 10
        self.speed = 1.5
        self.center_pos = (self.pos[0] + 50, self.pos[1] + 50)
        self.rect = None

    def is_colliding(self, point):
        return self.rect.collidepoint(point)

    @staticmethod
    def get_rand():
        if kills < 10:
            return random.randint(20, 50) / 10
        elif kills < 20:
            return random.randint(10, 50) / 10
        elif kills < 30:
            return random.randint(5, 50) / 10
        elif kills < 40:
            return random.randint(10, 30) / 10
        elif kills < 60:
            return random.randint(5, 30) / 10
        elif kills < 75:
            return random.randint(5, 20) / 10
        elif kills < 90:
            return random.randint(3, 20) / 10
        else:
            return random.randint(1, 10) / 10

    def shoot(self, px, py):
        self.bullets.append(
            Bullet(*(self.pos[0] + 50, self.pos[1] + 50), False, px, py))
        enemy_shoot_sound.play()

    def update(self, px, py):
        try:
            if kills < 10:
                self.speed = 0
                # print("speed = 0")
            elif kills < 30:
                self.speed = 45 / clock.get_fps()
        except ZeroDivisionError:
            pass
        if time.time() >= self.random + self.lastUpdate:
            self.shoot(px, py)
            self.lastUpdate = time.time()
            self.random = self.get_rand()

    def get_rect(self):
        enemy_pos = window.get_rect().center
        enemy_rect = player.get_rect(center=enemy_pos)
        enemy_rect.x = self.pos[0]
        enemy_rect.y = self.pos[1]
        return enemy_rect

    def draw(self, px, py):
        correction_angle = 0
        enemy_pos = window.get_rect().center
        enemy_rect = player.get_rect(center=enemy_pos)

        enemy_rect.x = self.pos[0]
        enemy_rect.y = self.pos[1]

        # px, py = player x player y
        dx, dy = px - enemy_rect.centerx, py - enemy_rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle
        # angle = 0
        rot_image = pygame.transform.rotate(self.enemy, angle)
        rot_image_rect = rot_image.get_rect(center=enemy_rect.center)
        self.rect = rot_image_rect
        # if kills > 10:
        self.move_towards_player((px + 50, py + 50))

        window.blit(rot_image, self.rect.topleft)

    def move_towards_player(self, player_position):
        enemy_position = list(self.center_pos)
        # print(self.pos, enemy_position)
        change = 0
        if enemy_position[0] < player_position[0]:
            change += 1
        if enemy_position[0] > player_position[0]:
            change += 1
        if enemy_position[1] < player_position[1]:
            change += 1
        if enemy_position[1] > player_position[1]:
            change += 1

        if change > 1:
            speed = self.speed / 2
        else:
            speed = self.speed

        if enemy_position[0] < player_position[0]:
            enemy_position[0] += speed
        if enemy_position[0] > player_position[0]:
            enemy_position[0] -= speed
        if enemy_position[1] < player_position[1]:
            enemy_position[1] += speed
        if enemy_position[1] > player_position[1]:
            enemy_position[1] -= speed

        self.pos = (enemy_position[0] - 50, enemy_position[1] - 50)
        self.center_pos = tuple(enemy_position)


def call_repeatedly(interval, max_ticks, func):
    stopped = Event()

    def loop():
        nonlocal max_ticks
        nonlocal t
        ticks = 0
        while not stopped.wait(interval):
            ticks += 1
            if ticks == max_ticks:
                return

            func(ticks)

    t = Thread(target=loop)
    t.daemon = True
    t.start()
    return stopped.set


def rotate():
    correction_angle = 0
    player_pos = window.get_rect().center
    rect_player = player.get_rect(center=player_pos)

    rect_player.left = x
    rect_player.top = y

    key = pygame.key.get_pressed()
    try:
        if powerup_speed:
            speed = 700 / clock.get_fps()
        else:
            speed = 450 / clock.get_fps()
    except ZeroDivisionError:
        speed = 7.5

    left = key[pygame.K_a] or key[pygame.K_LEFT]
    right = key[pygame.K_d] or key[pygame.K_RIGHT]
    up = key[pygame.K_w] or key[pygame.K_UP]
    down = key[pygame.K_s] or key[pygame.K_DOWN]

    x_unit = -1.0 if left else 1.0 if right else 0.0
    y_unit = -1.0 if up else 1.0 if down else 0.0

    if not (not x_unit and not y_unit):
        magnitude = (x_unit ** 2 + y_unit ** 2) ** 0.5
        x_dis = x_unit / magnitude * speed
        y_dis = y_unit / magnitude * speed

        x_min, x_max = 0, SCREEN_WIDTH - 110
        x_dis = max(x_min, min(x_max, x + x_dis)) - x

        y_min, y_max = 0, SCREEN_HEIGHT - 110
        y_dis = max(y_min, min(y_max, y + y_dis)) - y

        rect_player.move_ip(x_dis, y_dis)

    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - rect_player.centerx, my - rect_player.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    rot_image = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center=rect_player.center)

    window.blit(rot_image, rot_image_rect.topleft)
    return rect_player.left, rect_player.top, rot_image_rect


def get_num_enemies():
    global win
    waves_enemy = [1, 1, 2, 2, 3]
    try:
        return waves_enemy[wave - 1] - 1
    except IndexError:
        win = True
        return -1


bullets = []
enemies = []
pickups = []

run = True
done = False
dead = False
win = False
loading = False
clock = pygame.time.Clock()

x = 0
y = 0
bullet_count = 5

kills = 0
wave = 1

center_pos = (x + 50, y + 50)

while run:
    # print(clock.get_fps())
    window.fill((255, 255, 255))
    if loading:

        loading = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface(
                ).get_size()
                for enemy in enemies:
                    removed = 0
                    if not window.get_rect().collidepoint(
                            enemy.get_rect().center):
                        # check if enemy is out of screen after resizing
                        enemies.remove(enemy)
                        removed += 1
                    for x in range(removed):
                        enemies.append(Enemy())
                try:
                    if window.get_rect().collidepoint(player_rect.center):
                        player_rect.center = (0, 0)
                except NameError:
                    pass

            if not dead:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(num_buttons=3)[0]:
                        if bullet_count > 0:
                            pos = pygame.mouse.get_pos()
                            bullet_count -= 1

                            bullets.append(Bullet(*(x + 50, y + 50), True))
                            shoot_sound.play()
                        else:
                            empty_sound.play()

        if len(enemies) == 0:
            done = False
        if not done:

            if len(enemies) <= get_num_enemies():
                enemies.append(Enemy())
            else:
                done = True
        for pickup_object in pickups:

            pickup_object.update(window, player_rect)
            if not pickup_object.visible:
                pickups.remove(pickup_object)
        for enemy in enemies:
            for enemy_bullet in enemy.bullets:
                enemy_bullet.update(clock.get_fps())
                if not window.get_rect().collidepoint(enemy_bullet.pos):
                    try:
                        enemy.bullets.remove(enemy_bullet)
                    except ValueError:
                        print("[debug] " + repr(e))
                else:
                    enemy_bullet.draw(window)
                    if player_rect.collidepoint(enemy_bullet.pos):
                        if not dead:
                            enemy.bullets.remove(enemy_bullet)
                            death_sound.play()
                            # dead rip
                            dead = True
                            powerup_speed = False
            enemy.draw(x, y)

            enemy.update(x, y)


        def pick():
            global bullet_count
            bullet_count += 1
            bullet_pick_sound.play()


        def speed_picked():
            global powerup_speed
            powerup_speed = True
            call_repeatedly(0.1, 51, speed_tick)
            # speed_time()


        def speed_tick(ticks):
            global powerup_speed
            global speed_remaining
            speed_remaining = round(5 - (0.1 * ticks), 2)
            print(speed_remaining)
            if speed_remaining == 0:
                powerup_speed = False


        if not dead:
            # spawn powerups
            if (bullet_count < 3 and random.randint(1, (round(clock.get_fps()) * 20) + 1) == 5) or (
                    bullet_count == 0 and random.randint(1, (round(clock.get_fps()) * 5) + 1) == 5):
                pickups.append(Pickup("bullet", (random.randint(50, SCREEN_WIDTH - 50),
                                                 random.randint(50, SCREEN_HEIGHT - 50)), bullet_pick, pick))
            if random.randint(1, (round(clock.get_fps()) * 5) + 1) == 5:
                if not powerup_speed:
                    pickups.append(Pickup("speed", (random.randint(50, SCREEN_WIDTH - 50),
                                                    random.randint(50, SCREEN_HEIGHT - 50)), speed_pick, speed_picked))

        for bullet in bullets[:]:
            if not dead:
                bullet.update(clock.get_fps())
                for enemy in enemies:
                    if enemy.is_colliding(bullet.pos):
                        try:
                            bullets.remove(bullet)
                        except ValueError as e:
                            print("[debug] " + repr(e))

                        pickups.append(Pickup("bullet", enemy.center_pos, bullet_pick, pick))
                        enemies.remove(enemy)
                        if len(enemies) == 0:
                            wave += 1

                        kill_sound.play()
                        # bullet_count += 1
                        kills += 1
                if not window.get_rect().collidepoint(bullet.pos):
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        print("[debug] " + repr(e))
        if not dead:
            for bullet in bullets:
                bullet.draw(window)
            x, y, player_rect = rotate()
            center_pos = (x + 50, y + 50)
        else:

            text_surface = font100.render('Game over ', False, (0, 0, 0))
            kill_surface = font50.render(
                'You got ' + str(kills) + " kills", False, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2,
                                                      SCREEN_HEIGHT / 2 -
                                                      SCREEN_HEIGHT / 4))
            kill_rect = kill_surface.get_rect(center=(SCREEN_WIDTH / 2,
                                                      SCREEN_HEIGHT / 2 -
                                                      SCREEN_HEIGHT / 15))
            w, h = pygame.display.get_surface().get_size()
            window.blit(text_surface, text_rect)
            window.blit(kill_surface, kill_rect)
            rect = pygame.Rect(0, 0, SCREEN_WIDTH / 5, SCREEN_HEIGHT / 14)
            rect.center = (SCREEN_WIDTH / 2,
                           SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 15)
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window, (170, 170, 170), rect)
            else:
                pygame.draw.rect(window, (211, 211, 211), rect)
            again_surface = font10.render('Play Again', False, (0, 0, 0))
            again_rect = again_surface.get_rect(center=(SCREEN_WIDTH / 2,
                                                        SCREEN_HEIGHT / 2 +
                                                        SCREEN_HEIGHT / 15))
            window.blit(again_surface, again_rect)
            if pygame.mouse.get_pressed(num_buttons=3)[0] and rect.collidepoint(pygame.mouse.get_pos()):
                kills = 0
                wave = 1
                pickups.clear()
                bullets.clear()
                enemies.clear()
                bullet_count = 5
                dead = False

        if not dead:
            text_surface = font10.render('Kills: ' + str(kills), False,
                                         (0, 0, 0))
            window.blit(text_surface, (0, 0))
            kill_surface = font100.render(str(bullet_count), False, (0, 0, 0))
            kill_rect = kill_surface.get_rect(
                center=(SCREEN_WIDTH / 2 + SCREEN_WIDTH / 35, SCREEN_HEIGHT / 1.2 - SCREEN_HEIGHT / 20))
            window.blit(kill_surface, kill_rect)
            bullet_rect = bullet_icon.get_rect(
                center=(SCREEN_WIDTH / 2 - SCREEN_WIDTH / 35, SCREEN_HEIGHT / 1.2 - SCREEN_HEIGHT / 15))
            window.blit(bullet_icon, bullet_rect)
        fps_text = font10.render('FPS: ' + str(round(clock.get_fps())), False,
                                 (0, 0, 0))
        window.blit(fps_text, (SCREEN_WIDTH - SCREEN_WIDTH / 5, SCREEN_HEIGHT - 100))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
exit()
