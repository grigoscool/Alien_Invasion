import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Класс для управления ресурсами игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        # Создает игровое окно
        self.screen = pygame.display.set_mode((self.settings.screen_widht, self.settings.screen_heighr))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """Запуск осного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
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
    def _check_keydup_events(self, event):
        '''Реагирует на отпускание клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        # При каждом проходе цикла перериросвывать экран
        self.screen.fill(self.settings.bg_color)
        # при каждом проходу цикла перерисовывается корабль
        self.ship.blitme()
        # Отображение последнего прорисованного экрана
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()



