import math
import pygame
import json
import os

from resources.levels import level1
from pygame import mixer

# initialise pygame
pygame.init()

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3
LEVELS = 4
SETTINGS = 5

# Current game state
game_state = MENU

master_volume = 0.1
fps = 60
delay_tick = 0
current_level = 1
save_file = "save_game.json"

# create the screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_img = pygame.image.load("resources/images/space_background.jpg")
background_music = mixer.Sound("resources/audios/ppk_resurrection.mp3")
background_music.set_volume(master_volume)
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

# enemies (will be initialized properly in reset_game)
enemy_list = []
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


def draw_button(text, font, x, y, width, height, inactive_color, active_color, mouse_pos, clicked):
    """Draw a button and return True if clicked"""
    mouse_x, mouse_y = mouse_pos
    if x < mouse_x < x + width and y < mouse_y < y + height:
        color = active_color
        if clicked:
            return True
    else:
        color = inactive_color
    
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)
    return False


def reset_game():
    """Reset game to initial state"""
    global p_x, p_y, p_dx, p_health, score, game_over, win
    global enemy_list, active_enemy_list, delay_tick, killed_enemies
    global b_x, b_y, b_action
    
    p_x, p_y = 375, 480
    p_dx = 0
    p_health = 5
    score = 0
    game_over = False
    win = False
    enemy_list = level1.enemy_list.copy()
    active_enemy_list = []
    delay_tick = 0
    killed_enemies = []
    b_x, b_y = -100, -100
    b_action = False


def load_game():
    """Load saved game state"""
    global p_x, p_y, p_health, score, current_level, enemy_list, active_enemy_list
    
    if os.path.exists(save_file):
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                p_x = save_data.get('p_x', 375)
                p_y = save_data.get('p_y', 480)
                p_health = save_data.get('p_health', 5)
                score = save_data.get('score', 0)
                current_level = save_data.get('current_level', 1)
                # Reset enemy list for now (can be enhanced later)
                enemy_list = level1.enemy_list.copy()
                active_enemy_list = []
                return True
        except:
            return False
    return False


def save_game():
    """Save current game state"""
    save_data = {
        'p_x': p_x,
        'p_y': p_y,
        'p_health': p_health,
        'score': score,
        'current_level': current_level
    }
    try:
        with open(save_file, 'w') as f:
            json.dump(save_data, f)
        return True
    except:
        return False


