import pygame
import random
import math

from pygame import mixer

# initialise pygame
pygame.init()

master_volume = 0.25
fps = 60

# create the screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_img = pygame.image.load("resources/space_invaders/images/space_background.jpg")
background_music = mixer.Sound("resources/space_invaders/audios/ppk_resurrection.mp3")
background_music.set_volume(master_volume)
background_music.play(-1)
# title and icon
pygame.display.set_caption("Space Invaders")

# player
player_icon = pygame.image.load("resources/space_invaders/images/dolr.png")
p_x, p_y = 375, 480
p_dx = 0
p_ddx = 0.9
p_health = 5

score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
t_x, t_y = 25, 25

game_over_font = pygame.font.Font('freesansbold.ttf', 96)
game_over = False
game_over_sound = mixer.Sound("resources/space_invaders/audios/brass_fail.mp3")
game_over_sound.set_volume(master_volume)

# enemy

enemy_count = 6
enemy_icon = pygame.image.load("resources/space_invaders/images/generic_coin.png")
e_x, e_y, e_dx, e_dy = [], [], [], []
e_health = []

for e in range(enemy_count):
    e_x.append(random.randint(0, 750))
    e_y.append(random.randint(0, 370))
    e_dx.append(random.uniform(0.3, 0.7) if random.randint(0, 1) == 1 else random.uniform(-0.7, -0.3))
    e_dy.append(random.uniform(30, 50))
    e_health.append(3)

# bullet
bullet_icon = pygame.image.load("resources/space_invaders/images/bullet_chad.png")
b_x, b_y = -100, -100
b_dx, b_dy = 0, 1.5
b_action = False
b_sound = mixer.Sound("resources/space_invaders/audios/ah_haha.mp3")
b_sound.set_volume(master_volume)

enemy_bullet_collision_sound = mixer.Sound("resources/space_invaders/audios/hitmarker.wav")
enemy_bullet_collision_sound.set_volume(master_volume)
enemy_player_collision_sound = mixer.Sound("resources/space_invaders/audios/ahhhhhhh.mp3")
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

while running:

    screen.blit(background_img, (0, 0))
    display_text("Score: " + str(score), score_font, t_x, t_y)
    display_player_health(p_health)

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

        # enemy movement
        for e in range(enemy_count):
            e_x[e] += e_dx[e]

            # boundary check
            if e_x[e] <= 0:
                e_dx[e] = -e_dx[e]
                e_y[e] += e_dy[e]
            if e_x[e] >= 750:
                e_dx[e] = -e_dx[e]
                e_y[e] += e_dy[e]

            player(enemy_icon, e_x[e], e_y[e])

            # collision with bullet
            # shift coords to middle
            if collision(e_x[e] + 25, e_y[e] + 25, b_x + 12, b_y, 32):
                enemy_bullet_collision_sound.play()
                b_action = False
                b_y = -100
                e_health[e] -= 1

                # if dead
                if e_health[e] == 0:
                    score += 100
                    # respawn
                    e_x[e], e_y[e] = random.randint(0, 750), random.randint(0, 370)
                    e_dx[e] = random.uniform(0.3, 0.7) if random.randint(0, 1) == 1 else random.uniform(-0.3, -0.7)
                    e_dy[e] = random.uniform(30, 50)
                    e_health[e] = 3

            # collision with player
            if collision(e_x[e] + 25, e_y[e] + 25, p_x + 25, p_y + 25, 25):

                e_x[e], e_y[e] = random.randint(0, 750), random.randint(0, 370)
                e_dx[e] = random.uniform(0.3, 0.7) if random.randint(0, 1) == 1 else random.uniform(-0.3, -0.7)
                e_dy[e] = random.uniform(30, 50)

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

    # game over
    else:
        for e in range(enemy_count):
            player(enemy_icon, e_x[e], e_y[e])

        player(player_icon, p_x, p_y)

        display_text("GAME OVER", game_over_font, 100, 200)

    pygame.display.update()

pygame.quit()

