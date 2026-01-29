#--framework--
import pygame as pg
import sys
import random
#--------
pg.init()
pg.font.init()
#------
#CONST
WIDTH = 800
HEIGHT = 990
#--clock--a 
clock = pg.time.Clock()
#--color--
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (30,30,30)
RED = (255,0,0)
GREEN = (0,255,0)
#--Game-status
running = True
game_over = False
#---oтрисовка
screen = pg.display.set_mode((WIDTH,HEIGHT))
TITLE = pg.display.set_caption("---TANK---")
#---отрисовка танка----
Tank_width = 40
Tank_height = 100
Tank_speed = 10
Tank = pg.rect.Rect(WIDTH /2 - Tank_width /2, #y
                             HEIGHT - Tank_height *1.5, #x
                             Tank_height,
                             Tank_width)
#-------Aimmo-------
cartridges = []
cartridge_radius = 15
cartridge_speed = 10
cartridge_height = 25
cartridge_width = 30
shot_cooldown = 2
current_time = 0
#----enemies----враги---
enemies = []  
enemy_width = 60
enemy_height = 60
enemy_speed = 2
spawn_timer = 0
spawn_delay = 1000
#---fps---
FPS = 120
#--Game-status
running = True
game_over = False
#---GAME---
while running:
    current_time = pg.time.get_ticks()
    for event in pg.event.get():
        if game_over == True:
            sys.exit()
        if event.type == pg.QUIT:
            running = False
            game_over = True
            sys.exit()
        #-----если-нажат-эскейп---
        elif event.type == pg.KEYDOWN:
            if event.type == pg.K_ESCAPE:
                running = False
                game_over = True
        #---if---k_space-----
        if event.type == pg.K_SPACE and current_time - last_shot_time > shot_cooldown:
            new_cartridge = pg.Rect(Tank.centerx - cartridge_radius,
                                   Tank.top - cartridge_radius * 2,
                                   cartridge_radius * 2,
                                   cartridge_radius * 2)
            cartridges.append(new_cartridge)
            last_shot_time = current_time
#---------MAIN---------
    if not game_over:
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            Tank.x -= Tank_speed
        elif keys[pg.K_d]:
            Tank.x  += Tank_speed
        #------
        if current_time - spawn_timer > spawn_delay:
            #---случайная-позиция--на-верху--экрана
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy = pg.Rect(enemy_x, 0, enemy_width, enemy_height)
            enemies.append(enemy)
            spawn_timer = current_time

        #----автовыстрел-если-пробел--зажат----
        if keys[pg.K_SPACE] and len(cartridges) < 2:  # Ограничение количества снарядов
            new_cartridge = pg.Rect(Tank.centerx - cartridge_radius,
                                   Tank.top - cartridge_radius * 2,
                                   cartridge_radius * 2,
                                   cartridge_radius * 2)
            cartridges.append(new_cartridge)
        #--нельзя--выходить-за-границы-экрана---
        if Tank.left < 0:
            Tank.left = 0
        if Tank.right > WIDTH:  
            Tank.right = WIDTH    
        #---go-to-up--aimo
        for cartridge in cartridges[:]:  
            cartridge.y -= cartridge_speed
        #----delete---aimo
            if cartridge.bottom < 0:
                cartridges.remove(cartridge)
        if current_time - spawn_timer > spawn_delay:
        #--Случайная--позиция-вверху--экрана--
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy = pg.Rect(enemy_x, 0, enemy_width, enemy_height)
            enemies.append(enemy)
            spawn_timer = current_time
        #----enemy-касаються пули
        for cartridge in cartridges[:]:
            for enemy in enemies[:]:
                if cartridge.colliderect(enemy):
                    cartridges.remove(cartridge)
                    enemies.remove(enemy)
                    break
        #---враги-вниз---
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemies.remove(enemy)
        for enemy in enemies[:]:
            if Tank.colliderect(enemy):
                game_over = True
    #---заливка---
    screen.fill(GREY)
    #--DRAW---
    pg.draw.rect(screen,WHITE,(Tank))
    #-draw--врагиии----
    for enemy in enemies:
        # Простой квадратный враг
        pg.draw.rect(screen, GREEN, enemy)
        
    #---пули--
    for cartridge in cartridges:
        pg.draw.circle(screen, RED, cartridge.center, cartridge_radius)
    #---------
    pg.display.flip()
    clock.tick(FPS)
sys.exit()
pg.quit()