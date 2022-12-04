import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Кдасс создания пришельцa"""

    def __init__(self, ai_game):
        """Инициализирует пришельцев """
        super().__init__()
        self.screen = ai_game.screen

        # загрузка изображения пришельца
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение вещественной (точной) позиции пришельца
        self.x = float(self.rect.x)