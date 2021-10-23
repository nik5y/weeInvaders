import pygame

# initialise pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# title and icon
pygame.display.set_caption("Space Invaders")

# player
p_x, p_y = 370, 480


def player(p_x, p_y):
    screen.blit(pygame.Surface((10, 10)), (p_x, p_y))


fps = 30
fps_wait = [0.25, 0.25, 0.1, 0.1, 0.1, 0.1, 0.05]


def update_direction_old(mode, d, u, l, r):
    if mode.upper() == "DOWN":
        return d+1, 0, 0, 0
    elif mode.upper() == "UP":
        return 0, u+1, 0, 0
    elif mode.upper() == "LEFT":
        return 0, 0, l+1, 0
    elif mode.upper() == "RIGHT":
        return 0, 0, 0, r+1
    elif mode.upper() == "RESET":
        return 0, 0, 0, 0
    else:
        raise ValueError("wrong input for mode")


def update_direction(mode, direction_dict):

    if mode.lower() == "reset":
        direction_dict = dict.fromkeys(direction_dict, 0)
        return direction_dict
    elif mode.lower() in ["down", "up", "left", "right"]:
        temp = direction_dict[mode] + 1
        direction_dict = dict.fromkeys(direction_dict, 0)
        direction_dict[mode] = temp
        return direction_dict
    else:
        raise ValueError("wrong input for mode")


# game loop
running = True

# speed is shared among directions so that once player speeds up in one direction,
# he/she can turn yet retain the speed
speed = 0

directions = ["down", "up", "left", "right"]

direction_keys = {
    "down": pygame.K_DOWN,
    "up": pygame.K_UP,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

direction_ticks = {
    "down": 0,
    "up": 0,
    "left": 0,
    "right": 0
}


def move_player(x, y, direction, change):
    if direction == "down":
        return x, y + change
    elif direction == "up":
        return x, y - change
    elif direction == "left":
        return x - change, y
    elif direction == "right":
        return x + change, y
    else:
        raise ValueError("wrong direction")


while running:

    clock.tick(fps)
    screen.fill((168, 184, 117))
    # controls with holding
    # get pressed keys
    keys = pygame.key.get_pressed()
    # check for each direction key
    for direction in directions:
        if keys[direction_keys[direction]]:
            # make one move as soon as pressed
            if speed == 0 and direction_ticks[direction] == 0:
                p_x, p_y = move_player(p_x, p_y, direction, 10)

            # update amount of ticks per direction
            direction_ticks = update_direction(direction, direction_ticks)

            # check if required amount of ticks is reached
            # multiplied by fps to ensure same speed across fps's
            if direction_ticks[direction] == round(fps_wait[speed] * fps):
                # move
                p_x, p_y = move_player(p_x, p_y, direction, 10)
                # resetting ticks to start tick count for next movement
                direction_ticks = update_direction("reset", direction_ticks)
                # update index that controls required amount of ticks per movement
                if speed < len(fps_wait) - 1:
                    speed += 1

    # if no keys are pressed, reset tick counts and required tick count per movement
    if len(set(pygame.key.get_pressed())) == 1:
        direction_ticks = update_direction("reset", direction_ticks)
        speed = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN:
        #         p_y += 10
        #         print("down")
        #     if event.key == pygame.K_UP:
        #         p_y -= 10
        #         print("up")
        #     if event.key == pygame.K_LEFT:
        #         p_x -= 10
        #         print("left")
        #     if event.key == pygame.K_RIGHT:
        #         p_x += 10
        #         print("right")

    player(p_x, p_y)

    pygame.display.update()

pygame.quit()



# def action_switch(action, dt, limit, fps):
#     if dt > limit:
#         action()
#         dt += clock.tick(fps)
#     return dt
#
#
# def blip():
#     screen.blit(pygame.Surface((10, 10)), (100, 100))

# dt += clock.tick(fps)
#


# if keys[pygame.K_DOWN]:
#     d, u, l, r = update_direction("down", d, u, l, r)
#     if d == fps_wait[speed] * fps:
#         d, u, l, r = update_direction("reset", d, u, l, r)
#         p_y += 10
#         print(speed)
#         if speed < len(fps_wait) - 1:
#             speed += 1
#     print("down")
# if keys[pygame.K_UP]:
#     p_y -= 10
#     print("up")
# if keys[pygame.K_LEFT]:
#     p_x -= 10
#     print("left")
# if keys[pygame.K_RIGHT]:
#     p_x += 10
#     print("right")
#
# if len(set(pygame.key.get_pressed())) == 1:
#     d, u, l, r = update_direction("reset", d, u, l, r)
#     speed = 0
