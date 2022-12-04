class Settings():
    '''Класс для сохранения всех настроек игры Alien Invasion.'''

    def __init__(self):
        """Инициализирует настройки игры."""
        # параметры экрана
        self.screen_widht = 1920
        self.screen_heighr = 800
        self.bg_color = (230,230,230)
        # Настройка скорости корабля
        self.ship_speed = 1.5