class Settings():
    '''Класс для сохранения всех настроек игры Alien Invasion.'''

    def __init__(self):
        """Инициализирует настройки игры."""
        # параметры экрана
        self.screen_widht = 1920
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Настройка скорости корабля
        self.ship_speed = 1.5

        # Параметры снаряда
        self.bullet_speed = 1.0
        self.bullet_weight = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3