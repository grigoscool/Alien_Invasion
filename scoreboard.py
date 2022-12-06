import pygame.font
import pygame
from ship import Ship
from pygame.sprite import Group

class Scoreboard():
    """Класс для вывода игровой информации"""

    def __init__(self, ai_game):
        """Инициализация атрибутов подсчета очков"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font(None, 48)

        # Подготовка исходного изображения и рекорда
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Выводит начальный счет"""
        rounded_score = round(self.stats.score, -1)
        score_str = str("{:,}".format(rounded_score))
        self.score_image = self.font.render(score_str, True,
                                              self.text_color, self.settings.bg_color)

        # Вывод счета в правом верхнем углу экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 20
        self.score_rect.right = self.screen_rect.right - 20

    def prep_high_score(self):
        """Выводит рекордный счет"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = str("{:,}".format(rounded_high_score))
        self.high_score_image = self.font.render(high_score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Вывод рекордного счета в верхнем левом углу экрана
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = self.score_rect.top
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        # Выводит текущий уровень
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str,True,
                                            self.text_color, self.settings.bg_color)
        # Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        """Выводит количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def check_high_score(self):
        """Проверяет результат на рекордность"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Выводит счет на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)