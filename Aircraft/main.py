import random
import pygame as pg
import math
from pygame import mixer
import math
import time

pg.init()

pg.display.set_caption("Aircraft")
screen = pg.display.set_mode((800, 600))
t1 = time.time()

bg = pg.image.load("./Images/background.png")
icon = pg.image.load("./Aircraft/Images/ufo.png")
pg.display.set_icon(icon)
aircraft_font = pg.font.Font("./Aircraft/Fonts/FFFFORWA.TTF", 64)
aircraft_text = aircraft_font.render("Aircraft", True, (255, 255, 255))

mixer.music.load("./Aircraft/Sounds/background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.5)

player_image = pg.image.load("./Aircraft/Images/player.png")
player_x = 370
player_y = 480
player_x_change = 0

enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
noe = 6
for i in range(noe):
    enemy_image.append(pg.image.load("./Aircraft/Images/enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(3)
    enemy_y_change.append(40)

heart_image = pg.transform.scale(pg.image.load("./Aircraft/Images/heart.png"), (50, 50))
empty_heart_image = pg.transform.scale(pg.image.load("./Aircraft/Images/empty_heart.png"), (50, 50))
hearts_state = [heart_image, heart_image, heart_image]
heartsHide = [False, False, False]
hearts = 3
nh = 0

bullet_image = pg.image.load("./Aircraft/Images/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

score_value = 0
bs = int(open("./Aircraft/BS.txt").read())
font = pg.font.Font('./Aircraft/Fonts/FFFFORWA.TTF', 25)
text_x = 10
text_y = 50
text2_x = 10
text2_y = 10

game_over_font = pg.font.Font('./Aircraft/Fonts/FFFFORWA.TTF', 64)
new_bs_font = pg.font.Font('./Aircraft/Fonts/FFFFORWA.TTF', 40)
bsHide = True
nb = 0

button_play_x = 300
button_play_y = 200
button_play_color = (255, 100, 0)
button_play_hover = (150, 50, 0)
button_play_font = pg.font.Font("./Aircraft/Fonts/FFFFORWA.TTF", 45)
button_play_text = button_play_font.render("Play", True, (255, 255, 255))

button_quit_x = 300
button_quit_y = 300
button_quit_color = (255, 100, 0)
button_quit_hover = (150, 50, 0)
button_quit_font = pg.font.Font("./Aircraft/Fonts/FFFFORWA.TTF", 45)
button_quit_text = button_quit_font.render("Quit", True, (255, 255, 255))

button_menu_x = 740
button_menu_y = 10
button_menu_color = (255, 100, 0)
button_menu_hover = (150, 50, 0)
button_menu_image = pg.image.load("./Aircraft/Images/menu.png")
button_menu_image =  pg.transform.scale(button_menu_image, (40, 40))

def show_score(x, y, x2, y2):
    score = font.render("Scor " + str(score_value), True, (255, 255, 255))
    bestScore = font.render("Best Scor " + str(bs), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(bestScore, (x2, y2))

def game_over_text():
    global nb, firstHide, bsHide
    game_over_txt = game_over_font.render("Game Over!", True, (255, 255, 255))
    newBS = new_bs_font.render("New Best Score!", True, (255, 255, 0))
    screen.blit(game_over_txt, (170, 250))
    if best:
        screen.blit(newBS, (185, 180))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def heart(tm):
    global nh
    dis = 55
    for i in range(3):
        if not heartsHide[i]:
            screen.blit(hearts_state[i], (735-dis, 10))
        elif heartsHide[i] and 0 <= tm % 0.5 < 0.1 and nh <= 20:
            nh += 1
            screen.blit(hearts_state[i], (735-dis, 10))
        if nh >= 20:
            heartsHide[i] = False
            nh = 0
        dis += 55

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x+16, y+10))

def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    #distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    distance = math.dist([enemy_x, enemy_y], [bullet_x, bullet_y])
    if distance < 27:
        return True
    else:
        return False

best = False
play = False
running = True
while running:
    tm = time.time() - t1
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and play:
            if event.key == pg.K_LEFT:
                player_x_change = -5
            if event.key == pg.K_RIGHT:
                player_x_change = 5
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    mixer.Channel(1).play(mixer.Sound("./Aircraft/Sounds/laser.wav"))
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pg.KEYUP and play:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player_x_change = 0
        if event.type == pg.MOUSEBUTTONDOWN:
            if button_play_x <= mouse[0] <= button_play_x+200 and button_play_y <= mouse[1] <= button_play_y+80 and not play:
                play = True
            if button_quit_x <= mouse[0] <= button_quit_x+200 and button_quit_y <= mouse[1] <= button_quit_y+80 and not play:
                running = False
            if button_menu_x <= mouse[0] <= button_menu_x+50 and button_menu_y <= mouse[1] <= button_menu_y+50:
                play = False

    if not play:
        mouse = pg.mouse.get_pos()
        if button_play_x <= mouse[0] <= button_play_x+200 and button_play_y <= mouse[1] <= button_play_y+80:
            pg.draw.rect(screen, button_play_hover, (button_play_x, button_play_y, 200, 80))
        else:
            pg.draw.rect(screen, button_play_color, (button_play_x, button_play_y, 200, 80))
        screen.blit(button_play_text, (335, 204))
        
        if button_quit_x <= mouse[0] <= button_quit_x+200 and button_quit_y <= mouse[1] <= button_quit_y+80:
            pg.draw.rect(screen, button_quit_hover, (button_quit_x, button_quit_y, 200, 80))
        else:
            pg.draw.rect(screen, button_quit_color, (button_quit_x, button_quit_y, 200, 80))
        screen.blit(button_quit_text, (340, 306))
    
        screen.blit(aircraft_text, (250, 15))

    elif play:
        player_x = player_x + player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        if score_value > bs:
            with open("./Aircraft/BS.txt", "w") as file:
                file.write(str(score_value))
            best = True

        mouse = pg.mouse.get_pos()
        if button_menu_x <= mouse[0] <= button_menu_x+50 and button_menu_y <= mouse[1] <= button_menu_y+50:
            pg.draw.rect(screen, button_menu_hover, (button_menu_x, button_menu_y, 50, 50))
        else:
            pg.draw.rect(screen, button_menu_color, (button_menu_x, button_menu_y, 50, 50))
        screen.blit(button_menu_image, (744, 14))

        for i in range(noe):
            if enemy_y[i] > 440:
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 150)
                hearts -= 1
                try:
                    heartsHide[hearts] = True
                    hearts_state[hearts] = empty_heart_image
                except:
                    for i in range(3):
                        heartsHide[i] = False
                    for g in range(noe):
                        enemy_y[g] = 2000
                    game_over_text()
                if hearts == 0:
                    for g in range(noe):
                        enemy_y[g] = 2000
                    game_over_text()

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 3
                enemy_y[i] = enemy_y[i] + enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -3
                enemy_y[i] = enemy_y[i] + enemy_y_change[i]
            coll = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if coll:
                mixer.Channel(1).play(mixer.Sound("./Aircraft/Sounds/explosion.wav"))
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 150)
            enemy(enemy_x[i], enemy_y[i], i)
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y = bullet_y - bullet_y_change
        player(player_x, player_y)
        show_score(text_x, text_y, text2_x, text2_y)
        heart(tm)

    pg.display.update()