import pygame
import random

from scene import Scene
from ship import Ship
from bullet import Bullet
from alien import Alien
from ufo import UFO
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

        self.laser_sound = pygame.mixer.Sound('assets/sounds/laser.ogg')
        self.alein_explosion = pygame.mixer.Sound(
            'assets/sounds/alien_explosion.ogg')
        self.ship_explosion = pygame.mixer.Sound(
            'assets/sounds/ship_explosion.ogg')
        self.ufo_sound = pygame.mixer.Sound(
            'assets/sounds/ufo.ogg')

        self.background_sound = pygame.mixer.Sound(
            'assets/sounds/background.ogg')

        self.gg_sound = pygame.mixer.Sound(
            'assets/sounds/game_over.ogg')

        self.bullets = Group()
        self.fleet = Group()
        self.explosions = Group()
        self.bunkers = Group()

        self.fleet_drop_speed = 10

        self.rows = 8
        self.cols = self.get_number_aliens_x()

        self.game_stats = GameStats(director)

        self.old_ticks = pygame.time.get_ticks()

        self.ufo_time = random.randint(15, 30) * 1000
        self.ufo_ticks = pygame.time.get_ticks()

        self.ufo = None

    def exit(self):
        self.game_stats.save_scores()

    def reset(self, alien_speed=0.2):
        self.game_stats.reset()

        self.ship_bullets = 0

        self.alien_speed = alien_speed

        self.number_of_bunkers = 5

        self.bullets.empty()
        self.fleet.empty()
        self.bunkers.empty()

        self.create_fleet()
        self.create_bunkers()

        self.ship.reset()

        self.game_stats.save_scores()

        self.ufo_time = random.randint(15, 30) * 1000
        self.ufo_ticks = pygame.time.get_ticks()

        self.ufo = None

        self.background_sound.play(-1)

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

        if self.fleet.sprites()[-1].rect.bottom > screen_bottom:
            self.lose_ship()

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
                    if self.ufo is not None:
                        if bullet.rect.colliderect(self.ufo.rect):
                            self.game_stats.score += random.randint(1, 5) * \
                                1000
                            self.create_explosion(self.ufo.rect.center)
                            self.ship_bullets -= 1
                            self.alein_explosion.play()
                            self.ufo = None
                            self.ufo_sound.stop()
                    for bunker in self.bunkers:
                        if bunker.collide(bullet.rect):
                            self.bullets.remove(bullet)

                            self.ship_explosion.play()

                            self.ship_bullets -= 1

                            if not bunker.standing():
                                self.bunkers.remove(bunker)
            else:
                if bullet.rect.top >= screen_height:
                    self.bullets.remove(bullet)
                elif bullet.rect.colliderect(self.ship.rect):
                    self.create_explosion(self.ship.rect.center)
                    self.bullets.remove(bullet)

                    self.ship_explosion.play()

                    self.lose_ship()

                for bunker in self.bunkers:
                    if bunker.collide(bullet.rect):
                        self.bullets.remove(bullet)

                        self.ship_explosion.play()

                        if not bunker.standing():
                            self.bunkers.remove(bunker)

    def move_aliens_top(self):
        alien = Alien(self.director.screen,
                      alien_type=self.fleet.sprites()[0].alien_type)
        top_y = alien.rect.height

        prev_alien_y = self.fleet.sprites()[0].rect.y

        for alien in self.fleet.sprites():
            if (alien.rect.y > prev_alien_y):
                top_y += 2 * alien.rect.height

            prev_alien_y = alien.rect.y

            alien.rect.y = top_y

    def lose_ship(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1

            self.move_aliens_top()

            self.ship.reset()
        else:
            self.gg_sound.play()

            self.background_sound.stop()

            self.director.set_scene("menu")

    def update(self):
        if len(self.fleet.sprites()) == 0:
            self.ufo_sound.stop()
            self.background_sound.stop()
            self.alien_speed += 0.2
            self.reset(self.alien_speed)

        if self.ufo is not None:
            if self.ufo.check_edges():
                self.ufo = None

                self.ufo_sound.stop()

                self.ufo_time = random.randint(15, 30) * 1000
                self.ufo_ticks = pygame.time.get_ticks()
            else:
                self.ufo.update()
        else:
            if pygame.time.get_ticks() - self.ufo_ticks >= \
                    self.ufo_time:
                self.ufo = UFO(self.director.screen, self.alien_speed * 2)

                self.ufo_sound.play(-1)

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

        if self.fleet.sprites()[-1].rect.bottom >= \
                self.bunkers.sprites()[0].top_left_triangle_rect.top:
            for alien in self.fleet.sprites():
                for bunker in self.bunkers.sprites():
                    if bunker.collide(alien.rect):
                        self.create_explosion(alien.rect.center)
                        self.fleet.remove(alien)

                        self.alein_explosion.play()

                        if not bunker.standing():
                            self.bunkers.remove(bunker)

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

        if self.ufo is not None:
            self.ufo.render()
