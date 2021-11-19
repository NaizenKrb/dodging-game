import pygame
import os


class Settings(object):
    window_width = 700
    window_height = 200
    fps = 60
    title = "Demo AB 05: Kollisionsarten"
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    modus = "rect"


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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 10
        self.rect.centery = 10
        self.stop()

    def update(self):
        self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def stop(self):
        self.speed_v = self.speed_h = 0

    def down(self):
        self.speed_v = 1

    def up(self):
        self.speed_v = -1

    def left(self):
        self.speed_h = -1

    def right(self):
        self.speed_h = 1


class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        pygame.display.set_caption(Settings.title)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()

        self.brick = Obstacle("brick1.png", "brick2.png")
        self.spaceship = Obstacle("raumschiff1.png", "raumschiff2.png")
        self.alien = Obstacle("alienbig1.png", "alienbig2.png")
        self.bullet = Bullet("shoot.png")

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
                    self.bullet.down()
                elif event.key == pygame.K_UP:
                    self.bullet.up()
                elif event.key == pygame.K_LEFT:
                    self.bullet.left()
                elif event.key == pygame.K_RIGHT:
                    self.bullet.right()
                elif event.key == pygame.K_r:
                    Settings.modus = "rect"
                elif event.key == pygame.K_c:
                    Settings.modus = "circle"
                elif event.key == pygame.K_m:
                    Settings.modus = "mask"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.bullet.stop()
                elif event.key == pygame.K_UP:
                    self.bullet.stop()
                elif event.key == pygame.K_LEFT:
                    self.bullet.stop()
                elif event.key == pygame.K_RIGHT:
                    self.bullet.stop()

    def update(self):
        self.check_for_collision()
        self.bullet.update()
        self.all_obstacles.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_obstacles.draw(self.screen)
        self.bullet.draw(self.screen)
        text_surface_modus = self.font.render("Modus: {0}".format(Settings.modus), True, (255, 255, 255))
        self.screen.blit(text_surface_modus, dest=(10, Settings.window_height-30))

        pygame.display.flip()

    def resize(self):
        total_width = self.spaceship.rect.width
        total_width += self.alien.rect.width
        total_width += self.brick.rect.width

        padding = (Settings.window_width - total_width) // 4
        self.brick.rect.left = padding
        self.spaceship.rect.left = self.brick.rect.right + padding
        self.alien.rect.left = self.spaceship.rect.right + padding

    def check_for_collision(self):
        if Settings.modus == "circle":
            self.brick.hit = pygame.sprite.collide_circle(self.bullet, self.brick)
            self.spaceship.hit = pygame.sprite.collide_circle(self.bullet, self.spaceship)
            self.alien.hit = pygame.sprite.collide_circle(self.bullet, self.alien)
        elif Settings.modus == "mask":
            self.brick.hit = pygame.sprite.collide_mask(self.bullet, self.brick)
            self.spaceship.hit = pygame.sprite.collide_mask(self.bullet, self.spaceship)
            self.alien.hit = pygame.sprite.collide_mask(self.bullet, self.alien)
        else:
            self.brick.hit = pygame.sprite.collide_rect(self.bullet, self.brick)
            self.spaceship.hit = pygame.sprite.collide_rect(self.bullet, self.spaceship)
            self.alien.hit = pygame.sprite.collide_rect(self.bullet, self.alien)


if __name__ == '__main__':

    game = Game()
    game.run()
