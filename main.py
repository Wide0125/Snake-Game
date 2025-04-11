import pygame

pygame.init()
from random import randint
import sys

sys.stdin = open('High Score.txt', 'r')

SL = 3
snake = [[7, 7], [6, 7], [5, 7]]
prev_snake = [[6, 7], [5, 7], [4, 7]]
head_dir = 'East'
curr_dir = 'East'
tail_dir = 'West'
board = [[0] * 16 for _ in range(15)]
for i in range(len(snake)):
    if i == 0:
        board[snake[i][1]][snake[i][0]] = 2
    else:
        board[snake[i][1]][snake[i][0]] = 1
high_score = int(input())
frame_rate = 120
move_frame = 12
move_distance = 72 // move_frame


def apple(snake):
    apple = snake[0].copy()
    while apple in snake:
        apple[0] = randint(0, 15)
        apple[1] = randint(0, 14)
    return apple


AL = [13, 7]
prev_AL = AL.copy()


def eat(snake):
    global SL
    global AL
    global prev_AL
    SL += 1
    x = snake[-1][0] + (snake[-1][0] - snake[-2][0])
    y = snake[-1][1] + (snake[-1][1] - snake[-2][1])
    if x > 15:
        x -= 1
        if y == 0:
            y += 1
        else:
            y -= 1
    elif x < 0:
        x += 1
        if y == 0:
            y += 1
        else:
            y -= 1
    elif y > 14:
        y -= 1
        if x == 0:
            x += 1
        else:
            x -= 1
    elif y < 0:
        y += 1
        if x == 0:
            x += 1
        else:
            x -= 1
    snake.append([x, y])
    AL = apple(snake)


def move(dir):
    global curr_dir
    global prev_AL
    if dir == 'North':
        prev_location = [snake[0][0], snake[0][1] - 1]
        curr_dir = 'North'
        if prev_location[1] < 0:
            death()
    if dir == 'South':
        prev_location = [snake[0][0], snake[0][1] + 1]
        curr_dir = 'South'
        if prev_location[1] > 14:
            death()
    if dir == 'East':
        prev_location = [snake[0][0] + 1, snake[0][1]]
        curr_dir = 'East'
        if prev_location[0] > 15:
            death()
    if dir == 'West':
        prev_location = [snake[0][0] - 1, snake[0][1]]
        curr_dir = 'West'
        if prev_location[0] < 0:
            death()
    for i in range(len(snake)):
        if prev_location in snake:
            death()
        temp = snake[i]
        snake[i] = prev_location
        prev_location = temp
    for j in range(len(snake)):
        if j == 0:
            board[snake[j][1]][snake[j][0]] = 2
        else:
            board[snake[j][1]][snake[j][0]] = 1
    board[prev_location[1]][prev_location[0]] = 0
    prev_AL = AL.copy()
    if snake[0][0] == AL[0] and snake[0][1] == AL[1]:
        eat(snake)


def draw(frame, dir):
    prev_dir = dir
    board_s.fill((0, 0, 0))
    for x in range(1080 // 15):
        for y in range(1080 // 15):
            board_s.blit(cell, (x * 72, y * 72))
    board_s.blit(apple_s, (prev_AL[0] * 72 + 3, prev_AL[1] * 72 + 3))
    for i in range(len(prev_snake)):
        if prev_dir == 'East':
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3 + (move_distance * (frame % move_frame)), prev_snake[i][1] * 72 + 3))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3 + (move_distance * (frame % move_frame)), prev_snake[i][1] * 72 + 3))
        elif prev_dir == 'West':
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3 - (move_distance * (frame % move_frame)), prev_snake[i][1] * 72 + 3))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3 - (move_distance * (frame % move_frame)), prev_snake[i][1] * 72 + 3))
        elif prev_dir == 'North':
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 - (move_distance * (frame % move_frame))))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 - (move_distance * (frame % move_frame))))
        elif prev_dir == 'South':
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 + (move_distance * (frame % move_frame))))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 + (move_distance * (frame % move_frame))))
        if prev_snake[i][0] - prev_snake[min(len(prev_snake) - 1, i + 1)][0] > 0:
            prev_dir = 'East'
        elif prev_snake[i][0] - prev_snake[min(len(prev_snake) - 1, i + 1)][0] < 0:
            prev_dir = 'West'
        elif prev_snake[i][1] - prev_snake[min(len(prev_snake) - 1, i + 1)][1] > 0:
            prev_dir = 'South'
        elif prev_snake[i][1] - prev_snake[min(len(prev_snake) - 1, i + 1)][1] < 0:
            prev_dir = 'North'


def death():
    sys.stdout = open('High Score.txt', 'w')
    print(max(high_score, SL - 3))
    pygame.quit()
    raise SystemExit


screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
myFont = pygame.font.Font('JetBrainsMono-Regular.ttf', 45)
clock = pygame.time.Clock()
board_s = pygame.Surface((1152, 1080))
cell = pygame.image.load('cell.png').convert()
snake_body = pygame.image.load('snake.png').convert()
snake_head = pygame.image.load('snake_head.png').convert()
blank = pygame.image.load('blank.png').convert()
apple_s = pygame.image.load('apple.png').convert()

frame_count = 0
while True:
    frame_count += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and curr_dir != 'South':
        head_dir = 'North'
    if keys[pygame.K_a] and curr_dir != 'East':
        head_dir = 'West'
    if keys[pygame.K_d] and curr_dir != 'West':
        head_dir = 'East'
    if keys[pygame.K_s] and curr_dir != 'North':
        head_dir = 'South'
    if keys[pygame.K_ESCAPE]:
        death()
    score = myFont.render("Score: " + str(SL - 3), True, (255, 255, 255))
    high_score_text = myFont.render("High Score: " + str(high_score), True, (255, 255, 255))
    if frame_count % move_frame == 0:
        prev_snake = snake.copy()
        move(head_dir)
        head_dir = curr_dir
    screen.fill((0, 0, 0))
    draw(frame_count, curr_dir)
    screen.blit(board_s, (384, 0))
    screen.blit(score, (0, 0))
    screen.blit(high_score_text, (0, 50))
    clock.tick(frame_rate)
    pygame.event.pump()
    pygame.display.update()
    if frame_count == frame_rate:
        frame_count = 0
