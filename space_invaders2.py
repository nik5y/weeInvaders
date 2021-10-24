import math
import pygame

from resources.levels import level1
from pygame import mixer

# initialise pygame
pygame.init()

master_volume = 0.1
fps = 60
delay_tick = 0

# create the screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_img = pygame.image.load("resources/images/space_background.jpg")
background_music = mixer.Sound("resources/audios/ppk_resurrection.mp3")
background_music.set_volume(master_volume)
background_music.play(-1)
# title and icon
pygame.display.set_caption("Space Invaders")

# player
player_icon = pygame.image.load("resources/images/dolr.png")
p_x, p_y = 375, 480
p_dx = 0
p_ddx = 2.6
p_health = 5

score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
t_x, t_y = 25, 25

game_over_font = pygame.font.Font('freesansbold.ttf', 96)
game_over = False
game_over_sound = mixer.Sound("resources/audios/brass_fail.mp3")
game_over_sound.set_volume(master_volume)

win = False
win_sound = mixer.Sound("resources/audios/coffin_dance.mp3")
win_sound.set_volume(master_volume)

# enemies
enemy_list = level1.enemy_list
active_enemy_list = []

enemy_icon = pygame.image.load("resources/images/generic_coin.png")

# bullet
bullet_icon = pygame.image.load("resources/images/bullet_chad.png")
b_x, b_y = -100, -100
b_dx, b_dy = 0, 6
b_action = False
b_sound = mixer.Sound("resources/audios/ah_haha.mp3")
b_sound.set_volume(master_volume)

enemy_bullet_collision_sound = mixer.Sound("resources/audios/hitmarker.wav")
enemy_bullet_collision_sound.set_volume(master_volume)
enemy_player_collision_sound = mixer.Sound("resources/audios/ahhhhhhh.mp3")
enemy_player_collision_sound.set_volume(0.1)


def player(player_icon, p_x, p_y):
    screen.blit(player_icon, (p_x, p_y))


def bullet_fire(x, y):
    global b_action
    b_action = True
    screen.blit(bullet_icon, (x, y))


def coordinate_distance(e_x, e_y, b_x, b_y):
    return math.sqrt((e_x-b_x)*(e_x-b_x) + (e_y-b_y)*(e_y-b_y))


def collision(e_x, e_y, b_x, b_y, min_distance):
    return coordinate_distance(e_x, e_y, b_x, b_y) <= min_distance


def display_text(text, font, x, y):
    text_with_font = font.render(text, True, (255,255,255))
    screen.blit(text_with_font, (x, y))


def display_player_health(p_health):
    x, y, = 760, 25
    health_bar = pygame.Surface((15,35))
    health_bar.fill((255, 255, 255))
    for i in range(p_health):
        screen.blit(health_bar, (x, y))
        x -= 25


# game loop
running = True
reset_e = False
killed_enemies = []

while running:

    screen.blit(background_img, (0, 0))
    display_text("Score: " + str(score), score_font, t_x, t_y)
    display_player_health(p_health)
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                p_dx = -p_ddx
            if event.key == pygame.K_RIGHT:
                p_dx = p_ddx
            if event.key == pygame.K_SPACE and not b_action:
                b_sound.play()
                b_x = p_x + 12
                b_y = p_y
                bullet_fire(b_x, b_y)

        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                p_dx = 0

    if not game_over:
        # bullet movement
        if b_action:
            bullet_fire(b_x, b_y)
            b_y -= b_dy

        if b_y <= -35:
            b_action = False
            b_y = -100

        # player movement
        p_x += p_dx

        # boundary check
        if p_x <= 0:
            p_x = 0
        if p_x >= 750:
            p_x = 750

        player(player_icon, p_x, p_y)

        if len(enemy_list)>0:
            current_delay = enemy_list[0]["delay"]

            # enemy movement
            if delay_tick == current_delay * fps:

                # resetting delay for next enemy
                delay_tick = 0
                active_enemy_list.append(enemy_list.pop(0))
            else:
                delay_tick += 1

        for e in range(len(active_enemy_list)):

            active_enemy_list[e]["e_x"] += active_enemy_list[e]["e_dx"]

            # boundary check
            if active_enemy_list[e]["e_x"] <= 0:
                active_enemy_list[e]["e_dx"] = -active_enemy_list[e]["e_dx"]
                active_enemy_list[e]["e_y"] += active_enemy_list[e]["e_dy"]
            if active_enemy_list[e]["e_x"] >= 750:
                active_enemy_list[e]["e_dx"] = -active_enemy_list[e]["e_dx"]
                active_enemy_list[e]["e_y"] += active_enemy_list[e]["e_dy"]

            player(enemy_icon, active_enemy_list[e]["e_x"], active_enemy_list[e]["e_y"])

            # collision with bullet
            # shift coords to middle
            if collision(active_enemy_list[e]["e_x"] + 25, active_enemy_list[e]["e_y"] + 25, b_x + 12, b_y, 32):
                enemy_bullet_collision_sound.play()
                b_action = False
                b_y = -100
                active_enemy_list[e]["e_health"] -= 1

                # if dead
                if active_enemy_list[e]["e_health"] == 0:
                    score += 100
                    # delete from list
                    killed_enemies.append(e)
                    # checking if all enemies have been killed and no upcoming
                    if len(active_enemy_list) == 1 and len(enemy_list) == 0:
                        background_music.stop()
                        win_sound.play()
                        win = True
                        game_over = True

            # collision with player
            # in case only one enemy on screen currently and it has been shot with the bullet and removed
            if len(active_enemy_list) > 0:
                if collision(active_enemy_list[e]["e_x"] + 25, active_enemy_list[e]["e_y"] + 25, p_x + 25, p_y + 25, 25):

                    # delete from list
                    killed_enemies.append(e)

                    p_health -= 1

                    if p_health == 0:
                        # stop all possible sounds
                        background_music.stop()
                        enemy_player_collision_sound.stop()
                        enemy_bullet_collision_sound.stop()

                        game_over_sound.play()
                        game_over = True
                    else:
                        enemy_player_collision_sound.play()

        if len(killed_enemies) > 0:
            for enemy in killed_enemies:
                active_enemy_list.pop(enemy)
            killed_enemies = []

    # game over
    elif game_over and win:
        display_text("YOU WIN", game_over_font, 180, 200)

    else:
        for e in range(len(active_enemy_list)):
            player(enemy_icon, active_enemy_list[e]["e_x"], active_enemy_list[e]["e_y"])

        player(player_icon, p_x, p_y)

        display_text("GAME OVER", game_over_font, 100, 200)

    pygame.display.update()

pygame.quit()

