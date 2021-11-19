from random import randint
import pygame
import os


class Settings(object):
    window_width = 600
    window_height = 800
    fps = 60
    title = "Dodging Game"
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    nof_asteroids = 3

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
        self.image = pygame.transform.scale(self.image, (self.rect.width / 6, self.rect.height / 6) )
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
        if self.rect.bottom + self.speed_v >= Settings.window_height and self.speed_v != 0:           # Läuft unten raus
            self.rect.centery -= 10
            self.stopV()
        elif self.rect.top - self.speed_v  <= 0 and self.speed_v != 0:                                # Läuft oben raus
            self.rect.centery += 10
            self.stopV()
        elif self.rect.left - self.speed_h <= 0 and self.speed_h != 0:                                # Läuft links raus
            self.rect.centerx += 10
            self.stopH()
        elif self.rect.right + self.speed_h >= Settings.window_width and self.speed_h != 0:           # Läuft rechts raus
            self.rect.centerx -= 10
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
        self.speed_v = 4
    def up(self):
        self.speed_v = -4
    def left(self):
        self.speed_h = -4
    def right(self):
        self.speed_h = 4

class Asteroid(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "asteroid.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.scale = randint(2,4)
        self.image = pygame.transform.scale(self.image, (self.rect.width / self.scale, self.rect.height / self.scale) )
        self.rect = self.image.get_rect()
        
    def fall(self):
        self.speed = 
    def draw(self, screen):
        screen.blit(self.image, self.rect)   

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_CENTERED'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        
        
        self.asteroids = pygame.sprite.Group()
        for a in range(Settings.nof_asteroids):
            self.asteroids.add(Asteroid())
            
        self.background = Background()
        
        self.spaceship = Spaceship("spaceship.png")

        self.running = False
            
    def run(self):
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

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        self.asteroids.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':

    game = Game()
    game.run()
