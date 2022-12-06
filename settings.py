class Settings():
    '''Класс для сохранения всех настроек игры Alien Invasion.'''

    def __init__(self):
        """Инициализирует настройки игры."""
        # параметры экрана
        self.screen_widht = 1920
        self.screen_height = 1080
        self.bg_color = (230, 230, 230)

        # Настройка скорости корабля
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_weight = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Параметры пришельцев
        self.fleet_drop_speed = 10


        # Темп ускорения игры
        self.speedup_scale = 1.5

        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """Инициализирует настройки, меняющиеся во время игры"""
        self.alien_speed = 1.5
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        # 1 движение флота вправо, -1 влево
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает скорость игры"""
        self.alien_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale