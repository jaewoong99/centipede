import pygame
import random
import numpy as np

pygame.init()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
title = "pong"
pygame.display.set_caption(title)
border = 100
game_height = 500
(screen_width, screen_height) = 1000, border + game_height
screen = pygame.display.set_mode((screen_width, screen_height)) 
clock= pygame.time.Clock()

gameover = False
bar_width, bar_height = 15, 150
ball_side = 10
ball = pygame.Rect(screen_width/2-ball_side/2, (border+game_height/2)-ball_side/2, ball_side, ball_side)
#left_bar = pygame.Rect(50, screen_height/2 - bar_height/2, bar_width, bar_height) # left, top, width, height
right_bar = pygame.Rect(screen_width-50, border+game_height/2 - bar_height/2, bar_width, bar_height) # left, top, width, height
Border = pygame.Rect(0, 0, screen_width, border)
right_v = 0
left_v = 0
right_Fdir = 0
Force = 4
dt = 1
right_miss = 0
ball_vx, ball_vy = random.choice([(10, 10), (10,-10)])
while not gameover:
    clock.tick(30)
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, Border)
    text = large_font.render( "miss : {}".format(right_miss), True, (0,0,0) )
    screen.blit(text, (100,30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                right_Fdir = 1
            elif event.key == pygame.K_DOWN:
                right_Fdir = -1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_Fdir = 0
    right_v -= right_Fdir * Force * dt
    if right_bar.top < border:
        right_bar.top = border
        if right_v < 0:
            right_v = 0
    elif right_bar.bottom > screen_height:
        right_bar.bottom = screen_height
        if right_v > 0:
            right_v = 0 
    right_bar.top += right_v * dt
    
    ball.top += ball_vy * dt
    ball.left += ball_vx * dt
    if ball.bottom > screen_height or ball.top < border:
        ball_vy *= -1
    elif ball.colliderect(right_bar) and not stuck:
        theta = right_v / 30 * np.pi/3
        ball_vx *= -1
        ball_vy = random.choice([1,-1]) * ball_vx * np.tan(theta)
        stuck = True
    elif ball.left > screen_width:
        ball = pygame.Rect(screen_width/2-ball_side/2, border+0.25*game_height, ball_side, ball_side)
        ball_vx, ball_vy = random.choice([(10,10), (10,-10)])
        right_miss += 1
    elif ball.left < 0: # For a single player mode
        ball_vx *= -1
    else:
        stuck = False
    pygame.draw.rect(screen, WHITE, ball)
    #pygame.draw.rect(screen, RED, left_bar)
    pygame.draw.rect(screen, BLUE, right_bar)
    pygame.display.update()
pygame.quit()

# reflection => random direction
# speed => depend on the bar speed