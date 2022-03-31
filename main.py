import pygame
import game
from time import sleep
from pygame.locals import *
from constants import *
from random import randint

global player_1
global player_2
global ball
global objects_list

score = [0, 0]


def stop_game():
    sleep(STOP_TIME)
    game_init()


def objects_init():
    global player_1
    global player_2
    global ball

    player_1 = game.Player()
    player_2 = game.Player()
    ball = game.Ball()

    player_1.colision.set_values(PLAYERS_SIZE, PLAYER_1_COLOR)
    player_2.colision.set_values(PLAYERS_SIZE, PLAYER_2_COLOR)
    ball.colision.set_values([BALL_RADIUS * 2, BALL_RADIUS * 2], BALL_COLOR)

    ball.x = BALL_POSITION[0]
    ball.y = BALL_POSITION[1]
    player_1.x = PLAYER_1_X
    player_1.y = PLAYER_1_Y
    player_2.x = PLAYER_2_X
    player_2.y = PLAYER_2_Y

    player_1.vetor.speed_x = player_2.vetor.speed_x = PLAYER_SPEED
    ball.vetor.speed_x = ball.vetor.speed_y = BALL_SPEED

    ball.circle.radius = BALL_RADIUS
    ball.circle.center = [ball.x + BALL_RADIUS, ball.y + BALL_RADIUS]
    ball.circle.color = BALL_COLOR


def objects():
    global objects_list
    objects_list = [player_1, player_2, ball]

    update_objects()
    draw_objects()


def update_objects():
    for obj in objects_list:
        obj.update()


def draw_objects():
    for obj in objects_list:
        if obj.colision.visible:
            pygame.draw.rect(screen, obj.colision.color, obj.colision.rect)
        try:
            pygame.draw.circle(screen, obj.circle.color, obj.circle.center, obj.circle.radius)
        except:
            pass


def game_init():
    pygame.init()
    objects_init()
    window = pygame.display.set_mode(SIZE)
    return window


def game_update():
    bg_update()
    objects()
    colisions()
    pygame.display.flip()


def bg_update():
    pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, HEIGHT))


def colisions():
    global score
    # with players
    if ball.colision_with(player_2):
        ball.vetor.y = -ball.vetor.speed_y
    elif ball.colision_with(player_1):
        ball.vetor.y = ball.vetor.speed_y

    # with borders
    if ball.border_right >= screen.get_size()[0]:
        ball.vetor.x = -ball.vetor.speed_x
    elif ball.border_left <= 0:
        ball.vetor.x = ball.vetor.speed_x
    if ball.border_up <= 0:
        score[0] += 1
        stop_game()
    elif ball.border_down >= screen.get_size()[1]:
        score[1] += 1
        stop_game()


# GAME
screen = game_init()

while True:
    pygame.time.delay(6)

    for event in pygame.event.get():
        if event.type == QUIT:
            quit(0)

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                ball.vetor.x = ball.vetor.speed_x if randint(1, 2) == 1 else -ball.vetor.speed_x
                ball.vetor.y = ball.vetor.speed_y if randint(1, 2) == 1 else -ball.vetor.speed_y

            if event.key == K_RIGHT:
                player_2.keys.add('RIGHT')
            if event.key == K_LEFT:
                player_2.keys.add('LEFT')
            if event.key == K_d:
                player_1.keys.add('RIGHT')
            if event.key == K_a:
                player_1.keys.add('LEFT')

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player_2.keys.remove('RIGHT')
            if event.key == K_LEFT:
                player_2.keys.remove('LEFT')
            if event.key == K_d:
                player_1.keys.remove('RIGHT')
            if event.key == K_a:
                player_1.keys.remove('LEFT')

    game_update()
