from typing import Set
import pygame
import os


class Settings(object):
    window_width = 600
    window_height = 800
    fps = 60
    title = "Dodging Game"
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")

class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.image = pygame.image.load(os.path.join(Settings.image_path, "bg.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(Settings.window_width, Settings.window_height))
        
    def draw(self, screen):
        screen.blit(self.image, (0,0))
        
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width / 4, self.rect.height / 4) )
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = Settings.window_width // 2
        self.rect.centery = 720
        self.lives = 3
        self.stopV()
        self.stopH()
         
    def spaceshipInitialposition(self):
        self.rect.centerx = Settings.window_width / 2
        self.rect.centery = 700
            
    def update(self):
        if self.rect.bottom + self.speed_v >= Settings.window_height:       # Läuft unten raus
            self.rect.centery -= 10
            self.stopV()
        elif self.rect.top - self.speed_v  <= 0:
            self.rect.centery += 10
            self.stopV()
        elif self.rect.left - self.speed_h >= 0:                           # Läuft links raus
            self.rect.centerx -= 10
            self.stopH() 
        elif self.rect.right + self.speed_h >= Settings.window_width:           # Läuft rechts raus
            self.rect.centerx += 10
            self.stopH()    
        else: 
            self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def stopV(self):
        self.speed_v = 0
    def stopH(self):
        self.speed_h = 0
            
    def down(self):
        self.speed_v = 3
    def up(self):
            self.speed_v = -3
    def left(self):
        self.speed_h = -3
    def right(self):
        self.speed_h = 3


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, filename1, filename2) -> None:
        super().__init__()
        self.image_normal = pygame.image.load(os.path.join(Settings.image_path, filename1)).convert_alpha()
        self.image_hit = pygame.image.load(os.path.join(Settings.image_path, filename2)).convert_alpha()
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = 300
        self.rect.centery = Settings.window_height // 2
        self.hit = False

    def update(self):
        self.image = self.image_hit if (self.hit) else self.image_normal

    def draw(self, screen):
        screen.blit(self.image, self.rect)





class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        
        self.background = Background()
        
        self.brick = Obstacle("brick1.png", "brick2.png")
        self.spaceship = Obstacle("raumschiff1.png", "raumschiff2.png")
        self.alien = Obstacle("alienbig1.png", "alienbig2.png")
        self.spaceship = Spaceship("spaceship.png")

        self.all_obstacles = pygame.sprite.Group()
        self.all_obstacles.add(self.brick)
        self.all_obstacles.add(self.spaceship)
        self.all_obstacles.add(self.alien)

        self.running = False
            
    def run(self):
        self.resize()

        self.running = True
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.update()
            self.draw()
            
        pygame.quit()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.spaceship.down()
                elif event.key == pygame.K_UP:
                    self.spaceship.up()
                elif event.key == pygame.K_LEFT:
                    self.spaceship.left()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.spaceship.stopV()
                elif event.key == pygame.K_UP:
                    self.spaceship.stopV()
                elif event.key == pygame.K_LEFT:
                    self.spaceship.stopH()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.stopH()


    def update(self):
        self.spaceship.update()
        self.all_obstacles.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen)
        self.all_obstacles.draw(self.screen)
        self.spaceship.draw(self.screen)

        pygame.display.flip()

    def resize(self):
        total_width = self.spaceship.rect.width
        total_width += self.alien.rect.width
        total_width += self.brick.rect.width

        padding = (Settings.window_width - total_width) // 4
        self.brick.rect.left = padding
        self.spaceship.rect.left = self.brick.rect.right + padding
        self.alien.rect.left = self.spaceship.rect.right + padding

if __name__ == '__main__':

    game = Game()
    game.run()
