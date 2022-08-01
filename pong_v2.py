import pygame
import random
import numpy as np
    
class Bar(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((15,150))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v = 0
        
    def move(self, Fdir):
        self.v += Fdir * 4
        self.rect.y += self.v
        if self.rect.y <= 102:
            self.rect.y = 102
            if self.v < 0:
                self.v = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
            if self.v > 0:
                self.v = 0
        
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y, vx, vy):
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy
        self.stuck = False
        
    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.vy *= -1
        elif self.rect.top < 100:
            self.rect.top = 100
            self.vy *= -1
        elif self.rect.left < 0:
            self.rect.left = 0
            self.vx *= -1
        elif self.rect.left > 1000:
            self.rect.x = 495
            self.rect.y = 225
            self.vx = 10
            self.vy = 10
    
    def collide(self, bar):
        if self.rect.colliderect(bar.rect) and not self.stuck:
            theta = min((0.1+bar.v / 90) * np.pi, 0.4*np.pi)
            self.vx *= -1
            self.vy = random.choice([1, -1]) * self.vx * np.tan(theta)
            self.stuck = True
        else:
            self.stuck = False
            
def main():
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
    all_sprites_list = pygame.sprite.Group()
    right_bar = Bar(BLUE, 950, 275)
    all_sprites_list.add(right_bar)
    right_Fdir = 0
    ball_v = random.choice([(10,10), (10,-10)])
    ball = Ball(WHITE, 495, 245, ball_v[0], ball_v[1])
    all_sprites_list.add(ball)
    gameover = False
    while not gameover:
        clock.tick(30)
        screen.fill(BLACK)
        pygame.draw.line(screen, YELLOW, (0,95), (1000,95), 10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    right_Fdir = -1
                elif event.key == pygame.K_DOWN:
                    right_Fdir = 1
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    right_Fdir = 0
        right_bar.move(right_Fdir)
        ball.move()
        ball.collide(right_bar)
        all_sprites_list.draw(screen)
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()