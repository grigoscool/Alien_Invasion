import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''Класс для управления снарядами, выпущенными кораблем'''

    def __init__(self, ai_game):
        '''Создает объект снарядов в текущей позиции корабля'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда на 0,0 позиции и назначение правильно поз
        self.rect = pygame.Rect(0, 0, self.settings.bullet_weight, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда храниться в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # Обновление позиции в вещественном формате
        self.y -= self.settings.bullet_speed
        # Обновление позиции сняряда
        self.rect.y = self.y

    def draw_bullet(self):
        '''Вывод на экран'''
        pygame.draw.rect(self.screen, self.color, self.rect)


