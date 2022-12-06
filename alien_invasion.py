import sys
from time import sleep
import pygame

from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # Создает игровое окно
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_widht = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляров
        self.stats = GameStats(self)
        self.sd = Scoreboard(self)
        self.ship = Ship(self)

        # Создание групп объектов
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """Запуск осного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # Отслеживание событий клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keydup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # сбрасвает настройки до стартовых
            self.settings.initialize_dinamic_settings()
            # скрываетс указатель мыши
            pygame.mouse.set_visible(False)
            # Перед новой игрой запускает очистку статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sd.prep_score()
            self.sd.prep_level()
            # Перед новой игрой очищает флот и снаряды и возвращает корабль в центр
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        '''Реагирует на нажатие клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.quit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keydup_events(self, event):
        '''Реагирует на отпускание клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        # Создает флот пришельцев
        # Создает 1 пришельца
        alien = Alien(self)
        alien_widht, alien_height = alien.rect.size
        available_space_x = self.settings.screen_widht - (2 * alien_widht)
        number_aliens_x = available_space_x // (2 * alien_widht)

        # определяет количество рядов пришельцев
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота пришельцев
        for number_row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, number_row)

    def _create_alien(self, alien_number, number_row):
        # создаем пришельца и перемещаем в ряд
        alien = Alien(self)
        alien_widht, alien_height = alien.rect.size
        alien.x = alien_widht + 2 * alien_widht * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * number_row
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Проверяет достигли ли пришельцы края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускает пришельцев на уровень ниже и меняет направление движения"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        '''Обновляет позиции снарядов и удаляет улетевшие снаряды'''
        self.bullets.update()
        # Удаление снарядов вышедших за пределы экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        # Если не осталось пришельцев, создает новый флот
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sd.prep_level()

    def _check_bullet_alien_collisions(self):
        # Проверка попадания в пришельцев
        # При попадании снаряда убираем снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_point * len(alien)
                self.sd.prep_score()
                self.sd.check_high_score()

    def _update_aliens(self):
        '''Обновлет положение пришельцев'''
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка колизий между кораблем и пришельцем
        if pygame.sprite.spritecollideany(self.ship, self.aliens,):
            self._ship_hit()

        # Проверить добрались ли пришельцы до нижнего края
        self._check_aliens_bottom()

    def _ship_hit(self):
        '''Обрабатывает столкновение корабля с пришельцем'''
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # Очистка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и корабля в цетре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            # появляется указатель мышы
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет достиг ли пришелец дна"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        # При каждом проходе цикла перериросвывать экран
        self.screen.fill(self.settings.bg_color)

        # при каждом проходу цикла перерисовывается корабль
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Вывод инфы о счете
        self.sd.show_score()

        # Кнопка Play отображается если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()



