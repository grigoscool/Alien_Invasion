class GameStats():
    """Отслеживание статистики в игре"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии
        self.game_active = False

        # Рекорд
        x = open('high_score_ai.txt', 'r')
        self.high_score = int(x.readline())
        x.close()
        # Уровень игры
        self.level = 1

    def reset_stats(self):
        """Инициализирует статистику текущей серии игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

