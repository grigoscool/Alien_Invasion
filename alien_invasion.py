import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


    def run_game(self):
        """Запуск осного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()
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

    def _update_bullet(self):
        '''Обновляет позиции снарядов и удаляет улетевшие снаряды'''
        self.bullets.update()
        # Удаление снарядов вышедших за пределы экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        # При каждом проходе цикла перериросвывать экран
        self.screen.fill(self.settings.bg_color)
        # при каждом проходу цикла перерисовывается корабль
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отображение последнего прорисованного экрана
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()



