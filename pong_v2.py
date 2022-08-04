import pygame
import random
import numpy as np
    
class Bar(pygame.sprite.Sprite):
    def __init__(self, color, x, y, type = 2):
        super().__init__()
        if type == 1:
            self.image = pygame.Surface((150,150))
        elif type == 2:
            self.image = pygame.Surface((15,150))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v = 0
        self.dir = 0
    def move(self, Fdir):
        self.dir = Fdir
        self.v += self.dir * 4
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
    def __init__(self, color, x, y, vx, vy, type=2):
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy
        self.stuck = False
        self.right_miss = 0
        self.left_miss = 0
        self.type = type
        self.refl = 0
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
            if self.type == 2:
                self.left_miss += 1
                self.rect.x = 495
                self.rect.y = 500
                self.vx = -10
                self.vy = -10
            elif self.type == 1:
                self.refl += 1
                self.vx *= -1.2
        elif self.rect.left > 1000:
            self.right_miss += 1
            self.rect.x = 495
            self.rect.y = 190
            self.vx = 10
            self.vy = 10
    def collide(self, bar):
        if self.rect.colliderect(bar.rect):
            if not self.stuck:
                theta = min((0.1+bar.v / 90) * np.pi, 0.4*np.pi)
                self.vx *= -1
                self.vy = random.choice([1, -1]) * self.vx * np.tan(theta)
                self.stuck = True
        else:
            self.stuck = False
            
class Game:
    def __init__(self):
        pygame.init()
        self.large_font = pygame.font.SysFont(None, 72)
        self.small_font = pygame.font.SysFont(None, 50)
        title = "pong"
        pygame.display.set_caption(title)
        # border = 100
        # game_height = 500
        self.screen = pygame.display.set_mode((1000, 600)) 
        self.clock= pygame.time.Clock()
    def button(self, position, text):
        screen = self.screen
        text_render = self.small_font.render(text, 1, (255, 0, 0))
        x, y, w , h = text_render.get_rect()
        x, y = position
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
        return screen.blit(text_render, (x, y))
    def lobby(self):
        choose = False
        while not choose:
            self.screen.fill((252, 186, 3))
            option1 = self.button((200,200), "Single")
            option2 = self.button((700, 200), "Double")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choose = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if option1.collidepoint(pygame.mouse.get_pos()):
                        choose = True
                        self.single_gamestart()
                    elif option2.collidepoint(pygame.mouse.get_pos()):
                        choose = True
                        self.double_gamestart()
            pygame.display.update()
    def single_gamestart(self):
        BLACK = (0, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        WHITE = (255, 255, 255)
        YELLOW = (255, 255, 0)
        all_sprites_list = pygame.sprite.Group()
        right_bar = Bar(BLUE, 985, 275, 1)
        all_sprites_list.add(right_bar)
        ball_v = random.choice([(10,10), (10,-10)])
        ball = Ball(WHITE, 495, 245, ball_v[0], ball_v[1], 1)
        all_sprites_list.add(ball)
        gameover = False
        while not gameover:
            self.clock.tick(30)
            self.screen.fill(BLACK)
            score_right = self.large_font.render("score:{}".format(ball.refl),True, GREEN)
            self.screen.blit(score_right, (400,30))
            pygame.draw.line(self.screen, YELLOW, (0,95), (1000,95), 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        right_bar.dir = -1
                    elif event.key == pygame.K_DOWN:
                        right_bar.dir = 1
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        right_bar.dir = 0
            right_bar.move(right_bar.dir)
            ball.move()
            if ball.rect.right > 940:
                ball.collide(right_bar)
            all_sprites_list.draw(self.screen)
            pygame.display.update()
            if ball.right_miss == 3:
                gameover = True
                self.gameover()
    def double_gamestart(self):
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        WHITE = (255, 255, 255)
        YELLOW = (255, 255, 0)
        all_sprites_list = pygame.sprite.Group()
        right_bar = Bar(BLUE, 950, 275)
        left_bar = Bar(RED, 35, 275)
        all_sprites_list.add(right_bar)
        all_sprites_list.add(left_bar)
        ball_v = random.choice([(10,10), (10,-10)])
        ball = Ball(WHITE, 495, 245, ball_v[0], ball_v[1])
        all_sprites_list.add(ball)
        gameover = False
        while not gameover:
            self.clock.tick(30)
            self.screen.fill(BLACK)
            score_left = self.large_font.render("red score:{}".format(ball.right_miss),True, GREEN)
            score_right = self.large_font.render("blue score:{}".format(ball.left_miss),True, GREEN)
            self.screen.blit(score_left, (100,30))
            self.screen.blit(score_right, (700,30))
            pygame.draw.line(self.screen, YELLOW, (0,95), (1000,95), 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        right_bar.dir = -1
                    elif event.key == pygame.K_DOWN:
                        right_bar.dir = 1
                    elif event.key == pygame.K_w:
                        left_bar.dir = -1
                    elif event.key == pygame.K_s:
                        left_bar.dir = 1
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        right_bar.dir = 0
                    elif event.key in [pygame.K_w, pygame.K_s]:
                        left_bar.dir = 0
            right_bar.move(right_bar.dir)
            left_bar.move(left_bar.dir)
            ball.move()
            if ball.rect.right > 940:
                ball.collide(right_bar)
            elif ball.rect.left <= 60:
                ball.collide(left_bar)
            all_sprites_list.draw(self.screen)
            pygame.display.update()
            if ball.right_miss == 3 or ball.left_miss == 3:
                gameover = True
                self.gameover()
        
    def gameover(self):
        decision = False
        bg = (52, 235, 180)
        self.screen.fill(bg)
        gameovertext = self.large_font.render("Restart? yes=y, no=n, lobby=l", True, (235, 52, 125))
        self.screen.blit(gameovertext, (0,300))
        while not decision:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    decision = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        decision = True
                        self.double_gamestart()
                    elif event.key == pygame.K_n:
                        decision = True
                    elif event.key == pygame.K_l:
                        decision = True
                        self.lobby()
            pygame.display.update()
        pygame.quit()
    
if __name__ == "__main__":
    game = Game()
    game.lobby()