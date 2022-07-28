import pygame
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
(screen_width, screen_height) = 1000, 500
screen = pygame.display.set_mode((screen_width, screen_height)) 
clock= pygame.time.Clock()

gameover = False
bar_width, bar_height = 15, 80
ball_side = 10
ball = pygame.Rect(screen_width/2-ball_side/2, screen_height/2-ball_side/2, ball_side, ball_side)
left_bar = pygame.Rect(50, screen_height/2 - bar_height/2, bar_width, bar_height) # left, top, width, height
right_bar = pygame.Rect(screen_width-50, screen_height/2 - bar_height/2, bar_width, bar_height) # left, top, width, height
right_v = 0
left_v = 0
right_Fdir = 0
Force = 2
dt = 1
ball_vx, ball_vy = 10, 10 
while not gameover:
    clock.tick(20)
    screen.fill(BLACK)
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
    if right_bar.top < 0:
        right_bar.top = 0
        if right_v < 0:
            right_v = 0
    elif right_bar.bottom > screen_height:
        right_bar.bottom = screen_height
        if right_v > 0:
            right_v = 0 
    right_bar.top += right_v * dt
    
    ball.top += ball_vy * dt
    ball.left += ball_vx * dt
    if ball.bottom > screen_height or ball.top < 0:
        ball_vy *= -1
    elif ball.colliderect(right_bar) or ball.colliderect(left_bar):
        ball_vx *= -1
    elif ball.left > screen_width:
        ball = pygame.Rect(screen_width/2-ball_side/2, 0.25*screen_height, ball_side, ball_side)
        ball_vx, ball_vy = 10, 10
    pygame.draw.rect(screen, WHITE, ball)
    pygame.draw.rect(screen, RED, left_bar)
    pygame.draw.rect(screen, BLUE, right_bar)
    pygame.display.update()
pygame.quit()

# reflection => random direction
# speed => depend on the bar speed