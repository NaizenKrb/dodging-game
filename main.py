from random import randint, uniform
import pygame
import os


class Settings(object):
    window_width = 700
    window_height = 800
    fps = 60
    title = "Dodging Game"
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    default_spawn_speed = 120
    asteroid_default_speed = 2
    default_lives = 1
    
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = Settings.window_width // 2
        self.rect.centery = 720
        self.lives = Settings.default_lives
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
    def __init__(self,game) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, "asteroid.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.scale = uniform(1.5,3)
        self.image = pygame.transform.scale(self.image, (self.rect.width / self.scale, self.rect.height / self.scale) )
        self.rect = self.image.get_rect()
        self.speed = randint(1,game.asteroid_speed)
        self.rect.left = randint(0 ,Settings.window_width - self.rect.width)
        self.rect.bottom = 0 - self.rect.bottom

    def collision(self):
        if pygame.sprite.spritecollide(self,game.spaceship, False, pygame.sprite.collide_mask):
            game.spaceship.sprite.lives -= 1
            if game.spaceship.sprite.lives <= 0:
                game.game_over = True
            game.spaceship.sprite.spaceshipInitialposition()
            game.asteroids.empty()
            
    def asteroid_arrived(self):
        if self.rect.top >= Settings.window_height:
            game.asteroids.remove(self)
            game.points += 1
            print(game.points)
           
    def update(self):
        self.rect.move_ip((0, self.speed))
        self.collision()
        self.asteroid_arrived()
        
    def fall(self):
        self.speed = self.speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)   

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_CENTERED'] = "10, 50"
        pygame.init()
        pygame.font.init()
        self.font_name = pygame.font.get_default_font()
        self.game_font = pygame.font.SysFont(self.font_name, 72)
        self.info_font = pygame.font.SysFont(self.font_name, 30)
        self.menu_font = pygame.font.SysFont(self.font_name, 36)
        pygame.display.set_caption(Settings.title)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.pause = False
        self.start_screen = True
        self.game_over = False
        self.points = 0
        
        self.asteroid_speed = Settings.asteroid_default_speed
        self.counter = 0
        self.spawn_speed = Settings.default_spawn_speed
        
        self.asteroids = pygame.sprite.Group()
            
        self.background = Background()
        self.spaceship = pygame.sprite.GroupSingle()
        self.spaceship.add(Spaceship("spaceship.png"))

        self.running = False
    
    def incAsteroidspeed(self):
        if self.points >= 5 and self.asteroid_speed == Settings.asteroid_default_speed:
            self.asteroid_speed += 1
            self.spawn_speed -= 10
            print(self.asteroid_speed)
        if self.points >= 10 and self.asteroid_speed == Settings.asteroid_default_speed + 1:
            self.asteroid_speed += 1
            self.spawn_speed -= 10
            print(self.asteroid_speed)
        if self.points >= 15 and self.asteroid_speed == Settings.asteroid_default_speed + 2:
            self.asteroid_speed += 1
            self.spawn_speed -= 10
            print(self.asteroid_speed)
        if self.points >= 20 and self.asteroid_speed == Settings.asteroid_default_speed + 3:
            self.asteroid_speed += 1
            self.spawn_speed -= 10
            print(self.asteroid_speed)
        if self.points >= 25 and self.asteroid_speed == Settings.asteroid_default_speed + 4:
            self.asteroid_speed += 1
            self.spawn_speed -= 10
            print(self.asteroid_speed)
        if self.points == 30 and self.asteroid_speed == Settings.asteroid_default_speed + 5:
            self.spawn_speed -= 10
            print(self.asteroid_speed)
        if self.points == 35 and self.asteroid_speed == Settings.asteroid_default_speed + 5:
            self.spawn_speed -= 10
            print(self.asteroid_speed)
            
    def reset(self):
        self.points = 0
        self.spaceship.sprite.lives = Settings.default_lives
        self.spawn_speed = Settings.default_spawn_speed
        self.asteroid_speed = Settings.asteroid_default_speed  
    
    def start_menu(self):
        self.text_info = self.menu_font.render(('Press any button to start!'),1,(255,0,0))
        self.screen.blit(self.text_info,(80,150))
        pygame.display.update()
        
    def pause_overlay(self):
        self.overlay = pygame.Surface((Settings.window_width,Settings.window_height))
        pygame.Surface.fill(self.overlay,(136,136,136))
        self.overlay.set_alpha(3)
        self.screen.blit(self.overlay, self.overlay.get_rect())
        pygame.display.update()
        
    def death_screen(self):
        self.text = self.game_font.render('GAME OVER', 1, (255, 0, 0))
        self.text_points = self.game_font.render(('Punkte: {0}'.format(self.points)),1,(255,0,0))
        self.text_restart = self.info_font.render('Beliebige Taste drücken zum neustarten!',1,(255,255,255))
        self.screen.blit(self.text, (Settings.window_width/2 - self.text.get_rect().width/2, 100))
        self.screen.blit(self.text_points,(Settings.window_width/2 - self.text_points.get_rect().width/2,150))
        self.screen.blit(self.text_restart,(Settings.window_width/2 - self.text_restart.get_rect().width/2,250))
        pygame.display.update()

    def run(self):
        self.running = True
        self.draw()
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            if self.start_screen:
                self.start_menu()
            elif self.pause:
                self.pause_overlay()
            elif self.game_over:
                self.death_screen()
                self.reset()
            else:
                self.update()
                self.spawn()
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
                    self.spaceship.sprite.down()
                elif event.key == pygame.K_UP:
                    self.spaceship.sprite.up()
                elif event.key == pygame.K_LEFT:
                    self.spaceship.sprite.left()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.sprite.right()
                elif event.key == pygame.K_p:
                    self.pause = not self.pause
                if self.game_over:
                    self.game_over = False
                if self.start_screen and pygame.KEYDOWN:
                    self.start_screen = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.spaceship.sprite.stopV()
                elif event.key == pygame.K_UP:
                    self.spaceship.sprite.stopV()
                elif event.key == pygame.K_LEFT:
                    self.spaceship.sprite.stopH()
                elif event.key == pygame.K_RIGHT:
                    self.spaceship.sprite.stopH()

    def spawn(self):
        self.counter += 1
        if self.counter >= self.spawn_speed:
            self.counter = 0
            self.asteroids.add(Asteroid(self))
            
    
            
    def update(self):
        self.spaceship.update()
        self.asteroids.update()
        self.incAsteroidspeed()
        

    def draw(self):
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        self.asteroids.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':

    game = Game()
    game.run()
