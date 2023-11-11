import pygame
from math import ceil

pygame.init()
data = open("data.txt")
max_score = int(data.readlines()[1])
screen = pygame.display.set_mode((1800, 1000))
icon = pygame.image.load("ico.png").convert()
pygame.display.set_caption("Dodge", "ico.png")
pygame.display.set_icon(icon)
running = True
clr = True
last_score = 0
clock = pygame.time.Clock()
cooldown = 0
x = 225
y = 225
speed_enemy_y = 0
speed_enemy_x = 0
enemy_x = 1000
enemy_y = 500
change = 0
deceleration_pos_x, deceleration_neg_y, deceleration_pos_y, deceleration_neg_x = False, False, False, False
score_count = 2
score = 0
score_x = 900
max_score_x = 0
title_screen = pygame.image.load("title_screen.png").convert_alpha()
character1 = pygame.image.load("sprites/character.png").convert_alpha()
character2 = pygame.image.load("sprites/character2.png").convert_alpha()
score_hud = pygame.image.load("sprites/score_hud.png").convert()
boost_hud = pygame.image.load("sprites/boost_hud.png").convert_alpha()
boost_multi = 1


def menu():
    global running, event, enemy_x, enemy_y, x, y
    menu_running = True
    timer = 0
    while menu_running and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                menu_running = False
                enemy_x, enemy_y = 0, 0
                x, y = 900, 500
        screen.fill((200, 200, 200))
        screen.blit(title_screen, (0, 0))
        font = pygame.font.SysFont("Bahnschrift", 36)
        last_score_text = font.render(f"{last_score}", True, (204, 198, 0))
        max_score_text = font.render(f"{max_score}", True, (204, 198, 0))
        screen.blit(last_score_text, last_score_text.get_rect(center=(360, 240)))
        screen.blit(max_score_text, max_score_text.get_rect(center=(1450, 240)))
        if timer > 45:
            text_draw("[PRESS ENTER TO START]", pygame.font.SysFont("Bahnschrift", 16), (250, 250, 250), 815, 320)
            if timer > 90:
                timer = 0
        timer += 1
        clock.tick(60)
        pygame.display.flip()


def text_draw(text, font, text_clr, xt, yt):
    img = font.render(f"{text}", True, text_clr)
    screen.blit(img, (xt, yt))


def modify_data(num):
    global data
    data = open("data.txt", 'r')
    lines = data.readlines()
    data.close()

    lines[1] = str(num)

    data = open("data.txt", 'w')
    data.writelines(lines)
    data.close()


def enemy_calculation():
    global deceleration_neg_x, speed_enemy_y, speed_enemy_x, deceleration_pos_y, deceleration_neg_y, deceleration_pos_x
    if enemy_x > x:  # enemy calculation
        if not deceleration_pos_x:
            if speed_enemy_x < -2:
                speed_enemy_x -= 0.2
            else:
                speed_enemy_x -= 0.4
            if speed_enemy_x < -10:
                speed_enemy_x = -10
            deceleration_neg_x = True
        else:
            if speed_enemy_x < 0:
                deceleration_pos_x = False
            if -4 < speed_enemy_y < 4 or -4 < (speed_enemy_x and speed_enemy_y) > 4:
                speed_enemy_x -= 0.4
            else:
                speed_enemy_x -= 0.2
    else:
        if not deceleration_neg_x:
            if speed_enemy_x > 2:
                speed_enemy_x += 0.2
            else:
                speed_enemy_x += 0.4
            if speed_enemy_x > 10:
                speed_enemy_x = 10
            deceleration_pos_x = True
        else:
            if speed_enemy_x > 0:
                deceleration_neg_x = False
            if -4 < speed_enemy_y < 4 or -4 < (speed_enemy_x and speed_enemy_y) > 4:
                speed_enemy_x += 0.4
            else:
                speed_enemy_x += 0.2
    if enemy_y > y:
        if not deceleration_pos_y:
            if speed_enemy_y < -2:
                speed_enemy_y -= 0.2
            else:
                speed_enemy_y -= 0.4
            if speed_enemy_y < -10:
                speed_enemy_y = -10
            deceleration_neg_y = True
        else:
            if speed_enemy_y < 0:
                deceleration_pos_y = False
            if -4 < speed_enemy_x < 4 or -4 < (speed_enemy_x and speed_enemy_y) > 4:
                speed_enemy_y -= 0.4
            else:
                speed_enemy_y -= 0.2
    else:
        if not deceleration_neg_y:
            if speed_enemy_y > 2:
                speed_enemy_y += 0.2
            else:
                speed_enemy_y += 0.4
            if speed_enemy_y > 10:
                speed_enemy_y = 10
            deceleration_pos_y = True
        else:
            if speed_enemy_y > 0:
                deceleration_neg_y = False
            if -4 < speed_enemy_x < 4 or -4 < (speed_enemy_x and speed_enemy_y) > 4:
                speed_enemy_y += 0.4
            else:
                speed_enemy_y += 0.2


menu()
while running:
    screen.fill((200, 200, 200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if clr:
        multi = 1
    else:
        multi = 2
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        y += 5 * multi
    if pygame.key.get_pressed()[pygame.K_UP]:
        y -= 5 * multi
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        x -= 5 * multi
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        x += 5 * multi
    if pygame.key.get_pressed()[pygame.K_SPACE] and cooldown == 0:
        clr = not clr
        cooldown = 300
        change = 60
    if cooldown != 0:
        cooldown -= 1
    if change != 0:
        change -= 1
    else:
        clr = True
    if change != 0:
        boost_multi = change/60
        boost_text = "!"
        x_btext = 1661
    elif cooldown != 0:
        boost_multi = (240-cooldown)/240
        boost_text = str(ceil(cooldown/60))
        x_btext = 1650
    else:
        boost_multi = 1
        boost_text = "GO"
        x_btext = 1615
    enemy_calculation()
    hitbox_player = pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x - 60, y - 60, 160, 160))
    enemy_x = enemy_x + speed_enemy_x
    enemy_y = enemy_y + speed_enemy_y
    hitbox_enemy = pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(enemy_x - 5, enemy_y - 5, 60, 60))
    pygame.draw.rect(screen, (200, 75, 75), pygame.Rect(enemy_x, enemy_y, 50, 50))  # enemy
    if clr:
        screen.blit(character1, (x - 60, y - 60))
    else:
        screen.blit(character2, (x - 60, y - 60))
    if pygame.Rect.colliderect(hitbox_enemy, hitbox_player):
        last_score = score
        score = 0
        menu()
    score_count -= 1
    if score_count == 0:
        score += 1
        score_count = 2
    if score > max_score:
        max_score = score
    screen.blit(score_hud, (700, 10))
    screen.blit(boost_hud, (1550, 250))
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(1643, 360, 62, 366*abs(boost_multi-1)))
    text_draw(score, pygame.font.SysFont("Bahnschrift", 48), (204, 198, 0), 715, 49)
    text_draw(max_score, pygame.font.SysFont("Bahnschrift", 48), (0, 74, 164), 940, 27)
    text_draw(boost_text, pygame.font.SysFont("Bahnschrift", 90), (204, 198, 0), x_btext, 840)
    pygame.display.flip()
    clock.tick(60)
modify_data(max_score)
pygame.quit()