def draw_menu():
    """Draw main menu screen"""
    global game_state
    
    title_font = pygame.font.Font('freesansbold.ttf', 64)
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    # Check for mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_clicked = True
    
    # Draw title
    title_text = title_font.render("WEE INVADERS", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 150))
    screen.blit(title_text, title_rect)
    
    # Draw buttons
    button_y_start = 250
    button_spacing = 70
    button_width = 300
    button_height = 50
    
    if draw_button("New Game", button_font, 250, button_y_start, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        reset_game()
        game_state = PLAYING
        background_music.play(-1)
    
    if draw_button("Continue", button_font, 250, button_y_start + button_spacing, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        if load_game():
            game_state = PLAYING
            background_music.play(-1)
    
    if draw_button("Levels", button_font, 250, button_y_start + button_spacing * 2, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        game_state = LEVELS
    
    if draw_button("Settings", button_font, 250, button_y_start + button_spacing * 3, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        game_state = SETTINGS
    
    return True


def draw_levels():
    """Draw levels selection screen"""
    global game_state, current_level
    
    title_font = pygame.font.Font('freesansbold.ttf', 48)
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = MENU
                return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
    
    # Draw title
    title_text = title_font.render("SELECT LEVEL", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 100))
    screen.blit(title_text, title_rect)
    
    # Draw level buttons (for now just Level 1)
    button_width = 300
    button_height = 60
    
    if draw_button("Level 1", button_font, 250, 200, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        current_level = 1
        reset_game()
        game_state = PLAYING
        background_music.play(-1)
    
    # Back button
    if draw_button("Back", button_font, 250, 500, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        game_state = MENU
    
    return True


def draw_settings():
    """Draw settings screen"""
    global game_state, master_volume
    
    title_font = pygame.font.Font('freesansbold.ttf', 48)
    text_font = pygame.font.Font('freesansbold.ttf', 24)
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = MENU
                return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
    
    # Draw title
    title_text = title_font.render("SETTINGS", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 100))
    screen.blit(title_text, title_rect)
    
    # Draw volume info
    volume_text = text_font.render(f"Volume: {int(master_volume * 100)}%", True, (255, 255, 255))
    screen.blit(volume_text, (300, 250))
    
    # Volume buttons
    button_width = 150
    button_height = 50
    
    if draw_button("-", button_font, 300, 300, 50, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        master_volume = max(0.0, master_volume - 0.1)
        background_music.set_volume(master_volume)
    
    if draw_button("+", button_font, 450, 300, 50, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        master_volume = min(1.0, master_volume + 0.1)
        background_music.set_volume(master_volume)
    
    # Back button
    if draw_button("Back", button_font, 250, 500, 300, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        game_state = MENU
    
    return True


def draw_game_over_screen():
    """Draw game over screen with retry and menu options"""
    global game_state
    
    title_font = pygame.font.Font('freesansbold.ttf', 64)
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
    
    # Draw game over text
    display_text("GAME OVER", title_font, 100, 200)
    
    # Draw buttons
    button_width = 250
    button_height = 50
    
    if draw_button("Retry Level", button_font, 150, 350, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        reset_game()
        game_state = PLAYING
        background_music.play(-1)
    
    if draw_button("Main Menu", button_font, 400, 350, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        game_state = MENU
        background_music.play(-1)
    
    return True


def draw_win_screen():
    """Draw win screen with continue and menu options"""
    global game_state, current_level
    
    title_font = pygame.font.Font('freesansbold.ttf', 64)
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
    
    # Draw win text
    display_text("YOU WIN!", title_font, 180, 200)
    
    # Draw score
    score_text = button_font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (300, 280))
    
    # Draw buttons
    button_width = 250
    button_height = 50
    
    # For now, "Next Level" just goes back to level 1
    # This can be enhanced when more levels are added
    if draw_button("Next Level", button_font, 150, 380, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        current_level += 1
        reset_game()
        game_state = PLAYING
        background_music.play(-1)
    
    if draw_button("Main Menu", button_font, 400, 380, button_width, button_height,
                   (100, 100, 100), (150, 150, 150), mouse_pos, mouse_clicked):
        save_game()
        game_state = MENU
        background_music.play(-1)
    
    return True


# Initialize enemy list
enemy_list = level1.enemy_list.copy()

# game loop
running = True
reset_e = False
killed_enemies = []

while running:

    screen.blit(background_img, (0, 0))
    clock.tick(60)

    # Handle different game states
    if game_state == MENU:
        running = draw_menu()
        pygame.display.update()
        continue
    
    elif game_state == LEVELS:
        running = draw_levels()
        pygame.display.update()
        continue
    
    elif game_state == SETTINGS:
        running = draw_settings()
        pygame.display.update()
        continue
    
    elif game_state == GAME_OVER:
        # Draw game elements in background
        for e in range(len(active_enemy_list)):
            player(enemy_icon, active_enemy_list[e]["e_x"], active_enemy_list[e]["e_y"])
        player(player_icon, p_x, p_y)
        
        running = draw_game_over_screen()
        pygame.display.update()
        continue
    
    elif game_state == WIN:
        # Draw game elements in background
        for e in range(len(active_enemy_list)):
            player(enemy_icon, active_enemy_list[e]["e_x"], active_enemy_list[e]["e_y"])
        player(player_icon, p_x, p_y)
        
        running = draw_win_screen()
        pygame.display.update()
        continue
    
    # PLAYING state
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
            if event.key == pygame.K_ESCAPE:
                save_game()
                game_state = MENU
                background_music.stop()

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
                        game_state = WIN

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
                        game_state = GAME_OVER
                    else:
                        enemy_player_collision_sound.play()

        if len(killed_enemies) > 0:
            # Sort in reverse order to avoid index issues when popping
            killed_enemies.sort(reverse=True)
            for enemy in killed_enemies:
                if enemy < len(active_enemy_list):
                    active_enemy_list.pop(enemy)
            killed_enemies = []

    pygame.display.update()

pygame.quit()

