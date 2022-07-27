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
(screen_width, screen_height) = (500, 500)
screen = pygame.display.set_mode((screen_width, screen_height)) 
clock= pygame.time.Clock()
gameover = False
while not gameover:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

pygame.quit()