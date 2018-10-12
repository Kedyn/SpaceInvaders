import pygame
import random

from scene import Scene
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from game_stats import GameStats
from bunker import Bunker
from pygame.sprite import Group


class GameScene(Scene):
    def __init__(self, director, background=(0, 0, 0)):
        super().__init__(director)

        self.background = background

        self.ship = Ship(director.screen)

        self.ship_bullets_allowed = 3

        self.laser_sound = pygame.mixer.Sound('sounds/laser.ogg')
        self.alein_explosion = pygame.mixer.Sound('sounds/alien_explosion.ogg')
        self.ship_explosion = pygame.mixer.Sound('sounds/ship_explosion.ogg')

        self.bullets = Group()
        self.fleet = Group()
        self.explosions = Group()
        self.bunkers = Group()

        self.fleet_drop_speed = 10

        self.rows = 8
        self.cols = self.get_number_aliens_x()

        self.game_stats = GameStats(director)

        self.reset()

        self.old_ticks = pygame.time.get_ticks()

    def reset(self):
        self.game_stats.reset()

        self.ship_bullets = 0

        self.alien_speed = 0.2

        self.number_of_bunkers = 5

        self.bullets.empty()
        self.fleet.empty()
        self.bunkers.empty()

        self.create_fleet()
        self.create_bunkers()

    def get_number_aliens_x(self):
        alien = Alien(self.director.screen)
        available_space_x = self.director.screen.get_rect().width - 2 * \
            alien.rect.width
        number_aliens_x = int(available_space_x / (2 * alien.rect.width))

        return number_aliens_x

    def create_alien(self, alien_number, row_number, alien_type):
            alien = Alien(self.director.screen, alien_type=alien_type,
                          speed_factor=self.alien_speed)
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

    def create_bunkers(self):
        space = int((self.director.screen.get_rect().right -
                    ((self.number_of_bunkers - 1) * 56)) /
                    self.number_of_bunkers)
        x = space

        for i in range(self.number_of_bunkers):
            self.bunkers.add(Bunker(self.director.screen, x))

            x += space

    def fire_bullet(self, rect, bullet_type="ship"):
        if bullet_type is "ship":
            if self.ship_bullets < self.ship_bullets_allowed:
                new_bullet = Bullet(self.director.screen, rect.centerx,
                                    rect.top)

                self.bullets.add(new_bullet)
                self.laser_sound.play()

                self.ship_bullets += 1
        else:
            new_bullet = Bullet(self.director.screen, rect.centerx,
                                rect.top, (200, 0, 0), 1)

            self.bullets.add(new_bullet)
            self.laser_sound.play()

    def keydown(self, key):
        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.ship.moving_right = True
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.ship.moving_left = True
        elif key == pygame.K_SPACE:
            self.fire_bullet(self.ship.rect)

    def keyup(self, key):
        if key == pygame.K_RIGHT or key == pygame.K_d:
            self.ship.moving_right = False
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.ship.moving_left = False

    def create_explosion(self, center, character_type="alien"):
        new_explosion = Explosion(self.director.screen, center)

        self.explosions.add(new_explosion)

        if character_type is "alien":
            self.alein_explosion.play()
        else:
            self.ship_explosion.play()

    def change_fleet_direction(self):
        for alien in self.fleet.sprites():
            alien.direction *= -1
            alien.rect.y += self.fleet_drop_speed

    def check_explosions(self):
        for explosion in self.explosions.sprites():
            if explosion.explosion is 8:
                self.explosions.remove(explosion)

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
                            self.game_stats.score += alien.alien_type * 10
                            self.create_explosion(alien.rect.center)
                            self.fleet.remove(alien)
                            self.bullets.remove(bullet)

                            self.ship_bullets -= 1

                            self.alein_explosion.play()
            else:
                if bullet.rect.top >= screen_height:
                    self.bullets.remove(bullet)
                elif bullet.rect.colliderect(self.ship.rect):
                    self.create_explosion(self.ship.rect.center)
                    self.bullets.remove(bullet)

                    self.ship_explosion.play()

    def update(self):
        self.check_explosions()
        self.explosions.update()

        self.ship.update()

        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.fleet.update()

        if len(self.fleet.sprites()) > 0 and \
                pygame.time.get_ticks() - self.old_ticks >= \
                10000 / self.game_stats.level:
            fleet = self.fleet.sprites()
            self.fire_bullet(fleet[random.randint(0, len(fleet) - 1)].rect,
                             "alien")
            self.old_ticks = pygame.time.get_ticks()

        self.check_bullets()
        self.bullets.update()

        self.game_stats.update()

    def render(self):
        self.director.screen.fill(self.background)

        self.game_stats.render()

        for explsion in self.explosions.sprites():
            explsion.render()

        self.ship.render()

        for bullet in self.bullets.sprites():
            bullet.render()

        for alien in self.fleet.sprites():
            alien.render()

        for bunker in self.bunkers.sprites():
            bunker.render()
