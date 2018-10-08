import pygame

from scene import Scene
from ship import Ship
from bullet import Bullet
from alien import Alien
from pygame.sprite import Group


class GameScene(Scene):
    def __init__(self, director, background=(0, 0, 0)):
        super().__init__(director)

        self.background = background

        self.ship = Ship(director.screen)

        self.ship_bullets_allowed = 3
        self.ship_bullets = 0

        self.laser_sound = pygame.mixer.Sound('sounds/laser.ogg')

        self.bullets = Group()
        self.fleet = Group()

        self.fleet_drop_speed = 10

        self.level = 1
        self.rows = 8
        self.cols = self.get_number_aliens_x()

        self.reset()

    def get_number_aliens_x(self):
        alien = Alien(self.director.screen)
        available_space_x = self.director.screen.get_rect().width - 2 * \
            alien.rect.width
        number_aliens_x = int(available_space_x / (2 * alien.rect.width))

        return number_aliens_x

    def create_alien(self, alien_number, row_number, alien_type):
            alien = Alien(self.director.screen, type=alien_type)
            alien_width = alien.rect.width
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * \
                row_number
            self.fleet.add(alien)

    def create_fleet(self):
        alien_type = 0
        change_type = self.rows / 4

        for row_number in range(self.rows):
            if int(row_number % change_type) is 0:
                alien_type += 1

            for alien_number in range(self.cols):
                self.create_alien(alien_number, row_number, alien_type)

    def reset(self):
        self.ship_bullets = 0
        self.level = 1

        self.bullets.empty()
        self.fleet.empty()

        self.create_fleet()

    def fire_ship_bullet(self):
        if self.ship_bullets < self.ship_bullets_allowed:
            new_bullet = Bullet(self.director.screen, self.ship.rect.centerx,
                                self.ship.rect.top)

            self.bullets.add(new_bullet)
            self.laser_sound.play()

            self.ship_bullets += 1

    def keydown(self, key):
        if key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif key == pygame.K_SPACE:
            self.fire_ship_bullet()

    def keyup(self, key):
        if key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif key == pygame.K_LEFT:
            self.ship.moving_left = False

    def change_fleet_direction(self):
        for alien in self.fleet.sprites():
            alien.direction *= -1
            alien.rect.y += self.fleet_drop_speed

    def check_fleet_edges(self):
        for alien in self.fleet.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        screen_bottom = self.director.screen.get_rect().bottom

        for alien in self.fleet.sprites():
            if alien.rect.bottom is screen_bottom:
                self.change_fleet_direction()
                break

    def check_bullets(self):
        screen_height = self.director.screen.get_rect().height

        for bullet in self.bullets.sprites():
            if bullet.speed_factor < 0:
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                    self.ship_bullets -= 1
                else:
                    for alien in self.fleet.sprites():
                        if bullet.rect.colliderect(alien.rect):
                            self.fleet.remove(alien)
                            self.bullets.remove(bullet)
                            self.ship_bullets -= 1
            else:
                if bullet.rect.top >= screen_height:
                    self.bullets.remove(bullet)

    def update(self):
        self.ship.update()

        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.fleet.update()

        self.check_bullets()
        self.bullets.update()

    def render(self):
        self.director.screen.fill(self.background)

        self.ship.render()

        for bullet in self.bullets.sprites():
            bullet.render()

        for alien in self.fleet.sprites():
            alien.render()
