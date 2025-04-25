import pygame # pygame library (https://www.pygame.org/)
pygame.init() # initialize pygame
from random import randint # for placement of apple
import sys

sys.stdin = open("High Score.txt", "r") # access high score saved to file

# initialize variables and grid
snake_length = 3
snake = [[7, 7], [6, 7], [5, 7]] # location of snake starting from head
prev_snake = [[6, 7], [5, 7], [4, 7]] # location of snake during previous move frame
head_dir = "East" # direction to change snake head to at the next possible move frame
curr_dir = "East" # actual direction of snake head at any given moment
high_score = int(input())
framerate = 144
move_frame = 18 # set to move every nth frame (must be set to common divisor of frame_rate and move_distance)
move_distance = 72 // move_frame # distance to move every frame

# place apple on random location that isn't part of snake
def apple(snake):
    apple = snake[0].copy()
    while apple in snake:
        apple[0] = randint(0, 15)
        apple[1] = randint(0, 14)
    return apple

# initialize apple
apple_location = [13, 7]

# take in snake as parameter and add 1 length to its tail
def eat(snake):
    global snake_length
    global apple_location
    snake_length += 1
    x = snake[-1][0] + (snake[-1][0] - snake[-2][0]) # set x coordinate of the additional body
    y = snake[-1][1] + (snake[-1][1] - snake[-2][1]) # set y coordinate of the additional body
    if x > 15: # logic to place body somewhere else if position of additional body points to out of grid
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
    apple_location = apple(snake) # place new apple

# move snake towards its current direction
def move(dir):
    if dir == "North": # move head towards direction
        move_to = [snake[0][0], snake[0][1] - 1]
        if move_to[1] < 0: # check for out of board
            death_screen()
    if dir == "South":
        move_to = [snake[0][0], snake[0][1] + 1]
        if move_to[1] > 14:
            death_screen()
    if dir == "East":
        move_to = [snake[0][0] + 1, snake[0][1]]
        if move_to[0] > 15:
            death_screen()
    if dir == "West":
        move_to = [snake[0][0] - 1, snake[0][1]]
        if move_to[0] < 0:
            death_screen()
    for i in range(len(snake)): # make rest of body follow head movement
        if move_to in snake: # check for body collision
            death_screen()
        temp = snake[i]
        snake[i] = move_to
        move_to = temp
    if snake[0] == apple_location: # check for apple eaten
        eat(snake)


def draw(frame, dir): # draw board, snake, and apple onto pygame surface object and return it
    board_s = grid_s.copy() # intializes board surface from grid surface
    board_s.blit(apple_s, (apple_location[0] * 72 + 3, apple_location[1] * 72 + 3)) # draw apple
    distance_times_frame = move_distance * (frame % move_frame)
    for i in range(len(prev_snake)): # draw snake based on current direction and in-between (move) frame
        if dir == "East":
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3 + (distance_times_frame), prev_snake[i][1] * 72 + 3))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3 + (distance_times_frame), prev_snake[i][1] * 72 + 3))
        elif dir == "West":
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3 - (distance_times_frame), prev_snake[i][1] * 72 + 3))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3 - (distance_times_frame), prev_snake[i][1] * 72 + 3))
        elif dir == "North":
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 - (distance_times_frame)))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 - (distance_times_frame)))
        elif dir == "South":
            if i == 0:
                board_s.blit(snake_head, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 + (distance_times_frame)))
            else:
                board_s.blit(snake_body, (prev_snake[i][0] * 72 + 3, prev_snake[i][1] * 72 + 3 + (distance_times_frame)))
        
        if prev_snake[i][0] - prev_snake[min(len(prev_snake) - 1, i + 1)][0] > 0: # set direction to move next part of body to
            dir = "East"
        elif prev_snake[i][0] - prev_snake[min(len(prev_snake) - 1, i + 1)][0] < 0:
            dir = "West"
        elif prev_snake[i][1] - prev_snake[min(len(prev_snake) - 1, i + 1)][1] > 0:
            dir = "South"
        elif prev_snake[i][1] - prev_snake[min(len(prev_snake) - 1, i + 1)][1] < 0:
            dir = "North"
    return board_s

# initialize screen space and sprites
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
jetbrains_mono = pygame.font.Font("JetBrainsMono-Regular.ttf", 45)
title_instructions_text = jetbrains_mono.render("Press any key to start playing (or esc to exit).", True, (255, 255, 255))
clock = pygame.time.Clock()
cell = pygame.image.load("cell.png").convert()
grid_s = pygame.Surface((1152, 1080))
for x in range(1080 // 15):
        for y in range(1080 // 15):
            grid_s.blit(cell, (x * 72, y * 72))
snake_body = pygame.image.load("snake.png").convert()
snake_head = pygame.image.load("snake_head.png").convert()
apple_s = pygame.image.load("apple.png").convert()

frame_count = 0
title_width, title_height = title_instructions_text.get_size()
screen.blit(title_instructions_text, (960 - (title_width // 2), 540 - (title_height // 2)))
while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        exit()
    elif 1 in keys:
        break
    pygame.event.pump()
    pygame.display.update()

# main game loop
while True:
    frame_count += 1
    keys = pygame.key.get_pressed() # change direction based on keyboard input
    if keys[pygame.K_w] and curr_dir != "South":
        head_dir = "North"
    if keys[pygame.K_a] and curr_dir != "East":
        head_dir = "West"
    if keys[pygame.K_d] and curr_dir != "West":
        head_dir = "East"
    if keys[pygame.K_s] and curr_dir != "North":
        head_dir = "South"
    score = jetbrains_mono.render("Score: " + str(snake_length - 3), True, (255, 255, 255))
    high_score_text = jetbrains_mono.render("High Score: " + str(high_score), True, (255, 255, 255))
    if frame_count % move_frame == 0: # move snake every move_frame frames
        prev_snake = snake.copy()
        move(head_dir)
        curr_dir = head_dir
    screen.fill((0, 0, 0))
    curr_board_s = draw(frame_count, curr_dir)
    screen.blit(curr_board_s, (384, 0)) # draw board, score, and high score onto screen
    screen.blit(score, (0, 0))
    screen.blit(high_score_text, (0, 50))
    clock.tick(framerate) # pause loop for a certain amount of time to maintain framerate
    pygame.event.pump()
    pygame.display.update()
    if frame_count == framerate: # reset frame count once it reaches 120
        frame_count = 0
